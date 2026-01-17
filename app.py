import requests
from pathlib import Path
from modules.video_wav2lip import run_wav2lip

# ---------------- CONFIG ----------------
TTS_URL = "http://127.0.0.1:5055/tts"

PROJECT_ROOT = Path(r"D:\c\proj\ivyAssistant")
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = DATA_DIR / "outputs"

VOICE_REF = DATA_DIR / "voice_ref.wav"
TTS_WAV = OUT_DIR / "tts.wav"
FINAL_MP4 = OUT_DIR / "final.mp4"
# ----------------------------------------


def run_xtts(text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not VOICE_REF.exists():
        raise RuntimeError(f"voice_ref.wav missing: {VOICE_REF}")

    payload = {
        "text": text,
        "ref_wav": str(VOICE_REF),
        "language": "en",
        "outfile": str(TTS_WAV),
    }

    print("[1] Calling XTTS server...")
    r = requests.post(TTS_URL, json=payload, timeout=300)

    if r.status_code != 200:
        raise RuntimeError(f"TTS failed: {r.text}")

    # server may return outfile path (cleaned)
    try:
        out_json = r.json()
        out_path = Path(out_json.get("outfile", str(TTS_WAV)))
    except Exception:
        out_path = TTS_WAV

    if not out_path.exists():
        raise RuntimeError(f"TTS completed but wav not found: {out_path}")

    # ensure our app uses the created wav
    if out_path.resolve() != TTS_WAV.resolve():
        # copy/rename if server returned a different name
        TTS_WAV.write_bytes(out_path.read_bytes())

    print("[1] tts.wav created")


def main():
    print("=== Ivy Assistant Test ===")
    while True:
        text = input("\nEnter text (or 'q'): ").strip()
        if text.lower() == "q":
            break
        if not text:
            continue

        try:
            run_xtts(text)

            print("[2] Running Wav2Lip...")
            run_wav2lip(str(TTS_WAV), str(FINAL_MP4))

            print("\n✅ DONE →", FINAL_MP4)
        except Exception as e:
            print("\n❌ ERROR:", e)


if __name__ == "__main__":
    main()
