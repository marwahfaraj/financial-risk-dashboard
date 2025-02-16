import os
import pytest
import pandas as pd
from financial_risk_dashboard.scripts.data_processing import (
    execute_query,
    save_to_database,
    save_consumer_complaints_to_raw,
    process_stock_data,
)

# Mock data for testing
mock_stock_data = pd.DataFrame({
    "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
    "Close": [100, 105, 110],
    "Daily Return": [0.0, 0.05, 0.0476],  # Example values
    "ROI": [0.0, 0.05, 0.0476],          # Example values
    "Volatility": [0.0, 0.01, 0.02],      # Example values
    "Sharpe Ratio": [0.0, 5.0, 2.38],     # Example values
})

mock_complaints_data = pd.DataFrame({
    "date_received": pd.to_datetime(["2023-01-01", "2023-01-02"]),
    "company": ["Company A", "Company B"],
    "product": ["Product X", "Product Y"],
    "state": ["CA", "NY"],
})

# Test cases
def test_execute_query():
    # Mock database connection and cursor
    class MockCursor:
        def execute(self, query, params=None):
            pass
        def fetchall(self):
            return [("result1",), ("result2",)]

    cursor = MockCursor()
    result = execute_query(cursor, "SELECT * FROM table", fetch_result=True)
    assert result == [("result1",), ("result2",)]

def test_save_to_database():
    # Mock database connection and cursor
    class MockConnection:
        def commit(self):
            pass
        def close(self):
            pass
        def cursor(self):
            return MockCursor()

    class MockCursor:
        def execute(self, query, params=None):
            pass
        def close(self):
            pass

    # Mock data with all required columns
    mock_stock_data = pd.DataFrame({
        "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "Close": [100, 105, 110],
        "Daily Return": [0.0, 0.05, 0.0476],
        "ROI": [0.0, 0.05, 0.0476],
        "Volatility": [0.0, 0.01, 0.02],
        "Sharpe Ratio": [0.0, 5.0, 2.38],
    })

    # Call the function
    result = save_to_database(mock_stock_data, "AAPL")

    # Assert that the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

def test_save_consumer_complaints_to_raw():
    # Mock database connection and cursor
    class MockConnection:
        def commit(self):
            pass
        def close(self):
            pass
        def cursor(self):
            return MockCursor()

    class MockCursor:
        def executemany(self, query, params=None):
            pass
        def close(self):
            pass

    connection = MockConnection()
    save_consumer_complaints_to_raw(nrows=10)

def test_process_stock_data(tmpdir):
    # Create a temporary raw data file
    raw_data_file = tmpdir.join("AAPL_yahoo.csv")
    mock_stock_data.to_csv(raw_data_file, index=False)

    # Process the stock data
    result = process_stock_data(raw_data_file.basename)
    assert isinstance(result, pd.DataFrame)