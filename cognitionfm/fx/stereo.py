import numpy as np


def equal_power_pan(mono: np.ndarray, pan: float) -> np.ndarray:
    """pan in [-1, 1] -> (n, 2) stereo with constant perceived level."""
    theta = (np.clip(pan, -1.0, 1.0) + 1.0) * np.pi / 4.0
    return np.stack([mono * np.cos(theta), mono * np.sin(theta)], axis=1)
