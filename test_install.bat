@echo off
setlocal enabledelayedexpansion
title PRISM.CC AUTO-INSTALLER
color 0A

:: 1. Check for Python and Install if Missing
echo [!] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [?] Python is not installed. Preparing auto-installer...
    
    :: Updated to download the Python 3.13 installer
    set "PY_URL=https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe"
    set "PY_EXE=%TEMP%\python_installer.exe"
    
    echo [!] Downloading Python 3.13 from official server...
    curl -L -o "!PY_EXE!" "!PY_URL!"
    
    if exist "!PY_EXE!" (
        echo [!] Installing Python 3.13 silently... Please wait a few moments.
        :: Install for all users, prepend to system variables, disable test suite
        start /wait "" "!PY_EXE!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del "!PY_EXE!"
        
        :: Refresh path environment variables specifically targeting the Python 313 folders
        echo [!] Refreshing environment variables...
        set "PATH=%PATH%;%ProgramFiles%\Python313;%ProgramFiles%\Python313\Scripts"
        
        :: Double check installation status
        python --version >nul 2>&1
        if !errorlevel! neq 0 (
            echo [X] Python installation failed or requires a manual system restart.
            pause
            exit /b
        ) else (
            echo [+] Python 3.13 installed successfully.
        )
    ) else (
        echo [X] Failed to download the Python installer.
        pause
        exit /b
    )
) else (
    echo [+] Python is already installed.
)

:: 2. Setup Folders
set "URL=https://github.com/tallywker990w/prism.cc/archive/refs/heads/main.zip"
set "ZIP_NAME=prism_files.zip"
set "EXTRACT_DIR=%USERPROFILE%\Downloads\PRISM_CC"

echo [!] Creating Directory: %EXTRACT_DIR%
if not exist "%EXTRACT_DIR%" mkdir "%EXTRACT_DIR%"
cd /d "%EXTRACT_DIR%"

:: 3. Download the ZIP
echo [!] Downloading PRISM from GitHub...
curl -L -o %ZIP_NAME% %URL%

:: 4. Extract the ZIP using PowerShell
echo [!] Extracting files...
powershell -Command "Expand-Archive -Path '%EXTRACT_DIR%\%ZIP_NAME%' -DestinationPath '%EXTRACT_DIR%' -Force"

:: 5. Navigate into the extracted folder
cd prism.cc-main

:: 6. Install Requirements
echo [!] Installing Requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else if exist "requirments" (
    pip install -r requirments
) else (
    echo [?] No requirements file found, skipping.
)

:: 7. Launch Prism
echo [!] Launching PRISM...
start "" python main.py

echo [+] Setup Complete! You can find your files in %EXTRACT_DIR%
pause
