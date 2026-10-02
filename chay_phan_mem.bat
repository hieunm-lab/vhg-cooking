@echo off
chcp 65001 >nul
cd /d "%~dp0cong-cu-xao-nau"

echo Đang khởi động Công Cụ Xào Nấu Content...
echo Giao diện web sẽ tự động mở trên trình duyệt tại http://127.0.0.1:7860
echo.
python app.py --open
pause
