"""CLI: python -m cognitionfm render --recipe deep-work-verbal --duration 10m --seed 42"""

import argparse
import glob
import os
import sys

from .render import parse_duration, render

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(REPO_ROOT, "recipes")


def resolve_recipe(name_or_path: str) -> str:
    if os.path.isfile(name_or_path):
        return name_or_path
    candidate = os.path.join(RECIPES_DIR, f"{name_or_path}.yaml")
    if os.path.isfile(candidate):
        return candidate
    available = [os.path.splitext(os.path.basename(p))[0]
                 for p in glob.glob(os.path.join(RECIPES_DIR, "*.yaml"))]
    sys.exit(f"recipe {name_or_path!r} not found. Available: {', '.join(sorted(available))}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cognitionfm")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render", help="render a recipe to a mastered WAV")
    r.add_argument("--recipe", required=True, help="recipe name (in recipes/) or YAML path")
    r.add_argument("--duration", required=True, help="e.g. 10m, 90m, 1h30m")
    r.add_argument("--seed", type=int, default=1)
    r.add_argument("--out", default=None, help="output WAV path")

    sub.add_parser("recipes", help="list available recipes")

    v = sub.add_parser("video", help="wrap a rendered WAV into a YouTube-ready mp4")
    v.add_argument("--audio", required=True)
    v.add_argument("--out", default=None)
    v.add_argument("--image", default=None, help="cover image (PNG/JPG); flat color if omitted")
    v.add_argument("--recipe", default=None,
                   help="recipe name: auto-generates seed-linked cover art and note overlays")
    v.add_argument("--seed", type=int, default=1, help="seed for generated cover art")

    a = sub.add_parser("art", help="generate seed-linked cover art for a recipe")
    a.add_argument("--recipe", required=True)
    a.add_argument("--seed", type=int, default=1)
    a.add_argument("--out", default=None)

    s = sub.add_parser("stream", help="stream endless generative audio (RTMP URL or file)")
    s.add_argument("--recipe", required=True)
    s.add_argument("--url", required=True, help="rtmp://... or a local .flv path for testing")
    s.add_argument("--seed", type=int, default=1, help="starting seed; increments per segment")
    s.add_argument("--segment", default="30m", help="length of each generated segment")
    s.add_argument("--max-duration", default=None, help="stop after this long (testing); endless if omitted")

    args = ap.parse_args(argv)
    if args.cmd == "recipes":
        for p in sorted(glob.glob(os.path.join(RECIPES_DIR, "*.yaml"))):
            print(os.path.splitext(os.path.basename(p))[0])
        return
    if args.cmd == "art":
        from .art import generate_art
        name = os.path.splitext(os.path.basename(resolve_recipe(args.recipe)))[0]
        out = args.out or os.path.join(REPO_ROOT, "art", f"{name}-seed{args.seed}.png")
        print(generate_art(name, args.seed, out))
        return
    if args.cmd == "video":
        from .video import assemble_video
        frames, image = None, args.image
        if args.recipe and image is None:
            import yaml
            from .art import generate_art, generate_video_frames
            recipe_path = resolve_recipe(args.recipe)
            name = os.path.splitext(os.path.basename(recipe_path))[0]
            notes = yaml.safe_load(open(recipe_path)).get("notes")
            art_dir = os.path.join(REPO_ROOT, "art", f"{name}-seed{args.seed}")
            if notes:
                frames = generate_video_frames(name, args.seed, notes, art_dir)
            else:
                image = generate_art(name, args.seed, art_dir + ".png")
        out = args.out or os.path.splitext(args.audio)[0] + ".mp4"
        print(assemble_video(args.audio, out, image_path=image, frames=frames))
        return
    if args.cmd == "stream":
        from .stream import stream
        max_s = parse_duration(args.max_duration) if args.max_duration else None
        stream(resolve_recipe(args.recipe), args.url, seed0=args.seed,
               segment_s=parse_duration(args.segment), max_duration_s=max_s)
        return

    recipe_path = resolve_recipe(args.recipe)
    duration = parse_duration(args.duration)
    name = os.path.splitext(os.path.basename(recipe_path))[0]
    out = args.out or os.path.join(
        REPO_ROOT, "renders", f"{name}-{args.duration}-seed{args.seed}.wav")
    print(f"rendering {name} for {args.duration} (seed {args.seed}) -> {out}")
    render(recipe_path, duration, args.seed, out)


if __name__ == "__main__":
    main()
