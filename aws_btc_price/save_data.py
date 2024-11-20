import psycopg2
import requests
import os

def save_data(event, context):
    """
    Fetch daily Bitcoin price data from an API and store it in a PostgreSQL database.
    """

    # Get environment variables for database connection and API
    database_url = os.getenv('postgres_url')  # PostgreSQL database URL
    api_key = os.getenv("stock_api")         # API key for fetching Bitcoin data
    stock_url = os.getenv("stock_url")       # Base API URL
    full_url = f"{stock_url}{api_key}"       # Construct the full API endpoint

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    # Fetch data from the API
    try:
        data = requests.get(full_url).json()
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return

    # Insert data into the database
    for date, stats in data["Time Series (Digital Currency Daily)"].items():
        try:
            # Convert API response data to floats for insertion
            open_price = float(stats['1. open'])
            high = float(stats['2. high'])
            low = float(stats['3. low'])
            close = float(stats['4. close'])
            volume = float(stats['5. volume'])

            # Insert data into the table, ignoring conflicts on duplicate dates
            cur.execute('''
                INSERT INTO bitcoin_dayly_price (date, open, low, high, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO NOTHING
            ''', (date, open_price, low, high, close, volume))
        except Exception as e:
            print(f"Error inserting data for {date}: {e}")
            conn.rollback()  # Rollback the transaction on error

    # Commit all changes and close the database connection
    conn.commit()
    cur.close()
    conn.close()