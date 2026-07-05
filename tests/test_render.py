import glob
import os

import numpy as np
import soundfile as sf
import yaml

from cognitionfm.recipes import GENERATORS
from cognitionfm.render import parse_duration, render

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES = sorted(glob.glob(os.path.join(REPO, "recipes", "*.yaml")))


def test_parse_duration():
    assert parse_duration("10m") == 600.0
    assert parse_duration("1h30m") == 5400.0
    assert parse_duration("45s") == 45.0


def test_all_recipes_generate_valid_events():
    for path in RECIPES:
        cfg = yaml.safe_load(open(path))
        events = GENERATORS[cfg["generator"]](cfg, duration=120.0, seed=1)
        assert events, path
        assert all(0 <= ev.t < 120.0 for ev in events), path
        assert all(ev.dur <= 90.0 for ev in events), path  # carry-buffer contract
        ts = [ev.t for ev in events]
        assert ts == sorted(ts), path


def test_event_generation_deterministic():
    cfg = yaml.safe_load(open(RECIPES[0]))
    a = GENERATORS[cfg["generator"]](cfg, 300.0, seed=9)
    b = GENERATORS[cfg["generator"]](cfg, 300.0, seed=9)
    assert [(e.t, e.freq, e.amp) for e in a] == [(e.t, e.freq, e.amp) for e in b]


def test_render_smoke(tmp_path):
    out = str(tmp_path / "smoke.wav")
    stats = render(RECIPES[0], duration_s=20.0, seed=3, out_path=out, verbose=False)
    x, sr = sf.read(out, always_2d=True)
    assert sr == 48_000
    assert x.shape[0] == 20 * sr
    assert np.abs(x).max() <= 0.999  # never clips
    assert np.abs(x).max() > 0.001   # not silence
    assert not os.path.exists(stats["out_path"] + ".raw.wav")  # temp cleaned up
