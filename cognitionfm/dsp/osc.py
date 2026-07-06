"""Oscillators. Everything is rendered per-event as a numpy buffer."""

import numpy as np


def partial_stack(
    freq: float,
    n: int,
    sr: int,
    partials: list[tuple[float, float]],
    rng: np.random.Generator,
    detune_cents: float = 3.0,
    pairs: bool = True,
) -> np.ndarray:
    """Sum of detuned sine partials with random phases.

    `partials` is a list of (ratio, amplitude). With `pairs=True` each partial
    is doubled at ±detune for slow chorus beating - the only motion allowed in
    low-variability recipes.
    """
    t = np.arange(n, dtype=np.float64) / sr
    out = np.zeros(n, dtype=np.float64)
    nyquist_guard = sr * 0.45
    for ratio, amp in partials:
        base = freq * ratio
        if base >= nyquist_guard:
            continue
        detunes = (-1.0, 1.0) if pairs else (0.0,)
        for sign in detunes:
            cents = sign * rng.uniform(0.3, detune_cents)
            f = base * 2.0 ** (cents / 1200.0)
            a = amp / len(detunes)
            out += a * np.sin(2.0 * np.pi * f * t + rng.uniform(0.0, 2.0 * np.pi))
    return out
