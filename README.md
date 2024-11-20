
# Clear Guide to Bitcoin Analysis: AWS-Lambda, APIs, Web Scraping, LLMs, and Database Integration

## 🚀 Description
This project consists of three AWS Lambda functions to automate:
- Bitcoin price tracking 📊
- News collection 📰
- Sentiment analysis using Hugging Face 🤖

The data is stored in a Railway PostgreSQL database for further analysis.

## 📁 Project Structure

```plaintext
Bitcoin_Analysis/
├── create_table_DB/
│   ├── create_tables.py        # Script to create PostgreSQL tables
│   ├── requirements.txt        # Dependencies for this script
│   ├── .env                    # Environment variables for database connection
│
├── aws_btc_price/
│   ├── save_data.py            # Fetch Bitcoin prices and store in database
│   ├── requirements.txt        # Dependencies for this function
│
├── btc_news/
│   ├── get_bitcoin_news.py     # Fetch Bitcoin-related news
│   ├── requirements.txt        # Dependencies for this function
│
├── sentiment/
│   ├── sentiment_handler.py    # Perform sentiment analysis
│   ├── requirements.txt        # Dependencies for this function
│
├── README.md                   # Project documentation
├── LICENSE                     # Optional license
└── .gitignore                  # Ignore sensitive files
```
---


## ⚙️ Features

- **🚀 Automated Data Pipeline**:
  - 📊 **Fetch Bitcoin Prices**: Retrieve daily Bitcoin prices via APIs and store them in a PostgreSQL database.
  - 📰 **Scrape Bitcoin News**: Automatically scrape Bitcoin-related news articles from trusted sources.
  - 🤖 **Sentiment Analysis**: Analyze the sentiment of news articles using Hugging Face's LLM-based sentiment analysis.

- **🔗 API Integration**:
  - Leverages external APIs for Bitcoin price data and news collection.
  - Utilizes Hugging Face's Sentiment Analysis API for machine learning-powered insights.

- **🗄️ Database Storage**:
  - Stores all processed data (prices and news) in a Railway PostgreSQL database.
  - Ensures data is organized and ready for further analysis or visualization.




## 🛠️ 4. Functions

Before the AWS Lambda functions can process and store data, the required tables must be created in the Railway PostgreSQL database. You can do this using the provided create_table_DB/database_table.py script or manually with the following schemas.

**Database Table Schemas**

1️⃣ Bitcoin Daily Price Table

	•	Purpose: Store Bitcoin’s daily price data retrieved by the AWS Bitcoin Price Tracker.
	•	Schema:
```sql
CREATE TABLE bitcoin_daily_price (
    date DATE PRIMARY KEY,
    open FLOAT,
    low FLOAT,
    high FLOAT,
    close FLOAT,
    volume FLOAT
);
```



2️⃣ Sentiment News Table

	•	Purpose: Store sentiment analysis results of Bitcoin-related news articles.
	•	Schema:

```sql
CREATE TABLE sentiment_news (
    date DATE,
    title TEXT PRIMARY KEY,
    sentiment TEXT
);
```

**AWS Lambda Functions**

1️⃣ AWS Bitcoin Price Tracker

	•	Location: aws/aws_btc_price/save_data.py
	•	Purpose: Fetch Bitcoin’s daily price using an API and store the data in the bitcoin_daily_price table.

2️⃣ Bitcoin News Scraper

	•	Location: aws/btc_news/get_bitcoin_news.py
	•	Purpose: Scrape Bitcoin-related news articles from the web.

Example Output:

{
    "Bitcoin hits new all-time high!": "2024-11-19",
    "Regulation concerns shake the crypto market": "2024-11-18"
}

3️⃣ Bitcoin News Sentiment Analyzer

	•	Location: aws/sentiment/sentiment_handler.py
	•	Purpose: Analyze sentiment of Bitcoin news articles using Hugging Face’s sentiment analysis API and store the results in the sentiment_news table.



## 🌐 Environment Variables

Each AWS Lambda function requires specific environment variables. Set them manually in the AWS Management Console under **Configuration > Environment Variables**.

### 1️⃣ `aws_btc_price`

| Key           | Example Value                                      |
|---------------|----------------------------------------------------|
| `postgres_url`| `postgres://user:password@host:port/dbname`        |
| `stock_api`   | `your_stock_api_key`                               |
| `stock_url`   | `https://api.example.com/data?`                    |


### 2️⃣ `btc_news`

| Key           | Example Value                                      |
|---------------|----------------------------------------------------|
| `news_url`    | `https://www.ft.com/search?q=bitcoin`              |
| `user_agent`  | `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`        |



### 3️⃣ `sentiment_handler`

| Key           | Example Value                                      |
|---------------|----------------------------------------------------|
| `DATABASE_URL`| `postgres://user:password@host:port/dbname`        |
| `API_URL`     | `https://api-inference.huggingface.co/models/`     |
| `API_KEY`     | `your_huggingface_api_key`                         |


## 🔧 Setup Instructions


1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/bitcoin-analysis-project.git
   cd bitcoin-analysis-project
   ```
2. Before running the AWS Lambda functions, you must set up the required tables in the Railway PostgreSQL database. Use the provided create_table_DB/database_table.py script to automate this process.

3.	Configure Environment Variables:
	•	Set the environment variables in AWS Lambda (as listed above).
4.	Install Dependencies:
```bash
cd aws/create_table_DB
pip install -r requirements.txt
cd aws/aws_btc_price
pip install -r requirements.txt
cd ../btc_news
pip install -r requirements.txt
cd ../sentiment
pip install -r requirements.txt
```


5.	Deploy to AWS:
Run the deployment script to package and deploy all Lambda functions:
```bash
bash deploy.sh
```


## 🖼️ Example Workflow

	1.	Trigger 1: aws_btc_price fetches Bitcoin prices daily and stores them in DB.
	2.	Trigger 2: btc_news scrapes Bitcoin-related news.
	3.	Trigger 3: sentiment_handler analyzes news sentiment and stores the results in DB.

## 📊 Technologies Used

	•	AWS Lambda: Serverless computing for automation.
	•	Python 3.10: For function logic.
	•	PostgreSQL: Data storage (via Railway).
	•	APIs: External data fetching and Hugging Face for sentiment analysis.
	•	Hugging Face Transformers: LLM-based sentiment analysis.

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

## 💬 Contact

Feel free to connect with me:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fehmi-dataanalyst)  
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:katar.fhm@gmail.com)
---
