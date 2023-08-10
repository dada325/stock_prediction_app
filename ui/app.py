import streamlit as st
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
from database_utils import get_db_session, query_data
from your_model_file import StockData  # replace `your_model_file` with the actual module name

# Constants
MODEL_NAME = 'bert-base-uncased'
MODEL_PATH_TIME_SERIES = 'models/transformer_time_series'
MODEL_PATH_SENTIMENT = 'models/transformer_sentiment'
MAX_LEN = 250

# Load the tokenizers and models
tokenizer_time_series = BertTokenizer.from_pretrained(MODEL_NAME)
tokenizer_sentiment = BertTokenizer.from_pretrained(MODEL_NAME)
model_time_series = TFBertForSequenceClassification.from_pretrained(MODEL_PATH_TIME_SERIES)
model_sentiment = TFBertForSequenceClassification.from_pretrained(MODEL_PATH_SENTIMENT)

# Streamlit UI
st.title("Stock Price Prediction App")

stock_code = st.text_input("Enter Stock Code or Name:")

if stock_code:
    # Query the database for stock data (assuming this is how you set it up)
    with get_db_session() as db:
        stock_data = query_data(db, StockData, StockData.symbol == stock_code)
        
    # Placeholder for data visualization if you need
    # st.write(stock_data)
    
    # Time Series Prediction with Transformer Model
    st.header("Stock Price Forecast with Transformer Model")
    user_input_text = st.text_area("Enter stock-related text (news articles, financial reports, etc.):")

    if st.button("Predict Stock Price with Transformer"):
        # Encoding
        encodings = tokenizer_time_series.encode_plus(user_input_text, add_special_tokens=True, max_length=MAX_LEN, 
                                                      return_token_type_ids=False, padding='max_length', 
                                                      return_attention_mask=True, return_tensors='tf')

        # Inference
        logits = model_time_series(encodings['input_ids'], attention_mask=encodings['attention_mask']).logits
        prediction = tf.nn.softmax(logits, axis=1)
        
        # Interpret the prediction (this depends on how your output is structured)
        predicted_class = tf.argmax(prediction).numpy()[0]
        if predicted_class == 0:
            st.write("Predicted stock price movement: Drop")
        else:
            st.write("Predicted stock price movement: Rise")

    # Sentiment Analysis with Transformer Model
    st.header("Sentiment Analysis with Transformer Model")
    sentiment_input_text = st.text_area("Enter text for sentiment analysis:")

    if st.button("Analyze Sentiment"):
        # Encoding
        encodings = tokenizer_sentiment.encode_plus(sentiment_input_text, add_special_tokens=True, max_length=MAX_LEN, 
                                                    return_token_type_ids=False, padding='max_length', 
                                                    return_attention_mask=True, return_tensors='tf')

        # Inference
        logits = model_sentiment(encodings['input_ids'], attention_mask=encodings['attention_mask']).logits
        prediction = tf.nn.softmax(logits, axis=1)

        # Interpret the prediction (assuming binary sentiment: 0 = negative, 1 = positive)
        predicted_class = tf.argmax(prediction).numpy()[0]
        if predicted_class == 0:
            st.write("Sentiment: Negative")
        else:
            st.write("Sentiment: Positive")
