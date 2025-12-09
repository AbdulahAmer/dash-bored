from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_dataset(dataset_value: str) -> pd.DataFrame:
    if not dataset_value:
        return pd.DataFrame()
    if dataset_value.startswith("uploads/"):
        dataset_path = DATA_DIR / dataset_value
    else:
        dataset_path = DATA_DIR / "example" / dataset_value

    if not dataset_path.exists():
        return pd.DataFrame()

    if dataset_path.suffix.lower() == ".csv":
        return pd.read_csv(dataset_path)
    if dataset_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(dataset_path)
    return pd.DataFrame()


def detect_numeric_columns(df: pd.DataFrame) -> list:
    numeric_df = df.select_dtypes(include="number")
    return list(numeric_df.columns)


def build_summary(df: pd.DataFrame) -> dict:
    summary = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "columns": list(df.columns),
        "numeric_summary": {},
    }
    if not df.empty:
        numeric_cols = detect_numeric_columns(df)
        if numeric_cols:
            numeric_stats = df[numeric_cols].agg(["mean", "min", "max"]).round(2)
            summary["numeric_summary"] = numeric_stats.to_dict()
    return summary
