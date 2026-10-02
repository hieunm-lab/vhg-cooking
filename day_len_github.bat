@echo off
cd /d "%~dp0"

echo ======================================================================
echo   DANG TAI DU AN LEN GITHUB: hieunm-lab/vhg-cooking
echo ======================================================================
echo.

git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ======================================================================
    echo   [THANH CONG] Toan bo ma nguon da duoc tai len GitHub thanh cong!
    echo ======================================================================
) else (
    echo ======================================================================
    echo   [LUU Y] Neu co cua so trinh duyet hien ra, ban chi can bam xac thuc
    echo   roi chay lai file nay la xong.
    echo ======================================================================
)
echo.
pause
