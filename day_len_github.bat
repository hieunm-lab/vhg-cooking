@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo   ĐANG TẢI DỰ ÁN LÊN GITHUB
echo   Repository: https://github.com/hieunm-lab/vhg-cooking.git
echo ======================================================================
echo.

git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ======================================================================
    echo   [THÀNH CÔNG] Toàn bộ mã nguồn đã được tải lên GitHub thành công!
    echo ======================================================================
) else (
    echo ======================================================================
    echo   [LƯU Ý] Nếu có cửa sổ trình duyệt hiện ra, bạn chỉ cần bấm xác thực
    echo   rồi chạy lại file này là xong.
    echo ======================================================================
)
echo.
pause
