"""Minimal music theory: scales, degrees, frequencies."""

import numpy as np

SCALES = {
    "ionian":  [0, 2, 4, 5, 7, 9, 11],
    "lydian":  [0, 2, 4, 6, 7, 9, 11],
    "dorian":  [0, 2, 3, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
}

# Diatonic triads (scale-degree indices, 0-based) reachable from each other with
# smooth voice leading. Kept small and consonant on purpose: harmonic surprise
# is attention capture (evidence review §1.2).
CHORD_GRAPH = {
    0: [3, 5, 1],   # I  -> IV, vi, ii
    1: [4, 3],      # ii -> V, IV
    3: [0, 5, 4],   # IV -> I, vi, V
    4: [0, 5],      # V  -> I, vi
    5: [3, 1, 0],   # vi -> IV, ii, I
}


def midi_to_hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def scale_pitches(root_midi: int, mode: str, low: int, high: int) -> list[int]:
    """All scale pitches of `mode` on `root_midi` within [low, high]."""
    degrees = SCALES[mode]
    out = []
    for octave in range(-3, 4):
        for d in degrees:
            p = root_midi + 12 * octave + d
            if low <= p <= high:
                out.append(p)
    return sorted(out)


def triad_pitch_classes(root_midi: int, mode: str, degree: int) -> set[int]:
    degrees = SCALES[mode]
    return {(root_midi + degrees[(degree + i) % 7]) % 12 for i in (0, 2, 4)}


def walk_chords(rng: np.random.Generator, n_chords: int, start: int = 0) -> list[int]:
    """Random walk over CHORD_GRAPH starting at I."""
    seq, cur = [start], start
    for _ in range(n_chords - 1):
        cur = int(rng.choice(CHORD_GRAPH[cur]))
        seq.append(cur)
    return seq
