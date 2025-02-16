# import mysql.connector
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Database connection details
# DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME")
# }

# # Test connection
# try:
#     connection = mysql.connector.connect(**DB_CONFIG)
#     print("Connection successful!")
# except Exception as e:
#     print(f"Error connecting to database: {e}")
# finally:
#     if connection.is_connected():
# #         connection.close()
# import pandas as pd

# df= pd.read_csv('/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/processed/combined_stock_metrics.csv')
# print(df.columns)

import pandas as pd

# Load the consumer complaints dataset
file_path = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/raw/complaints.csv"
data = pd.read_csv(file_path, low_memory=False)

# Convert company names to lowercase for uniformity
data["Company"] = data["Company"].str.lower()

# Check if there are complaints about Apple or Meta
apple_complaints = data[data["Company"].str.contains("apple", na=False, case=False)]
meta_complaints = data[data["Company"].str.contains("meta|facebook", na=False, case=False)]

# Display the number of complaints found
len_apple = len(apple_complaints)
len_meta = len(meta_complaints)

print(apple_complaints['Company'].value_counts(), meta_complaints['Company'].value_counts())
