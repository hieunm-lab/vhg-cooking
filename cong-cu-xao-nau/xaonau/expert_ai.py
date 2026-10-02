"""Phân tích nguồn chuyên gia và sinh kịch bản bằng Gemini AI:
1. Bóc tách chủ đề, luận điểm đắt giá từ transcript để người dùng duyệt.
2. Sinh Tiêu đề, Hook, Kịch bản dẫn chuyện và khớp với kho highlight có sẵn.
"""
import json
import re
import urllib.request
import urllib.error
from pathlib import Path

from .config import expert_dir, load_settings, GAMES
from . import library


def _call_gemini(prompt: str, system_instruction: str = "", api_key: str = "") -> str:
    """Gọi Gemini REST API với model gemini-2.5-flash (hoặc gemini-1.5-flash)."""
    if not api_key:
        s = load_settings()
        api_key = s.get("gemini_api_key", "").strip()
    if not api_key:
        raise ValueError("Chưa có Gemini API Key! Hãy vào tab 'Cài đặt' để nhập key.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
        
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"Lỗi Gemini API ({e.code}): {err_msg}")


def analyze_topics_from_transcript(expert_id: str, log=print) -> list[dict]:
    """Dùng Gemini quét qua transcript để trích xuất các phân đoạn / chủ đề đắt giá cho người dùng duyệt."""
    edir = expert_dir(expert_id)
    seg_file = edir / "segments.json"
    meta_file = edir / "meta.json"
    
    if not seg_file.exists():
        raise FileNotFoundError(f"Chưa có transcript cho {expert_id}. Hãy chạy Transcribe trước.")
        
    segments = json.loads(seg_file.read_text(encoding="utf-8"))
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
    title = meta.get("title", expert_id)
    
    # Rút gọn transcript thành dạng thời gian + câu
    compact_lines = []
    for s in segments:
        m, sec = int(s["start"]) // 60, int(s["start"]) % 60
        compact_lines.append(f"[{m:02d}:{sec:02d}] {s.get('speaker','Speaker')}: {s['text']}")
    full_transcript = "\n".join(compact_lines)
    
    log(f"Đang dùng AI phân tích các luận điểm và chủ đề trong: {title}...")
    
    sys_inst = (
        "You are an elite NFL sports analyst and YouTube content strategist. "
        "Your task is to analyze a raw transcript of an NFL talk show / debate / podcast "
        "and segment it into distinct discussion topics / key takes for YouTube video repurposing. "
        "Output ONLY valid JSON matching the requested schema."
    )
    
    user_prompt = f"""
Analyze the following transcript from the video titled: "{title}"

Transcript:
\"\"\"
{full_transcript[:25000]}
\"\"\"

Identify the 4 to 8 most impactful, dramatic, or insightful discussion segments. For each segment, determine:
- start (in seconds, float or int)
- end (in seconds, float or int)
- speaker (Name of the expert/host if mentioned or recognizable, e.g. 'Stephen A. Smith', 'Shannon Sharpe', 'Colin Cowherd', etc. Otherwise 'Host' or 'Analyst')
- topic (Short, punchy topic title in Vietnamese, e.g. 'Stephen A. Smith chỉ trích hàng thủ lỏng lẻo', 'Colin Cowherd ca ngợi Kirk Cousins')
- summary (Summary in Vietnamese, 1-2 sentences capturing their argument)
- quote (The most impactful 1-2 sentence direct English quote from this segment)
- sentiment (One of: 'Tranh cãi', 'Khen ngợi', 'Chỉ trích', 'Dự đoán')
- hype_score (Integer 1 to 10 measuring drama and clickability for YouTube)
- players_mentioned (List of player or coach names mentioned, e.g. ['Kirk Cousins', 'Brock Bowers', 'Klint Kubiak'])

Return a JSON array of objects with the fields:
[
  {{
    "start": 125,
    "end": 260,
    "speaker": "Stephen A. Smith",
    "topic": "Stephen A. Smith tranh cãi về năng lực thật sự của Raiders",
    "summary": "...",
    "quote": "...",
    "sentiment": "Tranh cãi",
    "hype_score": 9,
    "players_mentioned": ["Kirk Cousins", "Brock Bowers"]
  }}
]
"""
    try:
        raw_json = _call_gemini(user_prompt, sys_inst)
        topics = json.loads(raw_json)
    except Exception as e:
        log(f"⚠ Lỗi gọi Gemini AI ({e}). Dùng phân đoạn heuristic dự phòng...")
        topics = _heuristic_topics(segments, title)

    # Bổ sung id và format thời gian hiển thị
    for i, t in enumerate(topics):
        t["id"] = f"{expert_id}_t{i+1}"
        t["expert_id"] = expert_id
        t["expert_title"] = title
        ms, ss = int(t["start"]) // 60, int(t["start"]) % 60
        me, se = int(t["end"]) // 60, int(t["end"]) % 60
        t["time_str"] = f"{ms:02d}:{ss:02d} → {me:02d}:{se:02d}"
        t["dur"] = round(t["end"] - t["start"], 1)

    # Lưu vào topics.json
    (edir / "topics.json").write_text(json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"✅ Đã bóc tách thành công {len(topics)} phân đoạn thảo luận đắt giá!")
    return topics


def _heuristic_topics(segments: list[dict], title: str) -> list[dict]:
    """Phân đoạn dự phòng khi không có mạng hoặc chưa nhập API key."""
    if not segments:
        return []
    total_dur = segments[-1]["end"]
    chunk_dur = max(60, min(180, total_dur / 5))
    topics = []
    cur_start = 0.0
    cur_text = []
    
    for s in segments:
        cur_text.append(s["text"])
        if s["end"] - cur_start >= chunk_dur:
            sample = " ".join(cur_text)
            topics.append({
                "start": round(cur_start, 1),
                "end": round(s["end"], 1),
                "speaker": s.get("speaker", "Chuyên gia"),
                "topic": f"Phân tích về diễn biến và phát biểu của đội ({int(cur_start)//60}p -> {int(s['end'])//60}p)",
                "summary": sample[:160] + "...",
                "quote": sample[:120] + "...",
                "sentiment": "Tranh cãi",
                "hype_score": 8,
                "players_mentioned": []
            })
            cur_start = s["end"]
            cur_text = []
            
    if cur_text:
        sample = " ".join(cur_text)
        topics.append({
            "start": round(cur_start, 1),
            "end": round(segments[-1]["end"], 1),
            "speaker": segments[-1].get("speaker", "Chuyên gia"),
            "topic": f"Tổng kết và dự đoán tương lai ({int(cur_start)//60}p -> {int(segments[-1]['end'])//60}p)",
            "summary": sample[:160] + "...",
            "quote": sample[:120] + "...",
            "sentiment": "Dự đoán",
            "hype_score": 7,
            "players_mentioned": []
        })
    return topics


def find_matching_highlights(players: list[str], keywords: list[str]) -> list[dict]:
    """Tìm kiếm các clip highlight liên quan trong kho CongCuXaoNau."""
    ms = library.analyzed_games()
    if not ms:
        return []
        
    query = " ".join(players + keywords)
    results = library.search(query, ms, only_high=False)
    # Lấy top 5 kết quả tốt nhất
    return results[:5]


def generate_full_script(selected_takes: list[dict], team_name="Raiders", log=print) -> dict:
    """Sinh Hook, 5 Tiêu đề giật gân, Kịch bản dẫn chuyện và bảng timeline khớp Highlight."""
    if not selected_takes:
        raise ValueError("Hãy chọn ít nhất 1 phân đoạn chuyên gia để tạo kịch bản.")

    log("Đang tổng hợp các phân đoạn chuyên gia và tra cứu kho highlight...")
    
    # 1. Tìm kiếm clip highlight tương ứng từ kho
    all_players = []
    for t in selected_takes:
        all_players.extend(t.get("players_mentioned", []))
    all_players = list(dict.fromkeys(all_players))
    
    available_clips = find_matching_highlights(all_players, ["touchdown", "pha dài", "ghi điểm"])
    clips_brief = []
    for c in available_clips:
        clips_brief.append({
            "clip_id": f"seg_{c['id']}",
            "game": c["_game"],
            "type": c.get("type_vi", ""),
            "players": c.get("players", []),
            "clock": f"Q{c.get('q','')} {c.get('clock','')}",
            "dur": c.get("dur", 4),
            "text": c.get("text", "")[:80]
        })

    # 2. Xây dựng prompt cho Gemini
    takes_prompt = []
    for idx, t in enumerate(selected_takes):
        takes_prompt.append(
            f"--- TAKE #{idx+1} ---\n"
            f"Source: {t.get('expert_title')} ({t.get('time_str')})\n"
            f"Speaker: {t.get('speaker')}\n"
            f"Topic: {t.get('topic')}\n"
            f"Quote: \"{t.get('quote')}\"\n"
            f"Summary: {t.get('summary')}\n"
            f"Sentiment: {t.get('sentiment')}\n"
        )
    takes_str = "\n".join(takes_prompt)
    clips_str = json.dumps(clips_brief, ensure_ascii=False, indent=2)

    sys_inst = (
        "You are the head writer and video director for a top-tier NFL YouTube channel "
        "(similar to 'Raiders Nation Update' or major sports news channels). "
        "Your videos get tens of thousands of views because of explosive hooks, emotional drama between experts, "
        "fast-paced narration, and tight synchronization with game highlight clips. "
        "Output ONLY valid JSON."
    )

    prompt = f"""
We are creating a high-retention YouTube video about the {team_name} based on curated opinions from elite NFL experts.

CURATED EXPERT TAKES (SELECTED BY USER):
{takes_str}

AVAILABLE HIGHLIGHT CLIPS IN OUR REPOSITORY (You can map them to sentences):
{clips_str}

REQUIREMENTS:
1. TITLES: Generate 5 high-CTR, dramatic, all-caps or punchy YouTube titles (e.g. '“NO ONE CAN STOP THE RAIDERS!” – ESPN GOES CRAZY AFTER WEEK 3 WIN!').
2. HOOK (First 15-20 seconds): Explosive opening that immediately introduces the heated debate between the experts. Grabs attention in the first 3 seconds.
3. NARRATION SCRIPT (in English, natural conversational American sports tone):
   - Seamlessly connect the selected takes into a compelling story.
   - Introduce what Expert A said, then contrast it with Expert B's counter-argument.
   - Include occasional soundbite markers where the video should briefly cut to the actual expert's voice/face.
   - End with a strong Call-To-Action asking fans for their thoughts in the comments.
4. TIMELINE (Breakdown into 4-5 second visual cuts):
   - For each 4-5 second segment:
     * time: e.g. "0:00 - 0:05"
     * narration: Sentence to speak
     * visual_type: 'motion_still' (Ken Burns zoom photo of player/coach), 'expert_soundbite' (cut 4-6s of actual expert speaking), or 'highlight_clip' (insert a game action clip)
     * visual_asset: Detailed description of what image or clip to display
     * matched_clip_id: If visual_type is 'highlight_clip', pick one clip_id from the available clips list (or null)
     * audio_direction: Voiceover AI + BGM / Expert soundbite original audio / Whoosh SFX

Return a single JSON object with the exact structure:
{{
  "titles": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"],
  "hook": "Full hook narration text...",
  "full_narration": "Full voiceover script in English...",
  "timeline": [
    {{
      "time": "0:00 - 0:05",
      "narration": "...",
      "visual_type": "motion_still",
      "visual_asset": "Dramatic photo of Kirk Cousins pumping his fist, slow zoom in with light particle overlay",
      "matched_clip_id": null,
      "audio_direction": "Voiceover AI + High energy hip-hop beat (-14dB)"
    }},
    {{
      "time": "0:05 - 0:09",
      "narration": "...",
      "visual_type": "highlight_clip",
      "visual_asset": "Highlight clip of fourth-quarter touchdown pass",
      "matched_clip_id": "seg_...",
      "audio_direction": "Voiceover AI + Game audio muted + Whoosh transition"
    }}
  ]
}}
"""
    log("Đang sinh kịch bản hoàn chỉnh bằng Gemini AI...")
    try:
        raw_json = _call_gemini(prompt, sys_inst)
        script_data = json.loads(raw_json)
    except Exception as e:
        log(f"⚠ Lỗi tạo kịch bản bằng Gemini ({e}). Tạo kịch bản mẫu cấu trúc chuẩn...")
        script_data = _fallback_script(selected_takes, team_name, clips_brief)

    log("✅ Kịch bản và Timeline đã được tạo thành công!")
    return script_data


def _fallback_script(selected_takes: list[dict], team_name: str, clips: list[dict]) -> dict:
    """Kịch bản dự phòng mẫu chuẩn phong cách Raiders Nation Update khi không có API key."""
    clip_id = clips[0]["clip_id"] if clips else None
    return {
        "titles": [
            f"“NO ONE CAN STOP THE {team_name.upper()}!” – EXPERTS GO CRAZY AFTER THRILLING PERFORMANCE!",
            f"BREAKING! NFL ANALYSTS MAKE SHOCKING PREDICTIONS ABOUT THE {team_name.upper()}!",
            f"“THEY ARE AFC'S WORST NIGHTMARE!” – NATIONAL MEDIA REACTS TO {team_name.upper()}!",
            f"ESPN BOMBSHELL! MAJOR DEBATE ERUPTS OVER {team_name.upper()} START!",
            f"IS THIS REAL? INSIDERS FINALLY ADMIT THE TRUTH ABOUT THE {team_name.upper()}!"
        ],
        "hook": f"What's up, {team_name} Nation! Just when the critics wrote us off, the national media is finally losing their minds over what this team is doing! Let's break down the heated debate exploding across the NFL world right now!",
        "full_narration": (
            f"What's up, {team_name} Nation! Welcome back to another update. "
            f"The debate surrounding our team has reached a boiling point after the recent performance. "
            f"On one side, analysts are praising the composure and clutch execution down the stretch. "
            f"However, not everyone is convinced just yet. Some critics argue there are still major flaws that need fixing. "
            f"Let's look at the tape and hear what the top experts are saying. Drop a comment below with your honest take and make sure to subscribe!"
        ),
        "timeline": [
            {
                "time": "0:00 - 0:05",
                "narration": f"What's up, {team_name} Nation! The debate surrounding our team has reached a boiling point!",
                "visual_type": "motion_still",
                "visual_asset": f"High-res action photo of star player, slow Ken Burns zoom with particle overlay",
                "matched_clip_id": None,
                "audio_direction": "Voiceover AI (-11dB) + Low hip-hop beat (-24dB)"
            },
            {
                "time": "0:05 - 0:10",
                "narration": "National experts are finally waking up to what we are building here!",
                "visual_type": "motion_still",
                "visual_asset": "Coach on the sideline calling plays, slow zoom",
                "matched_clip_id": None,
                "audio_direction": "Voiceover AI + Beat continues"
            },
            {
                "time": "0:10 - 0:14",
                "narration": "Just look at this incredible clutch moment that changed everything!",
                "visual_type": "highlight_clip",
                "visual_asset": "Key game highlight action footage (3s)",
                "matched_clip_id": clip_id,
                "audio_direction": "Game sound muted + Whoosh transition SFX"
            }
        ]
    }
