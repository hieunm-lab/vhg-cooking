"""Cấu hình chung: đường dẫn thư mục và file settings.json."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)  # đang chạy từ file .exe (PyInstaller)
# Thư mục gốc của tool: cạnh file .exe khi đóng gói, cạnh mã nguồn khi chạy bằng python
ROOT = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent.parent
BUNDLE = Path(getattr(sys, "_MEIPASS", ROOT))  # nơi chứa thư viện đã đóng gói
BIN = ROOT / "bin"                             # ffmpeg.exe, node.exe đi kèm
DATA = ROOT / "data"
MODELS = ROOT / "models"                       # model Whisper lưu trong thư mục tool (mang đi máy khác được)
if FROZEN or MODELS.exists():
    MODELS.mkdir(exist_ok=True)
    os.environ.setdefault("HF_HOME", str(MODELS))


def _tool(name: str) -> str:
    for p in (BIN / f"{name}.exe", BUNDLE / "bin" / f"{name}.exe"):
        if p.exists():
            return str(p)
    return shutil.which(name) or name


FFMPEG = _tool("ffmpeg")
NODE = _tool("node")
# chạy lệnh ngầm, không bật cửa sổ đen trên Windows
NO_WINDOW = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
GAMES = DATA / "games"      # mỗi trận một thư mục: data/games/<espn_event_id>/
CLIPS = DATA / "clips"      # clip HD đã xuất
EXPERTS = DATA / "experts"  # video & transcript chuyên gia: data/experts/<expert_id>/
SETTINGS_FILE = ROOT / "settings.json"

for d in (DATA, GAMES, CLIPS, EXPERTS):
    d.mkdir(parents=True, exist_ok=True)

DEFAULTS = {
    "gemini_api_key": "",
    "whisper_model": "small.en",   # small.en nhanh; medium.en chính xác hơn nhưng chậm hơn
    "whisper_device": "cuda",      # "cuda" (card NVIDIA) hoặc "cpu"
    "proxy_height": 360,           # bản phân tích nhẹ
    "hq_height": 1080,             # bản xuất clip chất lượng cao
    "ocr_fps": 1,                  # số khung hình đọc thanh tỷ số mỗi giây
}


def load_settings() -> dict:
    s = dict(DEFAULTS)
    if SETTINGS_FILE.exists():
        try:
            s.update(json.loads(SETTINGS_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    if os.environ.get("GEMINI_API_KEY") and not s["gemini_api_key"]:
        s["gemini_api_key"] = os.environ["GEMINI_API_KEY"]
    return s


def save_settings(s: dict) -> None:
    SETTINGS_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def game_dir(event_id: str) -> Path:
    d = GAMES / str(event_id)
    d.mkdir(parents=True, exist_ok=True)
    return d


def expert_dir(expert_id: str) -> Path:
    d = EXPERTS / str(expert_id)
    d.mkdir(parents=True, exist_ok=True)
    return d

