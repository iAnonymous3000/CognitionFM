"""Slow deterministic modulation.

`slow_drift` is a stateless value-noise function of absolute time: a seeded sum
of incommensurate slow sinusoids. Being a pure function of (t, seed) keeps
renders deterministic regardless of chunking.
"""

import numpy as np


def slow_drift(t: float | np.ndarray, seed: int, rate_hz: float = 0.004,
               components: int = 4) -> float | np.ndarray:
    """Smooth drift in [-1, 1], changing over minutes, deterministic per seed."""
    rng = np.random.default_rng(seed)
    freqs = rate_hz * rng.uniform(0.3, 1.7, components)
    phases = rng.uniform(0.0, 2.0 * np.pi, components)
    amps = rng.uniform(0.5, 1.0, components)
    amps /= amps.sum()
    out = sum(a * np.sin(2.0 * np.pi * f * np.asarray(t, dtype=np.float64) + p)
              for f, p, a in zip(freqs, phases, amps))
    return out
