# Description: This script creates a table in the PostgreSQL database.
import psycopg2
import dotenv
dotenv.load_dotenv()
import os


# Define database URL or connection parameters
database_url = os.getenv("postgres_url")

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
except Exception as e:
    print(f"Error: Unable to connect to the database. {e}")

# Drop and recreate the sentiment_news and bitcoin_dayly_price tables with title as the primary key
cur.execute("DROP TABLE IF EXISTS sentiment_news;")
cur.execute("""
CREATE TABLE sentiment_news (
    date TEXT,
    title TEXT PRIMARY KEY,
    sentiment TEXT
)
""")
cur.execute("DROP TABLE IF EXISTS bitcoin_dayly_price;")
cur.execute("""
  CREATE TABLE bitcoin_dayly_price (
    date TEXT PRIMARY KEY,
    open FLOAT,
    low FLOAT,
    high FLOAT,
    close FLOAT,
    volume FLOAT    
)
""")
conn.commit()
cur.close()
conn.close()