import sys
import subprocess
from google import genai
from google.genai import types

client = genai.Client(api_key="AQ.Ab8RN6JLSF5hvTk42FaM0pxJqlZRmKWtYFmRVU0hQiDlEm8vYg")
cfg = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))
    )
)

style = "You are a high-energy, fast-paced, passionate sports talk show host. Speak with infectious excitement, rapid cadence, and electrifying adrenaline!"
text = "Chiefs Kingdom! Testing Gemini 3.8 Flash TTS with the exact Hook style prompt!"
full_content = f'{style}\n\n"{text}"'

try:
    resp = client.models.generate_content(
        model="gemini-3.8-flash-tts",
        contents=full_content,
        config=cfg
    )
    raw = resp.candidates[0].content.parts[0].inline_data.data
    subprocess.run(["ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0", "-b:a", "192k", "data/clips/test_38_styled.mp3"], input=raw, check=True)
    print("SUCCESS! Generated test_38_styled.mp3 with exact Hook prompt! Size:", len(raw))
except Exception as e:
    print("FAILED:", e)
