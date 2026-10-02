@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Dang khoi dong Cong cu xao nau content...
python app.py --open
pause
