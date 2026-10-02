---
name: nguyen-lieu-video
description: Quy trình chuẩn bị toàn bộ nguyên liệu video thể thao 6 phần (Hook, Chuyên gia 1, Đoạn nối Bridge, Chuyên gia 2 No-Zoom, Phân tích Deep Dive, Outro, Kho Highlight trọn vẹn không đơ). Sử dụng khi người dùng yêu cầu làm tập mới hoặc chuẩn bị nguyên liệu để tự edit trên CapCut.
---

# KỸ NĂNG CHUẨN BỊ NGUYÊN LIỆU VIDEO (NGUYEN LIEU VIDEO SKILL)

Khi người dùng bắt đầu một tập video mới hoặc cung cấp video/ý tưởng nguồn:

## BƯỚC 1: HỎI THỜI LƯỢNG MỤC TIÊU
- AI lập tức hỏi người dùng: "Tập này anh/chị muốn làm video dài bao nhiêu phút (ví dụ: 3 phút, 5 phút, 8 phút, 10 phút...) để em tính toán thời lượng từng phần và số lượng highlight phù hợp nhất?"
- Dựa vào câu trả lời, chia timeline ước lượng:
  - 3 phút: Hook (15s) -> Chuyên gia 1 (45s) -> Nối (15s) -> Chuyên gia 2 (45s) -> Phân tích (45s) -> Outro (15s)
  - 5 phút: Hook (20s) -> Chuyên gia 1 (70s) -> Nối (20s) -> Chuyên gia 2 (70s) -> Phân tích (90s) -> Outro (30s)
  - 8-10 phút: Hook (30s) -> Chuyên gia 1 (2m) -> Nối (30s) -> Chuyên gia 2 (2m) -> Phân tích (2-3m) -> Outro (30s)

## BƯỚC 2: CHUẨN BỊ VÀ ĐÓNG GÓI 6 PHẦN NGUYÊN LIỆU VÀO THƯ MỤC
Tạo thư mục: `C:\Users\Thien\Downloads\kho video\Nguyen_Lieu_CapCut_[Tên_Tập]\` gồm:
1. `01_HOOK`: Voiceover Puck 3.8 + Text kịch bản + Phụ đề (.srt) + Video/ảnh mở màn.
2. `02_CHUYEN_GIA_1`: Clip chuyên gia 1 âm thanh lọc sạch + File gợi ý điểm chèn highlight.
3. `03_DOAN_NOI_BRIDGE`: Voiceover Puck 3.8 chuyển đoạn + Clip highlight đệm.
4. `04_CHUYEN_GIA_2`: Clip chuyên gia 2 16:9 gốc KHÔNG zoom/crop để người dùng tự do zoom khi dựng + gợi ý chèn highlight.
5. `05_PHAN_TICH_CUOI_DEEPDIVE`: Voiceover Puck 3.8 phân tích sâu + Thư mục highlight khớp các ý chính.
6. `06_OUTRO`: Voiceover Puck 3.8 kêu gọi like/share/sub + Clip highlight ăn mừng.
7. `07_KHO_HIGHLIGHT_CHON_LOC`: Các pha bóng hoàn chỉnh (snap -> play -> celebration), đảm bảo duration khớp 100% không bị đơ hình cuối clip.

## BƯỚC 3: TIÊU CHUẨN KỸ THUẬT ÂM THANH
- Voice Model: `gemini-3.8-flash-tts`
- Voice Name: `Puck`
- Chuẩn âm lượng: EBU R128 (-16 LUFS, True Peak -1.5 dBFS)
- Tuyệt đối không xuất hiện vạch đỏ trong CapCut.

## BƯỚC 4: QUY TẮC PHẢN HỒI
- Tuyệt đối không xuất code ("không code").
- Báo cáo rõ ràng đường dẫn thư mục và hướng dẫn sử dụng.
