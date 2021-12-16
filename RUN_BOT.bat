@ECHO OFF
ECHO "Starting bot"
start cmd /c "venv\Scripts\pip.exe install -r requirements.txt && venv\Scripts\python.exe main.py"