"""Filters applied per-event (stateless from the pipeline's perspective)."""

import numpy as np
from scipy.signal import lfilter


def one_pole_lowpass(x: np.ndarray, cutoff_hz: float, sr: int) -> np.ndarray:
    """Gentle 6 dB/oct lowpass; used to darken pads without killing them."""
    cutoff_hz = float(np.clip(cutoff_hz, 40.0, sr * 0.45))
    k = np.exp(-2.0 * np.pi * cutoff_hz / sr)
    return lfilter([1.0 - k], [1.0, -k], x)
