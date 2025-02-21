import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

import os
import pandas as pd

import os
import pandas as pd

# ✅ Set BASE_DIR to point to 'financial_risk_dashboard'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")  # Remove extra 'financial_risk_dashboard'
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")  # Go one level up to reach the models folder
GRAPHS_DIR = os.path.join(BASE_DIR, "..", "graphs")

# Ensure directories exist
os.makedirs(GRAPHS_DIR, exist_ok=True)

# ✅ Load processed stock metrics data
processed_file_path = os.path.join(PROCESSED_DATA_DIR, "processed_stock_metrics.csv")
print(f"Loading processed data from: {processed_file_path}")  # Debug statement
data = pd.read_csv(processed_file_path)

# ✅ Format Date column
data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)

# ✅ Ensure Complaint Count is numeric
data["Complaint_Count"] = pd.to_numeric(data["Complaint_Count"], errors="coerce").fillna(0)

# ✅ Load ElasticNet predictions
elastic_net_predictions_path = os.path.join(MODEL_DIR, "elastic_net_predictions.csv")
print(f"Loading ElasticNet predictions from: {elastic_net_predictions_path}")  # Debug statement
results_df = pd.read_csv(elastic_net_predictions_path)


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

# -----------------  Fix: Correlation Matrix (Remove Non-Numeric Columns) -------------------
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


# Plot Actual vs Predicted ROI
plt.figure(figsize=(10, 6))
plt.scatter(results_df['Actual_ROI'], results_df['Predicted_ROI'], alpha=0.7, color='blue', label='Predictions')
plt.plot([results_df['Actual_ROI'].min(), results_df['Actual_ROI'].max()],
         [results_df['Actual_ROI'].min(), results_df['Actual_ROI'].max()],
         color='orange', linestyle='--', label='Perfect Prediction Line')
plt.xlabel("Actual ROI")
plt.ylabel("Predicted ROI")
plt.title("Actual vs Predicted ROI (ElasticNet Regression)")
plt.legend()
plt.grid(True)
plt.show()
plt.savefig(os.path.join(GRAPHS_DIR, "elastic_net_actual_vs_pred.png"), dpi=300, bbox_inches='tight')


print(" All graphs have been saved in the 'graphs' folder.")
