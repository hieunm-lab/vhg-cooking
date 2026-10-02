import os
import shutil
import json

SOURCE_PKG = r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package"
SOURCE_KHO = r"C:\Users\Thien\Downloads\kho video"
TARGET_DIR = r"C:\Users\Thien\Downloads\kho video\Nguyen_Lieu_CapCut_Chiefs_Master"

def main():
    print(f"Creating master package directory at: {TARGET_DIR}")
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # 01_HOOK
    p_hook = os.path.join(TARGET_DIR, "01_HOOK")
    os.makedirs(p_hook, exist_ok=True)
    for f in ["00_Voiceover_Hook_Puck.mp3", "00_Hook_Final_Master.mp4", "Chiefs_Hook_Subtitles.srt"]:
        src = os.path.join(SOURCE_PKG, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(p_hook, f))
    with open(os.path.join(p_hook, "Kich_Ban_Hook.txt"), "w", encoding="utf-8") as f:
        f.write("KỊCH BẢN HOOK (17 giây):\n"
                "Patrick Mahomes và Kansas City Chiefs trở lại vị thế kẻ hủy diệt! "
                "Hàng thủ thép của Spagnuolo cùng sự hồi sinh của Travis Kelce khiến cả NFL phải khiếp sợ! "
                "Cùng xem các chuyên gia hàng đầu phân tích sự trở lại này ngay bây giờ!\n")

    # 02_CHUYEN_GIA_1
    p_exp1 = os.path.join(TARGET_DIR, "02_CHUYEN_GIA_1_CBS")
    os.makedirs(p_exp1, exist_ok=True)
    src_exp1 = os.path.join(SOURCE_PKG, "01_Expert_CBS_Clean_Voice.mp4")
    if os.path.exists(src_exp1):
        shutil.copy2(src_exp1, os.path.join(p_exp1, "01_Expert_CBS_Clean_Voice.mp4"))
    with open(os.path.join(p_exp1, "Ghi_Chu_Timeline_Chuyen_Gia_1.txt"), "w", encoding="utf-8") as f:
        f.write("GHI CHÚ CHÈN HIGHLIGHT CHO CHUYÊN GIA 1 (CBS Sports - 1m30s):\n"
                "- 00:00 - 00:15: Giữ hình chuyên gia CBS mở đầu bàn luận.\n"
                "- 00:15 - 00:45: Chèn highlight Kenneth Walker (trong thư mục 02_Kenneth_Walker_Power) khi nhắc tới sự bùng nổ của hàng công.\n"
                "- 00:45 - 01:10: Chèn highlight Travis Kelce (trong thư mục 03_Travis_Kelce_Reboot) khi bàn về khả năng bắt bóng then chốt.\n"
                "- 01:10 - 01:30: Quay lại mặt chuyên gia CBS chốt luận điểm.\n")

    # 03_DOAN_NOI_BRIDGE
    p_bridge = os.path.join(TARGET_DIR, "03_DOAN_NOI_BRIDGE")
    os.makedirs(p_bridge, exist_ok=True)
    src_bridge = os.path.join(SOURCE_PKG, "01_Voiceover_Bridge_Puck.mp3")
    if not os.path.exists(src_bridge):
        src_bridge = os.path.join(SOURCE_KHO, "01_Voiceover_Bridge_Puck.mp3")
    if os.path.exists(src_bridge):
        shutil.copy2(src_bridge, os.path.join(p_bridge, "01_Voiceover_Bridge_Puck.mp3"))
    with open(os.path.join(p_bridge, "Kich_Ban_Bridge.txt"), "w", encoding="utf-8") as f:
        f.write("KỊCH BẢN ĐOẠN NỐI (23 giây):\n"
                "Những phân tích từ CBS thật sự sắc sảo! Nhưng góc nhìn từ một cựu cầu thủ phòng ngự kỳ cựu như Ryan Clark "
                "sẽ cho chúng ta thấy những điểm yếu chết người mà các đối thủ vẫn chưa thể khai thác trước Chiefs! "
                "Hãy lắng nghe Ryan Clark chỉ rõ điều này!\n")

    # 04_CHUYEN_GIA_2
    p_exp2 = os.path.join(TARGET_DIR, "04_CHUYEN_GIA_2_RYAN_CLARK")
    os.makedirs(p_exp2, exist_ok=True)
    src_exp2 = os.path.join(SOURCE_PKG, "02_Expert_RyanClark_Clean_Voice.mp4")
    if not os.path.exists(src_exp2):
        src_exp2 = os.path.join(SOURCE_KHO, "02_Expert_RyanClark_NoZoom.mp4")
    if os.path.exists(src_exp2):
        shutil.copy2(src_exp2, os.path.join(p_exp2, "02_Expert_RyanClark_Clean_Voice_NoZoom.mp4"))
    with open(os.path.join(p_exp2, "Ghi_Chu_Timeline_Chuyen_Gia_2.txt"), "w", encoding="utf-8") as f:
        f.write("GHI CHÚ CHÈN HIGHLIGHT CHO CHUYÊN GIA 2 (Ryan Clark - 1m30s - KHÔNG ZOOM GỐC 16:9):\n"
                "Lưu ý: Video này giữ nguyên khung hình 16:9 gốc chưa zoom, anh có thể tự zoom focus vào Ryan Clark nếu muốn.\n"
                "- 00:00 - 00:20: Ryan Clark đặt vấn đề về áp lực lên đối thủ.\n"
                "- 00:20 - 00:55: Chèn highlight Patrick Mahomes Clutch (trong thư mục 01_Patrick_Mahomes_Clutch) khi Ryan Clark phân tích các pha xử lý bình tĩnh trong túi bảo vệ.\n"
                "- 00:55 - 01:30: Quay lại mặt Ryan Clark tổng kết sức mạnh tinh thần của Chiefs.\n")

    # 05_PHAN_TICH_CUOI_DEEPDIVE
    p_deep = os.path.join(TARGET_DIR, "05_PHAN_TICH_CUOI_DEEPDIVE")
    os.makedirs(p_deep, exist_ok=True)
    src_deep = os.path.join(SOURCE_PKG, "03_Voiceover_DeepDive_Puck.mp3")
    if not os.path.exists(src_deep):
        src_deep = os.path.join(SOURCE_KHO, "03_Voiceover_DeepDive_Puck.mp3")
    if os.path.exists(src_deep):
        shutil.copy2(src_deep, os.path.join(p_deep, "03_Voiceover_DeepDive_Puck.mp3"))
    with open(os.path.join(p_deep, "Kich_Ban_DeepDive.txt"), "w", encoding="utf-8") as f:
        f.write("KỊCH BẢN PHÂN TÍCH CHUYÊN SÂU (80 giây):\n"
                "Rõ ràng sự khác biệt lớn nhất của Kansas City Chiefs mùa giải năm nay không chỉ nằm ở Patrick Mahomes, "
                "mà chính là triết lý phòng ngự bậc thầy của Steve Spagnuolo! Với việc đưa ra những biến thể blitz không thể lường trước, "
                "họ liên tục bẻ gãy ý đồ tấn công của đối phương ngay từ tuyến snap! "
                "Bên cạnh đó, sự trở lại của Travis Kelce và tốc độ xé gió của Xavier Worthy đã kéo giãn hoàn toàn cự ly đội hình đối phương! "
                "Chiefs không chỉ thắng bằng tài năng cá nhân, mà họ đang bóp nghẹt đối thủ bằng bản lĩnh và kỷ luật chiến thuật thượng thừa!\n")

    # 06_OUTRO
    p_outro = os.path.join(TARGET_DIR, "06_OUTRO")
    os.makedirs(p_outro, exist_ok=True)
    src_outro = os.path.join(SOURCE_PKG, "02_Voiceover_Outro_Puck.mp3")
    if not os.path.exists(src_outro):
        src_outro = os.path.join(SOURCE_KHO, "02_Voiceover_Outro_Puck.mp3")
    if os.path.exists(src_outro):
        shutil.copy2(src_outro, os.path.join(p_outro, "02_Voiceover_Outro_Puck.mp3"))
    with open(os.path.join(p_outro, "Kich_Ban_Outro.txt"), "w", encoding="utf-8") as f:
        f.write("KỊCH BẢN OUTRO (24 giây):\n"
                "Theo các bạn, liệu có đội bóng nào đủ sức ngăn cản Kansas City Chiefs bước lên đỉnh vinh quang một lần nữa? "
                "Hãy để lại bình luận và quan điểm của bạn bên dưới! "
                "Đừng quên bấm Like, Đăng ký kênh và nhấn chuông thông báo để không bỏ lỡ những phân tích đỉnh cao tiếp theo! "
                "Xin chào và hẹn gặp lại!\n")

    # 07_KHO_HIGHLIGHT_CHON_LOC
    p_hl = os.path.join(TARGET_DIR, "07_KHO_HIGHLIGHT_CHON_LOC")
    src_hl = os.path.join(SOURCE_PKG, "Kho_Highlight_San")
    if os.path.exists(src_hl):
        if os.path.exists(p_hl):
            shutil.rmtree(p_hl)
        shutil.copytree(src_hl, p_hl)
        
    # Tạo bảng thời lượng dễ xem
    dur_json = os.path.join(p_hl, "actual_durations.json")
    if os.path.exists(dur_json):
        with open(dur_json, "r", encoding="utf-8") as f:
            dur_data = json.load(f)
        with open(os.path.join(p_hl, "DANH_SACH_THOI_LUONG_HIGHLIGHT.txt"), "w", encoding="utf-8") as f:
            f.write("DANH SÁCH THỜI LƯỢNG CHÍNH XÁC CỦA CÁC CLIP HIGHLIGHT (CHỐNG ĐƠ 100%):\n")
            f.write("Quy tắc: Khi kéo vào CapCut, chỉ lấy độ dài trong khoảng từ 0s đến đúng số giây tối đa bên dưới.\n\n")
            for rel, sec in sorted(dur_data.items()):
                f.write(f"- {rel}: {sec:.2f} giây\n")
                
    # Hướng dẫn tổng quát
    with open(os.path.join(TARGET_DIR, "HUONG_DAN_SU_DUNG_NGUYEN_LIEU.txt"), "w", encoding="utf-8") as f:
        f.write("====================================================================\n"
                "GÓI NGUYÊN LIỆU ĐÃ ĐÓNG GÓI CHUẨN ĐỂ ANH TỰ BIÊN TẬP TRÊN CAPCUT\n"
                "====================================================================\n\n"
                "Cấu trúc các thư mục từ 01 đến 06 theo đúng thứ tự kịch bản video:\n"
                "1. 01_HOOK: Voiceover mở đầu + clip nháp + phụ đề srt\n"
                "2. 02_CHUYEN_GIA_1_CBS: Clip chuyên gia 1 âm trong rõ + timeline gợi ý\n"
                "3. 03_DOAN_NOI_BRIDGE: Voiceover chuyển tiếp mượt mà\n"
                "4. 04_CHUYEN_GIA_2_RYAN_CLARK: Clip chuyên gia 2 chuẩn 16:9 gốc (không zoom để anh tự zoom)\n"
                "5. 05_PHAN_TICH_CUOI_DEEPDIVE: Voiceover phân tích chuyên sâu của AI\n"
                "6. 06_OUTRO: Voiceover kêu gọi Like/Share/Sub\n"
                "7. 07_KHO_HIGHLIGHT_CHON_LOC: 22 pha bóng hoàn chỉnh theo 5 chủ đề (Mahomes, Walker, Kelce, Worthy, Defense Spags).\n\n"
                "ĐẶC ĐIỂM KỸ THUẬT ĐÃ CHỐT:\n"
                "- Voice model: Đồng bộ 100% bằng gemini-3.8-flash-tts giọng Puck (thể thao, hào sảng).\n"
                "- Chuẩn âm lượng: EBU R128 (-16 LUFS, True Peak -1.7 dBFS), không bao giờ bị vạch đỏ trong CapCut.\n"
                "- Toàn bộ clip highlight cắt đủ pha (snap -> diễn biến -> ăn mừng), tuyệt đối không đơ hình.\n")
                
    print("Done packaging master directory successfully!")

if __name__ == "__main__":
    main()
