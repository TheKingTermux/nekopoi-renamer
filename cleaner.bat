@echo off
cd /d "%~dp0"

:MainMenu
echo "====================================================="
echo "   AUTO JAV + PPV + FC2 + KBJ + CN + CUS + Nekopoi"
echo "           CLEANER By TheKingTermux~ 💕"
echo "====================================================="
echo ""
echo "Pilih 1 untuk Python"
echo "pilih 2 untuk Powershell (Deprecated)"
echo "Pilih 3 untuk Keluar"

echo:
set /p pil= Masukkan Pilihan Anda [1-3] : 

if "%pil%"=="1" goto RunStable
if "%pil%"=="2" goto RunDeprecated
if "%pil%"=="3" goto Exit
goto MainMenu

:RunStable
cls
powershell -NoExit -ExecutionPolicy Bypass -File ".\debug.py"
pause
echo -------------------------
echo [Y] Run again |  [N] Back
echo -------------------------
set /p ulang= Choose [Y/N]: 
if /I "%ulang%"=="Y" goto RunStable
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:RunDeprecated
cls
powershell -NoExit -ExecutionPolicy Bypass -File  ".\debug.ps1"
pause
echo -------------------------
echo [Y] Run again |  [N] Back
echo -------------------------
set /p ulang= Choose [Y/N]: 
if /I "%ulang%"=="Y" goto RunDebug
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:exit
cls
echo "Terimakasih sudah menggunakan script ini"
pause
exit
