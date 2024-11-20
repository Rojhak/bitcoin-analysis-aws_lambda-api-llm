import os
import psycopg2
import requests

def query(payload, api_url, headers):
    """
    Sends a request to the Hugging Face Inference API to analyze sentiment.
    Args:
        payload (dict): The data to be sent to the API (e.g., article title).
        api_url (str): The URL of the Hugging Face API endpoint.
        headers (dict): The headers, including the authorization token.
    Returns:
        dict: The API response in JSON format if successful, or None if an error occurs.
    """
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

def sentiment_handler(event, context):
    """
    Processes Bitcoin-related news articles, performs sentiment analysis using 
    Hugging Face API, and stores the results in a PostgreSQL database.
    Args:
        event (dict): The event payload, which contains news articles and their dates.
        context: AWS Lambda context object (not used here).
    Returns:
        dict: A response indicating the success or failure of the operation.
    """
    print(f"Event received: {event}")
    
    # Validate the incoming event to ensure it's in the correct format
    if not event or not isinstance(event, dict):
        return {"statusCode": 400, "body": "Invalid news_data format"}

    news_data = event.get("responsePayload")  # Extract the news data from the event
    database_url = os.getenv("DATABASE_URL")  # PostgreSQL database connection URL
    api_url = os.getenv("API_URL")            # Hugging Face API endpoint
    api_key = os.getenv("API_KEY")            # Hugging Face API key
    headers = {"Authorization": f"Bearer {api_key}"}  # Headers for the API request

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
    except Exception as e:
        return {"statusCode": 500, "body": f"Error connecting to database: {e}"}

    # Process each news article in the payload
    for date, title in news_data.items():
        # Send the article title to Hugging Face API for sentiment analysis
        sentiment_response = query({"inputs": title}, api_url, headers)
        print(sentiment_response)  # Debugging: Log the API response
        sentiment = "Unknown"  # Default sentiment if the response is invalid
        if sentiment_response and isinstance(sentiment_response, list):
            sentiment = sentiment_response[0][0].get("label", "Unknown")  # Extract the sentiment label

        # Insert the result into the PostgreSQL database
        insert_query = """
        INSERT INTO sentiment_news (date, title, sentiment)
        VALUES (%s, %s, %s)
        ON CONFLICT (title) DO NOTHING;
        """
        try:
            cur.execute(insert_query, (date, title, sentiment))
            conn.commit()
            print(f"Inserted: {title} with sentiment {sentiment}")
        except Exception as e:
            conn.rollback()  # Rollback transaction on error
            print(f"Error inserting data for article '{title}': {e}")

    # Close the database connection
    cur.close()
    conn.close()
    return {"statusCode": 200, "body": "Sentiment analysis completed successfully"}