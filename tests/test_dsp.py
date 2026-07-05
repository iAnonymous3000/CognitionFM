import numpy as np
import pytest

from cognitionfm.dsp.env import asr_envelope
from cognitionfm.dsp.filters import one_pole_lowpass
from cognitionfm.dsp.osc import partial_stack

SR = 48_000


def test_envelope_shape_and_continuity():
    env = asr_envelope(SR * 10, SR, attack_s=2.0, release_s=4.0)
    assert env[0] == 0.0
    assert abs(env[-1]) < 1e-3
    assert env.max() <= 1.0
    # raised-cosine: no discontinuities anywhere
    assert np.abs(np.diff(env)).max() < 1e-3
    # sustain section is flat at 1
    assert np.allclose(env[SR * 3: SR * 5], 1.0)


def test_envelope_short_event_scales_segments():
    env = asr_envelope(SR, SR, attack_s=2.0, release_s=4.0)  # 1s event, 6s of ramps
    assert len(env) == SR
    assert env[0] == 0.0 and abs(env[-1]) < 1e-3
    assert env.max() <= 1.0


def test_one_pole_lowpass_attenuates_highs():
    t = np.arange(SR) / SR
    low = np.sin(2 * np.pi * 100 * t)
    high = np.sin(2 * np.pi * 8000 * t)
    cutoff = 500.0
    low_out = one_pole_lowpass(low, cutoff, SR)
    high_out = one_pole_lowpass(high, cutoff, SR)
    gain_low = np.abs(low_out[SR // 2:]).max()
    gain_high = np.abs(high_out[SR // 2:]).max()
    assert gain_low > 0.9
    assert gain_high < 0.15


def test_partial_stack_respects_nyquist():
    rng = np.random.default_rng(0)
    # 20 kHz fundamental is kept; its 40 kHz harmonic must be dropped, not
    # aliased (40 kHz would fold to 8 kHz at sr=48k)
    x = partial_stack(20_000.0, SR, SR, [(1.0, 1.0), (2.0, 1.0)], rng)
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(SR, 1 / SR)
    alias_band = spec[(freqs > 7_800) & (freqs < 8_200)].max()
    kept_band = spec[(freqs > 19_800) & (freqs < 20_200)].max()
    assert alias_band < kept_band * 1e-6


def test_partial_stack_deterministic_per_rng_seed():
    a = partial_stack(220.0, SR, SR, [(1.0, 1.0)], np.random.default_rng(5))
    b = partial_stack(220.0, SR, SR, [(1.0, 1.0)], np.random.default_rng(5))
    assert np.array_equal(a, b)
