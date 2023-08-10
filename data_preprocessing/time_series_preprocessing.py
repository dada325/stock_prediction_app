import pandas as pd
import os
from datetime import datetime

# Constants
INPUT_DIRECTORY = "data/"
OUTPUT_DIRECTORY = "processed_data/"

def load_data(symbol, directory=INPUT_DIRECTORY):
    """
    Load the stock data for a given symbol from the CSV file.

    Parameters:
    - symbol (str): The stock symbol.
    - directory (str): The directory where the data is stored.

    Returns:
    - pd.DataFrame: A DataFrame containing the stock data.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_{date_str}.csv"
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No data file found for symbol {symbol} on {date_str}")

    return pd.read_csv(filename, index_col=0, parse_dates=True)

def preprocess_data(df):
    """
    Preprocess the stock data.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing raw stock data.

    Returns:
    - pd.DataFrame: A DataFrame containing the preprocessed data.
    """
    # Convert columns to appropriate data types
    numeric_columns = ['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume', '8. split coefficient']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Calculate additional features like moving averages, RSI, etc.
    df['50_MA'] = df['4. close'].rolling(window=50).mean()
    df['200_MA'] = df['4. close'].rolling(window=200).mean()
    
    # Calculate daily returns
    df['daily_return'] = df['4. close'].pct_change()
    
    # Drop rows with NaN values (especially because of moving averages in the beginning)
    df.dropna(inplace=True)
    
    return df

def save_processed_data(df, symbol, directory=OUTPUT_DIRECTORY):
    """
    Save the preprocessed data to a new CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing preprocessed stock data.
    - symbol (str): The stock symbol.
    - directory (str): The directory to save the processed data in.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_processed_{date_str}.csv"
    
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    df.to_csv(filename)

if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL"]  # You can expand this list

    for symbol in symbols:
        try:
            df = load_data(symbol)
            df_processed = preprocess_data(df)
            save_processed_data(df_processed, symbol)
            print(f"Data for {symbol} preprocessed and saved successfully!")
        except Exception as e:
            print(f"Error preprocessing data for {symbol}. Error: {e}")
