@echo off
rem Construit l'exécutable (PyInstaller) puis l'installateur (Inno Setup)
setlocal
cd /d "%~dp0"

.venv\Scripts\python.exe -m pip install -q -r requirements.txt pyinstaller || exit /b 1

.venv\Scripts\python.exe -m PyInstaller --noconfirm --name VidDrop --onedir --console ^
  --add-data "../app.py;." ^
  --collect-all streamlit --copy-metadata streamlit ^
  --collect-all yt_dlp --collect-all yt_dlp_ejs ^
  --distpath build/dist --workpath build/work --specpath build ^
  launcher.py || exit /b 1

set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
"%ISCC%" installer\VidDrop.iss || exit /b 1

echo.
echo Installateur pret : build\installer\
