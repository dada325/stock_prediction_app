import pandas as pd
import os
from datetime import datetime
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Constants
INPUT_DIRECTORY = "sentiment_data/"
OUTPUT_DIRECTORY = "processed_sentiment_data/"

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def load_sentiment_data(symbol, directory=INPUT_DIRECTORY):
    """
    Load the sentiment data for a given symbol from the CSV file.

    Parameters:
    - symbol (str): The stock symbol.
    - directory (str): The directory where the sentiment data is stored.

    Returns:
    - pd.DataFrame: A DataFrame containing the sentiment data.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_sentiment_{date_str}.csv"
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No sentiment data file found for symbol {symbol} on {date_str}")

    return pd.read_csv(filename, index_col=0, parse_dates=True)

def preprocess_sentiment_data(df):
    """
    Preprocess the sentiment data.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing raw sentiment data.

    Returns:
    - pd.DataFrame: A DataFrame containing the preprocessed sentiment data.
    """
    # Lowercase all text data
    df['text'] = df['text'].str.lower()

    # Remove URLs, numbers, special characters
    df['text'] = df['text'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+', '', x, flags=re.MULTILINE))
    df['text'] = df['text'].apply(lambda x: re.sub(r'\@\w+|\#', '', x))
    df['text'] = df['text'].apply(lambda x: re.sub(r'\d+', '', x))
    df['text'] = df['text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

    # Tokenization, stopwords removal, and lemmatization
    df['text'] = df['text'].apply(lambda x: word_tokenize(x))
    df['text'] = df['text'].apply(lambda x: [word for word in x if word not in stop_words])
    df['text'] = df['text'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
    df['text'] = df['text'].apply(lambda x: ' '.join(x))

    return df

def save_processed_sentiment_data(df, symbol, directory=OUTPUT_DIRECTORY):
    """
    Save the preprocessed sentiment data to a new CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing preprocessed sentiment data.
    - symbol (str): The stock symbol.
    - directory (str): The directory to save the processed sentiment data in.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{directory}{symbol}_sentiment_processed_{date_str}.csv"
    
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    df.to_csv(filename)

if __name__ == "__main__":
    # Ensure you've downloaded the necessary NLTK data first:
    # import nltk
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('stopwords')

    symbols = ["AAPL", "MSFT", "GOOGL"]  # You can expand this list

    for symbol in symbols:
        try:
            df = load_sentiment_data(symbol)
            df_processed = preprocess_sentiment_data(df)
            save_processed_sentiment_data(df_processed, symbol)
            print(f"Sentiment data for {symbol} preprocessed and saved successfully!")
        except Exception as e:
            print(f"Error preprocessing sentiment data for {symbol}. Error: {e}")
