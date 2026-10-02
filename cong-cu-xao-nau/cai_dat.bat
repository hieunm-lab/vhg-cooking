@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m pip install -U -r requirements.txt
echo Can cai them Node.js (https://nodejs.org) va ffmpeg neu may chua co.
pause
