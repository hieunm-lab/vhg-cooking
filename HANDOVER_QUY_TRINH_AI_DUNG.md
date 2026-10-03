# BÀN GIAO QUY TRÌNH: CÁC PHẦN DO AI DỰNG (HOOK – MID – END)

Tài liệu này dành cho một AI khác (hoặc người vận hành) tiếp quản việc sản xuất nguyên liệu video thể thao NFL theo đúng cách đã làm ở tập **Kansas City Chiefs**. Đọc kèm `GEMINI.md` (quy tắc bắt buộc) và `.agents/skills/nguyen-lieu-video/SKILL.md`.

---

## 0. BỨC TRANH TỔNG THỂ

Cấu trúc một video (tập mẫu Chiefs, ~7 phút 36 giây):

| # | Phần | Ai làm | Nguồn tiếng | Thời lượng tập mẫu |
|---|------|--------|-------------|--------------------|
| 1 | HOOK | AI dựng | Voice AI + nhạc nền + 8% tiếng sân | 17,5 s |
| 2 | Chuyên gia 1 (CBS – Bill Cowher, The NFL Today) | Cắt lọc từ video gốc | Giọng gốc chuyên gia | ~1,5–2 phút |
| 3 | BRIDGE (đoạn nối) | AI dựng | Voice AI | 22,97 s |
| 4 | Chuyên gia 2 (Ryan Clark) | Cắt lọc, **giữ nguyên 16:9, không zoom** | Giọng gốc chuyên gia | 122,13 s |
| 5 | DEEP DIVE (phân tích cuối) | AI dựng | Voice AI | 80,77 s |
| 6 | OUTRO | AI dựng | Voice AI | 24,05 s |

"Mid" = Bridge. "End" = Deep Dive + Outro. Phần AI chịu trách nhiệm sáng tạo là **kịch bản + voice + chọn highlight khớp lời**.

**Ngôn ngữ voice: TIẾNG ANH** (kênh hướng tới khán giả Mỹ, xưng hô "Chiefs Kingdom"). Không dịch sang tiếng Việt.

---

## 1. BƯỚC CHUNG TRƯỚC KHI DỰNG

1. **Hỏi người dùng độ dài video mong muốn** (bắt buộc). Phân bổ gợi ý:
   - 3 phút: Hook 15s – CG1 45s – Bridge 15s – CG2 45s – Deep Dive 45s – Outro 15s
   - 5 phút: Hook 20s – CG1 70s – Bridge 20s – CG2 70s – Deep Dive 90s – Outro 30s
   - 8–10 phút: Hook 30s – CG1 2p – Bridge 30s – CG2 2p – Deep Dive 2–3p – Outro 30s
2. **Nghe/chép lời 2 video chuyên gia trước** (Whisper `small.en`, GPU nếu có). Toàn bộ kịch bản AI phải bám vào luận điểm mà chuyên gia thực sự nói – Bridge tóm ý CG1 và giới thiệu CG2, Deep Dive đánh giá ai đúng.
3. **Tính số chữ kịch bản theo thời lượng**: giọng Puck đọc kiểu radio thể thao ≈ **2,6–2,9 từ tiếng Anh / giây** (Bridge 61 từ → 22,97 s; Outro 66 từ → 24,05 s; Deep Dive ~215 từ → 80,77 s). Viết xong đếm từ, chia 2,75 để ước thời lượng.

---

## 2. CÔNG THỨC VIẾT KỊCH BẢN TỪNG PHẦN

### Quy tắc văn phong chung (cho mọi đoạn voice)
- Câu ngắn, mỗi câu một ý, kết bằng **dấu chấm than**; câu hỏi tu từ dùng **"?!"**.
- Nhấn mạnh bằng VIẾT HOA một từ ("Can ANY team…").
- Gọi tên cầu thủ đầy đủ (Patrick Mahomes, Travis Kelce, Kenneth Walker, Steve Spagnuolo/"Spags").
- Số viết bằng chữ ("sixty-yard", "number fifteen") để TTS đọc chuẩn.
- **Tuyệt đối không chèn chỉ dẫn phong cách vào văn bản** (ví dụ "Say energetically:") – model sẽ đọc to cả câu đó. Năng lượng đến từ dấu câu và nhịp câu.

### 2.1 HOOK (15–30 s)
Khung 4 nhịp:
1. Chào cộng đồng fan: "What's up, Chiefs Kingdom!"
2. Đặt mâu thuẫn: truyền thông nghĩ X… ("Just when the media thought our dynasty was slowing down…")
3. Tung "quả bom": chuyên gia nổi tiếng vừa nói điều gây sốc.
4. Mời xem: "Listen to what Ryan Clark had to say!" → cắt thẳng vào chuyên gia.

Hình ảnh Hook (tập mẫu, 5 cảnh, tổng 17,5 s):
| Thời điểm | Cảnh | Dài |
|---|---|---|
| 0,0–5,0 | Mahomes ăn mừng touchdown ở endzone | 5,0 s |
| 5,0–9,5 | Kenneth Walker chạy bứt phá 73 yard | 4,5 s |
| 9,5–13,5 | Kelce bắt bóng biên + đập bóng ăn mừng | 4,0 s |
| 13,5–16,0 | Ryan Clark khoa tay hùng hồn trong trường quay | 2,5 s |
| 16,0–17,5 | Mahomes bước về phía camera | 1,5 s |

Nguyên tắc: cảnh 4–5 giây, đổi cảnh trùng nhịp câu; cảnh chuyên gia đặt ngay trước câu "Listen to…".

### 2.2 BRIDGE (15–30 s) – 4 câu
1. Tóm luận điểm chính của CG1 (nêu tên + chương trình).
2. Hệ quả/khẳng định của luận điểm đó.
3. "But over on [chương trình CG2], [tên CG2] is sounding the alarm on…" – tạo đối lập.
4. "Listen closely to how [CG2] breaks this down right now!"

Bản mẫu (61 từ, 22,97 s):
> Chiefs Kingdom, Coach Bill Cowher and the CBS crew make a massive statement! When Patrick Mahomes gets legitimate backfield support, this offense becomes practically unstoppable! But over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm on the brutal AFC gauntlet! Listen closely to how Ryan Clark breaks this down right now!

Hình nền Bridge: 3 highlight trọn pha nối tiếp (Walker TD 8,00 s → Worthy bắt bóng biên 7,97 s → Mahomes chuyền no-look 7,00 s).

### 2.3 DEEP DIVE (45 s – 3 phút) – 5 khối
1. **Mở**: "Now let's break down the full picture!" + "Who actually has it right?!" → trả lời: cả hai đều đúng ở một mặt.
2. **Tấn công**: điều gì thay đổi (Walker chạy bóng → hàng thủ phải dồn lên → Mahomes ném cho Kelce/Worthy).
3. **Phòng ngự**: luận điểm truyền thông bỏ qua (Chris Jones, blitz của Spags hiệp 4).
4. **Thử thách phía trước**: đối thủ cụ thể (Josh Allen, Lamar Jackson, Joe Burrow) + yếu tố then chốt (sức khỏe hàng công/OL).
5. **Chốt câu hỏi lớn**: "three-peat" lịch sử + câu kết khẳng định.

Mỗi khối gắn một nhóm highlight trong kho (Tấn công → Walker/Kelce/Worthy; Phòng ngự → Defense_Spags; Siêu sao → Mahomes).

### 2.4 OUTRO (15–30 s) – 5 câu
1. "Chiefs Kingdom, the message is loud and clear!"
2. Tổng kết một câu về đội.
3. Câu hỏi tương tác: "Can ANY team in the NFL stop Kansas City right now?!"
4. Kêu gọi bình luận dự đoán tỉ số.
5. Like – subscribe – bật chuông – "We will catch you in the next one!"

Hình nền: clip ăn mừng (Mahomes fist pump, flex celeb).

---

## 3. TẠO VOICE (KHÓA CỨNG – KHÔNG ĐƯỢC THAY)

- **Model**: `gemini-3.8-flash-tts` qua Gemini API chính thức (thư viện `google-genai`), `response_modalities = AUDIO`.
- **Voice**: prebuilt `Puck`.
- **Không bao giờ dùng `gemini-2.5-flash-preview-tts`**: nó đọc trầm ~118 Hz, đều đều → lệch tông hẳn so với 3.8 (~147–188 Hz). Đây là lỗi lớn nhất đã xảy ra ở tập mẫu (Deep Dive bị khác giọng với Hook).
- **Không pitch-shift để "chữa" lệch giọng** (rubberband tạo tiếng robot). Nếu lệch → tạo lại bằng đúng model.
- Dữ liệu trả về là PCM thô **16-bit, 24 000 Hz, mono** → chuyển sang MP3 192 kbps.
- **Chuẩn hóa loudness bắt buộc** (EBU R128): Integrated **−16 LUFS**, True Peak **−1,5 dBFS**, LRA **11 LU** (bộ lọc `loudnorm` của FFmpeg). Kết quả đo được ở tập mẫu: đỉnh −1,7 dBFS, không vạch đỏ trong CapCut.
- Quota: key miễn phí chỉ ~10 lượt/ngày/model TTS. Giữa 2 lượt gọi nghỉ ~20 s. Tạo tất cả đoạn voice của một tập trong **cùng một phiên, cùng key, cùng model** để tông đồng nhất.
- Kiểm tra sau khi tạo: đo thời lượng (ffprobe) và cao độ trung bình; các đoạn của cùng tập nên nằm trong khoảng 145–190 Hz.
- API key đọc từ `cong-cu-xao-nau/settings.json` (không ghi key cứng vào script).

---

## 4. NHẠC NỀN (BGM)

- Chính: **"Epic Cinematic Tension Intro" (Royalty Free)** – youtube.com/watch?v=_TcXaAcbQ5Q – cinematic hip-hop, bass 808 tối, căng.
- Dự phòng: **"Cinematic Epic Tension Dark"** – youtube.com/watch?v=cGi4ioZGiek – kiểu trailer, dồn dập hơn (hợp Deep Dive/Outro).
- Mức trộn: voice 100%, BGM hệ số âm lượng **0,22** (≈ −13 dB tuyệt đối; trên CapCut để **−20 đến −24 dB so với voice**), fade-in 0,5 s, fade-out ~1,2–1,5 s trước khi hết đoạn.
- Hook có thêm tiếng gốc của clip (tiếng sân) ở mức **0,08** để tạo không khí.

---

## 5. KHO HIGHLIGHT – CÁCH CẮT

1. **Nguồn**: video highlight trận chính thức (NFL/YouTube), top-10 Mahomes, tổng hợp sack phòng ngự. Tải bằng yt-dlp; công cụ `cong-cu-xao-nau` (tab ①②) giúp tìm pha theo play-by-play ESPN + đồng hồ trên thanh tỉ số.
2. **Một clip = một pha trọn vẹn**: từ snap → diễn biến → kết thúc + cầu thủ ăn mừng. Độ dài thực tế 5,5–11 s. Không cắt ép theo số giây cố định của lời thoại.
3. Xuất 1280×720, 30 fps, H.264 CRF 18, **bỏ tiếng** (-an).
   - Ở tập mẫu có crop nhẹ 82% vùng giữa rồi scale lại (để bỏ bớt logo/viền). Nếu người dùng muốn tự zoom thì bỏ bước crop này.
4. **Chống đơ hình**: sau khi cắt, dùng ffprobe đo thời lượng thật và ghi vào `actual_durations.json`. Khi đặt lên timeline, độ dài sử dụng phải **≤ thời lượng thật** (tập mẫu dùng ví dụ 7,97 s cho file 8,0 s).
5. Đặt tên theo mẫu `[CầuThủ]_[STT]_[Mô tả pha].mp4` và chia thư mục theo chủ đề:
   `01_Patrick_Mahomes_Clutch`, `02_Kenneth_Walker_Power`, `03_Travis_Kelce_Reboot`, `04_Xavier_Worthy_Speed`, `05_Chiefs_Defense_Spags`.
6. **Thay toàn bộ hình minh họa trong video chuyên gia** (đồ họa, highlight của đài) bằng highlight trong kho của mình.

---

## 6. VIDEO CHUYÊN GIA

- Cắt các đoạn phát biểu đắt nhất, bỏ phần quảng cáo/lạc đề.
- Lọc tiếng: giảm ồn nền, cân âm lượng giọng nói.
- **Không zoom/crop** – giữ 16:9 gốc (1280×720 hoặc 1920×1080). Người dùng tự zoom trong CapCut. (Lỗi đã xảy ra: tự zoom Ryan Clark bị lệch khung.)
- Kèm bảng mốc thời gian gợi ý chèn highlight. Ví dụ CG2 tập mẫu: 30,0 s Kelce TD 8,47 s · 60,0 s Walker stiff-arm 7,47 s · 75,0 s Chris Jones strip-sack 8,0 s · 85,0 s Spags blitz 5,5 s · 92,0 s Frank Clark sack 7,0 s · 102,0 s Mahomes no-look 7,97 s.

---

## 7. ĐÓNG GÓI GIAO CHO NGƯỜI DÙNG

Thư mục `C:\Users\<user>\Downloads\kho video\Nguyen_Lieu_CapCut_[Ten_Tap]\`:
`00_NHAC_NEN_BGM`, `01_HOOK`, `02_CHUYEN_GIA_1`, `03_DOAN_NOI_BRIDGE`, `04_CHUYEN_GIA_2`, `05_PHAN_TICH_CUOI_DEEPDIVE`, `06_OUTRO`, `07_KHO_HIGHLIGHT_CHON_LOC` + file hướng dẫn. Script hỗ trợ: `cong-cu-xao-nau/dong_goi_nguyen_lieu.py` (hiện đang gắn cứng đường dẫn tập Chiefs – cần sửa tên tập/đường dẫn khi dùng cho tập mới).

Mỗi thư mục voice phải có: file MP3 đã chuẩn hóa + file text **đúng nguyên văn tiếng Anh đã đọc** + phụ đề .srt khớp thời gian.

---

## 8. NHỮNG LỖI ĐÃ GẶP – ĐỪNG LẶP LẠI

| Lỗi | Nguyên nhân | Cách đúng |
|---|---|---|
| Deep Dive khác giọng Hook | Dùng lẫn model 2.5 và 3.8 | Chỉ dùng 3.8 cho mọi đoạn |
| AI đọc to câu chỉ dẫn | Ghép style prompt vào văn bản | Chỉ đưa văn bản cần đọc |
| Vạch đỏ trong CapCut | Chưa chuẩn hóa loudness | loudnorm −16 LUFS / TP −1,5 |
| Highlight đơ hình cuối clip | Độ dài timeline > độ dài file | Đo bằng ffprobe, dùng ≤ thời lượng thật |
| Highlight cụt giữa pha | Cắt theo số giây của lời | Cắt trọn pha, rồi xếp lời quanh pha |
| Ryan Clark bị zoom lệch | Tự động crop khuôn mặt | Giữ nguyên 16:9 |
| Người dùng chê bản dựng hoàn chỉnh | AI tự render cả video | Chỉ giao nguyên liệu, người dùng tự dựng |
| File kịch bản .txt và .srt không khớp voice | Viết tóm tắt tiếng Việt / srt bản cũ | Lưu nguyên văn tiếng Anh, srt tạo lại theo voice cuối |
