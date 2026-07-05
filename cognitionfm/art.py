"""Generative cover art, seed-linked to the audio.

Same seed -> same art as the mix it accompanies (provenance made visible).
Aesthetic follows the audio rules: slow smooth fields, one accent color per
series, nothing busy. Each video gets materially distinct art, which also
satisfies platform originality policies (docs/04-publishing-plan.md).
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# accent per series (R, G, B); background stays near-black
SERIES = {
    "deep-work-verbal":     {"accent": (96, 148, 210), "title": "Deep Work - Verbal"},
    "deep-work-analytical": {"accent": (108, 190, 170), "title": "Deep Work - Analytical"},
    "downshift":            {"accent": (196, 150, 110), "title": "Downshift"},
    "sleep-wind-down":      {"accent": (110, 105, 165), "title": "Sleep Wind-Down"},
    "morning-ramp-up":      {"accent": (222, 186, 100), "title": "Morning Ramp-Up"},
}
DEFAULT = {"accent": (140, 140, 150), "title": "CognitionFM"}

FONT_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNS.ttf",
]


def _font(size: int):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _smooth_field(rng: np.random.Generator, w: int, h: int, waves: int = 5) -> np.ndarray:
    """Sum of slow 2D cosine waves, normalized to [0, 1]. The visual analog of
    the audio's slow_drift: smooth, seeded, never repeating exactly."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float64)
    x /= w
    y /= h
    field = np.zeros((h, w))
    for _ in range(waves):
        fx, fy = rng.uniform(0.4, 1.8, 2)
        phase = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.5, 1.0)
        field += amp * np.cos(2 * np.pi * (fx * x + fy * y) + phase)
    field -= field.min()
    field /= field.max()
    return field


def _render_base(recipe_name: str, seed: int, size: tuple[int, int]) -> Image.Image:
    w, h = size
    meta = SERIES.get(recipe_name, DEFAULT)
    accent = np.array(meta["accent"], dtype=np.float64)
    bg = np.array([13, 15, 19], dtype=np.float64)

    rng = np.random.default_rng([seed, len(recipe_name)])
    field = _smooth_field(rng, w, h) ** 1.8  # push toward dark; accent glows sparsely

    # radial vignette keeps edges calm and text readable
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    r = np.sqrt(((xx / w) - 0.5) ** 2 + ((yy / h) - 0.5) ** 2)
    field *= np.clip(1.15 - 1.1 * r, 0.15, 1.0)

    img = bg[None, None, :] + field[:, :, None] * (accent - bg)[None, None, :] * 0.55
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")

    draw = ImageDraw.Draw(im)
    title_font = _font(int(h * 0.062))
    sub_font = _font(int(h * 0.026))
    margin = int(h * 0.07)
    draw.text((margin, h - margin - int(h * 0.115)), meta["title"],
              font=title_font, fill=(235, 235, 235))
    draw.text((margin, h - margin - int(h * 0.03)),
              f"CognitionFM · original generative audio · seed {seed}",
              font=sub_font, fill=(150, 152, 158))
    return im


def generate_art(recipe_name: str, seed: int, out_path: str,
                 size: tuple[int, int] = (1920, 1080)) -> str:
    im = _render_base(recipe_name, seed, size)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    im.save(out_path)
    return os.path.abspath(out_path)


def generate_video_frames(recipe_name: str, seed: int, notes: list[str], out_dir: str,
                          size: tuple[int, int] = (1920, 1080)) -> list[str]:
    """One frame per note: base art + a caption top-left. The video pipeline
    cycles these - the 'why it sounds like this' rotation is baked into pixels
    (PIL typography; no dependence on ffmpeg's optional drawtext filter)."""
    w, h = size
    base = _render_base(recipe_name, seed, size)
    caption_font = _font(int(h * 0.028))
    margin = int(h * 0.06)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, note in enumerate(notes):
        im = base.copy()
        ImageDraw.Draw(im).text((margin, margin), note,
                                font=caption_font, fill=(205, 207, 212))
        p = os.path.join(out_dir, f"frame{i}.png")
        im.save(p)
        paths.append(os.path.abspath(p))
    return paths
