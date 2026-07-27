@echo off
setlocal
if "%~2"=="" exit /b 2
dk4tool make-xdelta "%~1" "%~2" --out out\dk4_en.xdelta

