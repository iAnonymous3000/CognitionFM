"""Encode short AAC previews of the rendered masters for the public site.

Usage: .venv/bin/python site/make_previews.py
Reads WAV entries from manifest.csv, takes the first PREVIEW_S seconds of each
local render, and writes site/audio/<recipe>-seed<seed>-90s.m4a (committed to
git, unlike the masters: previews are small enough to serve from Pages).

Requires ffmpeg. Masters are regenerable from manifest.csv if renders/ is empty.
"""

import csv
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "site", "audio")
PREVIEW_S = 90


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(REPO, "manifest.csv")) as f:
        rows = [r for r in csv.DictReader(f) if r["artifact"].endswith(".wav")]
    for r in rows:
        src = os.path.join(REPO, "renders", r["artifact"])
        if not os.path.exists(src):
            print(f"skip {r['artifact']}: not rendered locally")
            continue
        name = f"{r['recipe']}-seed{r['seed']}-{PREVIEW_S}s.m4a"
        out = os.path.join(OUT_DIR, name)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-t", str(PREVIEW_S), "-i", src,
            "-af", f"afade=t=out:st={PREVIEW_S - 3}:d=3",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            out,
        ], check=True)
        print(f"wrote site/audio/{name} ({os.path.getsize(out) // 1024} KiB)")


if __name__ == "__main__":
    main()
