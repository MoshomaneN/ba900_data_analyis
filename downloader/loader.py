import pandas as pd
from pathlib import Path

def load_ba900_csv(file_path: str) -> pd.DataFrame:
    """
    Load and parse an unstructured BA900 CSV file.
    Detects the header automatically and adds a 'source_file' column.
    """
    # Read the file as text and find where the actual data starts
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the line that starts with 'Description' (table header)
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("description"):
            header_index = i
            break

    if header_index is None:
        raise ValueError(f"No 'Description' header found in {file_path}")

    # Read from that line onwards as CSV
    df = pd.read_csv(file_path, skiprows=header_index)
    
    # Add file metadata
    df["source_file"] = Path(file_path).name

    # Extract bank name and date from the first few lines (above header)
    header_info = lines[:header_index]
    institution = None
    date = None

    for line in header_info:
        if line.lower().startswith("institution"):
            institution = line.split(",")[1].strip()
        if line.lower().startswith("date"):
            date = line.split(",")[1].strip()

    df["institution"] = institution
    df["date"] = date

    return df


def load_all_ba900_files(folder_path: str) -> pd.DataFrame:
    """
    Loads and combines all BA900 CSVs from a folder.
    Filters to include only the four major banks.
    """
    folder = Path(folder_path)
    all_files = list(folder.glob("*.csv"))

    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    frames = []
    for file in all_files:
        try:
            df = load_ba900_csv(file)
            frames.append(df)
            print(f"✅ Loaded {file.name}")
        except Exception as e:
            print(f"⚠️ Skipping {file.name} due to error: {e}")

    combined = pd.concat(frames, ignore_index=True)

    # Filter to include only the four big banks
    #major_banks = ["STANDARD BANK", "NEDBANK", "ABSA", "FIRST RAND"]
    #combined = combined[combined["institution"].str.upper().isin(major_banks)]


    return combined

combined_df = load_all_ba900_files("data/extracted")

# Save as CSV
combined_df.to_csv("data/BA900_combined_clean.csv", index=False, encoding="utf-8")
print("✅ Combined BA900 dataset saved as CSV: data/BA900_combined_clean.csv")







