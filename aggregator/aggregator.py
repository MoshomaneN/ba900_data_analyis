import pandas as pd

def aggregate_market_share(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby(['report_date', 'cib_category', 'institution', 'transaction_type'])['amount'].sum().reset_index()
    totals = agg.groupby(['report_date', 'cib_category', 'transaction_type'])['amount'].sum().reset_index().rename(columns={'amount':'total_amount'})
    agg = pd.merge(agg, totals, on=['report_date', 'cib_category', 'transaction_type'])
    agg['market_share_pct'] = (agg['amount'] / agg['total_amount']) * 100
    return agg
