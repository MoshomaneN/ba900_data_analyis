import zipfile
from pathlib import Path

def extract_all_zips(zip_folder: str, target_folder: str) -> list:
    """
    Extracts all ZIP files in a folder to the target folder.

    Args:
        zip_folder (str): Path containing ZIP files.
        target_folder (str): Path to extract CSVs into.

    Returns:
        List[str]: List of extracted CSV file paths.
    """
    zip_folder = Path(zip_folder)
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    extracted_files = []

    for zip_path in zip_folder.glob("*.zip"):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract all CSVs
                for file_name in zip_ref.namelist():
                    if file_name.lower().endswith(".csv"):
                        extracted_path = target_folder / Path(file_name).name
                        with zip_ref.open(file_name) as source, open(extracted_path, "wb") as target:
                            target.write(source.read())
                        extracted_files.append(str(extracted_path))
                        print(f"✅ Extracted {file_name} from {zip_path.name}")
        except zipfile.BadZipFile:
            print(f"⚠️ Skipping bad ZIP file: {zip_path.name}")

    if not extracted_files:
        print("⚠️ No CSV files were extracted.")

    return extracted_files


if __name__ == "__main__":
    # Example usage
    extracted_csvs = extract_all_zips("data/zipped", "data/extracted")
    print("\n✅ Extraction complete! Total CSVs extracted:", len(extracted_csvs))
