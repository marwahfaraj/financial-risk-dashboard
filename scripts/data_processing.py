import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
import subprocess

# Define directories
RAW_DATA_DIR = "../data/raw/"
PROCESSED_DATA_DIR = "../data/processed/"
SQL_SCRIPTS_DIR = "../sql/"
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
    """Save processed stock data to MySQL database and locally."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Ensure company exists
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
                name = VALUES(name), sector = VALUES(sector), description = VALUES(description)
            """, (stock_symbol, name, sector, description))
            connection.commit()

        # Save stock metrics data
        data = data.dropna(subset=["Date"])
        for _, row in data.iterrows():
            if not isinstance(row["Date"], pd.Timestamp):
                continue
            date_value = row["Date"].strftime('%Y-%m-%d')
            execute_query(cursor, """
                INSERT INTO stock_metrics (ticker, date, close_price, daily_return, roi, volatility, sharpe_ratio)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE close_price = VALUES(close_price),
                daily_return = VALUES(daily_return),
                roi = VALUES(roi),
                volatility = VALUES(volatility),
                sharpe_ratio = VALUES(sharpe_ratio)
            """, (stock_symbol, date_value, row["Close"], row["Daily Return"], row["ROI"], row["Volatility"], row["Sharpe Ratio"]))
        connection.commit()

        # Add ticker column to processed data
        data["ticker"] = stock_symbol

        processed_file_path = os.path.join(PROCESSED_DATA_DIR, f"processed_stock_metrics_{stock_symbol}.csv")
        data.to_csv(processed_file_path, index=False)
        print(f"Processed stock metrics for {stock_symbol} saved to {processed_file_path}.")

        return data

    except Exception as e:
        print(f"Error saving data for {stock_symbol}: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def save_consumer_complaints_to_raw(nrows=None):
    """Save consumer complaints to MySQL staging table (consumer_complaints_raw)."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        file_path = os.path.join(RAW_DATA_DIR, "complaints.csv")
        print(f"Processing complaints from {file_path}...")

        complaints = pd.read_csv(file_path, parse_dates=["Date received"], low_memory=False, nrows=nrows)
        
        # Drop rows with missing required values
        complaints = complaints.dropna(subset=["Date received", "Company", "Product", "State"])
        complaints = complaints.rename(columns={"Date received": "date_received", "Company": "company", "Product": "product", "State": "state"})

        # Fill NaN values with "Unknown"
        complaints = complaints.fillna("Unknown")

        # Validate and truncate 'state' values to a maximum of 50 characters
        complaints["state"] = complaints["state"].apply(lambda x: str(x)[:50] if len(str(x)) > 50 else x)

        # Select only relevant columns
        complaints = complaints[["date_received", "company", "product", "state"]]

        # Convert DataFrame rows into a list of tuples
        values = list(complaints.itertuples(index=False, name=None))

        for row in values[:5]:  # Print first 5 rows for debugging
            print(f"Fixed row for insertion: {row}")

        if values:
            query = """
                INSERT INTO consumer_complaints_raw (date_received, company, product, state)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE product = VALUES(product), state = VALUES(state)
            """
            cursor.executemany(query, values)
            connection.commit()
            print(f"Successfully saved {len(values)} raw consumer complaints to the database.")
        else:
            print("⚠ No valid complaints found to insert.")

    except Exception as e:
        print(f"Error saving consumer complaints to database: {e}")
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

        if "Close" not in data.columns:
            raise ValueError("Missing required column: Close")

        data = data.dropna(subset=["Close"])
        data["Daily Return"] = data["Close"].pct_change()
        data["Volatility"] = data["Daily Return"].rolling(window=20, min_periods=1).std()
        data["ROI"] = (data["Close"] / data["Close"].shift(1)) - 1
        rolling_mean = data["Daily Return"].rolling(window=20, min_periods=1).mean()
        rolling_std = data["Daily Return"].rolling(window=20, min_periods=1).std()
        data["Sharpe Ratio"] = rolling_mean / rolling_std

        data.bfill(inplace=True)
        data.ffill(inplace=True)

        stock_symbol = file_name.split("_")[0]
        return save_to_database(data.reset_index(), stock_symbol)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    combined_data = []
    for raw_file in os.listdir(RAW_DATA_DIR):
        if raw_file.endswith("_yahoo.csv"):
            stock_data = process_stock_data(raw_file)
            if not stock_data.empty:
                combined_data.append(stock_data)

    if combined_data:
        combined_data_df = pd.concat(combined_data, ignore_index=True)
        combined_data_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "combined_stock_metrics.csv"), index=False)
        print(f"Combined stock metrics saved.")

    save_consumer_complaints_to_raw(nrows=10000)
    subprocess.run(f"mysql -u {DB_CONFIG['user']} -p{DB_CONFIG['password']} {DB_CONFIG['database']} < {os.path.join(SQL_SCRIPTS_DIR, 'process_consumer_complaints.sql')}", shell=True)
