# 🎬 Công Cụ Xào Nấu & Trợ Lý Sản Xuất Nguyên Liệu Video (Antigravity AI)

Hệ thống kết hợp giữa **Phần mềm phân tích dữ liệu video/audio tự động** và **Trợ lý AI Antigravity** được tối ưu hóa đặc biệt cho quy trình sản xuất video tổng hợp thể thao, phân tích chuyên gia và dựng video trên CapCut.

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT TRÊN MÁY TÍNH MỚI

Khi bạn chuyển sang máy tính mới có cài sẵn Antigravity:

### Bước 1: Tải mã nguồn về máy
Mở Terminal hoặc Command Prompt trên máy mới và chạy lệnh clone repository:
```bash
git clone <URL_GITHUB_CUA_BAN>
```
*(Hoặc tải file ZIP từ GitHub về và giải nén vào một thư mục, ví dụ: `D:\HIeu\content tong hop`)*

### Bước 2: Chạy cài đặt tự động (1-Click)
- Vào thư mục vừa tải về.
- Bấm đúp vào file **`cai_dat_may_moi.bat`**.
- File sẽ tự động kiểm tra Python, cài đặt toàn bộ thư viện cần thiết và thiết lập môi trường.

*Yêu cầu hệ thống:*
- **Python 3.10+** (nhớ tích chọn *Add python.exe to PATH* khi cài Python).
- **FFmpeg** (đã được cấu hình trong PATH của Windows).
- Card đồ họa NVIDIA (khuyên dùng để Whisper chạy GPU siêu tốc; nếu không có card thì hệ thống tự chạy CPU).

### Bước 3: Sử dụng với Antigravity
1. Mở phần mềm **Antigravity**.
2. Chọn **Open Folder** (Mở thư mục) và trỏ tới thư mục dự án này.
3. **Antigravity sẽ tự động kích hoạt:**
   - Đọc quy tắc cốt lõi trong **`GEMINI.md`** & **`AGENTS.md`**.
   - Kích hoạt kỹ năng **`nguyen-lieu-video`** (`.agents/skills/nguyen-lieu-video/SKILL.md`).
   - Tự động hỏi thời lượng video mục tiêu khi bắt đầu một tập mới.
   - Chuẩn bị đầy đủ 6 gói nguyên liệu sạch chuẩn phát thanh (-16 LUFS, giọng Puck 3.8, highlight không đơ hình) để bạn kéo thả vào CapCut!

---

## 🖥️ SỬ DỤNG GIAO DIỆN WEB ĐỘC LẬP
Nếu bạn muốn dùng giao diện web trực quan để tìm kiếm pha bóng, tải highlight 1080p từ YouTube hoặc bóc tách kịch bản từ talkshow chuyên gia:
- Bấm đúp vào file **`chay_phan_mem.bat`**.
- Trình duyệt sẽ tự động mở giao diện tại địa chỉ: `http://127.0.0.1:7860`.

---

## 📁 CẤU TRÚC THƯ MỤC CHÍNH

```
content tong hop/
├── .agents/
│   └── skills/
│       └── nguyen-lieu-video/       # Kỹ năng Antigravity tự động đóng gói nguyên liệu
├── cong-cu-xao-nau/                 # Toàn bộ mã nguồn ứng dụng & các module xử lý
│   ├── app.py                       # Giao diện chính Gradio Web UI
│   ├── xaonau/                      # Module xử lý AI, TTS, OCR, Whisper, FFmpeg
│   ├── requirements.txt             # Danh sách thư viện Python cần thiết
│   ├── settings.json                # Cấu hình API key & voice settings
│   └── dong_goi_nguyen_lieu.py      # Script tự động gom 6 gói nguyên liệu
├── GEMINI.md                        # Quy tắc vận hành cốt lõi (Always-On Rule)
├── AGENTS.md                        # Quy tắc dự án cho AI Agent
├── cai_dat_may_moi.bat              # Script cài đặt 1-click cho máy mới
├── chay_phan_mem.bat                # Script khởi động giao diện web 1-click
└── README.md                        # Tài liệu hướng dẫn này
```

---

## ⚙️ CẤU HÌNH VOICE & CHUẨN ÂM THANH ĐÃ KHÓA CỐ ĐỊNH
- **TTS Model**: `gemini-3.8-flash-tts`
- **Voice Name**: `Puck` (phong cách dẫn chuyện thể thao năng lượng cao)
- **Chuẩn phát thanh**: EBU R128 (-16 LUFS, True Peak tối đa -1.7 dBFS, dải động 11 LU)
- **Chuẩn highlight**: Cắt trọn vẹn tình huống từ Snap đến Ăn mừng, cam kết 100% không đơ hình ở giây cuối timeline.
