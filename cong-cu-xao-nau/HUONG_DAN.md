# 🍳 Công cụ xào nấu content — Hướng dẫn sử dụng

Phần mềm chạy trên máy tính của bạn, mở trong trình duyệt tại địa chỉ `http://localhost:7860`.

## Khởi động
- Bấm đúp **`CongCuXaoNau.exe`**. Cửa sổ đen hiện lên, sau vài giây trình duyệt tự mở giao diện. Nếu trình duyệt không tự mở, vào `http://127.0.0.1:7860`.
- **Giữ cửa sổ đen mở trong lúc dùng.** Muốn tắt tool: đóng cửa sổ đen.
- Đã mở tool rồi mà bấm exe lần nữa: phần mềm chỉ mở lại trình duyệt, không chạy thêm bản thứ hai.
- Không cần cài Python, ffmpeg hay Node.js, mọi thứ đã nằm trong thư mục.
- Mang sang máy khác: copy **cả thư mục `CongCuXaoNau`** (không copy riêng file exe). Máy có card NVIDIA thì Whisper chạy bằng GPU, không có thì tự chạy bằng CPU (chậm hơn).
- Tool trục trặc: mở cửa sổ lệnh trong thư mục và chạy `CongCuXaoNau.exe --selftest` để biết thành phần nào lỗi.

### Thư mục bên trong
| Thư mục | Chứa gì |
|---|---|
| `data/games` | Kho các trận đã phân tích (video bản nhẹ, nhãn pha) |
| `data/clips` | Clip HD đã xuất, lấy file ở đây để dựng |
| `models` | Model Whisper |
| `bin` | ffmpeg, Node.js đi kèm |
| `_internal` | Thư viện của phần mềm, không đụng vào |

## Giai đoạn 1 (đã xong): Kho highlight tự động

### ① Tìm & phân tích trận
1. Chọn **Mùa giải / Giai đoạn / Tuần** → bấm **Tải danh sách trận**.
   - Sau đó **bấm vào dòng của trận muốn làm trong bảng** (hoặc chọn trong ô "Chọn trận"). Ô "Chọn trận" phải hiện đúng tên trận đó.
   - Đổi trận là phần mềm **tự tìm highlight** của trận mới, không cần bấm nút tìm.
   - Khi bấm phân tích, nếu tiêu đề video không có tên cả 2 đội, phần mềm sẽ cảnh báo để bạn kiểm tra lại.
2. Chọn trận đã đá → **🔎 Tìm video highlight**. Phần mềm tự chấm điểm video:
   - Ưu tiên kênh NFL chính thức, đúng mùa, đúng tuần.
   - Trừ điểm video preview, bình luận, sai năm.
3. Chọn video (mặc định là video điểm cao nhất), hoặc dán link YouTube khác.
4. Bấm **⬇ Tải & phân tích**. Khoảng 3–6 phút cho video 20 phút. Các bước phần mềm làm:
   - Tải bản nhẹ 360p để phân tích.
   - Tách cảnh, đo độ ồn âm thanh.
   - Tự học vị trí thanh tỷ số rồi đọc hiệp, đồng hồ, down theo từng giây (đã chạy được với CBS và Amazon Prime).
   - Chép lời bình luận viên bằng Whisper, có gợi ý tên cầu thủ của trận.
   - Khớp từng đoạn video với play-by-play của ESPN.

### ② Kho pha bóng
- Gõ tìm kiếm, ví dụ:
  - `Loop 56`, `Flowers`, `touchdown Henry`
  - `fg` (field goal), `td` (touchdown), `int` (đánh chặn), `sack`, `fumble`
  - `phút cuối`, `pha dài`, `ghi điểm`
- Để trống ô tìm kiếm và bấm Tìm để xem toàn bộ pha của trận.
- **Bấm vào một dòng** → xem clip thử + chi tiết:
  - Vị trí trong video, hiệp, đồng hồ, down, mô tả ESPN, cầu thủ.
  - **Pha phụ:** khi 1 đoạn có 2 pha liền nhau.
  - **Khoảnh khắc đỉnh:** lúc tiếng khán giả + bình luận viên lớn nhất, thường đúng lúc bắt bóng/ghi điểm. Dùng để canh trùng từ nhấn mạnh trong kịch bản.
  - Lời bình luận viên của đoạn.
- **⬇ Tải bản HD đoạn này** → tải đúng đoạn đó ở 1080p vào thư mục `data/clips/`. Tên file tự đặt theo trận, loại pha và cầu thủ.

### Cột "Tin cậy"
- **cao**: khớp hiệp + đồng hồ + down, và bình luận viên nhắc tên cầu thủ hoặc là pha ghi điểm.
- **trung bình**: khớp đồng hồ + down, hoặc suy ra từ lời bình luận (có ghi "(suy ra)").
- **thấp**: nên xem lại trước khi dùng.

### Mẹo
- Có sẵn phụ đề `.srt` từ Whisper GUI: đặt vào `data/games/<mã trận>/`, tên file chứa mã video YouTube. Phần mềm sẽ dùng file đó thay vì tự chép lời.
- **Tab ③ Cài đặt:**
  - Model Whisper: `small.en` nhanh, `medium.en` chính xác hơn.
  - Độ phân giải clip HD.
  - Gemini API key (dùng từ giai đoạn 2).
- Tick **"Phân tích lại từ đầu"** nếu muốn chạy lại toàn bộ một trận.

## Kết quả thử nghiệm (tuần 3, mùa 2026)
| Trận | Đài | Pha nhận diện | Pha ghi điểm tìm được | Pha dài ≥20 yard |
|---|---|---|---|---|
| BAL 34–31 DAL (Rio) | CBS | 77 | 12/12 | 15/16 |
| ATL 35–14 GB (TNF) | Amazon Prime | 60 | 8/8 | 10/13 |

## Giới hạn đã biết
- YouTube đôi khi chặn tải (lỗi 403). Phần mềm tự thử 3 chế độ tải. Nếu vẫn lỗi, đợi 15–30 phút rồi thử lại.
- Bản phân tích chỉ có 360p. Clip HD tải riêng theo đoạn.
- Mới thử trên đài CBS và Amazon Prime. Đài khác (FOX, NBC, ESPN) có thanh tỷ số khác và có thể cần tinh chỉnh.
- Dữ liệu ESPN là API công khai không chính thức, có thể thay đổi.
- Việc dùng footage thế nào để an toàn bản quyền là trách nhiệm của người biên tập.

## Giai đoạn 2 & 3 (Đã hoàn thiện): Studio Kịch bản (Nguồn chuyên gia)

### ③ Nạp Video Chuyên gia & Bóc tách Phân đoạn
1. Chuyển sang **Tab ③ Studio Kịch bản (Chuyên gia)**.
2. Nạp nguồn video/audio:
   - Kéo thả file video từ máy, hoặc dán đường dẫn file (ví dụ `D:\talkshows\first_take.mp4`).
   - Hoặc dán link YouTube podcast/talkshow.
3. Bấm **⬇ Nạp & Chạy Transcribe (Whisper)**:
   - Hệ thống tự động trích xuất âm thanh, nhận diện giọng nói (WhisperX / Faster-Whisper GPU CUDA).
   - Tự động dùng Gemini AI bóc tách các phân đoạn thảo luận, xác định người nói, trích xuất câu nói đắt giá (quotes) và chấm điểm kịch tính (Hype 1–10).

### Duyệt Luận điểm & Tạo Kịch bản ăn khớp Highlight
1. Xem danh sách các phân đoạn thảo luận trong bảng.
2. **Tích chọn `[x]` các đoạn bạn muốn đưa vào kịch bản** (có thể chọn 2–4 đoạn có tranh cãi hay nhất).
3. Nhập tên đội bóng tâm điểm (ví dụ: `Raiders`, `Chiefs`, `Cowboys`...).
4. Bấm **⚡ Tạo Kịch bản & Khớp Highlight**:
   - Hệ thống sinh **5 Tiêu đề giật gân** chuẩn click-through-rate.
   - Sinh **Hook mở đầu 15–20s** bùng nổ cảm xúc.
   - Viết **Kịch bản dẫn chuyện hoàn chỉnh** (kết nối ý kiến các chuyên gia).
   - Tự động tra cứu kho highlight (từ Tab ②) để **khớp đúng Clip Highlight 3s** minh họa cho câu nói.
   - Xuất file kịch bản `.md` tải về máy để bạn dễ dàng lồng tiếng hoặc đưa vào CapCut / Premiere / DaVinci Resolve.

## Các giai đoạn tiếp theo
4. Tự động dựng video template (ảnh zoom Ken Burns + overlay + phụ đề karaoke) và xuất timeline sang DaVinci Resolve / Premiere.
5. Tự động tạo ảnh Thumbnail giật gân.

