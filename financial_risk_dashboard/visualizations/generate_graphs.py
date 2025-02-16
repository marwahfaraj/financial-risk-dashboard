import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

# Load data
PROCESSED_DATA_DIR = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/processed/"
GRAPHS_DIR = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/graphs/"
os.makedirs(GRAPHS_DIR, exist_ok=True)  # Create graphs folder if it doesn't exist

# Load the processed dataset with complaint count
processed_file_path = os.path.join(PROCESSED_DATA_DIR, "processed_stock_metrics.csv")
data = pd.read_csv(processed_file_path)

# ✅ Fix: Ensure Date column is properly formatted
data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)

# ✅ Fix: Ensure Complaint Count is numeric
data["Complaint_Count"] = pd.to_numeric(data["Complaint_Count"], errors="coerce").fillna(0)

# Define custom colors
ORANGE = "#FF8F46"
BLUE = "#0F3166"
BLACK = "#000000"
GRAY = "#D3D3D3"
COLORS = [ORANGE, BLUE, BLACK, GRAY]

# Set global font and figure settings
plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# ----------------- 3D Plot: ROI vs Volatility vs Complaints -------------------
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot for different stocks
for idx, ticker in enumerate(data['ticker'].unique()):
    subset = data[data['ticker'] == ticker]
    ax.scatter(
        subset['ROI'], subset['Volatility'], subset['Complaint_Count'],
        label=ticker, color=COLORS[idx % len(COLORS)], alpha=0.7
    )

ax.set_xlabel("ROI", color=BLACK)
ax.set_ylabel("Volatility", color=BLACK)
ax.set_zlabel("Complaint Count", color=BLACK)
ax.set_title("3D Scatter: ROI vs Volatility vs Complaints", color=BLACK)
ax.legend(loc='upper left', fontsize=8)
plt.savefig(os.path.join(GRAPHS_DIR, "3D_ROI_vs_Volatility_vs_Complaints.png"), dpi=300, bbox_inches='tight')
plt.close()

# ----------------- ✅ Fix: Correlation Matrix (Remove Non-Numeric Columns) -------------------
df_corr = data.drop(columns=['Date', 'ticker', 'Stock Splits'], errors='ignore')  # Drop categorical columns

# Compute correlation matrix
correlation_matrix = df_corr.corr()

# Define custom colormap
custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", [ORANGE, "white", BLUE])

# Plot the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(
    correlation_matrix, annot=True, fmt=".2f", cmap=custom_cmap,
    cbar_kws={'label': 'Correlation'}, linewidths=0.5, linecolor=GRAY
)
plt.title("Correlation Matrix: Numerical Features", color=BLACK)
plt.savefig(os.path.join(GRAPHS_DIR, "correlation_matrix.png"), dpi=300, bbox_inches='tight')
plt.close()



# ----------------- ROI Distribution with Complaints Highlighted -------------------
plt.figure(figsize=(10, 6))
sns.boxplot(x='ticker', y='ROI', data=data, palette=COLORS)
plt.title("ROI Distribution Across Stocks", color=BLACK)
plt.xlabel("Ticker", color=BLACK)
plt.ylabel("ROI", color=BLACK)
plt.xticks(rotation=45)
plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
plt.savefig(os.path.join(GRAPHS_DIR, "ROI_distribution.png"), dpi=300, bbox_inches='tight')
plt.close()

print("✅ All graphs have been saved in the 'graphs' folder.")
