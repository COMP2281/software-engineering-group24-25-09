:: install llama model
ollama pull llama3.1:8b

:: check for python 3.13
:: Set the default Python path
set "PYTHONPATH=%userprofile%\AppData\Local\Programs\Python\Python313\python.exe"

:: Check if the default Python executable exists
if not exist "%PYTHONPATH%" (
    echo Default Python not found at: %PYTHONPATH%
    set /p "PYTHONPATH=Please enter the correct Python path: "
)

:: Use the Python path to run a command, for example, display the version
echo Running Python from: %PYTHONPATH%
"%PYTHONPATH%" --version

pause

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
