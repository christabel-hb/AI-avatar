from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import traceback
import subprocess

app = FastAPI()

_TTS = None
_DEVICE = "cpu"

class TTSIn(BaseModel):
    text: str
    ref_wav: str = "data/voice_ref.wav"
    language: str = "en"
    outfile: str = "data/outputs/tts.wav"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/tts")
def synth(inp: TTSIn):
    global _TTS
    out = Path(inp.outfile)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        if _TTS is None:
            from TTS.api import TTS
            _TTS = TTS(
                "tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=False
            )

        _TTS.tts_to_file(
            text=inp.text,
            speaker_wav=inp.ref_wav,
            language=inp.language,
            file_path=str(out),
            speed=1.1
        )

        return {"ok": True, "outfile": str(out)}

    except Exception:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="XTTS failed")
