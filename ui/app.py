import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Constants
MODEL_DIRECTORY = "models/"
MAX_SEQUENCE_LENGTH = 250
LOOKBACK_WINDOW = 60

# Load models and utilities
@st.cache(allow_output_mutation=True)
def load_models(symbol):
    time_series_model = tf.keras.models.load_model(f"{MODEL_DIRECTORY}time_series_model/{symbol}_lstm.h5")
    sentiment_model = tf.keras.models.load_model(f"{MODEL_DIRECTORY}sentiment_model/{symbol}_sentiment_lstm.h5")

    with open(f"{MODEL_DIRECTORY}sentiment_model/{symbol}_tokenizer.pkl", 'rb') as f:
        tokenizer = pickle.load(f)
    with open(f"{MODEL_DIRECTORY}sentiment_model/{symbol}_encoder.pkl", 'rb') as f:
        encoder = pickle.load(f)

    return time_series_model, sentiment_model, tokenizer, encoder

# Main Streamlit App
def main():
    st.title("Stock Forecast & Sentiment Analysis App")
    
    # Symbol selection
    symbol = st.selectbox("Select Stock Symbol", ["AAPL", "MSFT", "GOOGL"])
    time_series_model, sentiment_model, tokenizer, encoder = load_models(symbol)

    # Time Series Prediction
    st.header("Stock Price Forecast")
    st.write(f"Predicting the stock price for {symbol} for the next day.")
    
    # Here, you would ideally fetch the last 60 days of data for the selected stock to make a prediction
    # For demonstration purposes, let's assume we have a numpy array 'last_60_days_data' representing this
    # last_60_days_data = np.array([...])

    # prediction = time_series_model.predict(last_60_days_data.reshape(1, LOOKBACK_WINDOW, 1))
    # st.write(f"Predicted stock price for the next day: ${prediction[0][0]:.2f}")

    # Sentiment Analysis
    st.header("Sentiment Analysis")
    user_input_text = st.text_area("Paste a news article or social media post about the stock:")
    
    if st.button("Analyze Sentiment"):
        # Preprocess the text
        sequences = tokenizer.texts_to_sequences([user_input_text])
        data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
        
        # Predict sentiment
        sentiment_score = sentiment_model.predict(data)[0][0]
        sentiment_label = encoder.inverse_transform([int(sentiment_score > 0.5)])
        st.write(f"Sentiment: {sentiment_label[0]} (Score: {sentiment_score:.2f})")

if __name__ == "__main__":
    main()
