%userprofile%\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd frontend && npm install && cd ..
copy example.env .env
python config.py
