"""Voice generators: each returns a list of Events for the full render duration.

Design intent (docs/01-evidence-review.md §1.2): high self-similarity, slow
harmonic drift via smooth voice leading, no foreground melody, long attacks.
Voices run on independent, incommensurate cycles (Eno-style) so the texture
never audibly loops without ever introducing surprise.
"""

import numpy as np

from .events import Event
from .theory import midi_to_hz, scale_pitches, triad_pitch_classes, walk_chords


def drone_voice(rng: np.random.Generator, duration: float, root_hz: float,
                amp: float, event_dur_s: float = 60.0) -> list[Event]:
    """Overlapping sub-register root notes; a fifth joins occasionally."""
    events = []
    step = event_dur_s * 0.5
    t = 0.0
    while t < duration:
        events.append(Event(
            t=t, dur=event_dur_s, freq=root_hz, amp=amp * rng.uniform(0.85, 1.0),
            pan=rng.uniform(-0.08, 0.08), timbre="drone",
            attack_s=event_dur_s * 0.3, release_s=event_dur_s * 0.3,
        ))
        if rng.random() < 0.4:
            events.append(Event(
                t=t + rng.uniform(0.0, step), dur=event_dur_s * 0.7,
                freq=root_hz * 1.5, amp=amp * 0.35 * rng.uniform(0.7, 1.0),
                pan=rng.uniform(-0.2, 0.2), timbre="drone",
                attack_s=event_dur_s * 0.25, release_s=event_dur_s * 0.25,
            ))
        t += step
    return events


def pad_voice(rng: np.random.Generator, duration: float, root_midi: int, mode: str,
              register: tuple[int, int], chord_dur_range: tuple[float, float],
              amp: float, n_voices: int = 4, attack_frac: float = 0.35) -> list[Event]:
    """Sustained chords with minimal-motion voice leading over a small chord graph."""
    pitches = scale_pitches(root_midi, mode, *register)
    mean_dur = sum(chord_dur_range) / 2.0
    n_chords = int(duration / mean_dur) + 2
    chords = walk_chords(rng, n_chords)

    # initial voicing: n_voices pitches of chord 0 spread across the register
    pcs = triad_pitch_classes(root_midi, mode, chords[0])
    candidates = [p for p in pitches if p % 12 in pcs]
    idx = np.linspace(0, len(candidates) - 1, n_voices).astype(int)
    voicing = [candidates[i] for i in idx]

    events = []
    t = 0.0
    for degree in chords:
        if t >= duration:
            break
        chord_dur = rng.uniform(*chord_dur_range)
        pcs = triad_pitch_classes(root_midi, mode, degree)
        new_voicing = []
        for p in voicing:
            if p % 12 in pcs:
                new_voicing.append(p)  # common tone: don't move (self-similarity)
            else:
                near = [q for q in pitches if q % 12 in pcs]
                new_voicing.append(min(near, key=lambda q: abs(q - p)))
        voicing = new_voicing
        for i, p in enumerate(voicing):
            onset = t + rng.uniform(0.0, 6.0)  # stagger: chords bloom, never hit
            dur = chord_dur * rng.uniform(1.15, 1.35)
            weight = 1.0 - 0.12 * i  # lower voices slightly louder
            events.append(Event(
                t=onset, dur=dur, freq=midi_to_hz(p),
                amp=amp * weight * rng.uniform(0.75, 1.0),
                pan=rng.uniform(-0.55, 0.55), timbre="pad",
                attack_s=dur * attack_frac, release_s=dur * attack_frac,
            ))
        t += chord_dur
    return events


def shimmer_voice(rng: np.random.Generator, duration: float, root_midi: int, mode: str,
                  register: tuple[int, int], amp: float,
                  mean_interval_s: float = 22.0) -> list[Event]:
    """Rare, quiet, high single tones - texture sparkle, kept below salience."""
    pitches = scale_pitches(root_midi, mode, *register)
    events = []
    t = rng.exponential(mean_interval_s)
    while t < duration:
        dur = rng.uniform(8.0, 15.0)
        events.append(Event(
            t=t, dur=dur, freq=midi_to_hz(int(rng.choice(pitches))),
            amp=amp * rng.uniform(0.5, 1.0), pan=rng.uniform(-0.7, 0.7),
            timbre="shimmer", attack_s=dur * 0.4, release_s=dur * 0.45,
        ))
        t += rng.exponential(mean_interval_s)
    return events
