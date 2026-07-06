"""Chapter marks derived from the harmonic walk.

The pad voice starts a cluster of staggered events at every chord change, so
chord boundaries are recoverable from the event list alone. Reading them from
events (instead of instrumenting the generators) keeps the rng call sequence
untouched: published checksums stay valid.
"""

import yaml

from .recipes import GENERATORS

CLUSTER_GAP_S = 12.0  # > max onset stagger (6s), < min chord duration (20s)


def chord_change_times(cfg: dict, duration_s: float, seed: int) -> list[float]:
    events = GENERATORS[cfg["generator"]](cfg, duration_s, seed)
    pad_onsets = sorted(e.t for e in events if e.timbre == "pad")
    changes = []
    for t in pad_onsets:
        if not changes or t - changes[-1] > CLUSTER_GAP_S:
            changes.append(t)
    return changes


def chapter_marks(cfg: dict, duration_s: float, seed: int,
                  every_s: float = 600.0) -> list[float]:
    """One mark near each multiple of every_s, snapped to the nearest chord
    change so a chapter never starts mid-swell. Always includes 0:00."""
    changes = chord_change_times(cfg, duration_s, seed)
    marks = [0.0]
    k = 1
    while k * every_s < duration_s:
        target = k * every_s
        candidates = [c for c in changes if c > marks[-1] + every_s * 0.5]
        if not candidates:
            break
        snap = min(candidates, key=lambda c: abs(c - target))
        if snap < duration_s - every_s * 0.25:  # no stub chapter at the end
            marks.append(snap)
        k += 1
    return marks


def format_chapters(recipe_path: str, duration_s: float, seed: int,
                    every_s: float = 600.0) -> str:
    with open(recipe_path) as f:
        cfg = yaml.safe_load(f)
    lines = []
    for i, t in enumerate(chapter_marks(cfg, duration_s, seed, every_s)):
        h, rem = divmod(int(t), 3600)
        m, s = divmod(rem, 60)
        stamp = f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        lines.append(f"{stamp} Section {i + 1}")
    return "\n".join(lines)
