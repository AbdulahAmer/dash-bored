# DASH-BORED

A beginner-friendly Dash dashboard that lets you drag and drop CSV/Excel files, preview the data, view quick summary stats, and make simple charts. An example dataset is included so you can explore right away.

## Quick Start

### Prerequisites
- Python 3.10 or newer

### Run on macOS/Linux
```bash
./setup.sh
```
This script creates a virtual environment, installs dependencies, and starts the app at http://127.0.0.1:8050.

### Run on Windows
```bat
setup.bat
```

### Manual Steps
If you prefer manual setup:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Using the App
1. Open http://127.0.0.1:8050 in your browser.
2. Drag and drop a `.csv` or `.xlsx` file onto the upload area. The file is saved under `data/uploads/` and becomes selectable in the dataset dropdown.
3. Switch between **Table**, **Summary**, and **Chart** views.
4. Pick chart type (Histogram, Bar, Scatter) and choose X/Y axes.
5. Toggle **Light/Dark** theme to adjust styling.
6. Visit http://127.0.0.1:8050/example to load the built-in `example_sales.csv` dataset and use the same controls.

## Project Structure
```
app.py                 # Dash entry point and callbacks
requirements.txt       # Python dependencies
setup.sh / setup.bat   # One-command setup scripts
data/
  uploads/             # Saved user uploads
  example/example_sales.csv
layouts/               # Page layout factories
components/            # Reusable UI and graph builders
utils/                 # File handling and data loading helpers
assets/custom.css      # Styling and theme definitions
```

## Deployment Note
For simple hosting, install dependencies and run `gunicorn app:server --bind 0.0.0.0:8050`.
