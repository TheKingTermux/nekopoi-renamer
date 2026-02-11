@echo off
cd /d "%~dp0"

:MainMenu
cls
echo "====================================================="
echo "   AUTO JAV + PPV + FC2 + KBJ + CN + CUS + Nekopoi"
echo "           CLEANER By TheKingTermux~ 💕"
echo "====================================================="
echo ""
echo "Pilih 1 untuk Python (Main Script)"
echo "Pilih 2 untuk Python (Cleaner)"
echo "pilih 3 untuk Powershell (Deprecated)"
echo "Pilih 4 untuk Keluar"

echo:
set /p pil= Masukkan Pilihan Anda [1-4] : 

if "%pil%"=="1" goto RunStable
if "%pil%"=="2" goto RunCleaner
if "%pil%"=="3" goto RunDeprecated
if "%pil%"=="4" goto Exit
goto MainMenu

:RunStable
cls
python debug.py
pause
echo -------------------------
echo [Y] Run again |  [N] Back
echo -------------------------
set /p ulang= Choose [Y/N]: 
if /I "%ulang%"=="Y" goto RunStable
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:RunCleaner
cls
echo "Gunakan ini jika Main Script (Python) tidak bekerja dengan baik"
echo "Pilih 1 untuk Lanjut, Pilih 2 untuk Kembali"

echo:
set /p pilclean= Masukkan Pilihan Anda [1-2] : 

if "%pilclean%"=="1" goto RunCleanerFix
if "%pilclean%"=="2" goto MainMenu

:RunCleanerFix
cls
python cleaner.py
pause
echo -------------------------
echo [Y] Run again |  [N] Back
echo -------------------------
set /p ulang= Choose [Y/N]: 
if /I "%ulang%"=="Y" goto RunCleanerFix
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:RunDeprecated
cls
echo "Script ini sudah tidak bekerja dengan baik dibandingkan dengan Main Script (Python)"
echo "Pilih 1 untuk Lanjut, Pilih 2 untuk Kembali"

echo:
set /p pildepr= Masukkan Pilihan Anda [1-2] : 

if "%pildepr%"=="1" goto RunDeprecatedFix
if "%pildepr%"=="2" goto MainMenu

:RunDeprecatedFix
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



