"""ITU-R BS.1770-4 integrated loudness (LUFS) and true peak.

Streaming: feed blocks during the render, call `integrated()` once at the end.
Coefficients are the standard's published values for 48 kHz; the engine renders
at 48 kHz only.
"""

import numpy as np
from scipy.signal import lfilter, lfilter_zi, resample_poly

# K-weighting stage 1: high-shelf ("pre") filter, fs = 48000
PRE_B = np.array([1.53512485958697, -2.69169618940638, 1.19839281085285])
PRE_A = np.array([1.0, -1.69065929318241, 0.73248077421585])
# K-weighting stage 2: RLB high-pass, fs = 48000
RLB_B = np.array([1.0, -2.0, 1.0])
RLB_A = np.array([1.0, -1.99004745483398, 0.99007225036621])

HOP_S = 0.100      # gating blocks are 400 ms with 75% overlap = 100 ms hops
BLOCK_HOPS = 4


class LufsMeter:
    def __init__(self, sr: int):
        if sr != 48_000:
            raise ValueError("LufsMeter implements BS.1770 coefficients for 48 kHz only")
        self.sr = sr
        self.hop = int(HOP_S * sr)
        self._zi_pre = [lfilter_zi(PRE_B, PRE_A) * 0.0 for _ in range(2)]
        self._zi_rlb = [lfilter_zi(RLB_B, RLB_A) * 0.0 for _ in range(2)]
        self._sq_remainder = np.zeros((0, 2))
        self._hop_ms: list[np.ndarray] = []  # per-hop mean square, per channel

    def add(self, block: np.ndarray) -> None:
        filtered = np.empty_like(block, dtype=np.float64)
        for ch in (0, 1):
            y, self._zi_pre[ch] = lfilter(PRE_B, PRE_A, block[:, ch], zi=self._zi_pre[ch])
            y, self._zi_rlb[ch] = lfilter(RLB_B, RLB_A, y, zi=self._zi_rlb[ch])
            filtered[:, ch] = y
        sq = np.concatenate([self._sq_remainder, filtered ** 2])
        n_full = sq.shape[0] // self.hop
        for i in range(n_full):
            self._hop_ms.append(sq[i * self.hop:(i + 1) * self.hop].mean(axis=0))
        self._sq_remainder = sq[n_full * self.hop:]

    def integrated(self) -> float:
        """Gated integrated loudness in LUFS."""
        hops = np.array(self._hop_ms)  # (n_hops, 2)
        if hops.shape[0] < BLOCK_HOPS:
            return float("-inf")
        # 400 ms blocks: mean of 4 consecutive hops, per channel, then channel sum
        kernel = np.ones(BLOCK_HOPS) / BLOCK_HOPS
        block_ms = np.stack(
            [np.convolve(hops[:, ch], kernel, mode="valid") for ch in (0, 1)], axis=1
        )
        z = block_ms.sum(axis=1)  # stereo channel weights are 1.0
        with np.errstate(divide="ignore"):
            l_blocks = -0.691 + 10.0 * np.log10(z)
        abs_gate = l_blocks > -70.0
        if not abs_gate.any():
            return float("-inf")
        rel_threshold = -0.691 + 10.0 * np.log10(z[abs_gate].mean()) - 10.0
        gated = abs_gate & (l_blocks > rel_threshold)
        if not gated.any():
            return float("-inf")
        return float(-0.691 + 10.0 * np.log10(z[gated].mean()))


def true_peak_db(block: np.ndarray) -> float:
    """dBTP estimate via 4x oversampling (BS.1770 Annex 2 style)."""
    up = resample_poly(block, 4, 1, axis=0)
    peak = np.abs(up).max()
    return 20.0 * np.log10(peak) if peak > 0 else float("-inf")
