"""Final pass: gain to the recipe's LUFS target (true-peak-safe), edge fades,
24-bit PCM output. Streaming, so 3-hour files never load into memory."""

import numpy as np
import soundfile as sf


def finalize_file(
    raw_path: str,
    out_path: str,
    measured_lufs: float,
    measured_tp_db: float,
    target_lufs: float,
    tp_ceiling_db: float = -2.0,
    fade_s: float = 4.0,
    chunk_frames: int = 480_000,
) -> dict:
    lufs_gain_db = target_lufs - measured_lufs
    tp_allowed_gain_db = tp_ceiling_db - measured_tp_db
    gain_db = min(lufs_gain_db, tp_allowed_gain_db)
    gain = 10.0 ** (gain_db / 20.0)

    with sf.SoundFile(raw_path) as fin:
        total = fin.frames
        sr = fin.samplerate
        fade_n = int(fade_s * sr)
        with sf.SoundFile(out_path, "w", samplerate=sr, channels=2, subtype="PCM_24") as fout:
            pos = 0
            while pos < total:
                x = fin.read(min(chunk_frames, total - pos), dtype="float64", always_2d=True)
                n = x.shape[0]
                x *= gain
                if pos < fade_n:  # fade-in
                    idx = np.arange(pos, pos + n)
                    ramp = np.clip(idx / fade_n, 0.0, 1.0)
                    x *= (0.5 - 0.5 * np.cos(np.pi * ramp))[:, None]
                if pos + n > total - fade_n:  # fade-out
                    idx = np.arange(pos, pos + n)
                    ramp = np.clip((total - idx) / fade_n, 0.0, 1.0)
                    x *= (0.5 - 0.5 * np.cos(np.pi * ramp))[:, None]
                fout.write(np.clip(x, -0.999, 0.999))
                pos += n

    return {
        "gain_db_applied": round(gain_db, 2),
        "achieved_lufs_approx": round(measured_lufs + gain_db, 2),
        "true_peak_db_after": round(measured_tp_db + gain_db, 2),
        "limited_by_true_peak": tp_allowed_gain_db < lufs_gain_db,
    }
