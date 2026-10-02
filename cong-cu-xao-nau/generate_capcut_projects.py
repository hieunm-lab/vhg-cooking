import json
import uuid
import time
import shutil
from pathlib import Path

# Paths
capcut_root = Path(r"C:\Users\Thien\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft")
pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
lib = pkg / "Kho_Highlight_San"

# Base template from a clean project
template_draft_dir = capcut_root / "0928 (3)"
sample_cover = template_draft_dir / "draft_cover.jpg"

def create_capcut_project(project_name, main_video_path, main_duration_us, highlight_segments):
    draft_dir = capcut_root / project_name
    draft_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy cover if exists
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
    
    def add_video_material(file_path, duration_us, width=1280, height=720):
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
            "path": Path(file_path).as_posix(), "picture_from": "none", "picture_set_category_id": "",
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
        return vid_id

    def add_segment_helper(material_id, target_start_us, duration_us, source_start_us=0, volume=1.0, render_index=0):
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

    # Main track segment
    main_mat_id = add_video_material(main_video_path, main_duration_us)
    main_segment = add_segment_helper(main_mat_id, 0, main_duration_us, 0, volume=1.0, render_index=0)
    
    # Overlay track segments (Highlights)
    overlay_segments = []
    meta_materials_value = [{
        "create_time": int(time.time()),
        "duration": main_duration_us,
        "extra_info": Path(main_video_path).name,
        "file_Path": Path(main_video_path).as_posix(),
        "height": 720,
        "id": str(uuid.uuid4()),
        "import_time": int(time.time()),
        "import_time_ms": now_us,
        "item_source": 1, "md5": "", "metetype": "video",
        "roughcut_time_range": {"duration": main_duration_us, "start": 0},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": 0, "width": 1280
    }]
    
    for hl in highlight_segments:
        hl_path = hl["file"]
        hl_start = hl["start_us"]
        hl_dur = hl["dur_us"]
        hl_mat_id = add_video_material(hl_path, hl_dur)
        # Highlight volume = 0.0 (muted)
        hl_seg = add_segment_helper(hl_mat_id, hl_start, hl_dur, 0, volume=0.0, render_index=1)
        overlay_segments.append(hl_seg)
        
        meta_materials_value.append({
            "create_time": int(time.time()),
            "duration": hl_dur,
            "extra_info": Path(hl_path).name,
            "file_Path": Path(hl_path).as_posix(),
            "height": 720,
            "id": str(uuid.uuid4()),
            "import_time": int(time.time()),
            "import_time_ms": now_us,
            "item_source": 1, "md5": "", "metetype": "video",
            "roughcut_time_range": {"duration": hl_dur, "start": 0},
            "sub_time_range": {"duration": -1, "start": -1},
            "type": 0, "width": 1280
        })

    tracks = [
        {
            "attribute": 0, "flag": 0, "id": str(uuid.uuid4()).upper(),
            "is_default_name": True, "name": "Main Studio Track",
            "segments": [main_segment], "type": "video"
        },
        {
            "attribute": 0, "flag": 2, "id": str(uuid.uuid4()).upper(),
            "is_default_name": True, "name": "Overlay Highlights (Muted)",
            "segments": overlay_segments, "type": "video"
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
        "cover": None, "create_time": 0, "duration": main_duration_us, "extra_info": None,
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
        "draft_timeline_materials_size_": 200000000, "draft_type": "",
        "tm_draft_cloud_completed": "", "tm_draft_cloud_modified": 0,
        "tm_draft_create": now_us, "tm_draft_modified": now_us, "tm_draft_removed": 0,
        "tm_duration": main_duration_us
    }

    with open(draft_dir / "draft_content.json", "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)
    with open(draft_dir / "draft_meta_info.json", "w", encoding="utf-8") as f:
        json.dump(draft_meta, f, ensure_ascii=False, indent=2)

    return {
        "draft_cloud_last_action_download": False, "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "", "draft_cloud_tutorial_info": "", "draft_cloud_videocut_purchase_info": "",
        "draft_cover": (draft_dir / "draft_cover.jpg").as_posix(),
        "draft_fold_path": draft_dir.as_posix(),
        "draft_id": draft_id, "draft_is_ai_shorts": False, "draft_is_invisible": False,
        "draft_json_file": (draft_dir / "draft_content.json").as_posix(),
        "draft_name": project_name, "draft_new_version": "",
        "draft_root_path": capcut_root.as_posix(),
        "draft_timeline_materials_size": 200000000, "draft_type": "",
        "tm_draft_cloud_completed": "", "tm_draft_cloud_modified": 0,
        "tm_draft_create": now_us, "tm_draft_modified": now_us, "tm_draft_removed": 0,
        "tm_duration": main_duration_us
    }

# Build Project 1: CBS The NFL Today (3m08s)
cbs_highlights = [
    {"file": (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_04_SuperBowl_Deep_Bomb_Wasp.mp4").as_posix(), "start_us": 9000000, "dur_us": 5000000},
    {"file": (lib / "03_Travis_Kelce_Reboot" / "Kelce_01_Deep_Catch_Downfield.mp4").as_posix(), "start_us": 14000000, "dur_us": 5000000},
    {"file": (lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4").as_posix(), "start_us": 19000000, "dur_us": 6000000},
    {"file": (lib / "02_Kenneth_Walker_Power" / "Walker_02_FourthDown_60yd_HouseCall.mp4").as_posix(), "start_us": 86600000, "dur_us": 5000000},
    {"file": (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4").as_posix(), "start_us": 107000000, "dur_us": 5000000},
    {"file": (lib / "03_Travis_Kelce_Reboot" / "Kelce_03_VRoute_PlayAction_Catch.mp4").as_posix(), "start_us": 112000000, "dur_us": 5000000},
    {"file": (lib / "02_Kenneth_Walker_Power" / "Walker_04_RedZone_Plunge_TD.mp4").as_posix(), "start_us": 117000000, "dur_us": 5000000},
    {"file": (lib / "03_Travis_Kelce_Reboot" / "Kelce_04_FirstDown_Signal_Celeb.mp4").as_posix(), "start_us": 128000000, "dur_us": 5000000},
    {"file": (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_01_EndZone_Dive_TD.mp4").as_posix(), "start_us": 177000000, "dur_us": 5000000}
]

p1_entry = create_capcut_project(
    "01_Chiefs_CBS_Expert_Timeline",
    (pkg / "01_Expert_CBS_Clean_Voice.mp4").as_posix(),
    188633333,
    cbs_highlights
)

# Build Project 2: Stephen A. Smith & Ryan Clark (2m02s)
ryan_highlights = [
    {"file": (lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4").as_posix(), "start_us": 34600000, "dur_us": 5000000},
    {"file": (lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4").as_posix(), "start_us": 66600000, "dur_us": 5000000},
    {"file": (lib / "05_Chiefs_Defense_Spags" / "Defense_01_ChrisJones_Strip_Sack.mp4").as_posix(), "start_us": 77100000, "dur_us": 5000000},
    {"file": (lib / "05_Chiefs_Defense_Spags" / "Defense_02_Pocket_Crush_Sack.mp4").as_posix(), "start_us": 82100000, "dur_us": 5000000},
    {"file": (lib / "05_Chiefs_Defense_Spags" / "Defense_03_Edge_Pressure_Tackle.mp4").as_posix(), "start_us": 87100000, "dur_us": 4000000},
    {"file": (lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_02_NoLook_Magic_Pass.mp4").as_posix(), "start_us": 98600000, "dur_us": 5000000}
]

p2_entry = create_capcut_project(
    "02_Chiefs_RyanClark_Expert_Timeline",
    (pkg / "02_Expert_RyanClark_Clean_Voice.mp4").as_posix(),
    122133333,
    ryan_highlights
)

# Update root_meta_info.json
root_meta_file = capcut_root / "root_meta_info.json"
with open(root_meta_file, "r", encoding="utf-8") as f:
    root_data = json.load(f)

# Filter out old entries if existed
existing_stores = [e for e in root_data.get("all_draft_store", []) if e.get("draft_name") not in ["01_Chiefs_CBS_Expert_Timeline", "02_Chiefs_RyanClark_Expert_Timeline"]]
# Prepend our new projects to the very top!
root_data["all_draft_store"] = [p1_entry, p2_entry] + existing_stores

with open(root_meta_file, "w", encoding="utf-8") as f:
    json.dump(root_data, f, ensure_ascii=False, indent=2)

print("SUCCESSFULLY CREATED BOTH CAPCUT PROJECTS AND UPDATED ROOT META!")
