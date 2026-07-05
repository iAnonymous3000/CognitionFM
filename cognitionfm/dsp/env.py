"""Envelopes. Raised-cosine segments only - no discontinuities anywhere.

The attack-time floor in each recipe exists because sharp onsets are
changing-state events that capture attention (evidence review §1.2).
"""

import numpy as np


def asr_envelope(n: int, sr: int, attack_s: float, release_s: float) -> np.ndarray:
    """Attack-sustain-release envelope with raised-cosine ramps."""
    a = int(attack_s * sr)
    r = int(release_s * sr)
    if a + r > n:  # scale both down proportionally for short events
        scale = n / (a + r)
        a = max(int(a * scale), 1)
        r = max(n - a, 1)
    env = np.ones(n, dtype=np.float64)
    if a > 0:
        env[:a] = 0.5 * (1.0 - np.cos(np.pi * np.arange(a) / a))
    if r > 0:
        env[n - r:] = 0.5 * (1.0 + np.cos(np.pi * np.arange(r) / r))
    return env
