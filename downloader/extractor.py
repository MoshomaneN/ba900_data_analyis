import zipfile
from pathlib import Path

def extract_ba900_zip(zip_path: str, extract_to: str = "data/extracted"):
    Path(extract_to).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    print(f"✅ Extracted CSVs to {extract_to}")


