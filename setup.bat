@echo off
setlocal

python -m venv venv
if errorlevel 1 (
  echo Failed to create virtual environment.
  exit /b 1
)

call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

python app.py
