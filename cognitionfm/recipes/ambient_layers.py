"""`ambient_layers` generator: drone + voice-led pads + sparse shimmer.

Covers the unpulsed recipes (Deep Work - Verbal, Downshift, Sleep Wind-Down);
the YAML decides register, speed, arc, and layer levels.
"""

import numpy as np

from ..compose.events import MAX_EVENT_S, Event
from ..compose.theory import midi_to_hz
from ..compose.voices import drone_voice, pad_voice, shimmer_voice
from ..dsp.mod import slow_drift


def _arc_fn(kind: str, duration: float):
    """Energy arc across the render. 'descending' implements the falling
    intensity the stress/sleep literature favors (evidence review §2.5, §2.8)."""
    if kind == "descending":
        return lambda t: 1.0 - 0.65 * (0.5 - 0.5 * np.cos(np.pi * min(t / duration, 1.0)))
    if kind == "descending_to_silence":
        return lambda t: max(1.0 - 0.92 * (t / duration) ** 1.3, 0.05)
    if kind == "ascending":
        # arousal ramp: start at ~40%, reach full energy by the last quarter
        return lambda t: 0.4 + 0.6 * (0.5 - 0.5 * np.cos(np.pi * min(t / (duration * 0.75), 1.0)))
    return lambda t: 1.0  # flat


def generate(cfg: dict, duration: float, seed: int) -> list[Event]:
    rng = np.random.default_rng(seed)
    layers = cfg["layers"]
    root_midi = cfg["root_midi"]
    mode = cfg["mode"]
    arc = _arc_fn(cfg.get("arc", "flat"), duration)

    events: list[Event] = []
    if "drone" in layers:
        d = layers["drone"]
        events += drone_voice(rng, duration, root_hz=midi_to_hz(root_midi - 12),
                              amp=d["amp"], event_dur_s=d.get("event_dur_s", 60.0))
    if "pad" in layers:
        p = layers["pad"]
        events += pad_voice(rng, duration, root_midi, mode,
                            register=tuple(cfg["register"]),
                            chord_dur_range=tuple(cfg["chord_duration_s"]),
                            amp=p["amp"], n_voices=p.get("voices", 4))
    if "shimmer" in layers:
        s = layers["shimmer"]
        events += shimmer_voice(rng, duration, root_midi, mode,
                                register=tuple(s["register"]), amp=s["amp"],
                                mean_interval_s=s.get("mean_interval_s", 22.0))

    lp = cfg.get("lp_cutoff_hz", {"base": 2000, "drift_octaves": 0.5})
    attack_floor = cfg.get("attack_floor_s", 1.0)
    out = []
    for ev in events:
        if ev.t >= duration:
            continue
        ev.dur = min(ev.dur, MAX_EVENT_S)
        ev.attack_s = max(ev.attack_s, attack_floor)
        ev.amp *= arc(ev.t)
        # brightness drifts over minutes, deterministically - the only "motion"
        drift = slow_drift(ev.t, seed=seed + 101)
        ev.params["lp_cutoff"] = lp["base"] * 2.0 ** (lp["drift_octaves"] * drift)
        out.append(ev)
    out.sort(key=lambda e: e.t)
    return out
