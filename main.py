from downloader.extractor import extract_ba900_zip
from downloader.loader import load_ba900_csvs
from cleaner.cleaner import clean_and_categorize
from aggregator.aggregator import aggregate_market_share
from visualizer.plotter import plot_market_share_trends, plot_stacked_market_share

zip_path = "data/raw/BA900_2025-08-01_zipcsv.zip"

# Step 1 & 2
extract_ba900_zip(zip_path)
df = load_ba900_csvs("data/extracted")

# Step 3
cib_df = clean_and_categorize(df)

# Step 4
market_share_df = aggregate_market_share(cib_df)

# Step 5
plot_market_share_trends(market_share_df)
plot_stacked_market_share(market_share_df)






