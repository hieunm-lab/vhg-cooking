import json
import uuid
import time
import shutil
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

def get_or_add_video_material(file_path, duration_us, width=1280, height=720):
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
        "crop_ratio": "free", "crop_scale": 1.0, "duration": duration_us, "extra_type_option": 0,
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
        "duration": duration_us,
        "extra_info": Path(file_path).name,
        "file_Path": posix_path,
        "height": height,
        "id": str(uuid.uuid4()),
        "import_time": int(time.time()),
        "import_time_ms": now_us,
        "item_source": 1, "md5": "", "metetype": "video",
        "roughcut_time_range": {"duration": duration_us, "start": 0},
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

print("Assembling Harmonized Tracks...")

main_track_segments = []
overlay_track_segments = []
audio_track_segments = []

# --- 1. HOOK (0s -> 17.5s) ---
hook_file = pkg / "00_Hook_Final_Master.mp4"
hook_dur_us = 17500000
hook_mat = get_or_add_video_material(hook_file, hook_dur_us)
main_track_segments.append(add_segment(hook_mat, 0, hook_dur_us, 0, volume=1.0, render_index=0))

# --- 2. EXPERT 1 (CBS) (17.5s -> 206.133s) ---
t_cbs_start = 17500000
cbs_file = pkg / "01_Expert_CBS_Clean_Voice.mp4"
cbs_dur_us = 188633333
cbs_mat = get_or_add_video_material(cbs_file, cbs_dur_us)
main_track_segments.append(add_segment(cbs_mat, t_cbs_start, cbs_dur_us, 0, volume=1.0, render_index=0))

# Overlays for CBS (9 highlight clips)
cbs_hl_defs = [
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_04_SuperBowl_Deep_Bomb_Wasp.mp4", 9000000, 5000000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_01_Deep_Catch_Downfield.mp4", 14000000, 5000000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4", 19000000, 6000000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_02_FourthDown_60yd_HouseCall.mp4", 86600000, 5000000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4", 107000000, 5000000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_03_VRoute_PlayAction_Catch.mp4", 112000000, 5000000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_04_RedZone_Plunge_TD.mp4", 117000000, 5000000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_04_FirstDown_Signal_Celeb.mp4", 128000000, 5000000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_01_EndZone_Dive_TD.mp4", 177000000, 5000000)
]
for hl_file, rel_start, dur in cbs_hl_defs:
    mat_id = get_or_add_video_material(hl_file, dur)
    overlay_track_segments.append(add_segment(mat_id, t_cbs_start + rel_start, dur, 0, volume=0.0, render_index=1))

# --- 3. MID 1: BRIDGE (206.133s -> 230.493s = 24.36s) ---
t_bridge_start = t_cbs_start + cbs_dur_us
bridge_audio = pkg / "01_Voiceover_Bridge_Puck.mp3"
bridge_dur_us = 24360000
b_aud_mat = add_audio_material(bridge_audio, bridge_dur_us)
audio_track_segments.append(add_audio_segment(b_aud_mat, t_bridge_start, bridge_dur_us, 0, volume=1.0))

# 5 B-roll clips for Bridge on Main Track
bridge_clips = [
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_01_JetSweep_TD.mp4", 4800000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_05_FistPump_Roar.mp4", 4800000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_03_Tackle_Break_Burst.mp4", 4800000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_01_Deep_Catch_Downfield.mp4", 5000000),
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_02_Deep_Bomb_TD.mp4", 4960000)
]
curr_t = t_bridge_start
for f, d in bridge_clips:
    mat = get_or_add_video_material(f, d)
    main_track_segments.append(add_segment(mat, curr_t, d, 0, volume=0.0, render_index=0))
    curr_t += d

# --- 4. EXPERT 2 (STEPHEN A & RYAN CLARK) (230.493s -> 352.626s = 122.133s) ---
t_ryan_start = t_bridge_start + bridge_dur_us
ryan_file = pkg / "02_Expert_RyanClark_Clean_Voice.mp4"
ryan_dur_us = 122133333
ryan_mat = get_or_add_video_material(ryan_file, ryan_dur_us)
main_track_segments.append(add_segment(ryan_mat, t_ryan_start, ryan_dur_us, 0, volume=1.0, render_index=0))

# Overlays for Ryan Clark (6 highlight clips)
ryan_hl_defs = [
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4", 34600000, 5000000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4", 66600000, 5000000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_01_ChrisJones_Strip_Sack.mp4", 77100000, 5000000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_02_Pocket_Crush_Sack.mp4", 82100000, 5000000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_03_Edge_Pressure_Tackle.mp4", 87100000, 4000000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_02_NoLook_Magic_Pass.mp4", 98600000, 5000000)
]
for hl_file, rel_start, dur in ryan_hl_defs:
    mat_id = get_or_add_video_material(hl_file, dur)
    overlay_track_segments.append(add_segment(mat_id, t_ryan_start + rel_start, dur, 0, volume=0.0, render_index=1))

# --- 5. MID 2: CONTENT AI DEEP DIVE (352.626s -> 461.886s = 109.26s) ---
t_deep_start = t_ryan_start + ryan_dur_us
deep_audio = pkg / "03_Voiceover_DeepDive_Puck.mp3"
deep_dur_us = 109260000
d_aud_mat = add_audio_material(deep_audio, deep_dur_us)
audio_track_segments.append(add_audio_segment(d_aud_mat, t_deep_start, deep_dur_us, 0, volume=1.0))

# 23 B-roll clips for Deep Dive on Main Track
deep_clips = [
    (lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4", 4800000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_02_FourthDown_60yd_HouseCall.mp4", 4800000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_03_Sideline_Scramble_Magic.mp4", 4600000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_03_VRoute_PlayAction_Catch.mp4", 4700000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_04_RedZone_Plunge_TD.mp4", 4600000),
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_03_EndZone_HighStep.mp4", 4700000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_01_EndZone_Dive_TD.mp4", 4800000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_01_ChrisJones_Strip_Sack.mp4", 4600000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_02_Pocket_Crush_Sack.mp4", 4600000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_03_Edge_Pressure_Tackle.mp4", 4500000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_04_ThirdDown_Stop_Celeb.mp4", 4500000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_05_FistPump_Roar.mp4", 4600000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4", 4600000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_02_NoLook_Magic_Pass.mp4", 4700000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_03_Tackle_Break_Burst.mp4", 4600000),
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_01_JetSweep_TD.mp4", 4600000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_04_SuperBowl_Deep_Bomb_Wasp.mp4", 4700000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_04_FirstDown_Signal_Celeb.mp4", 4600000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_05_StiffArm_Sideline.mp4", 4600000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_06_Flex_Celebration.mp4", 4700000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_01_Deep_Catch_Downfield.mp4", 4700000),
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_02_Deep_Bomb_TD.mp4", 4700000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_01_EndZone_Dive_TD.mp4", 5760000)
]
curr_t = t_deep_start
for f, d in deep_clips:
    mat = get_or_add_video_material(f, d)
    main_track_segments.append(add_segment(mat, curr_t, d, 0, volume=0.0, render_index=0))
    curr_t += d

# --- 6. END: OUTRO & CTA (461.886s -> 489.686s = 27.80s) ---
t_outro_start = t_deep_start + deep_dur_us
outro_audio = pkg / "02_Voiceover_Outro_Puck.mp3"
outro_dur_us = 27800000
o_aud_mat = add_audio_material(outro_audio, outro_dur_us)
audio_track_segments.append(add_audio_segment(o_aud_mat, t_outro_start, outro_dur_us, 0, volume=1.0))

# 6 B-roll clips for Outro on Main Track
outro_clips = [
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_05_FistPump_Roar.mp4", 4500000),
    (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4", 4500000),
    (lib / "02_Kenneth_Walker_Power" / "Walker_02_FourthDown_60yd_HouseCall.mp4", 4500000),
    (lib / "04_Xavier_Worthy_Speed" / "Worthy_03_EndZone_HighStep.mp4", 4500000),
    (lib / "05_Chiefs_Defense_Spags" / "Defense_01_ChrisJones_Strip_Sack.mp4", 4500000),
    (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_06_Flex_Celebration.mp4", 5300000)
]
curr_t = t_outro_start
for f, d in outro_clips:
    mat = get_or_add_video_material(f, d)
    main_track_segments.append(add_segment(mat, curr_t, d, 0, volume=0.0, render_index=0))
    curr_t += d

total_duration_us = t_outro_start + outro_dur_us

tracks = [
    {
        "attribute": 0, "flag": 0, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "Main Video (Hook + Experts + B-Roll)",
        "segments": main_track_segments, "type": "video"
    },
    {
        "attribute": 0, "flag": 2, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "Expert Highlights Overlay (Muted)",
        "segments": overlay_track_segments, "type": "video"
    },
    {
        "attribute": 0, "flag": 0, "id": str(uuid.uuid4()).upper(),
        "is_default_name": True, "name": "AI Voiceover Track (Harmonized Puck)",
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

print(f"SUCCESS! Master CapCut Project harmonized: {project_name}")
print(f"Total duration: {total_duration_us / 1000000:.2f} seconds ({total_duration_us / 60000000:.2f} minutes)")
