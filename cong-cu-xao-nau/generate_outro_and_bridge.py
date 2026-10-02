import time
import subprocess
from pathlib import Path
from google import genai
from google.genai import types

data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

client = genai.Client(api_key="AQ.Ab8RN6JLSF5hvTk42FaM0pxJqlZRmKWtYFmRVU0hQiDlEm8vYg")
cfg = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))
    )
)

bridge_text = (
    "Coach Bill Cowher and the CBS crew make a massive statement! "
    "When Patrick Mahomes gets legitimate backfield support, this offense becomes practically unstoppable! "
    "But not everyone is convinced Kansas City has an easy road to another Lombardi trophy! "
    "Over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm on the brutal AFC gauntlet! "
    "Listen closely to how Ryan Clark breaks this down right now!"
)

outro_text = (
    "Chiefs Kingdom, the message is loud and clear! "
    "With Kenneth Walker pounding the rock and Patrick Mahomes commanding the field, this dynasty is ready to make history! "
    "But we want to hear from you! Can ANY team in the NFL stop Kansas City right now?! "
    "Drop your score predictions in the comments below! "
    "Smash that like button, hit subscribe, and turn on notifications so you never miss our breaking Chiefs coverage! "
    "We will catch you in the next one!"
)

def make_clip(text, out_mp3):
    resp = client.models.generate_content(model="gemini-2.5-flash-preview-tts", contents=text, config=cfg)
    raw = resp.candidates[0].content.parts[0].inline_data.data
    subprocess.run([
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0",
        "-b:a", "192k", str(out_mp3)
    ], input=raw, check=True, capture_output=True)
    return out_mp3

print("Generating Bridge...")
make_clip(bridge_text, data_clips / "test_25_bridge.mp3")
print("Sleeping 10s...")
time.sleep(10)
print("Generating Outro...")
make_clip(outro_text, data_clips / "test_25_outro.mp3")
print("ALL GENERATED SUCCESSFULLY!")
