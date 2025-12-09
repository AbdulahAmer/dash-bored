#!/usr/bin/env bash
set -e

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is required to run this project." >&2
  exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting Dash app and opening http://127.0.0.1:8050 ..."
python -m webbrowser http://127.0.0.1:8050 >/dev/null 2>&1 &
python app.py
