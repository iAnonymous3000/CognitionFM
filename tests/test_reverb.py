import numpy as np

from cognitionfm.fx.reverb import ConvolutionReverb, synth_impulse_response

SR = 48_000


def test_ir_decays_to_target():
    ir = synth_impulse_response(SR, t60_s=2.0, predelay_ms=0.0, seed=1)
    early = np.abs(ir[: SR // 10]).max()
    late = np.abs(ir[-SR // 10:]).max()
    assert late < early * 0.01  # ~-40 dB or more by the tail end


def test_streaming_equals_single_pass():
    """Chunked overlap-add must be sample-identical to one big convolution."""
    rng = np.random.default_rng(3)
    x = rng.standard_normal((SR * 2, 2)) * 0.1
    ir = synth_impulse_response(SR, t60_s=0.5, predelay_ms=5.0, seed=2)

    whole = ConvolutionReverb(ir, wet=0.4).process(x)

    chunked = ConvolutionReverb(ir, wet=0.4)
    parts = [chunked.process(x[i:i + 10_000]) for i in range(0, len(x), 10_000)]
    assert np.allclose(whole, np.vstack(parts), atol=1e-10)


def test_tail_carries_between_chunks():
    ir = synth_impulse_response(SR, t60_s=1.0, predelay_ms=0.0, seed=4)
    rv = ConvolutionReverb(ir, wet=1.0, dry=0.0)
    impulse = np.zeros((1000, 2))
    impulse[0] = 1.0
    rv.process(impulse)
    tail = rv.process(np.zeros((1000, 2)))
    assert np.abs(tail).max() > 0  # reverb rings into the silent chunk
