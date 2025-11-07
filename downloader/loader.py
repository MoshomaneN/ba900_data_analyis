import pandas as pd
from pathlib import Path

def load_ba900_csvs(folder_path: str) -> pd.DataFrame:
    folder = Path(folder_path)
    csv_files = list(folder.glob("*.csv"))
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file, encoding='utf-8', dtype=str)
        df['source_file'] = file.name
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Combined DataFrame: {len(combined_df)} rows, {len(combined_df.columns)} columns")
    return combined_df

