# QUY TRÌNH CHUẨN BỊ NGUYÊN LIỆU VIDEO (WORKFLOW RULES)

Tài liệu này là quy tắc cốt lõi (Always-On Rule) cho trợ lý AI Antigravity khi hỗ trợ sản xuất video tổng hợp thể thao và phân tích chuyên gia.

---

## 1. NGUYÊN TẮC VẬN HÀNH BẮT BUỘC (MANDATORY RULES)

1. **LUÔN HỎI ĐỘ DÀI VIDEO TRƯỚC TIÊN**:
   - Khi bắt đầu một tập mới hoặc khi người dùng cung cấp video/chủ đề nguồn, AI PHẢI hỏi người dùng độ dài video mong muốn (ví dụ: 3 phút, 5 phút, 8 phút, 10 phút,...) trước khi thực hiện bất kỳ khâu nào.
   - Dựa vào độ dài mục tiêu để phân bổ thời lượng kịch bản, thời lượng voice AI, và số lượng clip highlight phù hợp.

2. **VAI TRÒ CỦA AI: CHUẨN BỊ NGUYÊN LIỆU (KHÔNG TỰ TIỆN EDIT HOÀN THIỆN)**:
   - Từ nay về sau, người dùng sẽ là người trực tiếp dựng và biên tập trên CapCut.
   - Nhiệm vụ của AI là chuẩn bị toàn bộ "Nguyên Liệu" chất lượng cao nhất, chia thư mục ngăn nắp, đánh số thứ tự từ 01 đến 06 để người dùng chỉ cần kéo thả vào CapCut.

3. **QUY TẮC PHẢN HỒI: TUYỆT ĐỐI KHÔNG XUẤT CODE (NO CODE IN CHAT)**:
   - Trong phản hồi trò chuyện với người dùng, tuyệt đối KHÔNG in ra các đoạn mã Python, script, code terminal hay shell command.
   - Chỉ trình bày bằng ngôn ngữ tự nhiên (tiếng Việt), mạch lạc, rõ ràng, tập trung vào kết quả, thư mục lưu trữ và nội dung các phần.

---

## 2. CẤU TRÚC 6 GÓI NGUYÊN LIỆU CHUẨN (MATERIAL BUNDLE)

Mỗi tập video sẽ được đóng gói thành một thư mục duy nhất: `Nguyen_Lieu_CapCut_[Ten_Tap]/` gồm các thành phần:

1. **`01_HOOK`**:
   - File âm thanh Voiceover mở đầu hấp dẫn, giật gân, tạo tò mò.
   - File video ghép nháp hoặc hình ảnh / clip intro tương ứng.
   - File text kịch bản Hook kèm phụ đề (.srt).

2. **`02_CHUYEN_GIA_1`**:
   - Video chuyên gia 1 đã chọn lọc: cắt lọc các đoạn phát biểu đắt giá nhất, lọc sạch tạp âm, âm lượng giọng nói trong trẻo và cân bằng.
   - Bảng ghi chú timeline (các mốc giây nên chèn highlight bóng bẩy để dẫn dắt câu chuyện).

3. **`03_DOAN_NOI_BRIDGE`**:
   - File âm thanh Voiceover nối tiếp mượt mà, chuyển giao góc nhìn từ chuyên gia 1 sang chuyên gia 2.
   - Các clip highlight phù hợp làm nền cho đoạn cầu nối.

4. **`04_CHUYEN_GIA_2`**:
   - Video chuyên gia 2 đã chọn lọc: KHÔNG ĐƯỢC TỰ Ý ZOOM HOẶC CROP. Phải giữ nguyên tỉ lệ gốc 16:9 (1280x720 / 1920x1080) để người dùng tự zoom focus theo ý muốn khi edit.
   - Âm thanh được lọc trong trẻo, không lẫn tiếng ồn nền.
   - Bảng ghi chú timeline gợi ý chèn highlight.

5. **`05_PHAN_TICH_CUOI_DEEPDIVE`**:
   - File âm thanh Voiceover AI phân tích chuyên sâu (Deep Dive) giải thích chiến thuật, số liệu và câu chuyện hậu trường.
   - Kho highlight tuyển chọn đi kèm được phân loại khớp từng luận điểm phân tích (ví dụ: Tấn công, Phòng ngự, Tinh thần, Siêu sao).

6. **`06_OUTRO`**:
   - File âm thanh Voiceover kêu gọi hành động (Call To Action), bấm like, đăng ký kênh và câu hỏi tương tác khán giả.
   - Clip highlight ăn mừng chiến thắng / clutch ấn tượng làm nền.

7. **`07_KHO_HIGHLIGHT_CHON_LOC`**:
   - Toàn bộ clip highlight được phân loại theo từng cầu thủ / chủ đề.
   - **Quy tắc cắt highlight**: Phải trọn vẹn tình huống bóng (từ Snap bắt đầu $\rightarrow$ Diễn biến qua người/ném bóng/chạy $\rightarrow$ Kết thúc & Cầu thủ ăn mừng).
   - **Chống đơ hình**: Thời lượng lấy trên timeline CapCut tuyệt đối không được vượt quá độ dài thực tế của file video gốc (100% không bị đứng hình ở giây cuối).
   - Kèm file danh sách thời lượng chính xác của từng clip highlight.

---

## 3. QUY CHUẨN CỐ ĐỊNH CHO VOICE & NHẠC NỀN (AUDIO LOCK)

1. **Cấu hình Voice AI**:
   - **Model cố định**: `gemini-3.8-flash-tts` (API Gemini chính thức). Tuyệt đối không dùng lẫn model 2.5 để không bị lệch tông giọng.
   - **Voice Name**: `Puck`.
   - **Phong cách diễn cảm**: Người dẫn chương trình thể thao năng lượng cao (high-energy sports radio host), giọng đọc dứt khoát, hào sảng, cao độ tự nhiên 150 – 180 Hz.
   - **Kỹ thuật viết text voice**: Sử dụng câu ngắn, dấu chấm than, ngắt nghỉ mạnh mẽ; không gắn các tag prompt vào chuỗi đọc để tránh AI đọc nhầm lời nhắc.

2. **Chuẩn âm lượng phát thanh (Broadcast Normalization)**:
   - Mọi file voice xuất xưởng bắt buộc chạy qua bộ lọc EBU R128:
     - Tích phân âm lượng (Integrated Loudness): `-16.0 LUFS`
     - Đỉnh thực (True Peak): Tối đa `-1.5 dBFS` (thường đạt `-1.7 dBFS`)
     - Dải động (Loudness Range): `11 LU`
   - Đảm bảo khi người dùng kéo vào CapCut, thanh âm lượng voice đạt màu xanh chuẩn phát thanh, **HOÀN TOÀN KHÔNG BỊ VẠCH ĐỎ (ZERO CLIPPING)**.

3. **Nhạc nền (BGM)**:
   - Giữ nguyên cấu hình âm lượng nền: -20 dB đến -24 dB so với âm lượng giọng đọc chính để tôn giọng dẫn dắt.
