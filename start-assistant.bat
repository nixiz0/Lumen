@echo off

REM Change to the directory where the script is located
cd /d %~dp0

echo Checking the Scoop Installation...
REM Check if Scoop is installed
where scoop >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Scoop is not installed. Installing Scoop...
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
    powershell -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')"
    
    REM Restart the terminal
    echo ---
    echo Please restart your .bat to continue the installation..
    pause
    exit
) ELSE (
    echo Scoop is already installed.
)

REM Check if ffmpeg is installed
scoop list | findstr /C:"ffmpeg" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ffmpeg is not installed. Installing ffmpeg...
    scoop install ffmpeg

    REM Restart the terminal
    echo ---
    echo => "Go in your OS and users (like C:\Users\)"
    echo => "Go on your_user_name\scoop\apps\ffmpeg\your_version_of_ffmpeg\bin"
    echo => "Copy the absolute path on the url on the top"
    echo => "Open your environnement variables"
    echo => "Go on 'PATH' in your user on your environnement variables"
    echo => "Click on 'new' button and paste the url that you copied"
    echo Now please restart your .bat to continue the installation..
    pause
    exit
) ELSE (
    echo ffmpeg is already installed.
)

REM Check if CUDA is installed
nvcc --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Restart the .bat when you will have installed your CUDA
    echo CUDA is not installed. Please download and install the CUDA 11.8 but check if this version is compatible with your GPU:
    echo https://developer.nvidia.com/cuda-11-8-0-download-archive
    pause
    exit
) ELSE (
    echo CUDA is installed.
    nvcc --version
    FOR /F "tokens=2 delims= " %%i IN ('nvcc --version ^| findstr /R /C:"release [0-9]\.[0-9]"') DO (
        SET CUDA_VERSION=cu%%i
        echo CUDA version detected: %CUDA_VERSION%
    )
)

REM Creation, installation & activation of local env
IF NOT EXIST .env (
    echo Creation of the environment...
    python -m venv .env
    cd .env\Scripts
    call activate.bat
    cd ../..
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install -r requirements.txt
) ELSE (
    echo Environnement activation...
    cd .env\Scripts
    call activate.bat
    cd ../..
)

FOR /F "tokens=*" %%A IN ('powershell -Command "Get-Command ollama"') DO SET OLLAMA_COMMAND=%%A
IF "%OLLAMA_COMMAND%"=="" (
    echo Ollama is not installed on your system.
    echo Please download it from https://ollama.com/download/windows
    pause
    exit
) ELSE (
    start cmd /k ollama serve
)

streamlit run menu.py