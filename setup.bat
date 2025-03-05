:: install llama model
ollama pull llama3.1:8b

:: check for python 3.13
:: Set the default Python path
set "PYTHONPATH=%userprofile%\AppData\Local\Programs\Python\Python313\python.exe"

:: Check if Python is available in the PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH.
    echo Using default Python: %PYTHONPATH%
) else (
    :: Python is found; get its version
    for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%a"

    :: Check if the version starts with "3.13"
    echo %PYTHON_VERSION% | findstr /b "3.13" >nul
    if %errorlevel% equ 0 (
        :: Python version is 3.13, so update PYTHONPATH using the path from PATH
        for /f "delims=" %%p in ('where python') do (
            set "PYTHONPATH=%%p"
            goto :updateDone
        )
        :updateDone
        echo Python version is 3.13.
        echo Using Python from PATH: %PYTHONPATH%
    ) else (
        echo Python in PATH is not 3.13 (found version: %PYTHON_VERSION%).
        echo Using default Python: %PYTHONPATH%
    )
)

:: Run further commands using the determined PYTHONPATH
echo Running Python: %PYTHONPATH% --version
"%PYTHONPATH%" --version

%userprofile%\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
pushd frontend
call npm install
popd
copy example.env .env
python config.py
echo Start the application with start.bat
pause
