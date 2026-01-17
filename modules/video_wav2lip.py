import subprocess
from pathlib import Path

WAV2LIP_DIR = r"D:\tools\Wav2Lip"
CHECKPOINT = r"D:\tools\Wav2Lip\checkpoints\wav2lip_gan.pth"
FACE = r"D:\c\proj\ivyAssistant\data\drivers\neutral.mp4"

def run_wav2lip(audio_wav, outfile):
    audio_wav = Path(audio_wav).resolve()
    outfile = Path(outfile).resolve()

    cmd = [
        "python", "inference.py",
        "--checkpoint_path", CHECKPOINT,
        "--face", FACE,
        "--audio", str(audio_wav),
        "--outfile", str(outfile),
        "--nosmooth"
    ]

    subprocess.run(cmd, cwd=WAV2LIP_DIR, check=True)
    return str(outfile)
