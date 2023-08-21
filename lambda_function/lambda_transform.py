import psycopg2
import json
import pandas as pd
import numpy as np

# Your actual RDS credentials
db_host = 
db_port =
db_name =
db_user =
db_password =

def calculate_rsi(data, window):
    print("Calculating RSI")
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def lambda_handler(event, context):
    try:
        print("Connecting to the database")
        # Connect to the database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()

        print("Fetching raw stock data")
        # Fetch raw stock data from the 'stock_data' table
        select_query = "SELECT * FROM stock_data"
        cursor.execute(select_query)
        raw_data = cursor.fetchall()

        print("Transforming data")
        # Convert raw_data to DataFrame for easier manipulation
        df = pd.DataFrame(raw_data, columns=['id', 'timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume'])

        print("Calculating Volatility")
        df['volatility'] = df['close_price'].rolling(window=10).std()

        print("Calculating Moving Average")
        df['moving_average'] = df['close_price'].rolling(window=10).mean()

        print("Calculating RSI")
        df['rsi'] = calculate_rsi(df['close_price'], window=14)

        print("Calculating Seasonal Decomposition")
        df['seasonal'] = df['close_price'].rolling(window=5).mean()

        print("Inserting transformed data back into the database")
        # Now, save this transformed data back into a new or the same database table
        for i, row in df.iterrows():
            insert_query = """INSERT INTO transformed_stock_data (timestamp, moving_average, volatility, rsi, seasonal) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (row['timestamp'], row['moving_average'], row['volatility'], row['rsi'], row['seasonal']))

        connection.commit()
        cursor.close()
        connection.close()

        print("Data transformed successfully")
        return {
            'statusCode': 200,
            'body': json.dumps('Data transformed successfully!')
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {e}")
        }
