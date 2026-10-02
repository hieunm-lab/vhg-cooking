@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo   CÀI ĐẶT CÔNG CỤ XÀO NẤU & ANTIGRAVITY WORKFLOW TRÊN MÁY MỚI
echo ======================================================================
echo.

:: 1. Kiểm tra Python
echo [1/4] Đang kiểm tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Máy tính chưa cài đặt Python hoặc chưa tick "Add Python to PATH".
    echo Vui lòng tải và cài đặt Python 3.10+ từ: https://www.python.org/downloads/
    echo Lưu ý: Trong lúc cài, nhớ bấm tích chọn "Add python.exe to PATH".
    pause
    exit /b 1
)
python --version
echo - Python đã sẵn sàng!
echo.

:: 2. Cài đặt các thư viện cần thiết
echo [2/4] Đang cài đặt các thư viện từ requirements.txt...
cd cong-cu-xao-nau
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [CẢNH BÁO] Có một số gói thư viện chưa cài đặt xong. Vui lòng kiểm tra kết nối mạng.
) else (
    echo - Toàn bộ thư viện đã được cài đặt thành công!
)
cd ..
echo.

:: 3. Thiết lập file cấu hình settings.json
echo [3/4] Kiểm tra cấu hình cài đặt...
if not exist "cong-cu-xao-nau\settings.json" (
    if exist "cong-cu-xao-nau\settings.example.json" (
        copy "cong-cu-xao-nau\settings.example.json" "cong-cu-xao-nau\settings.json" >nul
        echo - Đã tạo file cong-cu-xao-nau\settings.json từ mẫu.
        echo (Bạn có thể mở file này để điền API key Gemini nếu dùng chức năng phân tích trực tuyến).
    )
) else (
    echo - File settings.json đã tồn tại sẵn.
)
echo.

:: 4. Kiểm tra FFmpeg
echo [4/4] Kiểm tra công cụ FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LƯU Ý] Máy tính chưa nhận diện FFmpeg trong hệ thống (PATH).
    echo Để phần mềm xử lý video và âm thanh mượt mà nhất:
    echo - Tải FFmpeg tại: https://www.gyan.dev/ffmpeg/builds/ (bản ffmpeg-release-essentials.zip)
    echo - Giải nén và thêm thư mục bin vào Environment Variables (PATH) của Windows.
) else (
    echo - FFmpeg đã được nhận diện trong hệ thống!
)
echo.

echo ======================================================================
echo   HOÀN TẤT CÀI ĐẶT!
echo ======================================================================
echo 1. Để chạy giao diện web: Bấm đúp file "chay_phan_mem.bat".
echo 2. Để dùng với trợ lý AI: Mở Antigravity và mở thư mục này ra.
echo    Antigravity sẽ tự động nhận diện quy tắc chuẩn bị nguyên liệu video
echo    và sẵn sàng đồng hành cùng bạn!
echo ======================================================================
pause
