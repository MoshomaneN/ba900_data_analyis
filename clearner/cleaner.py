import pandas as pd
import re

def clean_and_categorize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    drop_cols = ['date,august', '2025']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    df = df.rename(columns={'date': 'line_description', 'august_2025': 'amount'})
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

    # CIB categories
    category_map = {
        'corporate_loan': ['loan', 'advance', 'corporate'],
        'corporate_deposit': ['deposit', 'corporate'],
        'fca': ['foreign_currency_asset', 'fca'],
        'cfc': ['foreign_currency_commitment', 'cfc']
    }
    df['cib_category'] = None
    for category, keywords in category_map.items():
        mask = df['line_description'].astype(str).str.lower().str.contains('|'.join(keywords))
        df.loc[mask, 'cib_category'] = category
    df = df[df['cib_category'].notnull()]

    # Major banks
    bank_map = {
        'standard bank': 'STANDARD BANK',
        'nedbank': 'NEDBANK',
        'absa': 'ABSA',
        'first rand': 'FIRST RAND'
    }
    df['institution'] = None
    for k, v in bank_map.items():
        mask = df['line_description'].str.lower().str.contains(k)
        df.loc[mask, 'institution'] = v
    df = df[df['institution'].notnull()]

    # Report date
    def extract_date(file_name):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', file_name)
        return pd.to_datetime(match.group(1)) if match else pd.NaT
    df['report_date'] = df['source_file'].apply(extract_date)

    # Transaction type
    transactional_keywords = ['loan', 'advance', 'deposit', 'transfer', 'fca', 'cfc']
    non_transactional_keywords = ['investment', 'securities', 'bond', 'derivative', 'provision', 'reserve']

    def classify_transactional(line_desc: str):
        line = str(line_desc).lower()
        if any(k in line for k in transactional_keywords):
            return 'transactional'
        elif any(k in line for k in non_transactional_keywords):
            return 'non_transactional'
        else:
            return 'unknown'

    df['transaction_type'] = df['line_description'].apply(classify_transactional)
    df = df[df['transaction_type'] != 'unknown']

    print(f"✅ Cleaned DataFrame: {len(df)} rows for major SA banks with transaction type")
    return df
