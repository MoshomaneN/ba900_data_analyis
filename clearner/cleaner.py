import pandas as pd

def clean_ba900(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and filters BA900 dataset for analysis.
    Focuses on CIB-related items (FCA, FEA, CFC, etc.)
    and ensures consistent column naming.

    Args:
        df (pd.DataFrame): Raw combined DataFrame.

    Returns:
        pd.DataFrame: Cleaned and filtered DataFrame.
    """

    # --- 1️⃣ Standardize column names ---
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # --- 2️⃣ Identify possible description column ---
    possible_desc_cols = ["description", "line_description", "item", "account_description", "line"]
    desc_col = next((col for col in possible_desc_cols if col in df.columns), None)

    if not desc_col:
        raise KeyError(f"No description column found. Checked: {possible_desc_cols}")

    # --- 3️⃣ Filter for CIB-related entries ---
    keywords = ["fca", "fea", "cfc", "corporate", "investment", "foreign currency"]
    mask = df[desc_col].astype(str).str.lower().str.contains("|".join(keywords))
    cib_df = df[mask].copy()

    # --- 4️⃣ Add Transactional Flag ---
    transactional_keywords = ["deposit", "loan", "transaction", "cash", "trade", "funds"]
    cib_df["is_transactional"] = cib_df[desc_col].astype(str).str.lower().str.contains("|".join(transactional_keywords))

    # --- 5️⃣ Add Metadata if Missing ---
    if "institution" not in cib_df.columns:
        cib_df["institution"] = "UNKNOWN"
    if "date" not in cib_df.columns:
        cib_df["date"] = pd.NaT

    # --- 6️⃣ Cleanup numeric columns ---
    for col in cib_df.select_dtypes(include=["object"]).columns:
        # Convert number-like columns safely
        cib_df[col] = cib_df[col].replace(",", "", regex=True)

    return cib_df
