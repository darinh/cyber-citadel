@echo off
REM One-click local playback for this course (Windows). Needs Python 3.
cd /d "%~dp0"
where py >nul 2>nul && (py serve.py %*) || (python serve.py %*)
