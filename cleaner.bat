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
echo "Pilih 5 untuk menginstall Python"

echo:
set /p pil= Masukkan Pilihan Anda [1-5] : 

if "%pil%"=="1" goto RunStable
if "%pil%"=="2" goto RunCleaner
if "%pil%"=="3" goto RunDeprecated
if "%pil%"=="4" goto Exit
if "%pil%"=="5" goto Python
goto MainMenu

:RunStable
cls
call :CheckPython
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
call :CheckPython
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

:Exit
cls
echo "Terimakasih sudah menggunakan script ini"
pause
exit

:Python
cls
call :CheckPython
echo.
pause
goto MainMenu

:CheckPython
where python >nul 2>nul
if %errorlevel% equ 0 (
    goto :eof
)

echo Python tidak ditemukan.
call :InstallPython
goto :eof

:InstallPython
echo.
echo Mendeteksi arsitektur sistem...

if defined PROCESSOR_ARCHITEW6432 (
    set ARCH=64
) else (
    if /I "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set ARCH=64
    ) else (
        set ARCH=32
    )
)

if "%ARCH%"=="64" (
    set PYTHON_URL=https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe
    echo Sistem 64-bit terdeteksi.
) else (
    set PYTHON_URL=https://www.python.org/ftp/python/3.12.2/python-3.12.2.exe
    echo Sistem 32-bit terdeteksi.
)

set PYTHON_INSTALLER=%cd%\python_installer.exe

echo.
echo Mengunduh Python...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

if exist "%PYTHON_INSTALLER%" (
    echo.
    echo Menginstall Python secara silent...
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del "%PYTHON_INSTALLER%"
    set PATH=%PATH%;C:\Program Files\Python312\;C:\Program Files\Python312\Scripts\
    echo.
    echo Python berhasil diinstall.
    timeout /t 3 >nul
) else (
    echo Gagal mengunduh Python.
    pause
    exit
)

goto :eof
