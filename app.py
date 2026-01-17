import requests
import subprocess
from pathlib import Path

# ---------------- CONFIG ----------------
TTS_URL = "http://127.0.0.1:5055/tts"

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = DATA_DIR / "outputs"

TTS_WAV = OUT_DIR / "tts.wav"
FINAL_MP4 = OUT_DIR / "final.mp4"

WAV2LIP_DIR = Path("D:/tools/Wav2Lip")
WAV2LIP_PYTHON = Path("C:/Users/bhchr/miniconda3/envs/wav2lip/python.exe")
WAV2LIP_CHECKPOINT = WAV2LIP_DIR / "checkpoints/wav2lip_gan.pth"
FACE_VIDEO = DATA_DIR / "drivers" / "neutral.mp4"

# ----------------------------------------

def run_xtts(text: str):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "text": text,
        "outfile": str(TTS_WAV)
    }

    print("[1] Calling XTTS server...")
    r = requests.post(TTS_URL, json=payload, timeout=120)

    if r.status_code != 200:
        raise RuntimeError(f"TTS failed: {r.text}")

    if not TTS_WAV.exists():
        raise RuntimeError("TTS completed but tts.wav was not created")

    print("[1] tts.wav created")


def run_wav2lip():
    print("[2] Running Wav2Lip...")

    cmd = [
        str(WAV2LIP_PYTHON),
        "inference.py",
        "--checkpoint_path", str(WAV2LIP_CHECKPOINT),
        "--face", str(FACE_VIDEO),
        "--audio", str(TTS_WAV),
        "--outfile", str(FINAL_MP4),
        "--nosmooth"
    ]

    subprocess.run(
        cmd,
        cwd=str(WAV2LIP_DIR),
        check=True
    )

    if not FINAL_MP4.exists():
        raise RuntimeError("Wav2Lip finished but final.mp4 not created")

    print("[2] final.mp4 created")


def main():
    print("=== Ivy Assistant Test ===")
    while True:
        text = input("\nEnter text (or 'q'): ").strip()
        if text.lower() == "q":
            break

        try:
            run_xtts(text)
            run_wav2lip()
            print("\n✅ DONE →", FINAL_MP4)
        except Exception as e:
            print("\n❌ ERROR:", e)


if __name__ == "__main__":
    main()
