import os
import pandas as pd
import yfinance as yf
import quandl

# Set up Quandl API key
quandl.ApiConfig.api_key = 'YOUR_API_KEY'

# Create a directory for raw data if it doesn't exist
RAW_DATA_DIR = "../data/raw/"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


def fetch_yahoo_finance_data(ticker, period="1y"):
    """Fetch historical stock data from Yahoo Finance."""
    print(f"Fetching data for {ticker} from Yahoo Finance...")
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    file_path = os.path.join(RAW_DATA_DIR, f"{ticker}_yahoo.csv")
    data.to_csv(file_path)
    print(f"Data saved to {file_path}")


def fetch_quandl_data(dataset):
    """Fetch mutual fund data from Quandl."""
    print(f"Fetching data for {dataset} from Quandl...")
    data = quandl.get(dataset)
    file_path = os.path.join(RAW_DATA_DIR, f"{dataset.split('/')[1]}_quandl.csv")
    data.to_csv(file_path)
    print(f"Data saved to {file_path}")


if __name__ == "__main__":
    # Fetch data from Yahoo Finance
    fetch_yahoo_finance_data("AAPL", period="1y")
    fetch_yahoo_finance_data("MSFT", period="1y")

    # Fetch data from Quandl
    fetch_quandl_data("WIKI/AAPL")
    fetch_quandl_data("WIKI/MSFT")
