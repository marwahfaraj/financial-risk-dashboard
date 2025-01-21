import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Define directories
RAW_DATA_DIR = "../data/raw/"
PROCESSED_DATA_DIR = "../data/processed/"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Load environment variables
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def execute_query(cursor, query, params=None, fetch_result=False):
    """Helper function to execute a query and optionally fetch results."""
    try:
        cursor.execute(query, params or ())
        if fetch_result:
            return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def save_to_database(data, stock_symbol):
    """Save processed data to MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Ensure the company exists in the companies table
        company_details = {
            "AAPL": ("Apple Inc.", "Technology", "Consumer electronics."),
            "MSFT": ("Microsoft Corp.", "Technology", "Enterprise software."),
            "GOOGL": ("Alphabet Inc.", "Technology", "Search and advertising."),
            "META": ("Meta Platforms", "Technology", "Social media and VR.")
        }
        if stock_symbol in company_details:
            name, sector, description = company_details[stock_symbol]
            execute_query(cursor, """
                INSERT INTO companies (ticker, name, sector, description)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                sector = VALUES(sector),
                description = VALUES(description)
            """, (stock_symbol, name, sector, description))
            connection.commit()

            # Link the company to a category
            category_id = execute_query(cursor, "SELECT category_id FROM categories WHERE name = %s", (sector,), fetch_result=True)
            if not category_id:
                execute_query(cursor, """
                    INSERT INTO categories (name)
                    VALUES (%s)
                    ON DUPLICATE KEY UPDATE name = VALUES(name)
                """, (sector,))
                connection.commit()
                category_id = execute_query(cursor, "SELECT category_id FROM categories WHERE name = %s", (sector,), fetch_result=True)

            if category_id:
                category_id = category_id[0][0]
                execute_query(cursor, """
                    INSERT INTO stock_categories (ticker, category_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE category_id = VALUES(category_id)
                """, (stock_symbol, category_id))
                connection.commit()

        # Process and save data into stock_metrics
        data = data.dropna(subset=["Date"])
        for _, row in data.iterrows():
            if not isinstance(row["Date"], pd.Timestamp):
                continue
            date_value = row["Date"].strftime('%Y-%m-%d')
            execute_query(cursor, """
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
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        print(f"Processing {file_path}...")
        data = pd.read_csv(file_path, index_col="Date", parse_dates=True)

        # Ensure required columns exist
        if "Close" not in data.columns:
            raise ValueError("Missing required column: Close")

        # Drop rows with missing data in the 'Close' column
        data = data.dropna(subset=["Close"])

        # Calculate financial metrics
        data["Daily Return"] = data["Close"].pct_change()  # Daily return calculation
        data["Volatility"] = data["Daily Return"].rolling(window=20, min_periods=1).std()  # Volatility
        data["ROI"] = (data["Close"] / data["Close"].shift(1)) - 1  # Return on Investment
        rolling_mean = data["Daily Return"].rolling(window=20, min_periods=1).mean()
        rolling_std = data["Daily Return"].rolling(window=20, min_periods=1).std()
        data["Sharpe Ratio"] = rolling_mean / rolling_std  # Sharpe ratio

        # Handle missing or insufficient data for rolling calculations
        data.fillna(method="bfill", inplace=True)  # Backfill missing data
        data.fillna(method="ffill", inplace=True)  # Forward fill as fallback

        # Save processed data
        processed_file_path = os.path.join(PROCESSED_DATA_DIR, f"processed_{file_name}")
        data.to_csv(processed_file_path)
        print(f"Processed data saved to {processed_file_path}")

        # Save data to database
        stock_symbol = file_name.split("_")[0]  # Extract stock symbol from file name
        save_to_database(data.reset_index(), stock_symbol)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    raw_files = os.listdir(RAW_DATA_DIR)
    for raw_file in raw_files:
        process_stock_data(raw_file)
