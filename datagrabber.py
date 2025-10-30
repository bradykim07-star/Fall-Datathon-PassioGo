import json
import requests
import pandas as pd
from datetime import datetime

# Fetch bus ridership data from the API for a specific date
def api_fetch(api_url, date=None):
    """
    Fetches JSON data from the API.
    If a date is provided, it appends it as a query parameter.
    """
    if date:
        api_url = f"{api_url}?date={date}"
    print(f"Fetching {api_url}...")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        print("Fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {api_url}. Error: {e}")
        return None

# Convert JSON data to CSV
def ridership_to_csv(json_data, csv_file_name):
    if json_data is None:
        print("No data to save.")
        return

    rows = []
    for bus_id, time_data in json_data.items():
        for minute, ridership_count in time_data.items():
            rows.append([bus_id, minute, ridership_count])

    df = pd.DataFrame(rows, columns=['bus_id', 'time', 'ridership_count'])
    df['bus_id'] = pd.to_numeric(df['bus_id'])
    df['time'] = pd.to_numeric(df['time'])
    df['ridership_count'] = pd.to_numeric(df['ridership_count'])
    df = df.sort_values(by=['time']).reset_index(drop=True)

    df.to_csv(csv_file_name, index=False)
    print(f"Saved CSV as {csv_file_name}")
    print(df.head())

# -----------------------------
# USER SETTINGS
# -----------------------------
api_url = "https://demo.rubus.live/bus_ridership"
# Example: use "2025-10-15" for a past date, or None for today
#fetch_date = "2025-10-20"
fetch_date = "2025-10-4"

#grab feb 5 2025, feb 12 2025, feb 19 2025, feb 26 2025, mar 5 2025
#grab sep 3, sep 10, sep 17, sep 24, oct 1

# Create a safe filename
safe_date = fetch_date if fetch_date else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"ridership_{safe_date}.csv"

# Fetch and save
ridership_data = api_fetch(api_url, date=fetch_date)
ridership_to_csv(ridership_data, output_filename)
