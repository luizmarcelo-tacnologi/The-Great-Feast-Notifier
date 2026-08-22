@echo off
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
py -m PyInstaller --onedir --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py
if errorlevel 1 (exit /b 1)
"%localappdata%\Programs\Inno Setup 7\ISCC.exe" installer.iss