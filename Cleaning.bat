@echo off
setlocal
cd /d "%~dp0"
del /q "*.spec" 2>nul
if exist "build\" rmdir /s /q "build"
if exist "dist\" rmdir /s /q "dist"
if exist "installer\" rmdir /s /q "installer"
pause