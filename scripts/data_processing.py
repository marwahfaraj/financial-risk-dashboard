import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Define raw and processed data directories
RAW_DATA_DIR = "../data/raw/"
PROCESSED_DATA_DIR = "../data/processed/"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
load_dotenv()

# Database connection details
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def save_to_database(data, stock_symbol):
    """Save processed data to MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Drop rows where Date is missing or invalid
        data = data.dropna(subset=["Date"])

        for index, row in data.iterrows():
            if not isinstance(row["Date"], pd.Timestamp):
                print(f"Skipping row with invalid date: {row}")
                continue
            date_value = row["Date"].strftime('%Y-%m-%d')

            print(f"Inserting data for {stock_symbol} on {date_value}...")
            cursor.execute("""
                INSERT INTO stock_metrics (ticker, date, close_price, daily_return, roi, volatility, sharpe_ratio)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                close_price = VALUES(close_price),
                daily_return = VALUES(daily_return),
                roi = VALUES(roi),
                volatility = VALUES(volatility),
                sharpe_ratio = VALUES(sharpe_ratio)
            """, (
                stock_symbol,
                date_value,
                row["Close"],
                row["Daily Return"],
                row["ROI"],
                row["Volatility"],
                row["Sharpe Ratio"]
            ))
        connection.commit()
        print(f"Data for {stock_symbol} saved to database.")
    except Exception as e:
        print(f"Error saving data for {stock_symbol} to database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def process_stock_data(file_name):
    """Process raw stock data and calculate financial metrics."""
    try:
        # Load raw data
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        print(f"Processing {file_path}...")
        data = pd.read_csv(file_path, index_col="Date", parse_dates=True)

        # Ensure relevant columns exist
        required_columns = ["Close"]
        for column in required_columns:
            if column not in data.columns:
                raise ValueError(f"Missing required column: {column}")

        # Drop rows with missing values in the Close column
        data = data.dropna(subset=["Close"])

        # Calculate daily returns
        data["Daily Return"] = data["Close"].pct_change()

        # Calculate moving averages (20-day and 50-day)
        data["20-Day MA"] = data["Close"].rolling(window=20, min_periods=1).mean()
        data["50-Day MA"] = data["Close"].rolling(window=50, min_periods=1).mean()

        # Calculate volatility (standard deviation of daily returns over 20 days)
        data["Volatility"] = data["Daily Return"].rolling(window=20, min_periods=1).std()

        # Calculate ROI (Return on Investment)
        data["ROI"] = data["Close"].pct_change()  # Change logic if needed for ROI definition

        # Calculate Sharpe Ratio
        rolling_mean = data["Daily Return"].rolling(window=20, min_periods=1).mean()
        rolling_std = data["Daily Return"].rolling(window=20, min_periods=1).std()
        data["Sharpe Ratio"] = rolling_mean / rolling_std

        # Handle any NaN values in calculated columns
        data.fillna(0, inplace=True)

        # Save processed data
        processed_file_path = os.path.join(PROCESSED_DATA_DIR, f"processed_{file_name}")
        data.to_csv(processed_file_path)
        print(f"Processed data saved to {processed_file_path}")

        # Save to database
        stock_symbol = file_name.split("_")[0]  # Extract stock symbol from file name
        save_to_database(data.reset_index(), stock_symbol)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


if __name__ == "__main__":
    # List all raw data files
    raw_files = os.listdir(RAW_DATA_DIR)

    # Process each file
    for raw_file in raw_files:
        process_stock_data(raw_file)
