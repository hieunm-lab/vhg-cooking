import subprocess
import json
from pathlib import Path
from xaonau.analyze import transcribe

video_path = Path("data/clips/cowboys_report_hook.webm")
audio_wav = Path("data/clips/cowboys_audio.wav")

# 1. Extract audio
subprocess.run([
    "ffmpeg", "-y", "-i", str(video_path), "-vn", "-ac", "1", "-ar", "16000", str(audio_wav)
], check=True, capture_output=True)

# 2. Transcribe first 60 seconds
model = transcribe.get_model("small.en", "cuda")
segments, info = model.transcribe(str(audio_wav))

print(f"Detected language: {info.language} ({info.language_probability:.2f})")
print("\n--- TRANSCRIPT (First 60s) ---")
for s in segments:
    if s.start > 60:
        break
    print(f"[{s.start:04.1f}s -> {s.end:04.1f}s]: {s.text}")
