import os
import pandas as pd
import mysql.connector

# Define raw and processed data directories
RAW_DATA_DIR = "../data/raw/"
PROCESSED_DATA_DIR = "../data/processed/"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",  # Replace with your MySQL username
    "password": "your_password",  # Replace with your MySQL password
    "database": "financial_dashboard"
}

def save_to_database(data, stock_symbol):
    """Save processed data to MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Replace NaN values to ensure valid database insertion
        data = data.fillna(value={
            "Daily Return": 0.0,
            "Volatility": 0.0,
        })

        # Insert each row into the database
        for index, row in data.iterrows():
            print(f"Inserting data for {stock_symbol} on {index}...")
            cursor.execute("""
                INSERT INTO stock_metrics (ticker, date, close_price, daily_return, roi, volatility, sharpe_ratio)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                stock_symbol,
                index,
                row["Close"],
                row["Daily Return"],
                None,  # Replace with actual ROI calculation if applicable
                row["Volatility"],
                None  # Replace with actual Sharpe Ratio calculation if applicable
            ))
        connection.commit()
        print(f"Data for {stock_symbol} saved to database.")
    except Exception as e:
        print(f"Error saving data for {stock_symbol} to database: {e}")
    finally:
        if connection.is_connected():
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

        # Calculate daily returns
        data["Daily Return"] = data["Close"].pct_change()

        # Calculate moving averages (20-day and 50-day)
        data["20-Day MA"] = data["Close"].rolling(window=20).mean()
        data["50-Day MA"] = data["Close"].rolling(window=50).mean()

        # Calculate volatility (standard deviation of daily returns over 20 days)
        data["Volatility"] = data["Daily Return"].rolling(window=20).std()

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
