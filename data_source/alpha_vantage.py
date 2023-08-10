import requests
import os
import json
import pandas as pd
from datetime import datetime

# Constants
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")  # Store your API key as an environment variable for security
FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"

# Ensure that you don't hard-code the API key directly in the script. Use environment variables or secret management tools.


def fetch_data(symbol, outputsize="compact"):
    """
    Fetch daily adjusted time series data for a given stock symbol from Alpha Vantage.

    Parameters:
    - symbol (str): The stock symbol to fetch data for.
    - outputsize (str): The size of the data ("compact" for latest 100 data points, "full" for up to 20 years data).

    Returns:
    - pd.DataFrame: A DataFrame containing the stock data.
    """
    params = {
        "function": FUNCTION,
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raise an error for failed requests

    data = response.json()
    daily_data = data.get("Time Series (Daily)")

    if not daily_data:
        raise ValueError(f"No data found for symbol {symbol}")

    df = pd.DataFrame.from_dict(daily_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return df


def save_to_csv(df, symbol, directory="data/"):
    """
    Save the fetched data to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing stock data.
    - symbol (str): The stock symbol.
    - directory (str): The directory to save the data in.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_{date_str}.csv"
    
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    df.to_csv(filename)


if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL"]  # You can expand this list

    for symbol in symbols:
        try:
            df = fetch_data(symbol)
            save_to_csv(df, symbol)
            print(f"Data for {symbol} fetched and saved successfully!")
        except Exception as e:
            print(f"Error fetching data for {symbol}. Error: {e}")
