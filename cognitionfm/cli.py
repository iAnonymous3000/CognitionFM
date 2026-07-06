"""CLI: python -m cognitionfm render --recipe deep-work-verbal --duration 10m --seed 42"""

import argparse
import glob
import os
import sys

from . import REPO_ROOT
from .render import parse_duration, render

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

    v = sub.add_parser("video", help="wrap a rendered WAV into a distribution-ready mp4")
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

    p = sub.add_parser("play", help="render (if not cached) and play a recipe locally")
    p.add_argument("--recipe", required=True)
    p.add_argument("--duration", default="25m", help="session length (default 25m)")
    p.add_argument("--seed", type=int, default=1)

    lg = sub.add_parser("log", help="append a session row to logs/listening-log.csv")
    lg.add_argument("--playlist", required=True, help="e.g. deep-work-verbal, or a [PERSONAL] name")
    lg.add_argument("--condition", required=True, help="A = playlist, B = control")
    lg.add_argument("--focus", type=int, required=True, help="1-5: how often did you drift?")
    lg.add_argument("--state", type=int, required=True, help="1-5: calm/energized as intended?")
    lg.add_argument("--friction", type=int, required=True, help="1-5: want to switch it off?")
    lg.add_argument("--anchor", default="", help="the playlist's objective-ish anchor value")
    lg.add_argument("--notes", default="")

    c = sub.add_parser("chapters", help="print chapter marks for a (recipe, duration, seed)")
    c.add_argument("--recipe", required=True)
    c.add_argument("--duration", required=True)
    c.add_argument("--seed", type=int, default=1)
    c.add_argument("--every", default="10m", help="target chapter spacing (default 10m)")

    args = ap.parse_args(argv)
    try:
        _dispatch(args)
    except (ValueError, RuntimeError) as e:
        sys.exit(f"error: {e}")


def _dispatch(args):
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
    if args.cmd == "play":
        import subprocess
        recipe_path = resolve_recipe(args.recipe)
        name = os.path.splitext(os.path.basename(recipe_path))[0]
        wav = os.path.join(REPO_ROOT, "renders",
                           f"{name}-{args.duration}-seed{args.seed}.wav")
        if not os.path.exists(wav):
            print(f"rendering {name} for {args.duration} (seed {args.seed}) first...")
            render(recipe_path, parse_duration(args.duration), args.seed, wav)
        player = ["afplay", wav] if sys.platform == "darwin" else ["xdg-open", wav]
        print(f"playing {os.path.relpath(wav, REPO_ROOT)}  (ctrl-c stops)")
        try:
            subprocess.run(player)
        except KeyboardInterrupt:
            print("\nstopped. Log the session: python -m cognitionfm log "
                  f"--playlist {name} --condition A --focus N --state N --friction N")
        return
    if args.cmd == "log":
        from .sessionlog import append_session
        row = append_session(
            os.path.join(REPO_ROOT, "logs", "listening-log.csv"),
            args.playlist, args.condition, args.focus, args.state,
            args.friction, args.anchor, args.notes)
        print(f"logged: {row}")
        return
    if args.cmd == "chapters":
        from .chapters import format_chapters
        print(format_chapters(resolve_recipe(args.recipe),
                              parse_duration(args.duration), args.seed,
                              every_s=parse_duration(args.every)))
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
