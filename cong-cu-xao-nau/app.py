"""CÔNG CỤ XÀO NẤU CONTENT — giao diện chính (chạy: python app.py, hoặc bấm đúp start.bat)."""
import os
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
import queue
import re
import threading
import traceback

import gradio as gr
import pandas as pd

import time

from xaonau import expert, expert_ai, library, nfl, pipeline, yt, gemini_tts
from xaonau.config import DATA, CLIPS, load_settings, save_settings

STYPES = {"Mùa giải chính": 2, "Tiền mùa giải": 1, "Playoff": 3}


def _default_week():
    try:
        season, week, stype = nfl.current_week()
        return season, max(1, week - 1) if stype == 2 else week
    except Exception:
        return 2026, 1


# ---------------- Tab 1: tìm & phân tích ----------------
def load_games(season, stype_label, week):
    games = nfl.week_games(int(season), int(week), STYPES[stype_label])
    df = pd.DataFrame([{
        "Ngày": g["date"], "Trận": f"{g['away']} @ {g['home']}",
        "Tỷ số": f"{g['away_score']}–{g['home_score']}" if g["status"] == "STATUS_FINAL" else "",
        "Trạng thái": "Đã đá" if g["status"] == "STATUS_FINAL" else "Chưa đá",
    } for g in games])
    choices = [(f"{g['short']} ({g['away_score']}–{g['home_score']})" if g["status"] == "STATUS_FINAL" else f"{g['short']} (chưa đá)", g["id"]) for g in games]
    return df, gr.Dropdown(choices=choices, value=choices[0][1] if choices else None), games


def pick_game_row(evt: gr.SelectData, games):
    """Bấm vào một dòng trong bảng trận -> chọn luôn trận đó."""
    i = evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index
    if not games or i is None or i >= len(games):
        return gr.Dropdown()
    return gr.Dropdown(value=games[i]["id"])


def find_hl(game_id, games):
    g = next((x for x in games or [] if x["id"] == game_id), None)
    if not g:
        empty = pd.DataFrame(columns=["Điểm phù hợp", "Tiêu đề", "Kênh", "Dài", "Lượt xem", "Ghi chú"])
        return empty, gr.Dropdown(choices=[], value=None), []
    if g["status"] != "STATUS_FINAL":
        gr.Warning(f"Trận {g['short']} chưa đá, chưa có highlight.")
    c = yt.find_highlights(g)
    df = pd.DataFrame([{"Điểm phù hợp": x["score"], "Tiêu đề": x["title"], "Kênh": x["channel"],
                        "Dài": library.fmt_t(x["duration"]), "Lượt xem": f"{x['views']:,}", "Ghi chú": x["notes"]} for x in c])
    choices = [(f"[{x['score']}] {x['title']} · {x['channel']} · {library.fmt_t(x['duration'])}", x["id"]) for x in c]
    return df, gr.Dropdown(choices=choices, value=choices[0][1] if choices else None), c


def _vid_from_url(u):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/)([A-Za-z0-9_-]{11})", u or "")
    return m[1] if m else None


def run_analysis(game_id, vid_choice, url, force, cands, games):
    vid = _vid_from_url(url) or vid_choice
    if not game_id or not vid:
        raise gr.Error("Cần chọn trận và chọn (hoặc dán link) video highlight.")
    meta = next((c for c in cands or [] if c["id"] == vid), {"id": vid})
    q, lines = queue.Queue(), []
    g = next((x for x in games or [] if x["id"] == game_id), None)
    if g:
        lines.append(f"Trận đang phân tích: {g['away']} @ {g['home']}")
        t = (meta.get("title") or "").lower()
        nicks = [g.get("away_nick") or g["away"].split()[-1], g.get("home_nick") or g["home"].split()[-1]]
        if t and not all(n.lower() in t for n in nicks):
            lines.append(f"⚠ CẢNH BÁO: tiêu đề video không có tên cả 2 đội ({' / '.join(nicks)}): «{meta['title']}». "
                         "Kiểm tra lại đã chọn đúng trận và đúng video chưa.")
        yield "\n".join(lines)

    def work():
        try:
            pipeline.analyze(game_id, vid, meta, force=bool(force), log=q.put)
        except Exception as e:
            q.put(f"❌ Lỗi: {e}")
            q.put(traceback.format_exc(limit=2))
        q.put(None)
    threading.Thread(target=work, daemon=True).start()
    while True:
        m = q.get()
        if m is None:
            break
        lines.append(m)
        yield "\n".join(lines)


def analyzed_df():
    ms = library.analyzed_games()
    return pd.DataFrame([{"Trận": library.game_label(m), "Số đoạn": m["n_segments"], "Pha nhận diện": m["n_plays"],
                          "Tin cậy cao": m["n_high"], "Video": (m.get("video") or {}).get("title", ""),
                          "Phân tích lúc": m["analyzed_at"]} for m in ms])


# ---------------- Tab 2: kho pha bóng ----------------
def game_choices():
    ms = library.analyzed_games()
    return [("Tất cả các trận", "__all__")] + [(library.game_label(m), f"{m['event_id']}|{m['video_id']}") for m in ms]


def refresh_games():
    ch = game_choices()
    return gr.Dropdown(choices=ch, value=ch[1][1] if len(ch) > 1 else "__all__")


def do_search(query, game_sel, only_scoring, only_high, quarter):
    ms = library.analyzed_games()
    if game_sel and game_sel != "__all__":
        ev, vid = game_sel.split("|")
        ms = [m for m in ms if m["event_id"] == ev and m["video_id"] == vid]
    qn = {"Tất cả": None, "Hiệp 1": 1, "Hiệp 2": 2, "Hiệp 3": 3, "Hiệp 4": 4, "Hiệp phụ": 5}[quarter]
    rows = library.search(query or "", ms, only_scoring, only_high, qn)
    df = pd.DataFrame([{
        "#": s["id"], "Bắt đầu": library.fmt_t(s["start"]), "Dài (s)": s["dur"],
        "Hiệp": s.get("q") or "", "Đồng hồ": s.get("clock", ""), "Down": s.get("down", ""),
        "Loại pha": s.get("type_vi", ""), "Mô tả (ESPN)": s.get("text", ""),
        "Cầu thủ": ", ".join(s.get("players", [])[:3]), "Tin cậy": s.get("confidence", ""),
        "Bình luận viên": (s.get("commentary", "")[:140] + "…") if len(s.get("commentary", "")) > 140 else s.get("commentary", ""),
        "Trận": s["_game"],
    } for s in rows])
    info = f"Tìm thấy **{len(rows)}** đoạn." + (" Bấm vào một dòng để xem thử." if rows else "")
    return df, rows, info


def on_select(evt: gr.SelectData, rows):
    if not rows:
        return None, "", None
    s = rows[evt.index[0]]
    also = "".join(f"\n- *Pha phụ trong cùng đoạn:* {a['type_vi']} — {a['text']}" for a in s.get("also", []))
    md = (f"### Đoạn #{s['id']} · {s.get('type_vi','')}\n"
          f"**Trận:** {s['_game']}  \n"
          f"**Vị trí trong video:** {library.fmt_t(s['start'])} → {library.fmt_t(s['end'])} ({s['dur']}s) · "
          f"**khoảnh khắc đỉnh** ≈ {library.fmt_t(s['peak'])} (giây {s['peak'] - s['start']:.1f} của đoạn)  \n"
          f"**Hiệp/đồng hồ/down:** Q{s.get('q','')} · {s.get('clock','')} · {s.get('down','')} · {s.get('yardline','')}  \n"
          f"**Mô tả ESPN:** {s.get('text','')}{also}  \n"
          f"**Nhãn:** {', '.join(s.get('tags', []))} · **Độ tin cậy:** {s.get('confidence','')}"
          + (f" (bình luận viên có nhắc: {', '.join(s['mentioned'])})" if s.get("mentioned") else "") + "  \n"
          f"**Hình:** {s.get('pct_san',0)}% toàn cảnh sân, {s.get('pct_can',0)}% cận cảnh/khác, {s.get('n_shots',0)} shot  \n"
          f"**Bình luận viên:** _{s.get('commentary','')}_")
    try:
        vid = library.preview(s)
    except Exception as e:
        vid, md = None, md + f"\n\n⚠ Không tạo được bản xem thử: {e}"
    return vid, md, s


def do_export(sel, pad):
    if not sel:
        raise gr.Error("Hãy chọn một đoạn trong bảng trước.")
    logs = []
    path = library.export_hq(sel, float(pad), log=logs.append)
    return path, "\n".join(logs + [f"✅ Đã lưu: {path}"])


# ---------------- Tab 3: Studio Kịch bản (Chuyên gia) ----------------
def expert_choices():
    exps = expert.list_experts()
    if not exps:
        return []
    return [(f"{e['title']} ({int(e.get('duration',0))//60}p {int(e.get('duration',0))%60:02d}s)", e['id']) for e in exps]


def refresh_expert_choices():
    ch = expert_choices()
    return gr.Dropdown(choices=ch, value=ch[0][1] if ch else None)


def run_ingest_expert(file_obj, path_str, yt_url, title_str, force_transcribe):
    q, lines = queue.Queue(), []
    
    def work():
        try:
            target_path = None
            if file_obj is not None:
                target_path = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
            elif path_str and path_str.strip():
                target_path = path_str.strip().strip('"').strip("'")
            
            if target_path:
                q.put(f"📂 Đang nạp file video/audio từ máy: {target_path}...")
                meta = expert.ingest_file(target_path, title=title_str or "", log=q.put)
            elif yt_url and yt_url.strip():
                q.put(f"🌐 Đang tải âm thanh từ YouTube: {yt_url.strip()}...")
                meta = expert.ingest_youtube(yt_url.strip(), title=title_str or "", log=q.put)
            else:
                raise ValueError("Hãy chọn 1 file video trên máy (kéo thả hoặc dán đường dẫn) hoặc dán link YouTube.")
            
            eid = meta["id"]
            q.put(f"🎙 Bắt đầu transcribe với Whisper ({meta['title']})...")
            expert.run_transcribe(eid, force=bool(force_transcribe), log=q.put)
            
            q.put(f"🧠 Dùng Gemini AI bóc tách chủ đề và các luận điểm đắt giá...")
            expert_ai.analyze_topics_from_transcript(eid, log=q.put)
            
            q.put(f"🎉 Hoàn tất! Chọn video này ở danh sách bên dưới để duyệt phân đoạn.")
        except Exception as e:
            q.put(f"❌ Lỗi: {e}")
            q.put(traceback.format_exc(limit=2))
        q.put(None)
        
    threading.Thread(target=work, daemon=True).start()
    while True:
        m = q.get()
        if m is None:
            break
        lines.append(m)
        yield "\n".join(lines)


def load_expert_details(expert_id):
    if not expert_id:
        empty_df = pd.DataFrame(columns=["#", "Thời gian", "Người nói", "Chủ đề", "Trích dẫn hay (Quote)", "Cảm xúc", "Hype (1-10)"])
        return empty_df, gr.CheckboxGroup(choices=[]), "", []
    
    data = expert.get_expert_data(expert_id)
    topics = data.get("topics", [])
    
    rows = []
    cb_choices = []
    for idx, t in enumerate(topics):
        tag = f"#{idx+1}: [{t.get('time_str','')}] {t.get('speaker','')} - {t.get('topic','')[:45]}"
        cb_choices.append((tag, t["id"]))
        rows.append({
            "#": idx + 1,
            "Thời gian": t.get("time_str", ""),
            "Người nói": t.get("speaker", ""),
            "Chủ đề": t.get("topic", ""),
            "Trích dẫn hay (Quote)": (t.get("quote", "")[:90] + "…") if len(t.get("quote", "")) > 90 else t.get("quote", ""),
            "Cảm xúc": t.get("sentiment", ""),
            "Hype (1-10)": t.get("hype_score", 8),
        })
    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["#", "Thời gian", "Người nói", "Chủ đề", "Trích dẫn hay (Quote)", "Cảm xúc", "Hype (1-10)"])
    
    edir = expert.expert_dir(expert_id)
    txt_file = edir / "transcript.txt"
    full_text = txt_file.read_text(encoding="utf-8") if txt_file.exists() else "Chưa có transcript."
    
    default_vals = [c[1] for c in cb_choices[:3]]
    return df, gr.CheckboxGroup(choices=cb_choices, value=default_vals), full_text, topics


def make_script(selected_topic_ids, expert_id, team_name, all_topics):
    import time
    if not expert_id:
        raise gr.Error("Hãy chọn video chuyên gia trước.")
    if not selected_topic_ids:
        raise gr.Error("Hãy chọn ít nhất 1 phân đoạn chủ đề để viết kịch bản.")
        
    sel_takes = [t for t in (all_topics or []) if t["id"] in selected_topic_ids]
    if not sel_takes:
        data = expert.get_expert_data(expert_id)
        sel_takes = [t for t in data.get("topics", []) if t["id"] in selected_topic_ids]
        
    logs = []
    script = expert_ai.generate_full_script(sel_takes, team_name=team_name or "Raiders", log=logs.append)
    
    titles_md = "### 📌 5 Tiêu đề đề xuất (Click-through-rate cao):\n"
    for i, tit in enumerate(script.get("titles", [])):
        titles_md += f"{i+1}. **{tit}**\n"
        
    hook_md = f"### 🔥 Hook mở đầu (15–20s):\n> {script.get('hook', '')}"
    
    narration_txt = script.get("full_narration", "")
    
    tl_rows = []
    for item in script.get("timeline", []):
        tl_rows.append({
            "Thời gian": item.get("time", ""),
            "Lời thoại (Voiceover)": item.get("narration", ""),
            "Loại hình ảnh": item.get("visual_type", ""),
            "Chi tiết hình ảnh / Clip": item.get("visual_asset", ""),
            "Mã Clip Highlight": item.get("matched_clip_id") or "-",
            "Ghi chú âm thanh": item.get("audio_direction", "")
        })
    tl_df = pd.DataFrame(tl_rows)
    
    safe_team = re.sub(r'\W+', '_', team_name or "Raiders")
    out_file = CLIPS / f"kich_ban_{safe_team}_{int(time.time())}.md"
    content = f"# KỊCH BẢN VIDEO YOUTUBE: {team_name}\n\n{titles_md}\n\n{hook_md}\n\n### 🎙 Kịch bản dẫn chuyện đầy đủ:\n\n{narration_txt}\n\n### 🎬 Timeline dựng hình ảnh & Highlight:\n\n"
    for r in tl_rows:
        content += f"- **[{r['Thời gian']}]** ({r['Loại hình ảnh']})\n  - Lời thoại: *{r['Lời thoại (Voiceover)']}*\n  - Hình ảnh: {r['Chi tiết hình ảnh / Clip']}\n  - Highlight khớp: `{r['Mã Clip Highlight']}`\n  - Âm thanh: {r['Ghi chú âm thanh']}\n\n"
    out_file.write_text(content, encoding="utf-8")
    
    return titles_md, hook_md, narration_txt, tl_df, str(out_file)


def run_gemini_voice(text, voice_choice, style_text):
    if not text or not text.strip():
        return None, None, "⚠️ Vui lòng nhập hoặc dán lời thoại cần đọc vào ô văn bản!"
    voice_name = gemini_tts.VOICE_PRESETS.get(voice_choice, "Fenrir")
    out_dir = CLIPS / "voiceovers"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"voice_{voice_name}_{int(time.time())}.mp3"
    try:
        gemini_tts.generate_gemini_speech(
            text=text.strip(),
            voice_name=voice_name,
            style_prompt=style_text.strip(),
            output_path=out_file
        )
        return str(out_file), str(out_file), f"✅ Đã tạo thành công giọng đọc ({voice_name})! File lưu tại: {out_file.name}"
    except Exception as e:
        return None, None, f"❌ Lỗi tạo giọng đọc: {e}"


# ---------------- Tab 4: cài đặt ----------------
def save_cfg(key, model, device, hq):
    s = load_settings()
    s.update({"gemini_api_key": key.strip(), "whisper_model": model, "whisper_device": device, "hq_height": int(hq)})
    save_settings(s)
    return "✅ Đã lưu cài đặt."


GUIDE = """
## Cách dùng phần mềm

### 🅰 Giai đoạn 1: Kho highlight tự động
1. **Tab ① Tìm & phân tích trận** → chọn mùa, tuần → *Tải danh sách trận* → chọn trận đã đá.
2. Bấm **Tìm video highlight** → chọn video kênh NFL chính thức hoặc dán link YouTube.
3. Bấm **Tải & phân tích** → Máy tự động tách cảnh, đọc bảng tỷ số OCR, chép lời bình luận viên và khớp với play-by-play ESPN.
4. **Tab ② Kho pha bóng** → gõ tìm kiếm (ví dụ: `Loop 56`, `touchdown Henry`, `fg`, `Flowers`, `phút cuối`, `pha dài`) → bấm vào một dòng để xem thử → bấm **Tải bản HD đoạn này** để lấy clip 1080p về dựng phim.

### 🅱 Giai đoạn 2 & 3: Studio Kịch bản (Nguồn chuyên gia)
1. **Tab ③ Studio Kịch bản (Chuyên gia)**:
   - **Bước 1**: Nạp video talkshow/podcast chuyên gia (chọn file từ máy, dán đường dẫn file trên máy, hoặc dán link YouTube) → bấm **⬇ Nạp & Chạy Transcribe**.
   - Máy tự động trích xuất âm thanh, chạy nhận dạng giọng nói Whisper (hỗ trợ WhisperX / GPU CUDA), và dùng Gemini AI bóc tách các phân đoạn thảo luận kịch tính.
   - **Bước 2**: Duyệt danh sách các phân đoạn thảo luận trong bảng (xem thời gian, ai nói, chủ đề gì, câu nói đắt giá). **Tích chọn `[x]` các đoạn bạn muốn đưa vào video**.
   - **Bước 3**: Bấm **⚡ Tạo Kịch bản & Khớp Highlight**:
     - Sinh **5 Tiêu đề giật gân** (CTR cao).
     - Sinh **Hook mở đầu** (15-20s).
     - Sinh **Kịch bản dẫn chuyện hoàn chỉnh** (kết nối ý kiến các chuyên gia).
     - Xuất **Timeline chi tiết** chia từng nhịp 4-5s, chỉ định rõ câu nào dùng ảnh zoom, câu nào cắt soundbite tiếng thật chuyên gia, và câu nào chèn clip highlight từ kho pha bóng của phần mềm.
     - Tải file kịch bản `.md` về máy để đưa vào dựng phim.

**Mẹo làm video hay:**
- Để video an toàn bản quyền, hãy dùng tỷ lệ 70% ảnh zoom (Ken Burns) + 20% clip highlight ngắn (2-4s, tắt tiếng trận đấu) + 10% soundbite tiếng thật chuyên gia.
- Giữ âm lượng nhạc nền thấp hơn giọng đọc 12-15dB.
"""


def build():
    season0, week0 = _default_week()
    S = load_settings()
    with gr.Blocks(title="Công cụ xào nấu content") as app:
        gr.Markdown("# 🍳 CÔNG CỤ XÀO NẤU CONTENT\nKho highlight NFL tự động: tìm → tải → băm pha → gắn nhãn → tìm kiếm → xuất clip")
        games_st, cands_st, rows_st, sel_st = gr.State([]), gr.State([]), gr.State([]), gr.State(None)

        with gr.Tab("① Tìm & phân tích trận"):
            with gr.Row():
                season = gr.Number(value=season0, label="Mùa giải", precision=0)
                stype = gr.Dropdown(list(STYPES), value="Mùa giải chính", label="Giai đoạn")
                week = gr.Number(value=week0, label="Tuần", precision=0)
                btn_games = gr.Button("Tải danh sách trận", variant="primary")
            games_df = gr.Dataframe(value=pd.DataFrame(columns=["Ngày", "Trận", "Tỷ số", "Trạng thái"]), interactive=False, max_height=260)
            game_dd = gr.Dropdown(label="Chọn trận (hoặc bấm vào một dòng trong bảng trên) — đổi trận là tự tìm highlight", choices=[])
            btn_find = gr.Button("🔎 Tìm video highlight")
            cands_df = gr.Dataframe(value=pd.DataFrame(columns=["Điểm phù hợp", "Tiêu đề", "Kênh", "Dài", "Lượt xem", "Ghi chú"]), interactive=False, max_height=260, wrap=True)
            with gr.Row():
                vid_dd = gr.Dropdown(label="Chọn video highlight", choices=[], scale=3)
                url = gr.Textbox(label="…hoặc dán link YouTube khác", scale=2)
            force = gr.Checkbox(label="Phân tích lại từ đầu (bỏ kết quả cũ)", value=False)
            btn_run = gr.Button("⬇ Tải & phân tích", variant="primary")
            log = gr.Textbox(label="Tiến độ", lines=12, max_lines=30)
            gr.Markdown("### Các trận đã có trong kho")
            done_df = gr.Dataframe(value=analyzed_df, interactive=False, max_height=240)

            btn_games.click(load_games, [season, stype, week], [games_df, game_dd, games_st])
            games_df.select(pick_game_row, games_st, game_dd)
            # đổi trận -> xoá link dán tay cũ và tự tìm lại highlight của trận mới
            game_dd.change(lambda: "", None, url).then(find_hl, [game_dd, games_st], [cands_df, vid_dd, cands_st])
            btn_find.click(find_hl, [game_dd, games_st], [cands_df, vid_dd, cands_st])
            btn_run.click(run_analysis, [game_dd, vid_dd, url, force, cands_st, games_st], log).then(analyzed_df, None, done_df)

        with gr.Tab("② Kho pha bóng"):
            with gr.Row():
                game_sel = gr.Dropdown(label="Trận", choices=game_choices(), value="__all__", scale=3)
                btn_ref = gr.Button("↻ Làm mới danh sách", scale=1)
            with gr.Row():
                query = gr.Textbox(label="Tìm pha (tên cầu thủ, loại pha, số yard…)", placeholder="Ví dụ: Loop 56 · touchdown Henry · fg · phút cuối", scale=4)
                quarter = gr.Dropdown(["Tất cả", "Hiệp 1", "Hiệp 2", "Hiệp 3", "Hiệp 4", "Hiệp phụ"], value="Tất cả", label="Hiệp", scale=1)
            with gr.Row():
                only_sc = gr.Checkbox(label="Chỉ pha ghi điểm")
                only_hi = gr.Checkbox(label="Chỉ độ tin cậy cao")
                btn_search = gr.Button("Tìm", variant="primary")
            info = gr.Markdown()
            res_df = gr.Dataframe(value=pd.DataFrame(columns=["#", "Bắt đầu", "Dài (s)", "Hiệp", "Đồng hồ", "Down", "Loại pha", "Mô tả (ESPN)", "Cầu thủ", "Tin cậy", "Bình luận viên", "Trận"]), interactive=False, max_height=420, wrap=True)
            with gr.Row():
                with gr.Column(scale=3):
                    pv = gr.Video(label="Xem thử (bản 360p)", height=360, autoplay=True)
                with gr.Column(scale=2):
                    detail = gr.Markdown()
                    pad = gr.Slider(0, 3, value=0.5, step=0.5, label="Lấy dư trước/sau (giây)")
                    btn_hq = gr.Button("⬇ Tải bản HD đoạn này", variant="primary")
                    hq_file = gr.File(label="Clip HD")
                    hq_log = gr.Textbox(label="Trạng thái", lines=3)
            btn_ref.click(refresh_games, None, game_sel)
            for trig in (btn_search.click, query.submit):
                trig(do_search, [query, game_sel, only_sc, only_hi, quarter], [res_df, rows_st, info])
            res_df.select(on_select, rows_st, [pv, detail, sel_st])
            btn_hq.click(do_export, [sel_st, pad], [hq_file, hq_log])

        with gr.Tab("③ Studio Kịch bản (Chuyên gia)"):
            gr.Markdown("### 🎙 Nạp Video Chuyên gia ➔ Duyệt Phân đoạn Chủ đề ➔ Sinh Kịch bản & Khớp Highlight")
            expert_topics_st = gr.State([])
            
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("#### Bước 1: Nạp Video Chuyên gia (Talkshow, Podcast, Họp báo)")
                    with gr.Row():
                        exp_file = gr.File(label="Tải lên file video/audio từ máy", file_types=["video", "audio"], scale=2)
                        exp_path = gr.Textbox(label="…hoặc dán đường dẫn file trên máy", placeholder="Ví dụ: D:\\videos\\first_take_week3.mp4", scale=2)
                    with gr.Row():
                        exp_url = gr.Textbox(label="…hoặc dán link YouTube talkshow", placeholder="https://www.youtube.com/watch?v=...", scale=3)
                        exp_title = gr.Textbox(label="Tên gợi nhớ (tuỳ chọn)", placeholder="Ví dụ: First Take Week 3", scale=2)
                    exp_force = gr.Checkbox(label="Chạy lại từ đầu (bỏ transcript cũ)", value=False)
                    btn_exp_ingest = gr.Button("⬇ Nạp & Chạy Transcribe (Whisper)", variant="primary")
                    exp_log = gr.Textbox(label="Tiến độ xử lý", lines=6, max_lines=15)
                
                with gr.Column(scale=2):
                    gr.Markdown("#### Video Chuyên gia đã có")
                    with gr.Row():
                        exp_dd = gr.Dropdown(label="Chọn video chuyên gia", choices=expert_choices(), scale=3)
                        btn_exp_ref = gr.Button("↻ Làm mới", scale=1)
                    with gr.Accordion("Xem toàn bộ Transcript", open=False):
                        exp_full_txt = gr.Textbox(label="Lời thoại", lines=12, max_lines=25, interactive=False)

            gr.Markdown("---")
            gr.Markdown("#### Bước 2: Duyệt các phân đoạn chủ đề đắt giá (Bấm chọn để đưa vào kịch bản)")
            exp_topics_df = gr.Dataframe(
                value=pd.DataFrame(columns=["#", "Thời gian", "Người nói", "Chủ đề", "Trích dẫn hay (Quote)", "Cảm xúc", "Hype (1-10)"]),
                interactive=False, max_height=320, wrap=True
            )
            exp_cb_group = gr.CheckboxGroup(label="Tích chọn các đoạn bạn muốn đưa vào kịch bản:", choices=[])
            
            with gr.Row():
                team_name_in = gr.Textbox(label="Tên đội bóng tâm điểm", value="Raiders", scale=2)
                btn_gen_script = gr.Button("⚡ Tạo Kịch bản & Khớp Highlight", variant="primary", scale=2)

            gr.Markdown("---")
            gr.Markdown("#### Bước 3: Kịch bản hoàn chỉnh & Timeline dựng video")
            res_titles = gr.Markdown()
            res_hook = gr.Markdown()
            with gr.Row():
                with gr.Column(scale=3):
                    res_narration = gr.Textbox(label="Kịch bản dẫn chuyện (Voiceover Text)", lines=10, max_lines=20)
                with gr.Column(scale=1):
                    script_file_out = gr.File(label="Tải file Kịch bản (.md)")
            
            gr.Markdown("##### 🎬 Timeline chi tiết: Ghép Clip Highlight & Soundbite chuyên gia theo từng câu (4-5s)")
            res_timeline_df = gr.Dataframe(
                value=pd.DataFrame(columns=["Thời gian", "Lời thoại (Voiceover)", "Loại hình ảnh", "Chi tiết hình ảnh / Clip", "Mã Clip Highlight", "Ghi chú âm thanh"]),
                interactive=False, max_height=360, wrap=True
            )

            gr.Markdown("---")
            gr.Markdown("#### Bước 4: 🎙 Sinh Giọng Đọc Diễn Xuất Google AI Studio (Cảm Xúc & Kịch Tính)")
            gr.Markdown(
                "Tạo giọng đọc dẫn chuyện mãnh liệt, giật gân chuẩn phong cách thể thao Mỹ. "
                "AI Studio hiểu chỉ dẫn đạo diễn (hét lớn, gằn giọng, dồn dập, nghẹt thở) vượt trội hơn hẳn TTS thông thường."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    tts_voice = gr.Dropdown(
                        choices=list(gemini_tts.VOICE_PRESETS.keys()),
                        value=list(gemini_tts.VOICE_PRESETS.keys())[0],
                        label="Chọn Giọng Đọc AI Studio"
                    )
                    tts_style = gr.Textbox(
                        value=gemini_tts.DEFAULT_STYLE,
                        label="Chỉ dẫn diễn xuất & Cảm xúc (Style Prompt)",
                        lines=4
                    )
                with gr.Column(scale=2):
                    tts_text = gr.Textbox(
                        label="Lời thoại cần đọc (có thể copy từ Kịch bản, Hook hoặc đoạn Bridge ở trên)",
                        lines=5,
                        placeholder="Dán đoạn văn bản cần tạo giọng đọc vào đây..."
                    )
                    btn_tts_gen = gr.Button("⚡ Tạo Giọng Đọc MP3 (Google AI Studio)", variant="primary")
                    tts_status = gr.Markdown()
                    with gr.Row():
                        tts_audio_play = gr.Audio(label="Nghe thử giọng đọc", type="filepath")
                        tts_file_out = gr.File(label="Tải file Audio (.mp3)")

            btn_tts_gen.click(
                run_gemini_voice,
                [tts_text, tts_voice, tts_style],
                [tts_audio_play, tts_file_out, tts_status]
            )

            # Events
            btn_exp_ref.click(refresh_expert_choices, None, exp_dd)
            btn_exp_ingest.click(
                run_ingest_expert,
                [exp_file, exp_path, exp_url, exp_title, exp_force],
                exp_log
            ).then(refresh_expert_choices, None, exp_dd)
            
            exp_dd.change(
                load_expert_details,
                exp_dd,
                [exp_topics_df, exp_cb_group, exp_full_txt, expert_topics_st]
            )
            
            btn_gen_script.click(
                make_script,
                [exp_cb_group, exp_dd, team_name_in, expert_topics_st],
                [res_titles, res_hook, res_narration, res_timeline_df, script_file_out]
            )

        with gr.Tab("④ Cài đặt"):
            key = gr.Textbox(value=S["gemini_api_key"], type="password", label="Google AI Studio / Gemini API Key (Lấy miễn phí tại https://aistudio.google.com/app/apikey)")
            wm = gr.Dropdown(["small.en", "medium.en", "large-v3"], value=S["whisper_model"], label="Model Whisper")
            wd = gr.Dropdown(["cuda", "cpu"], value=S["whisper_device"], label="Chạy Whisper trên")
            hq = gr.Dropdown([720, 1080], value=S["hq_height"], label="Độ phân giải clip HD")
            btn_save = gr.Button("Lưu", variant="primary")
            saved = gr.Markdown()
            btn_save.click(save_cfg, [key, wm, wd, hq], saved)

        with gr.Tab("Hướng dẫn"):
            gr.Markdown(GUIDE)
    return app


def selftest():
    """Kiểm tra nhanh từng thành phần: chạy `CongCuXaoNau.exe --selftest`."""
    import subprocess
    import numpy as np
    from xaonau import config
    from xaonau.analyze import scorebug, transcribe

    def step(name, fn):
        try:
            print(f"[OK]  {name}: {fn()}")
        except Exception as e:
            print(f"[LỖI] {name}: {e}")
    print("Thư mục tool:", config.ROOT)
    step("ffmpeg", lambda: subprocess.run([config.FFMPEG, "-version"], capture_output=True, text=True).stdout.split("\n")[0][:60])
    step("node", lambda: subprocess.run([config.NODE, "--version"], capture_output=True, text=True).stdout.strip())
    step("OCR", lambda: f"{len(scorebug.ocr()(np.full((60, 200, 3), 255, np.uint8))[0] or [])} vùng chữ (ảnh trắng)")
    S = load_settings()
    step("Whisper", lambda: f"{S['whisper_model']} trên {transcribe.get_model(S['whisper_model'], S['whisper_device']).model.device}")
    step("ESPN", lambda: f"mùa {nfl.current_week()}")
    step("YouTube", lambda: yt.search("NFL highlights", 2)[0]["title"][:50])
    input("\nNhấn Enter để đóng…")


def main():
    import socket
    import sys
    import webbrowser
    from xaonau.config import FROZEN
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--selftest" in sys.argv:
        selftest()
        return
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 7860
    with socket.socket() as sk:
        busy = sk.connect_ex(("127.0.0.1", port)) == 0
    if busy:  # tool đã mở sẵn -> chỉ mở lại trình duyệt
        webbrowser.open(f"http://127.0.0.1:{port}")
        return
    print("=" * 60)
    print("  CÔNG CỤ XÀO NẤU CONTENT")
    print(f"  Đang mở giao diện tại http://127.0.0.1:{port}")
    print("  Giữ cửa sổ này mở trong lúc dùng. Đóng cửa sổ = tắt tool.")
    print("=" * 60)
    build().launch(server_name="127.0.0.1", server_port=port, inbrowser=FROZEN or "--open" in sys.argv,
                   allowed_paths=[str(DATA)], theme=gr.themes.Soft())


if __name__ == "__main__":
    main()
