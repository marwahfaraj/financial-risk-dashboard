import os
import pandas as pd
import yfinance as yf

# Create a directory for raw data if it doesn't exist
RAW_DATA_DIR = "../data/raw/"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


def fetch_yahoo_finance_data(ticker, period="1y"):
    """Fetch historical stock data from Yahoo Finance."""
    try:
        print(f"Fetching data for {ticker} from Yahoo Finance...")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        file_path = os.path.join(RAW_DATA_DIR, f"{ticker}_yahoo.csv")
        data.to_csv(file_path)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error fetching Yahoo Finance data for {ticker}: {e}")


if __name__ == "__main__":
    # Fetch data from Yahoo Finance
    fetch_yahoo_finance_data("AAPL", period="1y")
    fetch_yahoo_finance_data("MSFT", period="1y")
    fetch_yahoo_finance_data("GOOGL", period="1y")
    fetch_yahoo_finance_data("META", period="1y")
