@echo off
setlocal enabledelayedexpansion

:: Check for Python 3.13

:: Set the default Python path
set "PYTHONPATH=%userprofile%\AppData\Local\Programs\Python\Python313\python.exe"

:: Check if the default Python executable exists
if exist "%PYTHONPATH%" (
    :: Extract version from python --version
    for /f "tokens=2 delims= " %%a in ('"%PYTHONPATH%" --version 2^>^&1') do (
        set "PYTHONVERSION=%%a"
    )
    :: Check if verison is correct
    if "!PYTHONVERSION:~0,4!"=="3.13" (
        goto :found
    )
)

:: Try every Python executable in PATH
for /f "delims=" %%p in ('where python') do (
    :: Extract version from python --version
    for /f "tokens=2 delims= " %%a in ('"%%p" --version 2^>^&1') do (
        set "PYTHONVERSION=%%a"
    )
    :: Check if verison is correct
    if "!PYTHONVERSION:~0,4!"=="3.13" (
        set "PYTHONPATH=%%p"
        goto :found
    )
)

echo Python 3.13 not found
set /p "PYTHONPATH=Please enter the correct Python path: "

:: Check if the Python executable exists
if exist "%PYTHONPATH%" (
    :: Extract version from python --version
    for /f "tokens=2 delims= " %%a in ('"%PYTHONPATH%" --version 2^>^&1') do (
        set "PYTHONVERSION=%%a"
    )
    :: Check if verison is correct
    if "!PYTHONVERSION:~0,4!"=="3.13" (
        goto :found
    ) else (
        echo %PYTHONPATH% has version !PYTHONVERSION!
    )
) else (
    echo %PYTHONPATH% not found
)

:: Exit if Python not found
pause
exit /b 1

:: Continue if Python found
:found
echo Running Python from: %PYTHONPATH%
"%PYTHONPATH%" --version

:: Create a virtual environment
echo Creating virtual environment
"%PYTHONPATH%" -m venv .venv
call .venv\Scripts\activate

:: Install Python dependencies
echo Installing Python dependencies
pip install -r requirements.txt

:: Install Llama model
echo Installing Llama model
ollama pull llama3.1:8b

:: Install Node.js dependencies
echo Installing Node.js dependencies
pushd frontend
call npm install
popd

:: Generate config file
echo Generating config file
copy example.env .env
python config.py

echo Start the application with start.bat
pause
