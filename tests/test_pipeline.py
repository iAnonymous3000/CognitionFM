"""End-to-end smoke tests for the distribution pipeline: validation guards,
cover art, video assembly, and the stream path (local file mode)."""

import os
import shutil
import subprocess

import pytest

from cognitionfm.art import _series_rng, generate_art
from cognitionfm.render import MIN_RENDER_S, parse_duration, render
from cognitionfm.stream import _endless_chunks, stream

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE = os.path.join(REPO, "recipes", "downshift.yaml")

needs_ffmpeg = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg/ffprobe not installed")


def ffprobe_duration_s(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def test_parse_duration_rejects_nonpositive():
    with pytest.raises(ValueError):
        parse_duration("0s")
    with pytest.raises(ValueError):
        parse_duration("0h0m0s")


def test_render_rejects_too_short(tmp_path):
    with pytest.raises(ValueError, match="duration"):
        render(RECIPE, 1.0, 1, str(tmp_path / "x.wav"), verbose=False)


def test_endless_chunks_rejects_hanging_config():
    # segment < 2x crossfade would buffer forever without ever yielding
    gen = _endless_chunks({"generator": "ambient_layers"}, 1, 5.0, 8.0)
    with pytest.raises(ValueError, match="crossfade"):
        next(gen)


def test_art_smoke(tmp_path):
    p = generate_art("downshift", 7, str(tmp_path / "a.png"))
    assert os.path.getsize(p) > 10_000  # a real image, not a stub


def test_art_rng_distinct_for_same_length_names():
    # regression: seeding by len(name) gave same-length series (sleep-wind-down
    # vs morning-ramp-up) an identical composition for the same seed
    a = _series_rng("sleep-wind-down", 42).random(8)
    b = _series_rng("morning-ramp-up", 42).random(8)
    assert not (a == b).all()


@needs_ffmpeg
def test_video_duration_matches_audio(tmp_path):
    from cognitionfm.video import assemble_video
    wav = str(tmp_path / "s.wav")
    render(RECIPE, MIN_RENDER_S, 1, wav, verbose=False)
    mp4 = assemble_video(wav, str(tmp_path / "s.mp4"))
    assert abs(ffprobe_duration_s(mp4) - MIN_RENDER_S) < 1.5


@needs_ffmpeg
def test_stream_max_duration_is_exact(tmp_path):
    # regression: -shortest alone let the looped image overrun 5s audio to 18s
    flv = str(tmp_path / "s.flv")
    stream(RECIPE, flv, seed0=1, segment_s=30.0, crossfade_s=8.0,
           max_duration_s=20.0)
    # allow ~1s of FLV container rounding (last-packet timestamp), nothing more
    assert abs(ffprobe_duration_s(flv) - 20.0) < 1.5
