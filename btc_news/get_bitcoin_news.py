import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_bitcoin_news(event, context):
    """
    Scrapes Bitcoin-related news articles from the Financial Times website 
    and returns a dictionary of article titles and their publication dates.
    """

    page_number = 20  # Start scraping from the last page
    proceed = True  # Flag to control pagination
    news_data = {}  # Dictionary to store articles (title as key, date as value)

    while page_number > 0 and proceed:
        # Set headers for the HTTP request to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Construct the URL for the current page
        url = f"https://www.ft.com/search?q=bitcoin&page={page_number}&sort=date&isFirstView=true"

        # Make an HTTP GET request to fetch the page content
        page = requests.get(url, headers)

        # Handle errors in fetching the page
        if page.status_code != 200:
            print(f"Error: Failed to retrieve page {url}, status code: {page.status_code}")
            proceed = False  # Stop scraping if the page fetch fails
            continue

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")

        # Find all article elements on the page
        articles = soup.find_all('div', class_='o-teaser__heading')
        if not articles:  # If no articles are found, stop pagination
            print("No more articles found.")
            proceed = False
            continue

        # Process each article on the page
        for article in articles:
            # Extract the article title
            title_tag = article.find('a')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # Extract the publication date of the article
            date_tag = article.find_next_sibling('div', class_='o-teaser__timestamp')
            if date_tag:
                time_tag = date_tag.find('time')
                if time_tag and time_tag.has_attr('datetime'):
                    date_text = time_tag['datetime']
                    try:
                        # Convert the date to ISO format
                        date = datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z').date().isoformat()
                    except ValueError:
                        date = None  # Handle invalid date formats
                else:
                    date = None
            else:
                date = None

            # Add the article to the dictionary if the date is valid
            if date:
                news_data[title] = date
            else:
                print(f"Skipping article '{title}' due to missing or invalid date.")

        # Move to the previous page
        page_number -= 1

    print(f"Scraped news data: {news_data}")

    # Return the dictionary containing article titles and publication dates
    return news_data