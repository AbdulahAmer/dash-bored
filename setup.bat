@echo off

python --version >NUL 2>&1
if errorlevel 1 (
    echo Python is required to run this project.
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

call venv\Scripts\activate

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo Starting Dash app and opening http://127.0.0.1:8050 ...
start "" http://127.0.0.1:8050
python app.py
