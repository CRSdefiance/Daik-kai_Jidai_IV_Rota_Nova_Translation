@echo off
setlocal
if "%~1"=="" exit /b 2
dk4tool manifest "%~1" --out work\manifest.json || exit /b
dk4tool extract-files "%~1" --out work\files || exit /b
dk4tool scan "%~1" --out work\scan_report.json

