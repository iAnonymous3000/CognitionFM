"""`pulse_layers` generator: machine-steady soft pulse + bass + slow pads.

For Deep Work - Analytical (docs/02-playlists.md #2): a predictable pulse is
tolerated at lower verbal load and helps time-on-task feel. Predictability is
the point - no swing, no fills, no surprises. Percussive attacks are soft
("thump", not "snare"); the recipe's attack floor applies to sustained layers
only.
"""

import numpy as np

from ..compose.events import Event
from ..compose.theory import midi_to_hz, triad_pitch_classes, walk_chords, scale_pitches
from ..compose.voices import pad_voice
from ..dsp.mod import slow_drift

MAX_EVENT_S = 90.0
SUSTAINED = {"pad", "drone", "shimmer"}


def generate(cfg: dict, duration: float, seed: int) -> list[Event]:
    rng = np.random.default_rng(seed)
    root_midi = cfg["root_midi"]
    mode = cfg["mode"]
    bpm = float(rng.uniform(*cfg["tempo_bpm"]))  # one steady tempo per render
    beat = 60.0 / bpm
    layers = cfg["layers"]

    events: list[Event] = []

    # Pulse: soft thump every beat, quiet tock on the offbeat of every 2nd beat.
    if "pulse" in layers:
        p = layers["pulse"]
        n_beats = int(duration / beat)
        for b in range(n_beats):
            t = b * beat
            events.append(Event(
                t=t, dur=0.35, freq=midi_to_hz(root_midi - 24), amp=p["amp"],
                pan=0.0, timbre="thump", attack_s=0.03, release_s=0.25,
            ))
            if b % 2 == 1:
                events.append(Event(
                    t=t + beat / 2.0, dur=0.25, freq=midi_to_hz(root_midi + 7),
                    amp=p["amp"] * 0.25, pan=rng.uniform(-0.3, 0.3),
                    timbre="tock", attack_s=0.02, release_s=0.18,
                ))

    # Bass: root notes following a chord walk, two bars per note.
    if "bass" in layers:
        bl = layers["bass"]
        bar = beat * 4.0
        note_dur = bar * 2.0
        n_notes = int(duration / note_dur) + 1
        chords = walk_chords(rng, n_notes)
        low = scale_pitches(root_midi - 12, mode, root_midi - 17, root_midi - 5)
        for i, degree in enumerate(chords):
            pcs = triad_pitch_classes(root_midi, mode, degree)
            roots = [q for q in low if q % 12 in pcs]
            pitch = roots[0] if roots else root_midi - 12
            events.append(Event(
                t=i * note_dur, dur=note_dur * 0.95, freq=midi_to_hz(pitch),
                amp=bl["amp"], pan=0.0, timbre="drone",
                attack_s=0.08, release_s=note_dur * 0.3,
            ))

    if "pad" in layers:
        pd = layers["pad"]
        events += pad_voice(rng, duration, root_midi, mode,
                            register=tuple(cfg["register"]),
                            chord_dur_range=tuple(cfg["chord_duration_s"]),
                            amp=pd["amp"], n_voices=pd.get("voices", 3))

    lp = cfg.get("lp_cutoff_hz", {"base": 2200, "drift_octaves": 0.5})
    attack_floor = cfg.get("attack_floor_s", 1.0)
    out = []
    for ev in events:
        if ev.t >= duration:
            continue
        ev.dur = min(ev.dur, MAX_EVENT_S)
        if ev.timbre in SUSTAINED:
            ev.attack_s = max(ev.attack_s, attack_floor)
        drift = slow_drift(ev.t, seed=seed + 101)
        ev.params["lp_cutoff"] = lp["base"] * 2.0 ** (lp["drift_octaves"] * drift)
        out.append(ev)
    out.sort(key=lambda e: e.t)
    return out
