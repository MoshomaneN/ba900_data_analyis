import zipfile
from pathlib import Path
import re

def extract_all_zips(zip_folder: str, target_folder: str) -> list:
    """
    Extract CSVs from all ZIP files and rename them to include the date from the ZIP name.
    Example output:  1223_2025_03_01.csv
    """

    zip_folder = Path(zip_folder)
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    extracted_files = []

    # Regex to extract YYYY-MM-DD from the zip filename
    date_pattern = re.compile(r"(\d{4})[-_](\d{2})[-_](\d{2})")

    for zip_path in zip_folder.glob("*.zip"):
        print(f"\n📦 Processing ZIP: {zip_path.name}")

        # Detect date from filename
        match = date_pattern.search(zip_path.name)
        if match:
            yyyy, mm, dd = match.groups()
            date_str = f"{yyyy}_{mm}_{dd}"
        else:
            print(f"⚠️ No date found in ZIP name → using NO_DATE")
            date_str = "NO_DATE"

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():

                    if file_name.lower().endswith(".csv"):
                        clean_name = Path(file_name).stem   # "1223"
                        suffix = Path(file_name).suffix     # ".csv"

                        # New filename: 1223_2025_03_01.csv
                        new_filename = f"{clean_name}_{date_str}{suffix}"
                        extracted_path = target_folder / new_filename

                        with zip_ref.open(file_name) as source, open(extracted_path, "wb") as target:
                            target.write(source.read())

                        extracted_files.append(str(extracted_path))
                        print(f"  ✓ Extracted → {new_filename}")

        except zipfile.BadZipFile:
            print(f"❌ Bad ZIP file, skipped: {zip_path.name}")

    if not extracted_files:
        print("⚠️ No CSV files were extracted from any ZIPs.")

    return extracted_files



if __name__ == "__main__":
    # Example usage
    extracted_csvs = extract_all_zips("data/zipped", "data/extracted")
    print("\n✅ Extraction complete! Total CSVs extracted:", len(extracted_csvs))
