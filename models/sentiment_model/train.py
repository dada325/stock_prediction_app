import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Constants
DATA_DIRECTORY = "gpt4_processed_sentiment_data/"
MODEL_DIRECTORY = "models/sentiment_model/"
MAX_NUM_WORDS = 10000
MAX_SEQUENCE_LENGTH = 250

# Load data
def load_sentiment_data(symbol, directory=DATA_DIRECTORY):
    filename = f"{directory}{symbol}_gpt4_sentiment.csv"
    return pd.read_csv(filename, index_col=0, parse_dates=True)

# Preprocess data for LSTM
def preprocess_for_lstm(df):
    # Tokenize and pad sequences
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(df['text'])
    sequences = tokenizer.texts_to_sequences(df['text'])
    word_index = tokenizer.word_index
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    
    # Encode labels
    encoder = LabelEncoder()
    labels = encoder.fit_transform(df['gpt4_sentiment'])
    
    return data, labels, tokenizer, encoder

# LSTM model definition
def create_lstm_sentiment_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=MAX_NUM_WORDS, output_dim=128, input_length=input_shape[0]),
        tf.keras.layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    symbol = "AAPL"

    df = load_sentiment_data(symbol)
    data, labels, tokenizer, encoder = preprocess_for_lstm(df)

    # Train-validation split
    x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, shuffle=True)

    model = create_lstm_sentiment_model(x_train.shape[1:])
    model.fit(x_train, y_train, epochs=5, batch_size=32, validation_data=(x_val, y_val))

    # Save model, tokenizer, and encoder
    model.save(f"{MODEL_DIRECTORY}{symbol}_sentiment_lstm.h5")
    with open(f"{MODEL_DIRECTORY}{symbol}_tokenizer.pkl", 'wb') as f:
        import pickle
        pickle.dump(tokenizer, f)
    with open(f"{MODEL_DIRECTORY}{symbol}_encoder.pkl", 'wb') as f:
        pickle.dump(encoder, f)

    print(f"Sentiment model for {symbol} trained and saved successfully!")
