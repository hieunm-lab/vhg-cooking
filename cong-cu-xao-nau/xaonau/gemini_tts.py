"""Module tạo giọng đọc giật gân, giàu cảm xúc bằng Google AI Studio (Gemini Voice / Audio).
Hỗ trợ các giọng: Fenrir, Puck, Charon, Zephyr, Kore, Aoede...
Cho phép tinh chỉnh phong cách (style instruction): kịch tính, thể thao giật gân, gằn giọng, cao trào.
"""
import base64
import json
import os
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from .config import FFMPEG, load_settings

VOICE_PRESETS = {
    "Fenrir (Mãnh liệt, gằn giọng, uy lực - Khuyên dùng Thể thao/Kịch tính)": "Fenrir",
    "Puck (Nhiệt huyết, dồn dập, sôi nổi - Bình luận viên thể thao trẻ)": "Puck",
    "Charon (Trầm hùng, nghẹt thở - Phong cách Trailer bom tấn)": "Charon",
    "Zephyr (Dứt khoát, sắc bén, hiện đại)": "Zephyr",
    "Kore (Nữ sắc sảo, tự tin, đanh thép)": "Kore",
    "Aoede (Nữ truyền cảm, cao trào cảm xúc)": "Aoede",
}

DEFAULT_STYLE = (
    "You are an electrifying, sensational American sports talk radio host. "
    "Your voice must be packed with raw intensity, adrenaline, high stakes, and dramatic inflections. "
    "Speak with visceral emotion, dramatic pauses, and breathless excitement. "
    "Deliver these exact words with maximum hype and passion:"
)


def _pcm_to_mp3(pcm_bytes: bytes, output_path: Path, sample_rate: int = 24000) -> None:
    """Chuyển đổi raw PCM 16-bit mono sang file MP3 chất lượng cao chuẩn phát thanh bằng FFmpeg."""
    cmd = [
        FFMPEG, "-y",
        "-f", "s16le",
        "-ar", str(sample_rate),
        "-ac", "1",
        "-i", "pipe:0",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a", "192k",
        str(output_path)
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input=pcm_bytes)
    if p.returncode != 0:
        raise RuntimeError(f"FFmpeg chuyển đổi PCM thất bại: {stderr.decode('utf-8', errors='ignore')}")


def generate_gemini_speech(
    text: str,
    voice_name: str = "Fenrir",
    style_prompt: str = DEFAULT_STYLE,
    api_key: str = "",
    output_path: Optional[Path] = None,
    model: str = "gemini-3.8-flash-tts",
) -> Path:
    """Tạo audio giọng đọc từ Google AI Studio bằng Gemini API.
    
    Args:
        text: Đoạn văn bản cần đọc.
        voice_name: Tên giọng (Fenrir, Puck, Charon, Zephyr, Kore, Aoede).
        style_prompt: Chỉ dẫn diễn xuất cảm xúc cho AI.
        api_key: Gemini API Key (nếu để trống sẽ tự lấy từ settings.json).
        output_path: Đường dẫn file mp3 đầu ra.
        model: Model hỗ trợ audio (mặc định gemini-3.8-flash-tts).
    """
    if not api_key:
        s = load_settings()
        api_key = s.get("gemini_api_key", "").strip()
    if not api_key:
        raise ValueError(
            "Chưa có Gemini API Key! Hãy lấy key miễn phí tại https://aistudio.google.com "
            "và dán vào tab 'Cài đặt' hoặc biến môi trường GEMINI_API_KEY."
        )

    if output_path is None:
        output_path = Path("output_gemini_voice.mp3")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Thử dùng SDK google-genai trước
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        
        full_content = text

        config = types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name
                    )
                )
            ),
        )

        response = client.models.generate_content(
            model=model,
            contents=full_content,
            config=config,
        )

        # Lấy audio data
        part = response.candidates[0].content.parts[0]
        inline_data = getattr(part, "inline_data", None)
        if not inline_data:
            raise RuntimeError("Gemini không trả về dữ liệu âm thanh (inline_data rỗng).")

        audio_bytes = inline_data.data
        mime = getattr(inline_data, "mime_type", "audio/pcm")

        if "wav" in mime:
            # Nếu đã có header WAV, convert sang MP3
            temp_wav = output_path.with_suffix(".temp.wav")
            temp_wav.write_bytes(audio_bytes)
            subprocess.run([FFMPEG, "-y", "-i", str(temp_wav), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", str(output_path)], check=True, capture_output=True)
            temp_wav.unlink(missing_ok=True)
        else:
            # Mặc định là raw PCM 24kHz
            _pcm_to_mp3(audio_bytes, output_path, sample_rate=24000)

        return output_path

    except Exception as e_sdk:
        # Fallback gọi trực tiếp REST API nếu SDK gặp trục trặc
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{style_prompt}\n\n\"{text}\"" if style_prompt else text}
                    ]
                }
            ],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": voice_name
                        }
                    }
                }
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                part = data["candidates"][0]["content"]["parts"][0]
                inline = part.get("inlineData", {})
                b64_data = inline.get("data", "")
                if not b64_data:
                    raise RuntimeError("Gemini REST API không trả về audio data.")
                raw_bytes = base64.b64decode(b64_data)
                mime = inline.get("mimeType", "audio/pcm")
                if "wav" in mime:
                    temp_wav = output_path.with_suffix(".temp.wav")
                    temp_wav.write_bytes(raw_bytes)
                    subprocess.run([FFMPEG, "-y", "-i", str(temp_wav), "-b:a", "192k", str(output_path)], check=True, capture_output=True)
                    temp_wav.unlink(missing_ok=True)
                else:
                    _pcm_to_mp3(raw_bytes, output_path, sample_rate=24000)
                return output_path
        except urllib.error.HTTPError as e_rest:
            err = e_rest.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Lỗi gọi Gemini TTS: SDK err={e_sdk}, REST err({e_rest.code})={err}")
