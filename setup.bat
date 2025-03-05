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
