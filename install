@echo off
setlocal
title PRISM.CC AUTO-INSTALLER
color 0A

:: 1. Setup Folders
set "URL=https://github.com/tallywker990w/prism.cc/archive/refs/heads/main.zip"
set "ZIP_NAME=prism_files.zip"
set "EXTRACT_DIR=%USERPROFILE%\Downloads\PRISM_CC"

echo [!] Creating Directory: %EXTRACT_DIR%
if not exist "%EXTRACT_DIR%" mkdir "%EXTRACT_DIR%"
cd /d "%EXTRACT_DIR%"

:: 2. Download the ZIP
echo [!] Downloading PRISM from GitHub...
curl -L -o %ZIP_NAME% %URL%

:: 3. Extract the ZIP using PowerShell
echo [!] Extracting files...
powershell -Command "Expand-Archive -Path '%EXTRACT_DIR%\%ZIP_NAME%' -DestinationPath '%EXTRACT_DIR%' -Force"

:: 4. Navigate into the extracted folder (GitHub adds "-main" to the folder name)
cd prism.cc-main

:: 5. Install Requirements
echo [!] Installing Requirements (req.txt)...
if exist "requirments" (
    pip install -r requirments
) else if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [?] No requirements file found, skipping.
)

:: 6. Launch Prism
echo [!] Launching PRISM...
start "" python main.py

echo [+] Setup Complete! You can find your files in %EXTRACT_DIR%
pause
