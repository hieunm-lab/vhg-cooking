@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Dang dong goi Cong cu xao nau content thanh file exe...
python -m PyInstaller CongCuXaoNau.spec --noconfirm --distpath "..\_build_dist" --workpath "..\_build_work"
echo.
echo Xong. Copy thu muc _internal va file CongCuXaoNau.exe moi trong ..\_build_dist\CongCuXaoNau
echo de thay the ban cu trong thu muc CongCuXaoNau (giu nguyen data, models, bin).
pause
