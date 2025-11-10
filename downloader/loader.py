import pandas as pd
from pathlib import Path

def load_ba900_csv(file_path: str) -> pd.DataFrame:
    """
    Load and parse a single unstructured BA900 CSV file.

    Handles:
        - Unknown encoding (tries utf-8 then latin1)
        - Skips initial metadata rows
        - Adds institution, date, and source_file columns

    Args:
        file_path (str): Path to a single BA900 CSV file.

    Returns:
        pd.DataFrame: Parsed DataFrame with metadata.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read all lines to find the table header
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Find header line that starts with "Description"
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("description"):
            header_index = i
            break

    if header_index is None:
        raise ValueError(f"No 'Description' header found in {file_path}")

    # Attempt reading CSV with utf-8, fallback to latin1
    try:
        df = pd.read_csv(file_path, skiprows=header_index, encoding="utf-8")
    except UnicodeDecodeError:
        print(f"⚠️ UTF-8 failed for {file_path}, trying latin1...")
        df = pd.read_csv(file_path, skiprows=header_index, encoding="latin1")

    # Add source file name
    df["source_file"] = file_path.name

    # Extract institution and date from lines above header
    institution, date = None, None
    for line in lines[:header_index]:
        lower_line = line.lower()
        if lower_line.startswith("institution"):
            institution = line.split(",")[1].strip()
        elif lower_line.startswith("date"):
            date = line.split(",")[1].strip()

    df["institution"] = institution
    df["date"] = date

    return df
