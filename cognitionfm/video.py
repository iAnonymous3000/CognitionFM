"""Assemble a YouTube-ready mp4: cover image (or flat color) + rendered audio.

Still image at 2 fps keeps files small; h264/yuv420p + AAC is what YouTube
recommends for maximum compatibility.
"""

import os
import subprocess
import tempfile


def _write_concat_list(frames: list[str], tmpdir: str, cycle_s: float = 25.0) -> str:
    """ffconcat playlist cycling the caption frames; looped via -stream_loop.
    Last file is repeated per the concat demuxer's last-duration quirk."""
    path = os.path.join(tmpdir, "frames.ffconcat")
    with open(path, "w") as f:
        f.write("ffconcat version 1.0\n")
        for p in frames:
            f.write(f"file '{p}'\nduration {cycle_s}\n")
        f.write(f"file '{frames[-1]}'\n")
    return path


def _audio_duration_s(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def assemble_video(audio_path: str, out_path: str, image_path: str | None = None,
                   frames: list[str] | None = None,
                   color: str = "0x0f1216", size: str = "1920x1080") -> str:
    """Video source priority: caption `frames` slideshow > still `image_path` >
    flat color. Frames come from art.generate_video_frames."""
    duration = _audio_duration_s(audio_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        if frames:
            playlist = _write_concat_list(frames, tmpdir)
            video_input = ["-stream_loop", "-1", "-f", "concat", "-safe", "0",
                           "-i", playlist]
            vf = ["-vf", "fps=2,format=yuv420p"]
        elif image_path:
            video_input = ["-loop", "1", "-framerate", "2", "-i", image_path]
            vf = []
        else:
            video_input = ["-f", "lavfi", "-i", f"color=c={color}:s={size}:r=2"]
            vf = []
        # explicit -t: with buffered still-image video, -shortest overshoots
        cmd = [
            "ffmpeg", "-y", *video_input, "-i", audio_path, *vf,
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duration:.3f}", out_path,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    return os.path.abspath(out_path)
