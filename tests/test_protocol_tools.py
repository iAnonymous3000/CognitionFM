"""Tests for chapter derivation and session logging."""

import csv
import os

import pytest
import yaml

from cognitionfm.chapters import chapter_marks, chord_change_times, format_chapters
from cognitionfm.sessionlog import append_session

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE = os.path.join(REPO, "recipes", "deep-work-verbal.yaml")


def _cfg():
    with open(RECIPE) as f:
        return yaml.safe_load(f)


def test_chord_changes_are_deterministic_and_ordered():
    a = chord_change_times(_cfg(), 600.0, seed=42)
    b = chord_change_times(_cfg(), 600.0, seed=42)
    assert a == b
    assert a == sorted(a)
    # chord durations are 25-45s, so 600s should hold roughly 13-24 changes
    assert 8 <= len(a) <= 30


def test_chapter_marks_start_at_zero_and_respect_spacing():
    marks = chapter_marks(_cfg(), 1800.0, seed=42, every_s=300.0)
    assert marks[0] == 0.0
    assert marks == sorted(marks)
    assert all(m < 1800.0 for m in marks)
    gaps = [b - a for a, b in zip(marks, marks[1:])]
    assert all(g > 150.0 for g in gaps)  # never closer than half the spacing


def test_format_chapters_output_shape():
    text = format_chapters(RECIPE, 1800.0, seed=42, every_s=600.0)
    lines = text.split("\n")
    assert lines[0] == "00:00 Section 1"
    assert all(" Section " in ln for ln in lines)


def test_append_session_creates_header_and_validates(tmp_path):
    log = str(tmp_path / "log.csv")
    append_session(log, "deep-work-verbal", "a", 4, 5, 5, anchor="2", notes="ok")
    append_session(log, "deep-work-verbal", "B", 3, 3, 4)
    rows = list(csv.DictReader(open(log)))
    assert len(rows) == 2
    assert rows[0]["condition"] == "A"  # normalized to uppercase
    assert rows[0]["focus"] == "4"
    with pytest.raises(ValueError, match="condition"):
        append_session(log, "x", "C", 3, 3, 3)
    with pytest.raises(ValueError, match="focus"):
        append_session(log, "x", "A", 6, 3, 3)
