import matplotlib.pyplot as plt
import seaborn as sns

def plot_market_share_trends(df):
    sns.set(style="whitegrid")
    categories = df['cib_category'].unique()
    for category in categories:
        for txn_type in df['transaction_type'].unique():
            cat_df = df[(df['cib_category']==category) & (df['transaction_type']==txn_type)]
            plt.figure(figsize=(10,6))
            sns.lineplot(data=cat_df, x='report_date', y='market_share_pct', hue='institution', marker='o')
            plt.title(f"Market Share Trend - {category.upper()} ({txn_type})")
            plt.ylabel("Market Share (%)")
            plt.xlabel("Report Date")
            plt.ylim(0,100)
            plt.legend(title="Institution")
            plt.tight_layout()
            plt.show()

def plot_stacked_market_share(df):
    categories = df['cib_category'].unique()
    txn_types = df['transaction_type'].unique()
    for category in categories:
        for txn_type in txn_types:
            cat_df = df[(df['cib_category']==category) & (df['transaction_type']==txn_type)].copy()
            pivot_df = cat_df.pivot_table(index='report_date', columns='institution', values='market_share_pct', fill_value=0)
            pivot_df = pivot_df[['STANDARD BANK', 'NEDBANK', 'ABSA', 'FIRST RAND']]
            pivot_df.plot(kind='bar', stacked=True, figsize=(12,6), colormap='tab20')
            plt.title(f"Stacked Market Share - {category.upper()} ({txn_type})")
            plt.ylabel("Market Share (%)")
            plt.xlabel("Report Date")
            plt.ylim(0,100)
            plt.legend(title="Institution", bbox_to_anchor=(1.05,1), loc='upper left')
            plt.tight_layout()
            plt.show()
