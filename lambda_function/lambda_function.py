import psycopg2
import requests
import json

def check_and_add_unique_constraint(cursor):
    try:
        cursor.execute("ALTER TABLE stock_data ADD CONSTRAINT unique_timestamp UNIQUE (timestamp);")
    except Exception as e:
        # If the constraint already exists, this will throw an error, which we can safely ignore
        print(f"Could not add constraint: {e}")
        pass
    

def lambda_handler(event, context):
    print("Lambda function started.")  # Debug statement
    try:
        # Debug statements for variable initialization
        print("Initializing variables.")
        
        # Replace these variables with your Alpha Vantage API key and RDS credentials
        alpha_vantage_api_key = "EBLCGSC2KBINP5BM"
        db_host = 
        db_port = 
        db_name = 
        db_user = 
        db_password = 

        # Debug statements before API call
        print("About to make an API call to Alpha Vantage.")
        
        # Alpha Vantage API URL for fetching real-time stock data for Apple Inc. (AAPL)
        api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey={alpha_vantage_api_key}"

        # Fetch data from Alpha Vantage API
        response = requests.get(api_url)
        data = response.json()

        # Debug statement after API call
        print("Received data from Alpha Vantage.")
        
        # Extract the latest stock data (you can modify this based on your requirements)
        latest_data = data['Time Series (5min)']
        latest_timestamp = next(iter(latest_data))
        latest_stock_info = latest_data[latest_timestamp]
        
        # Debug statement before DB connection
        print("About to connect to the database.")
        
        # Connect to RDS PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        
        # Debug statement after successful DB connection
        print("Connected to the database.")
        
        # Check and add unique constraint
        check_and_add_unique_constraint(cursor)
        
        # SQL query to insert data into table (replace this query based on your table schema)
        insert_query = """INSERT INTO stock_data (timestamp, open_price, high_price, low_price, close_price, volume) VALUES (%s, %s, %s, %s, %s, %s)"""
        
        # Insert the latest stock data into the PostgreSQL table
        cursor.execute(insert_query, (latest_timestamp, latest_stock_info['1. open'], latest_stock_info['2. high'], latest_stock_info['3. low'], latest_stock_info['4. close'], latest_stock_info['5. volume']))
        
        # Debug statement after data insertion
        print("Data inserted into the database.")
        
        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database connection closed.")  # Debug statement
        return {
            'statusCode': 200,
            'body': json.dumps('Data inserted successfully!')
        }

    except Exception as e:
        print(f"Error occurred: {e}")  # Debug statement
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {e}")
        }
