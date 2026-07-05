"""Endless generative stream: segments with fresh seeds, crossfaded, piped
into ffmpeg toward an RTMP ingest (or a local file for testing).

This is the structural advantage over licensed-playlist channels: the audio
never loops, because it is generated, not replayed. The engine renders ~20x
realtime, so underruns are not a concern; ffmpeg's `-re` paces the pipe and
OS backpressure paces us.
"""

import os
import subprocess

import numpy as np
import yaml

from .art import generate_art
from .master.loudness import LufsMeter
from .render import SR, iter_chunks


def _calibrate_gain_db(cfg: dict, seed: int, sample_s: float = 120.0) -> float:
    """Live streams can't two-pass normalize; recipes are level-stable, so a
    static gain measured on a sample segment holds."""
    meter = LufsMeter(SR)
    for chunk in iter_chunks(cfg, sample_s, seed):
        meter.add(chunk)
    measured = meter.integrated()
    if not np.isfinite(measured):
        raise RuntimeError(
            "calibration measured no signal (-inf LUFS); recipe layer amps may be zero")
    return cfg.get("lufs_target", -20.0) - measured


def _endless_chunks(cfg: dict, seed0: int, segment_s: float, crossfade_s: float):
    """Yield chunks forever: each segment gets seed0+k, and segment boundaries
    are raised-cosine crossfades so the join is inaudible."""
    if segment_s < 2 * crossfade_s:
        # the first-buffer wait below needs 2*crossfade of audio per segment;
        # shorter segments would buffer forever and never yield
        raise ValueError(
            f"segment ({segment_s:.0f}s) must be >= 2x crossfade ({crossfade_s:.0f}s)")
    xf_n = int(crossfade_s * SR)
    fade_in = (0.5 - 0.5 * np.cos(np.pi * np.arange(xf_n) / xf_n))[:, None]
    fade_out = fade_in[::-1]
    tail = None
    seed = seed0
    while True:
        hold = np.zeros((0, 2))
        first = True
        # render crossfade_s extra: the surplus becomes the next segment's tail
        for chunk in iter_chunks(cfg, segment_s + crossfade_s, seed):
            buf = np.vstack([hold, chunk]) if hold.shape[0] else chunk
            if first:
                if buf.shape[0] < 2 * xf_n:
                    hold = buf
                    continue
                if tail is not None:
                    buf[:xf_n] = buf[:xf_n] * fade_in + tail * fade_out
                else:
                    buf[:xf_n] *= fade_in  # very first segment fades from silence
                first = False
            out, hold = buf[:-xf_n], buf[-xf_n:]
            yield out
        tail = hold
        seed += 1


def stream(recipe_path: str, url: str, seed0: int = 1, segment_s: float = 1800.0,
           crossfade_s: float = 8.0, max_duration_s: float | None = None) -> None:
    if segment_s < 4 * crossfade_s:
        crossfade_s = segment_s / 4.0
        print(f"note: crossfade clamped to {crossfade_s:.1f}s (segment is {segment_s:.0f}s)")
    with open(recipe_path) as f:
        cfg = yaml.safe_load(f)
    name = os.path.splitext(os.path.basename(recipe_path))[0]

    gain = 10.0 ** (_calibrate_gain_db(cfg, seed0) / 20.0)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    art_path = generate_art(name, seed0, os.path.join(repo_root, "art", f"stream-{name}.png"))

    is_rtmp = url.startswith(("rtmp://", "rtmps://"))
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        *(["-re"] if is_rtmp else []),  # realtime pacing only for actual streaming
        "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "pipe:0",
        "-loop", "1", "-framerate", "2", "-i", art_path,
        "-map", "1:v", "-map", "0:a",
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
        "-pix_fmt", "yuv420p", "-r", "2", "-g", "4",  # keyframe every 2s (ingest requirement)
        "-c:a", "aac", "-b:a", "128k", "-ar", str(SR),
        # capped runs use -t on both streams; -shortest would race the eagerly
        # encoded image loop against the paced audio pipe and cut the mux early.
        # endless runs use -shortest so output stops soon after stdin closes.
        *(["-t", f"{max_duration_s:.3f}"] if max_duration_s else ["-shortest"]),
        *(["-f", "flv"] if is_rtmp else []),
        url,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    max_samples = int(max_duration_s * SR) if max_duration_s else None
    written = 0
    try:
        for out in _endless_chunks(cfg, seed0, segment_s, crossfade_s):
            if max_samples is not None and written + out.shape[0] > max_samples:
                out = out[: max_samples - written]
            pcm = np.clip(out * gain, -0.999, 0.999)
            proc.stdin.write((pcm * 32767.0).astype("<i2").tobytes())
            written += out.shape[0]
            if max_samples is not None and written >= max_samples:
                break
    except BrokenPipeError:
        print("ffmpeg closed the pipe (ingest ended?)")
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.wait()
    print(f"streamed {written / SR:.0f}s to {url}")
