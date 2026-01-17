import subprocess
from pathlib import Path

# =======================
# SWITCH HERE (ONE LINE)
# True  -> use happy.jpg (static image driver)
# False -> use neutral.mp4 (video driver)
USE_IMAGE_DRIVER = True
# =======================

# ----- fixed paths (your real paths) -----
PROJECT_ROOT = Path(r"D:\c\proj\ivyAssistant")

WAV2LIP_DIR = Path(r"D:\tools\Wav2Lip")
PY_WAV2LIP = r"C:\Users\bhchr\miniconda3\envs\wav2lip\python.exe"

GAN = WAV2LIP_DIR / "checkpoints" / "wav2lip_gan.pth"
NONGAN = WAV2LIP_DIR / "checkpoints" / "wav2lip.pth"

if NONGAN.exists():
    CHECKPOINT = NONGAN
elif GAN.exists():
    CHECKPOINT = GAN
else:
    raise RuntimeError(
        "No Wav2Lip checkpoint found. Put wav2lip_gan.pth or wav2lip.pth inside:\n"
        f"{WAV2LIP_DIR / 'checkpoints'}"
    )

FACE_IMAGE = PROJECT_ROOT / "data" / "drivers" / "happy.jpg"
FACE_VIDEO = PROJECT_ROOT / "data" / "drivers" / "neutral.mp4"
FACE_INPUT = FACE_IMAGE if USE_IMAGE_DRIVER else FACE_VIDEO


def run_wav2lip(audio_wav: str, outfile: str) -> str:
    audio_wav = Path(audio_wav).resolve()
    outfile = Path(outfile).resolve()
    outfile.parent.mkdir(parents=True, exist_ok=True)

    if not audio_wav.exists():
        raise RuntimeError(f"Audio not found: {audio_wav}")
    if not FACE_INPUT.exists():
        raise RuntimeError(f"Face input not found: {FACE_INPUT}")
    if not WAV2LIP_DIR.exists():
        raise RuntimeError(f"Wav2Lip dir not found: {WAV2LIP_DIR}")

    cmd = [
        PY_WAV2LIP,
        "inference.py",
        "--checkpoint_path",
        str(CHECKPOINT),
        "--face",
        str(FACE_INPUT),
        "--audio",
        str(audio_wav),
        "--outfile",
        str(outfile),

        # GTX 1650 safe
        "--face_det_batch_size",
        "1",
        "--wav2lip_batch_size",
        "1",

        # Better stability/quality
        "--pads",
        "0",
        "20",
        "0",
        "0",
        # DO NOT add --nosmooth (often worsens blur)
    ]

    print(f"▶ Wav2Lip: {CHECKPOINT.name} | driver={FACE_INPUT.name}")
    subprocess.run(cmd, cwd=str(WAV2LIP_DIR), check=True)

    if not outfile.exists():
        raise RuntimeError(f"Wav2Lip finished but output missing: {outfile}")

    return str(outfile)
