"""Convolution reverb with a synthetic impulse response.

A shaped-noise IR gives a dense, non-metallic tail (no comb-filter ringing)
and is fully vectorizable: each chunk is FFT-convolved and the tail carried
into the next chunk (overlap-add), so 3-hour renders stream in constant memory.
"""

import numpy as np
from scipy.signal import fftconvolve, lfilter


def _one_pole(x: np.ndarray, cutoff_hz: float, sr: int, highpass: bool = False) -> np.ndarray:
    k = np.exp(-2.0 * np.pi * cutoff_hz / sr)
    low = lfilter([1.0 - k], [1.0, -k], x, axis=0)
    return x - low if highpass else low


def synth_impulse_response(
    sr: int,
    t60_s: float = 7.0,
    damp_hz: float = 3200.0,
    hf_t60_ratio: float = 0.35,
    predelay_ms: float = 20.0,
    seed: int = 7,
) -> np.ndarray:
    """Stereo IR: decorrelated noise, exponential decay, darker/faster-decaying highs."""
    n = int(t60_s * sr)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal((n, 2))
    t = np.arange(n, dtype=np.float64)[:, None] / sr

    low = _one_pole(noise, damp_hz, sr)
    high = noise - low
    env_low = np.exp(-6.91 * t / t60_s)                    # -60 dB at t60
    env_high = np.exp(-6.91 * t / (t60_s * hf_t60_ratio))  # highs die faster
    ir = low * env_low + high * env_high

    fade_in = int(0.010 * sr)
    ir[:fade_in] *= np.linspace(0.0, 1.0, fade_in)[:, None]
    ir = np.vstack([np.zeros((int(predelay_ms * 1e-3 * sr), 2)), ir])
    ir /= np.sqrt((ir ** 2).sum(axis=0)).max()             # unit energy per channel
    return ir.astype(np.float64)


class ConvolutionReverb:
    def __init__(self, ir: np.ndarray, wet: float = 0.4, dry: float = 1.0):
        self.ir = ir
        self.wet = wet
        self.dry = dry
        self._tail = np.zeros((ir.shape[0] - 1, 2), dtype=np.float64)

    def process(self, block: np.ndarray) -> np.ndarray:
        """block: (n, 2) float. Returns dry+wet mix of the same length."""
        n = block.shape[0]
        wet = np.stack(
            [fftconvolve(block[:, ch], self.ir[:, ch]) for ch in (0, 1)], axis=1
        )
        wet[: self._tail.shape[0]] += self._tail
        out = self.dry * block + self.wet * wet[:n]
        # carry everything past this block into the next call
        tail = np.zeros_like(self._tail)
        remainder = wet[n:]
        tail[: remainder.shape[0]] = remainder
        self._tail = tail
        return out
