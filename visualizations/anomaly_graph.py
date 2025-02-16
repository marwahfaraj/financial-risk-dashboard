import os
import pandas as pd
import numpy as np
import plotly.express as px

# Define directories
RAW_DATA_DIR = "../data/raw/"
GRAPHS_DIR = "../graphs/"
os.makedirs(GRAPHS_DIR, exist_ok=True)

# Load Consumer Complaints Data
file_path = os.path.join(RAW_DATA_DIR, "complaints.csv")

if not os.path.exists(file_path):
    print(f"Error: The file {file_path} does not exist. Ensure the data is in the correct directory.")
    exit()

# Load CSV with correct column names
data = pd.read_csv(file_path, parse_dates=["Date received"], low_memory=False)

# Print column names to verify
print("Columns in dataset:", data.columns.tolist())

# Ensure expected columns exist
required_columns = {"Date received", "Company", "Product", "State"}
if not required_columns.issubset(data.columns):
    print(f"Error: Missing required columns. Found columns: {list(data.columns)}")
    exit()

# Convert categorical columns to numeric using Label Encoding
data["Company"] = data["Company"].astype("category").cat.codes
data["Product"] = data["Product"].astype("category").cat.codes
data["State"] = data["State"].astype("category").cat.codes

# Selecting features for anomaly detection
features = ["Company", "Product", "State"]

# Apply Isolation Forest for anomaly detection
from sklearn.ensemble import IsolationForest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
data["Anomaly"] = model.fit_predict(data[features])

# Count anomalies
num_anomalies = (data["Anomaly"] == -1).sum()
print(f"🚨 Detected {num_anomalies} anomalies out of {len(data)} records.")

# Create an interactive scatter plot using Plotly
fig = px.scatter(
    data, x="Date received", y="Company",
    color="Anomaly",
    color_discrete_map={1: "blue", -1: "red"},
    title="Anomaly Detection in Consumer Complaints (Interactive)",
    labels={"Date received": "Date Received", "Company": "Company (Encoded)"},
    hover_data=["Product", "State"]  # Show additional details on hover
)

# Update layout for better readability
fig.update_layout(
    plot_bgcolor="white",
    xaxis=dict(title="Date Received", showgrid=True, gridcolor="lightgray"),
    yaxis=dict(title="Company (Encoded)", showgrid=True, gridcolor="lightgray"),
    legend_title="Anomaly"
)

# Show interactive graph
fig.show()
# Define the path to save the graph
anomaly_graph_path = os.path.join(GRAPHS_DIR, "consumer_complaints_anomalies.png")

# Save the graph as an image
fig.write_image(anomaly_graph_path, scale=2)  # Higher scale for better resolution

print(f"✅ Anomaly detection graph saved at: {anomaly_graph_path}")
