import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

### PROCESS STOCK DATA AND SAVE TO DATABASE ###
def save_stock_data_to_db(data, stock_symbol):
    """Save processed stock data to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

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

    except Exception as e:
        print(f"Error saving stock data for {stock_symbol} to database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

### PROCESS CONSUMER COMPLAINTS DATA AND SAVE TO DATABASE ###
def save_consumer_complaints_to_db(nrows=None):
    """Save consumer complaints data to the MySQL database efficiently."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        file_path = os.path.join(RAW_DATA_DIR, "complaints.csv")
        print(f"Processing complaints from {file_path}...")

        # Read CSV and parse the date
        complaints = pd.read_csv(file_path, parse_dates=["Date received"], low_memory=False, nrows=nrows)

        # Debugging: Print total number of records before filtering
        print(f"Total complaints before filtering: {len(complaints)}")

        # Filter last 6 months
        six_months_ago = datetime.today() - timedelta(days=180)
        complaints = complaints[complaints["Date received"] >= six_months_ago]

        # Debugging: Print number of complaints after filtering
        print(f"Complaints from last 6 months: {len(complaints)}")

        # Drop missing values
        complaints = complaints.dropna(subset=["Date received", "Company", "Product"])

        # Debugging: Print number of complaints after dropping missing values
        print(f"Valid complaints after dropping missing values: {len(complaints)}")

        # Rename columns to match MySQL table
        complaints = complaints.rename(columns={
            "Date received": "date_received",
            "Company": "company",
            "Product": "product",
            "State": "state"
        })

        # Fill missing state values
        complaints["state"] = complaints["state"].fillna("Unknown")

        # ✅ Select only required columns to match SQL table schema
        complaints = complaints[["date_received", "company", "product", "state"]]

        # Convert to list of tuples for MySQL bulk insert
        values = list(complaints.itertuples(index=False, name=None))

        # Debugging: Print first 5 values to check format
        print(f"First 5 complaint records to insert: {values[:5]}")

        if values:
            query = """
                INSERT INTO consumer_complaints (date_received, company, product, state)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE product = VALUES(product), state = VALUES(state)
            """
            cursor.executemany(query, values)
            connection.commit()
            print(f"Successfully saved {len(values)} consumer complaints to the database.")
        else:
            print("⚠ No valid complaints found to insert.")

    except Exception as e:
        print(f"Error saving consumer complaints to database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


### PROCESS RAW STOCK DATA FILES ###
def process_stock_data(file_name):
    """Process raw stock data and calculate financial metrics."""
    try:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        print(f"Processing {file_path}...")
        data = pd.read_csv(file_path, index_col="Date", parse_dates=True)

        if "Close" not in data.columns:
            raise ValueError("Missing required column: Close")

        data = data.dropna(subset=["Close"])
        stock_symbol = file_name.split("_")[0]
        data['ticker'] = stock_symbol

        data["Daily Return"] = data["Close"].pct_change()
        data["Volatility"] = data["Daily Return"].rolling(window=20, min_periods=1).std()
        data["ROI"] = (data["Close"] / data["Close"].shift(1)) - 1
        data["Sharpe Ratio"] = data["Daily Return"].rolling(window=20, min_periods=1).mean() / data["Volatility"]

        data = data.bfill().ffill()

        save_stock_data_to_db(data.reset_index(), stock_symbol)
        return data.reset_index()
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith("_yahoo.csv"):
            process_stock_data(file)

    save_consumer_complaints_to_db(nrows=10000)
