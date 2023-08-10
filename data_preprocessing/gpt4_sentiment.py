import requests
import os
import pandas as pd
from datetime import datetime

# Constants
INPUT_DIRECTORY = "sentiment_data/"
OUTPUT_DIRECTORY = "gpt4_processed_sentiment_data/"
GPT4_API_ENDPOINT = "YOUR_GPT4_API_ENDPOINT"
API_KEY = os.environ.get("GPT4_API_KEY")

def load_sentiment_data(symbol, directory=INPUT_DIRECTORY):
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_sentiment_{date_str}.csv"
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No sentiment data file found for symbol {symbol} on {date_str}")

    return pd.read_csv(filename, index_col=0, parse_dates=True)

def get_sentiment_from_gpt4(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Multiple prompts for better accuracy
    prompts = [
        f"Rate the sentiment of the following text from -1 (very negative) to 1 (very positive): '{text}'",
        f"Analyze the sentiment of this statement: '{text}'. Provide a score between -1 (negative) and 1 (positive).",
        f"How positive or negative is the following statement? '{text}' (Answer with a value between -1 and 1)"
    ]

    scores = []
    for prompt in prompts:
        payload = {
            "prompt": prompt,
            "max_tokens": 50
        }

        response = requests.post(GPT4_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        
        try:
            # Extract the sentiment score from the response and convert to a float
            score = float(response.json()["choices"][0]["text"].strip())
            scores.append(score)
        except ValueError:
            continue

    # Return the average sentiment score from multiple prompts
    return sum(scores) / len(scores) if scores else 0

def preprocess_sentiment_with_gpt4(df):
    df['gpt4_sentiment'] = df['text'].apply(get_sentiment_from_gpt4)
    return df

def save_processed_sentiment_data(df, symbol, directory=OUTPUT_DIRECTORY):
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_gpt4_sentiment_{date_str}.csv"
    
    os.makedirs(directory, exist_ok=True)
    df.to_csv(filename)

if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        try:
            df = load_sentiment_data(symbol)
            df_processed = preprocess_sentiment_with_gpt4(df)
            save_processed_sentiment_data(df_processed, symbol)
            print(f"GPT-4 sentiment data for {symbol} processed and saved successfully!")
        except Exception as e:
            print(f"Error processing GPT-4 sentiment data for {symbol}. Error: {e}")
