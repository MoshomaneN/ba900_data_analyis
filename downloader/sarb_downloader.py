import os
import requests
from datetime import datetime
from pathlib import Path

BASE_URL = "https://www.resbank.co.za/en/home/what-we-do/statistics/ba-returns/ba900"

def download_ba900_data(start_year=2024, start_month=12, end_year=2025, end_month=9, save_dir="data/raw"):
    os.makedirs(save_dir, exist_ok=True)

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                continue

            month_name = datetime(year, month, 1).strftime("%B")
            file_name = f"BA900_{year}_{month:02d}.xlsx"
            file_path = Path(save_dir) / file_name

            possible_names = [
                f"BA900-{month_name}-{year}.xlsx",
                f"BA900 {month_name} {year}.xlsx",
                f"BA900 Return - {month_name} {year}.xlsx",
                f"BA900-{month_name[:3]}-{year}.xlsx"
            ]

            success = False
            for name in possible_names:
                url = f"{BASE_URL}/{name}"
                print(f"Trying {url}...")
                response = requests.get(url)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Downloaded and saved: {file_path}")
                    success = True
                    break
                else:
                    print(f"❌ {url} not found ({response.status_code})")

            if not success:
                print(f"⚠️ Could not find BA900 file for {month_name} {year}.")


