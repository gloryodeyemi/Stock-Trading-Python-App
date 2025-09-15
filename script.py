import requests
import openai
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key from the environment variables
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
STOCK_API_URL = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# Get the first page of tickers
response = requests.get(STOCK_API_URL)
data = response.json()
tickers = []

# Add the first page of tickers to the list
for ticker in data['results']:
    tickers.append(ticker)

# Get the next page of tickers
while 'next_url' in data:
    print("Requesting next page: ", data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    print(data)
    try:
        for ticker in data['results']:
            tickers.append(ticker)
    except KeyError:
        print("No results found")
        break

example_ticker = {'ticker': 'HUBC', 'name': 'Hub Cyber Security Ltd. Ordinary Shares', 'market': 'stocks', 'locale': 'us', 'primary_exchange': 'XNAS', 'type': 'CS', 'active': True, 'currency_name': 'usd', 'cik': '0001905660', 'last_updated_utc': '2025-09-15T06:04:58.615265371Z'}

# Write results to CSV with the same schema as example_ticker
schema_columns = list(example_ticker.keys())

# Create DataFrame from collected tickers
df = pd.DataFrame(tickers)

# Ensure all schema columns exist; add missing ones as None
for col in schema_columns:
    if col not in df.columns:
        df[col] = None

# Keep only schema columns and order them
df = df[schema_columns]

output_path = os.path.join(os.getcwd(), 'tickers.csv')
df.to_csv(output_path, index=False)
print(f"Wrote {len(df)} rows to {output_path}")
