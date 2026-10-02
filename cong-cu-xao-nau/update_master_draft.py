import json
import uuid
import time
import shutil
import subprocess
from pathlib import Path

# Paths
capcut_root = Path(r"C:\Users\Thien\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft")
pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
lib = pkg / "Kho_Highlight_San"

project_name = "00_CHIEFS_FULL_VIDEO_MASTER_EDIT"
draft_dir = capcut_root / project_name
draft_dir.mkdir(parents=True, exist_ok=True)

# Sample cover
sample_cover = capcut_root / "0928 (3)" / "draft_cover.jpg"
if sample_cover.exists():
    shutil.copy(sample_cover, draft_dir / "draft_cover.jpg")

now_us = int(time.time() * 1000000)
draft_id = str(uuid.uuid4()).upper()

# Load exact durations
with open(lib / "actual_durations.json", "r", encoding="utf-8") as f:
    durations_map = json.load(f)

# Helper to find full path of highlight by filename
def get_hl_path(file_name):
    matches = list(lib.rglob(file_name))
    if not matches:
        raise FileNotFoundError(f"Highlight not found: {file_name}")
    return matches[0]

def get_exact_duration_us(file_path):
    fn = Path(file_path).name
    if fn in durations_map:
        return int(durations_map[fn] * 1000000)
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return int(float(res.stdout.strip()) * 1000000)

materials = {
    "ai_translates": [], "audio_balances": [], "audio_effects": [], "audio_fades": [],
    "audio_track_indexes": [], "audios": [], "beats": [], "canvases": [], "chromas": [],
    "color_curves": [], "common_mask": [], "digital_humans": [], "drafts": [], "effects": [],
    "flowers": [], "green_screens": [], "handwrites": [], "hsl": [], "images": [],
    "log_color_wheels": [], "loudnesses": [], "manual_deformations": [],
    "material_animations": [], "material_colors": [], "multi_language_refs": [],
    "placeholder_infos": [], "placeholders": [], "plugin_effects": [], "primary_color_wheels": [],
    "realtime_denoises": [], "shapes": [], "smart_crops": [], "smart_relights": [],
    "sound_channel_mappings": [], "speeds": [], "stickers": [], "tail_leaders": [],
    "text_templates": [], "texts": [], "time_marks": [], "transitions": [], "video_effects": [],
    "video_trackings": [], "videos": [], "vocal_beautifys": [], "vocal_separations": []
}

meta_materials_value = []
video_material_cache = {}

def get_or_add_video_material(file_path, file_total_duration_us, width=1280, height=720):
    posix_path = Path(file_path).as_posix()
    if posix_path in video_material_cache:
        return video_material_cache[posix_path]
    
    vid_id = str(uuid.uuid4()).upper()
    v_mat = {
        "aigc_history_id": "", "aigc_item_id": "", "aigc_type": "none", "audio_fade": None,
        "beauty_body_preset_id": "", "beauty_face_preset_infos": [], "cartoon_path": "",
        "category_id": "", "category_name": "", "check_flag": 62978047,
        "crop": {"lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0, "lower_right_y": 1.0,
                 "upper_left_x": 0.0, "upper_left_y": 0.0, "upper_right_x": 1.0, "upper_right_y": 0.0},
        "crop_ratio": "free", "crop_scale": 1.0, "duration": file_total_duration_us, "extra_type_option": 0,
        "formula_id": "", "freeze": None, "has_audio": True, "has_sound_separated": False,
        "height": height, "id": vid_id, "intensifies_audio_path": "", "intensifies_path": "",
        "is_ai_generate_content": False, "is_copyright": False, "is_text_edit_overdub": False,
        "is_unified_beauty_mode": False, "live_photo_cover_path": "", "live_photo_timestamp": -1,
        "local_id": "", "local_material_from": "", "local_material_id": "", "material_id": "",
        "material_name": Path(file_path).name, "material_url": "",
        "matting": {"custom_matting_id": "", "expansion": 0, "feather": 0, "flag": 0,
                    "has_use_quick_brush": False, "has_use_quick_eraser": False,
                    "interactiveTime": [], "path": "", "reverse": False, "strokes": []},
        "media_path": "", "multi_camera_info": None, "object_locked": None, "origin_material_id": "",
        "path": posix_path, "picture_from": "none", "picture_set_category_id": "",
        "picture_set_category_name": "", "request_id": "", "reverse_intensifies_path": "",
        "reverse_path": "", "smart_match_info": None, "smart_motion": None, "source": 0,
        "source_platform": 0, "stable": {"matrix_path": "", "stable_level": 0, "time_range": {"duration": 0, "start": 0}},
        "team_id": "", "type": "video",
        "video_algorithm": {"ai_background_configs": [], "aigc_generate": None, "algorithms": [],
                            "complement_frame_config": None, "deflicker": None, "gameplay_configs": [],
                            "motion_blur_config": None, "mouth_shape_driver": None, "noise_reduction": None,
                            "path": "", "quality_enhance": None, "smart_complement_frame": None,
                            "super_resolution": None, "time_range": None},
        "width": width
    }
    materials["videos"].append(v_mat)
    
    meta_materials_value.append({
        "create_time": int(time.time()),
        "duration": file_total_duration_us,
        "extra_info": Path(file_path).name,
        "file_Path": posix_path,
        "height": height,
        "id": str(uuid.uuid4()),
        "import_time": int(time.time()),
        "import_time_ms": now_us,
        "item_source": 1, "md5": "", "metetype": "video",
        "roughcut_time_range": {"duration": file_total_duration_us, "start": 0},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": 0, "width": width
    })
    
    video_material_cache[posix_path] = vid_id
    return vid_id

def add_segment(material_id, target_start_us, duration_us, source_start_us=0, volume=1.0, render_index=0):
    seg_id = str(uuid.uuid4()).upper()
    speed_id = str(uuid.uuid4()).upper()
    phi_id = str(uuid.uuid4()).upper()
    canvas_id = str(uuid.uuid4()).upper()
    scm_id = str(uuid.uuid4()).upper()
    vs_id = str(uuid.uuid4()).upper()

    materials["speeds"].append({"curve_speed": None, "id": speed_id, "mode": 0, "speed": 1.0, "type": "speed"})
    materials["placeholder_infos"].append({"error_path": "", "error_text": "", "id": phi_id, "meta_type": "none", "res_path": "", "res_text": "", "type": "placeholder_info"})
    materials["canvases"].append({"album_image": "", "blur": 0.0, "color": "", "id": canvas_id, "image": "", "image_id": "", "image_name": "", "source_platform": 0, "team_id": "", "type": "canvas_color"})
    materials["sound_channel_mappings"].append({"audio_channel_mapping": 0, "id": scm_id, "is_config_open": False, "type": ""})
    materials["vocal_separations"].append({"choice": 0, "id": vs_id, "production_path": "", "removed_sounds": [], "time_range": None, "type": "vocal_separation"})

    return {
        "caption_info": None, "cartoon": False,
        "clip": {"alpha": 1.0, "flip": {"horizontal": False, "vertical": False}, "rotation": 0.0,
                 "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}},
        "common_keyframes": [], "desc": "", "enable_adjust": True, "enable_adjust_mask": False,
        "enable_color_correct_adjust": False, "enable_color_curves": True, "enable_color_match_adjust": False,
        "enable_color_wheels": True, "enable_hsl": False, "enable_lut": True, "enable_smart_color_adjust": False,
        "enable_video_mask": True,
        "extra_material_refs": [speed_id, phi_id, canvas_id, scm_id, vs_id],
        "group_id": "", "hdr_settings": {"intensity": 1.0, "mode": 1, "nits": 1000},
        "id": seg_id, "intensifies_audio": False, "is_loop": False, "is_placeholder": False,
        "is_tone_modify": False, "keyframe_refs": [], "last_nonzero_volume": 1.0, "lyric_keyframes": None,
        "material_id": material_id, "raw_segment_id": "", "render_index": render_index,
        "render_timerange": {"duration": 0, "start": 0},
        "responsive_layout": {"enable": False, "horizontal_pos_layout": 0, "size_layout": 0, "target_follow": "", "vertical_pos_layout": 0},
        "reverse": False, "source_timerange": {"duration": duration_us, "start": source_start_us},
        "speed": 1.0, "state": 0, "target_timerange": {"duration": duration_us, "start": target_start_us},
        "template_id": "", "template_scene": "default", "track_attribute": 0,
        "track_render_index": render_index, "uniform_scale": {"on": True, "value": 1.0},
        "visible": True, "volume": volume
    }

def add_audio_material(file_path, duration_us):
    aud_id = str(uuid.uuid4()).upper()
    a_mat = {
        "ai_music_type": 0, "aigc_history_id": "", "aigc_item_id": "", "app_id": 0,
        "category_id": "", "category_name": "", "check_flag": 1, "copyright_limit_type": "none",
        "duration": duration_us, "effect_id": "", "formula_id": "", "id": aud_id,
        "intensifies_path": "", "is_ai_clone_tone": False, "is_ai_clone_tone_post": False,
        "is_text_edit_overdub": False, "is_ugc": False, "local_material_id": "", "lyric_type": 0,
        "music_id": "", "music_source": "", "name": Path(file_path).name,
        "path": Path(file_path).as_posix(), "pgc_id": "", "pgc_name": "", "query": "",
        "request_id": "", "resource_id": "", "search_id": "",
        "similiar_music_info": {"original_song_id": "", "original_song_name": ""},
        "sound_separate_type": "", "source_from": "", "source_platform": 0, "team_id": "",
        "text_id": "", "third_resource_id": "", "tone_category_id": "", "tone_category_name": "",
        "tone_effect_id": "", "tone_effect_name": "", "tone_emotion_name_key": "",
        "tone_emotion_role": "", "tone_emotion_scale": 0.0, "tone_emotion_selection": "",
        "tone_emotion_style": "", "tone_platform": "", "tone_second_category_id": "",
        "tone_second_category_name": "", "tone_speaker": "", "tone_type": "",
        "tts_generate_scene": "", "tts_task_id": "", "type": "extract_music", "video_id": "",
        "wave_points": []
    }
    materials["audios"].append(a_mat)
    return aud_id

def add_audio_segment(material_id, target_start_us, duration_us, source_start_us=0, volume=1.0):
    seg_id = str(uuid.uuid4()).upper()
    speed_id = str(uuid.uuid4()).upper()
    materials["speeds"].append({"curve_speed": None, "id": speed_id, "mode": 0, "speed": 1.0, "type": "speed"})
    
    return {
        "caption_info": None, "cartoon": False, "clip": None, "common_keyframes": [],
        "desc": "", "enable_adjust": False, "enable_adjust_mask": False,
        "enable_color_correct_adjust": False, "enable_color_curves": True,
        "enable_color_match_adjust": False, "enable_color_wheels": True,
        "enable_hsl": False, "enable_lut": False, "enable_smart_color_adjust": False,
        "enable_video_mask": True,
        "extra_material_refs": [speed_id],
        "group_id": "", "hdr_settings": None, "id": seg_id, "intensifies_audio": False,
        "is_loop": False, "is_placeholder": False, "is_tone_modify": False,
        "keyframe_refs": [], "last_nonzero_volume": 1.0, "lyric_keyframes": None,
        "material_id": material_id, "raw_segment_id": "", "render_index": 0,
        "render_timerange": {"duration": 0, "start": 0},
        "responsive_layout": {"enable": False, "horizontal_pos_layout": 0, "size_layout": 0, "target_follow": "", "vertical_pos_layout": 0},
        "reverse": False, "source_timerange": {"duration": duration_us, "start": source_start_us},
        "speed": 1.0, "state": 0, "target_timerange": {"duration": duration_us, "start": target_start_us},
        "template_id": "", "template_scene": "default", "track_attribute": 0,
        "track_render_index": 2, "uniform_scale": None, "visible": True, "volume": volume
    }

main_track_segments = []
overlay_track_segments = []
audio_track_segments = []

# --- 1. HOOK (0s -> 17.5s) ---
print("1. Adding Hook...")
hook_file = pkg / "00_Hook_Final_Master.mp4"
hook_dur_us = get_exact_duration_us(hook_file)
hook_mat = get_or_add_video_material(hook_file, hook_dur_us)
main_track_segments.append(add_segment(hook_mat, 0, hook_dur_us, 0, volume=1.0, render_index=0))

# --- 2. EXPERT 1 (CBS) ---
print("2. Adding Expert 1 (CBS) and Narrative Overlays...")
t_cbs_start = hook_dur_us
cbs_file = pkg / "01_Expert_CBS_Clean_Voice.mp4"
cbs_dur_us = get_exact_duration_us(cbs_file)
cbs_mat = get_or_add_video_material(cbs_file, cbs_dur_us)
main_track_segments.append(add_segment(cbs_mat, t_cbs_start, cbs_dur_us, 0, volume=1.0, render_index=0))

# Exact overlays for CBS
cbs_overlays = [
    ("Mahomes_02_SuperBowl_LIV_Wasp_TyreekHill.mp4", 9000000),
    ("Kelce_01_Deep_48yd_Bomb_Catch.mp4", 18000000),
    ("Walker_01_FourthDown_60yd_HouseCall.mp4", 28000000),
    ("Walker_02_RedZone_10yd_Plunge_TD.mp4", 86000000),
    ("Kelce_02_RedZone_11yd_Touchdown.mp4", 107000000),
    ("Kelce_03_Route_Diagram_Analysis.mp4", 118000000),
    ("Mahomes_01_Titans_27yd_Scramble_TD.mp4", 175000000)
]
for fn, rel_start in cbs_overlays:
    f_path = get_hl_path(fn)
    exact_dur = get_exact_duration_us(f_path)
    mat_id = get_or_add_video_material(f_path, exact_dur)
    overlay_track_segments.append(add_segment(mat_id, t_cbs_start + rel_start, exact_dur, 0, volume=0.0, render_index=1))

# --- 3. MID 1: BRIDGE (AI Voiceover Puck) ---
print("3. Adding Bridge (Puck voice + Complete Highlights)...")
t_bridge_start = t_cbs_start + cbs_dur_us
bridge_audio = pkg / "01_Voiceover_Bridge_Puck.mp3"
bridge_dur_us = get_exact_duration_us(bridge_audio)
b_aud_mat = add_audio_material(bridge_audio, bridge_dur_us)
audio_track_segments.append(add_audio_segment(b_aud_mat, t_bridge_start, bridge_dur_us, 0, volume=1.0))

bridge_highlight_files = [
    ("Walker_03_Mahomes_to_Walker_5yd_TD.mp4", 8000000),
    ("Worthy_03_Sideline_17yd_Speed_Catch.mp4", 7970000),
    ("Mahomes_04_NoLook_CrossBody_Pass.mp4", 7000000)
]
curr_t = t_bridge_start
remaining_bridge_us = bridge_dur_us
for fn, dur_us in bridge_highlight_files:
    f_path = get_hl_path(fn)
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, min(dur_us, remaining_bridge_us))
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use
    remaining_bridge_us -= dur_to_use
    if remaining_bridge_us <= 0:
        break

if remaining_bridge_us > 0:
    f_path = get_hl_path("Mahomes_04_NoLook_CrossBody_Pass.mp4")
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, remaining_bridge_us)
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use

# --- 4. EXPERT 2 (RYAN CLARK & STEPHEN A.) ---
print("4. Adding Expert 2 (Ryan Clark) and Defensive Overlays...")
t_ryan_start = t_bridge_start + bridge_dur_us
ryan_file = pkg / "02_Expert_RyanClark_Clean_Voice.mp4"
ryan_dur_us = get_exact_duration_us(ryan_file)
ryan_mat = get_or_add_video_material(ryan_file, ryan_dur_us)
main_track_segments.append(add_segment(ryan_mat, t_ryan_start, ryan_dur_us, 0, volume=1.0, render_index=0))

ryan_overlays = [
    ("Kelce_02_RedZone_11yd_Touchdown.mp4", 30000000),
    ("Walker_05_StiffArm_Power_15yd_Run.mp4", 60000000),
    ("Defense_01_ChrisJones_Strip_Sack.mp4", 75000000),
    ("Defense_03_Spags_Exotic_Blitz_Sack.mp4", 85000000),
    ("Defense_04_FrankClark_Edge_Sack.mp4", 92000000),
    ("Mahomes_04_NoLook_CrossBody_Pass.mp4", 102000000)
]
for fn, rel_start in ryan_overlays:
    f_path = get_hl_path(fn)
    exact_dur = get_exact_duration_us(f_path)
    mat_id = get_or_add_video_material(f_path, exact_dur)
    overlay_track_segments.append(add_segment(mat_id, t_ryan_start + rel_start, exact_dur, 0, volume=0.0, render_index=1))

# --- 5. MID 2: CONTENT AI DEEP DIVE (Puck Voice - Beat Synchronized) ---
print("5. Adding Content AI Deep Dive (Synchronized to spoken beats)...")
t_deep_start = t_ryan_start + ryan_dur_us
deep_audio = pkg / "03_Voiceover_DeepDive_Puck.mp3"
deep_dur_us = get_exact_duration_us(deep_audio)
d_aud_mat = add_audio_material(deep_audio, deep_dur_us)
audio_track_segments.append(add_audio_segment(d_aud_mat, t_deep_start, deep_dur_us, 0, volume=1.0))

# Exact Whisper-aligned beats for Deep Dive (3.8 Flash):
# Beat 1: Intro & Reality Check (0s -> 11.72s)
# Beat 2: Kenneth Walker ground explosion (11.72s -> 22.88s)
# Beat 3: Downfield passing to Kelce & Worthy (22.88s -> 29.06s)
# Beat 4: Steve Spagnuolo defense & Chris Jones (29.06s -> 46.26s)
# Beat 5: Brutal AFC Gauntlet & O-Line protection (46.26s -> 64.34s)
# Beat 6: Three-peat dynasty climax (64.34s -> 80.77s)

deep_beats = [
    # Beat 1: Intro & Reality Check
    ("Mahomes_05_Playoff_FistPump_Celeb.mp4", 5720000),
    ("Mahomes_06_Touchdown_Flex_Celeb.mp4", 6000000),
    # Beat 2: Kenneth Walker Ground Explosion
    ("Walker_04_Explosive_22yd_Breakaway.mp4", 3660000),
    ("Walker_01_FourthDown_60yd_HouseCall.mp4", 7500000),
    # Beat 3: Downfield Passing to Kelce & Worthy
    ("Kelce_01_Deep_48yd_Bomb_Catch.mp4", 3090000),
    ("Worthy_02_Deep_Bomb_35yd_Touchdown.mp4", 3090000),
    # Beat 4: Steve Spagnuolo Defense & Chris Jones
    ("Defense_01_ChrisJones_Strip_Sack.mp4", 6200000),
    ("Defense_03_Spags_Exotic_Blitz_Sack.mp4", 5500000),
    ("Defense_02_Ragland_Fumble_Return_TD.mp4", 5500000),
    # Beat 5: Brutal AFC Gauntlet & O-Line
    ("Mahomes_01_Titans_27yd_Scramble_TD.mp4", 9080000),
    ("Walker_05_StiffArm_Power_15yd_Run.mp4", 5000000),
    ("Kelce_02_RedZone_11yd_Touchdown.mp4", 4000000),
    # Beat 6: Historic Three-Peat Climax
    ("Mahomes_02_SuperBowl_LIV_Wasp_TyreekHill.mp4", 7970000),
    ("Mahomes_03_AFCChamp_60yd_Watkins_TD.mp4", 8460000)
]

curr_t = t_deep_start
remaining_deep_us = deep_dur_us
for fn, dur_us in deep_beats:
    f_path = get_hl_path(fn)
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, min(dur_us, remaining_deep_us))
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use
    remaining_deep_us -= dur_to_use
    if remaining_deep_us <= 0:
        break

if remaining_deep_us > 0:
    f_path = get_hl_path("Mahomes_06_Touchdown_Flex_Celeb.mp4")
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, remaining_deep_us)
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use

# --- 6. END: OUTRO & CTA (Puck Voice - Beat Synchronized) ---
print("6. Adding Outro & CTA (Beat Synchronized)...")
t_outro_start = t_deep_start + deep_dur_us
outro_audio = pkg / "02_Voiceover_Outro_Puck.mp3"
outro_dur_us = get_exact_duration_us(outro_audio)
o_aud_mat = add_audio_material(outro_audio, outro_dur_us)
audio_track_segments.append(add_audio_segment(o_aud_mat, t_outro_start, outro_dur_us, 0, volume=1.0))

outro_beats = [
    ("Walker_02_RedZone_10yd_Plunge_TD.mp4", 7050000),
    ("Worthy_01_JetSweep_Speed_TD.mp4", 7000000),
    ("Kelce_04_FirstDown_Signal_Celeb.mp4", 5000000),
    ("Mahomes_05_Playoff_FistPump_Celeb.mp4", 5000000)
]
curr_t = t_outro_start
remaining_outro_us = outro_dur_us
for fn, dur_us in outro_beats:
    f_path = get_hl_path(fn)
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, min(dur_us, remaining_outro_us))
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use
    remaining_outro_us -= dur_to_use
    if remaining_outro_us <= 0:
        break

if remaining_outro_us > 0:
    f_path = get_hl_path("Mahomes_06_Touchdown_Flex_Celeb.mp4")
    full_dur_us = get_exact_duration_us(f_path)
    dur_to_use = min(full_dur_us, remaining_outro_us)
    mat = get_or_add_video_material(f_path, full_dur_us)
    main_track_segments.append(add_segment(mat, curr_t, dur_to_use, 0, volume=0.0, render_index=0))
    curr_t += dur_to_use

total_duration_us = t_outro_start + outro_dur_us

tracks = [
    {
        "attribute": 0, "flag": 0, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "Main Video (Hook + Experts + Narrative Highlights)",
        "segments": main_track_segments, "type": "video"
    },
    {
        "attribute": 0, "flag": 2, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "Expert Highlights Overlay (100% Muted, 0 Freezing)",
        "segments": overlay_track_segments, "type": "video"
    },
    {
        "attribute": 0, "flag": 0, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "AI Voiceover Track (Harmonized Puck Voice)",
        "segments": audio_track_segments, "type": "audio"
    }
]

draft_content = {
    "canvas_config": {"background": None, "height": 720, "ratio": "original", "width": 1280},
    "color_space": 0,
    "config": {
        "adjust_max_index": 1, "attachment_info": [], "combination_max_index": 1,
        "export_range": None, "extract_audio_last_index": 1, "lyrics_recognition_id": "",
        "lyrics_sync": True, "lyrics_taskinfo": [], "maintrack_adsorb": True, "material_save_mode": 0,
        "multi_language_current": "none", "multi_language_list": [], "multi_language_main": "none",
        "multi_language_mode": "none", "original_sound_last_index": 1, "record_audio_last_index": 1,
        "sticker_max_index": 1, "subtitle_keywords_config": None, "subtitle_recognition_id": "",
        "subtitle_sync": True, "subtitle_taskinfo": [], "system_font_list": [], "video_mute": False,
        "zoom_info_params": None
    },
    "cover": None, "create_time": 0, "duration": total_duration_us, "extra_info": None,
    "fps": 30.0, "free_render_index_mode_on": False, "group_container": None, "id": draft_id,
    "is_drop_frame_timecode": False, "keyframe_graph_list": [],
    "keyframes": {"adjusts": [], "audios": [], "effects": [], "filters": [], "handwrites": [], "stickers": [], "texts": [], "videos": []},
    "last_modified_platform": {"app_id": 359289, "app_source": "cc", "app_version": "5.3.0", "device_id": "fd4a7f389f13846010300b5fb1f7a314", "hard_disk_id": "", "mac_address": "d10e1f392e9283e563af3a08c9259c8f", "os": "windows", "os_version": "10.0.26200"},
    "lyrics_effects": [],
    "materials": materials,
    "mutable_config": None, "name": project_name, "new_version": "126.0.0", "path": "",
    "platform": {"app_id": 359289, "app_source": "cc", "app_version": "5.3.0", "device_id": "fd4a7f389f13846010300b5fb1f7a314", "hard_disk_id": "", "mac_address": "d10e1f392e9283e563af3a08c9259c8f", "os": "windows", "os_version": "10.0.26200"},
    "relationships": [], "render_index_track_mode_on": True, "retouch_cover": None,
    "source": "default", "static_cover_image_path": "", "time_marks": None,
    "tracks": tracks, "update_time": 0, "version": 360000
}

draft_meta = {
    "cloud_package_completed_time": "", "draft_cloud_capcut_purchase_info": "",
    "draft_cloud_last_action_download": False, "draft_cloud_materials": [],
    "draft_cloud_package_type": "", "draft_cloud_purchase_info": "", "draft_cloud_template_id": "",
    "draft_cloud_tutorial_info": "", "draft_cloud_videocut_purchase_info": "",
    "draft_cover": "draft_cover.jpg", "draft_deeplink_url": "",
    "draft_enterprise_info": {"draft_enterprise_extra": "", "draft_enterprise_id": "", "draft_enterprise_name": "", "enterprise_material": []},
    "draft_fold_path": draft_dir.as_posix(), "draft_id": draft_id, "draft_is_ae_produce": False,
    "draft_is_ai_packaging_used": False, "draft_is_ai_shorts": False, "draft_is_ai_translate": False,
    "draft_is_article_video_draft": False, "draft_is_from_deeplink": "false", "draft_is_invisible": False,
    "draft_materials": [
        {"type": 0, "value": meta_materials_value},
        {"type": 1, "value": []}, {"type": 2, "value": []}, {"type": 3, "value": []},
        {"type": 6, "value": []}, {"type": 7, "value": []}, {"type": 8, "value": []}
    ],
    "draft_materials_copied_info": [], "draft_name": project_name, "draft_need_rename_folder": False,
    "draft_new_version": "", "draft_removable_storage_device": "",
    "draft_root_path": capcut_root.as_posix(), "draft_segment_extra_info": [],
    "draft_timeline_materials_size_": 400000000, "draft_type": "",
    "tm_draft_cloud_completed": "", "tm_draft_cloud_modified": 0,
    "tm_draft_create": now_us, "tm_draft_modified": now_us, "tm_draft_removed": 0,
    "tm_duration": total_duration_us
}

with open(draft_dir / "draft_content.json", "w", encoding="utf-8") as f:
    json.dump(draft_content, f, ensure_ascii=False, indent=2)
with open(draft_dir / "draft_meta_info.json", "w", encoding="utf-8") as f:
    json.dump(draft_meta, f, ensure_ascii=False, indent=2)

root_meta_file = capcut_root / "root_meta_info.json"
with open(root_meta_file, "r", encoding="utf-8") as f:
    root_data = json.load(f)

p_entry = {
    "draft_cloud_last_action_download": False, "draft_cloud_purchase_info": "",
    "draft_cloud_template_id": "", "draft_cloud_tutorial_info": "", "draft_cloud_videocut_purchase_info": "",
    "draft_cover": (draft_dir / "draft_cover.jpg").as_posix(),
    "draft_fold_path": draft_dir.as_posix(),
    "draft_id": draft_id, "draft_is_ai_shorts": False, "draft_is_invisible": False,
    "draft_json_file": (draft_dir / "draft_content.json").as_posix(),
    "draft_name": project_name, "draft_new_version": "",
    "draft_root_path": capcut_root.as_posix(),
    "draft_timeline_materials_size": 400000000, "draft_type": "",
    "tm_draft_cloud_completed": "", "tm_draft_cloud_modified": 0,
    "tm_draft_create": now_us, "tm_draft_modified": now_us, "tm_draft_removed": 0,
    "tm_duration": total_duration_us
}

existing_stores = [e for e in root_data.get("all_draft_store", []) if e.get("draft_name") != project_name]
root_data["all_draft_store"] = [p_entry] + existing_stores

with open(root_meta_file, "w", encoding="utf-8") as f:
    json.dump(root_data, f, ensure_ascii=False, indent=2)

print("\nSUCCESS! Master CapCut Project harmonized with ZERO FREEZE & COMPLETE HIGHLIGHTS:")
print(f"Project Name: {project_name}")
print(f"Total Duration: {total_duration_us / 1000000:.2f}s ({total_duration_us / 60000000:.2f}m)")
print(f"Main Track Segments: {len(main_track_segments)}")
print(f"Overlay Track Segments: {len(overlay_track_segments)}")
print(f"Audio Track Segments: {len(audio_track_segments)}")
