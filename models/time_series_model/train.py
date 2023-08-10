import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Constants
DATA_DIRECTORY = "processed_data/"
MODEL_DIRECTORY = "models/time_series_model/"
LOOKBACK_WINDOW = 60  # Number of past days to use for predicting the next day

# Load data
def load_data(symbol, directory=DATA_DIRECTORY):
    filename = f"{directory}{symbol}_processed.csv"
    return pd.read_csv(filename, index_col=0, parse_dates=True)

# Preprocess data for LSTM
def preprocess_for_lstm(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['4. close'].values.reshape(-1, 1))

    x, y = [], []
    for i in range(LOOKBACK_WINDOW, len(scaled_data)):
        x.append(scaled_data[i-LOOKBACK_WINDOW:i, 0])
        y.append(scaled_data[i, 0])
    x, y = np.array(x), np.array(y)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))

    return x, y, scaler

# LSTM model definition
def create_lstm_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(units=50),
        tf.keras.layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == "__main__":
    symbol = "AAPL"  # Can be parameterized or extended to multiple symbols

    df = load_data(symbol)
    x, y, scaler = preprocess_for_lstm(df)

    # Train-validation split
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, shuffle=False)

    model = create_lstm_model((x_train.shape[1], 1))
    model.fit(x_train, y_train, epochs=50, batch_size=32, validation_data=(x_val, y_val))

    # Optionally: Evaluate model
    predictions = model.predict(x_val)
    mse = mean_squared_error(y_val, predictions)
    print(f"Validation MSE: {mse}")

    # Save model and scaler
    model.save(f"{MODEL_DIRECTORY}{symbol}_lstm.h5")
    with open(f"{MODEL_DIRECTORY}{symbol}_scaler.pkl", 'wb') as f:
        import pickle
        pickle.dump(scaler, f)

    print(f"Model for {symbol} trained and saved successfully!")
