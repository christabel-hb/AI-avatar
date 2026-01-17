# AI-avatar

## What this is 🎭 (still in progress)

**AI-avatar** is a work‑in‑progress virtual avatar project (female manhwa/anime style).

Current pipeline:

1. Generates speech audio from text using an XTTS FastAPI server.
2. Runs Wav2Lip to produce a lip-synced video.

The goal is a real-time conversational avatar (LLM → TTS → lip-sync video → UI).

## Setup

Create and activate a Python environment, then install dependencies.

- App (client): `requirements-app.txt`
- TTS server: `requirements-tts.txt`
- Wav2Lip Python deps: `requirements-wav2lip.txt`

> Note: Wav2Lip itself is expected at `D:\tools\Wav2Lip` and requires its own setup/checkpoint.

## Run

### 1) Start the TTS server

Run in its own terminal:

```powershell
.\.venv310\Scripts\python.exe -m uvicorn tts_server:app --host 127.0.0.1 --port 5055
```

### 2) Run the client

```powershell
.\.venv310\Scripts\python.exe app.py
```

Outputs are written to `data/outputs/`.

## Demo outputs

This repo includes a small sample output so you can quickly see what the pipeline produces:

- `data/outputs/demo.mp4`
- `data/outputs/tts.wav`

## Wav2Lip (external dependency)

This project uses **Wav2Lip** for lip-syncing.

- Official repo: https://github.com/Rudrabha/Wav2Lip

In this workspace we assume Wav2Lip is available at `D:\tools\Wav2Lip`.
You’ll also need to download a Wav2Lip checkpoint (for example `wav2lip_gan.pth` or `wav2lip.pth`) and place it where your Wav2Lip setup expects it.

## Notes

- This repo ignores `data/outputs/` and other generated media by default (see `.gitignore`).
- If you want GPU acceleration for Wav2Lip, you need a CUDA-enabled PyTorch build.

### What’s ignored (and why)

This project intentionally does **not** commit:

- Virtual environments (e.g. `.venv310/`) — they’re machine-specific and huge.
- Python cache files (e.g. `__pycache__/`).
- Generated outputs (e.g. most of `data/outputs/`, `*.wav`, `*.mp4`) — these are regenerated and can be large.

I *did* commit a small allow-listed demo (`data/outputs/demo.mp4` and `data/outputs/tts.wav`) for convenience.

