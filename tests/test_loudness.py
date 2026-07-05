import numpy as np

from cognitionfm.master.loudness import LufsMeter, true_peak_db

SR = 48_000


def _sine_stereo(freq, db_fs, seconds):
    t = np.arange(int(seconds * SR)) / SR
    amp = 10 ** (db_fs / 20.0)
    x = amp * np.sin(2 * np.pi * freq * t)
    return np.stack([x, x], axis=1)


def test_bs1770_reference_tone():
    """EBU Tech 3341 case 1: 997 Hz sine at -18 dBFS in both channels -> -18 LUFS."""
    meter = LufsMeter(SR)
    meter.add(_sine_stereo(997.0, -18.0, 10.0))
    assert abs(meter.integrated() - (-18.0)) < 0.2


def test_bs1770_streaming_matches_single_pass():
    x = _sine_stereo(440.0, -24.0, 8.0)
    whole = LufsMeter(SR)
    whole.add(x)
    chunked = LufsMeter(SR)
    for i in range(0, len(x), 12_345):  # deliberately awkward chunk size
        chunked.add(x[i:i + 12_345])
    assert abs(whole.integrated() - chunked.integrated()) < 0.05


def test_gating_ignores_silence():
    """Silence padding must not drag integrated loudness down (absolute gate)."""
    tone = _sine_stereo(997.0, -18.0, 5.0)
    silence = np.zeros((SR * 5, 2))
    meter = LufsMeter(SR)
    meter.add(np.vstack([tone, silence]))
    assert abs(meter.integrated() - (-18.0)) < 0.3


def test_true_peak_on_full_scale_sine():
    x = _sine_stereo(997.0, 0.0, 1.0)
    tp = true_peak_db(x)
    assert -0.2 < tp < 0.5  # oversampled peak of a sine ~ 0 dBTP
