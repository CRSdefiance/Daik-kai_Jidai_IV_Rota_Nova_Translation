@echo off
setlocal
if "%~2"=="" exit /b 2
dk4tool insert-script "%~1" "%~2" --out out\noop.nds --mode fixed

