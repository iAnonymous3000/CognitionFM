"""Chunked render pipeline: recipe YAML -> events -> streamed audio -> mastered WAV.

Memory stays constant regardless of duration: events are synthesized into a
rolling carry buffer, reverb streams via overlap-add, loudness is metered on
the fly, and the master pass is file-to-file.
"""

import os
import re
import tempfile

import numpy as np
import soundfile as sf
import yaml

from .compose.events import Event
from .dsp.env import asr_envelope
from .dsp.filters import one_pole_lowpass
from .dsp.osc import partial_stack
from .fx.reverb import ConvolutionReverb, synth_impulse_response
from .fx.stereo import equal_power_pan
from .master.loudness import LufsMeter, true_peak_db
from .master.normalize import finalize_file
from .recipes import GENERATORS

SR = 48_000
CHUNK_S = 10.0
CARRY_TAIL_S = 95.0  # > ambient_layers.MAX_EVENT_S; events must fit entirely

# timbre -> (partials [(ratio, amp)], detune_cents)
PATCHES = {
    "drone":   ([(1.0, 1.0), (2.0, 0.35), (3.0, 0.10)], 2.0),
    "pad":     ([(1.0, 1.0), (2.0, 0.55), (3.0, 0.33), (4.0, 0.22), (5.0, 0.14), (6.0, 0.09)], 4.0),
    "shimmer": ([(1.0, 1.0), (2.0, 0.20), (3.0, 0.06)], 5.0),
    "thump":   ([(1.0, 1.0), (2.0, 0.15)], 1.0),
    "tock":    ([(1.0, 1.0), (3.0, 0.08)], 2.0),
}


def parse_duration(text: str) -> float:
    """'10m', '90m', '1h30m', '600s' -> seconds."""
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", text.strip())
    if not m or not any(m.groups()):
        raise ValueError(f"unparseable duration: {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return float(h * 3600 + mi * 60 + s)


def synth_event(ev: Event, idx: int, seed: int, sr: int) -> np.ndarray:
    """Render one event to stereo. Seeded by (seed, idx): deterministic and
    independent of chunk boundaries."""
    rng = np.random.default_rng([seed, idx])
    n = int(ev.dur * sr)
    if n <= 0:
        return np.zeros((0, 2))
    partials, detune = PATCHES[ev.timbre]
    x = partial_stack(ev.freq, n, sr, partials, rng, detune_cents=detune)
    x = one_pole_lowpass(x, ev.params.get("lp_cutoff", 3000.0), sr)
    x *= asr_envelope(n, sr, ev.attack_s, ev.release_s) * ev.amp
    return equal_power_pan(x, ev.pan)


def iter_chunks(cfg: dict, duration_s: float, seed: int):
    """Yield post-reverb float64 stereo chunks for a recipe. Shared by the
    file renderer and the live stream; both stay constant-memory."""
    events = GENERATORS[cfg["generator"]](cfg, duration_s, seed)
    rv = cfg.get("reverb", {})
    ir = synth_impulse_response(
        SR, t60_s=rv.get("t60_s", 7.0), damp_hz=rv.get("damp_hz", 3200.0),
        predelay_ms=rv.get("predelay_ms", 20.0), seed=seed,
    )
    reverb = ConvolutionReverb(ir, wet=rv.get("wet", 0.4))

    chunk_n = int(CHUNK_S * SR)
    carry = np.zeros((chunk_n + int(CARRY_TAIL_S * SR), 2), dtype=np.float64)
    total_n = int(duration_s * SR)
    ev_i = 0
    pos = 0
    while pos < total_n:
        n = min(chunk_n, total_n - pos)
        chunk_start = pos / SR
        chunk_end = (pos + n) / SR
        while ev_i < len(events) and events[ev_i].t < chunk_end:
            ev = events[ev_i]
            stereo = synth_event(ev, ev_i, seed, SR)
            offset = int((ev.t - chunk_start) * SR)
            m = min(stereo.shape[0], carry.shape[0] - offset)
            carry[offset:offset + m] += stereo[:m]
            ev_i += 1
        out = reverb.process(carry[:n].copy())
        carry[:-n] = carry[n:]
        carry[-n:] = 0.0
        pos += n
        yield out


def render(recipe_path: str, duration_s: float, seed: int, out_path: str,
           verbose: bool = True) -> dict:
    with open(recipe_path) as f:
        cfg = yaml.safe_load(f)

    meter = LufsMeter(SR)
    tp_max = float("-inf")
    n_events = len(GENERATORS[cfg["generator"]](cfg, duration_s, seed))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    raw_fd, raw_path = tempfile.mkstemp(suffix=".raw.wav",
                                        dir=os.path.dirname(os.path.abspath(out_path)))
    os.close(raw_fd)
    try:
        with sf.SoundFile(raw_path, "w", samplerate=SR, channels=2, subtype="FLOAT") as raw:
            pos = 0
            for out in iter_chunks(cfg, duration_s, seed):
                meter.add(out)
                tp_max = max(tp_max, true_peak_db(out))
                raw.write(out.astype(np.float32))
                pos += out.shape[0]
                if verbose and (pos // int(CHUNK_S * SR)) % 6 == 0:
                    print(f"  rendered {pos / SR:6.0f}s / {duration_s:.0f}s", flush=True)

        lufs = meter.integrated()
        stats = finalize_file(
            raw_path, out_path,
            measured_lufs=lufs, measured_tp_db=tp_max,
            target_lufs=cfg.get("lufs_target", -20.0),
            tp_ceiling_db=cfg.get("truepeak_max_dbtp", -2.0),
        )
    finally:
        if os.path.exists(raw_path):
            os.remove(raw_path)

    stats.update({
        "recipe": cfg.get("name", os.path.basename(recipe_path)),
        "duration_s": duration_s, "seed": seed,
        "events": n_events, "raw_lufs": round(lufs, 2),
        "out_path": os.path.abspath(out_path),
    })
    if verbose:
        print(f"  events={stats['events']} raw={stats['raw_lufs']} LUFS "
              f"-> {stats['achieved_lufs_approx']} LUFS, "
              f"TP {stats['true_peak_db_after']} dBTP")
    return stats
