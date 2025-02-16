import os
import pandas as pd
import yfinance as yf

# Create directories if they don't exist
RAW_DATA_DIR = "../../data/raw/"
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
    # Fetch stock data
    tickers = ["AAPL", "MSFT", "GOOGL", "META"]
    for ticker in tickers:
        fetch_yahoo_finance_data(ticker, period="1y")

    # Save Consumer Complaints file to raw data (Assume it's already downloaded)
    consumer_complaints_file = "../../data/raw/complaints.csv"
    if os.path.exists(consumer_complaints_file):
        print(f"Consumer complaints data already saved at: {consumer_complaints_file}")
    else:
        print("Please download the Consumer Complaints file and save it to '../data/raw/'")
