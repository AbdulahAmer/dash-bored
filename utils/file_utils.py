import base64
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
EXAMPLE_DIR = DATA_DIR / "example"


def ensure_data_dirs_exist():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    EXAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_filename(filename: str) -> str:
    cleaned = filename.replace(" ", "_")
    return "".join(char for char in cleaned if char.isalnum() or char in {"_", "."})


def save_uploaded_file(contents: str, filename: str) -> str:
    ensure_data_dirs_exist()
    if "," not in contents:
        raise ValueError("Invalid upload contents")
    header, encoded = contents.split(",", 1)
    data = base64.b64decode(encoded)
    sanitized = _sanitize_filename(filename)
    save_path = UPLOADS_DIR / sanitized
    with open(save_path, "wb") as f:
        f.write(data)
    relative_value = f"uploads/{sanitized}"
    return relative_value


def list_available_datasets():
    ensure_data_dirs_exist()
    options = []
    example_file = EXAMPLE_DIR / "example_sales.csv"
    if example_file.exists():
        options.append({
            "label": "Example: Example Sales Data",
            "value": "example_sales.csv",
        })

    for file in sorted(UPLOADS_DIR.iterdir()):
        if file.is_file() and file.suffix.lower() in {".csv", ".xlsx"}:
            options.append({
                "label": f"Uploaded: {file.name}",
                "value": f"uploads/{file.name}",
            })
    return options
