import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, chi2_contingency
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Load data
PROCESSED_DATA_DIR = "../data/processed/"
GRAPHS_DIR = "../graphs/"
os.makedirs(GRAPHS_DIR, exist_ok=True)  # Create graphs folder if it doesn't exist

combined_file_path = os.path.join(PROCESSED_DATA_DIR, "combined_stock_metrics.csv")
data = pd.read_csv(combined_file_path)

# Ensure Date is a datetime object
data['Date'] = pd.to_datetime(data['Date'])

# Define custom colors
ORANGE = "#FF8F46"
BLUE = "#0F3166"
BLACK = "#000000"
GRAY = "#D3D3D3"
COLORS = [ORANGE, BLUE, BLACK, GRAY]

# Set global font and figure settings
plt.rcParams.update({
    "font.family": "Times New Roman",  # Use Times New Roman font
    "font.size": 12,                  # Set default font size
    "axes.titlesize": 14,             # Title font size
    "axes.labelsize": 12,             # Axis labels font size
    "xtick.labelsize": 10,            # X-tick font size
    "ytick.labelsize": 10             # Y-tick font size
})

# 1. Closing Price Trends
plt.figure(figsize=(10, 6))
for idx, ticker in enumerate(data['ticker'].unique()):
    ticker_data = data[data['ticker'] == ticker]
    plt.plot(ticker_data['Date'], ticker_data['Close'], label=ticker, color=COLORS[idx % len(COLORS)])
plt.title("Closing Price Trends", color=BLACK)
plt.xlabel("Date", color=BLACK)
plt.ylabel("Closing Price", color=BLACK)
plt.legend()
plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
plt.savefig(os.path.join(GRAPHS_DIR, "closing_price_trends.png"), dpi=300)
plt.close()

# 2. Daily Returns Distribution (Separate Graphs)
tickers = data['ticker'].unique()
for ticker, color in zip(tickers, COLORS):
    plt.figure(figsize=(8, 5))
    sns.histplot(data[data['ticker'] == ticker]['Daily Return'], kde=True, color=color, bins=50, alpha=0.7)
    plt.title(f"Daily Returns Distribution for {ticker}", color=BLACK)
    plt.xlabel("Daily Return", color=BLACK)
    plt.ylabel("Frequency", color=BLACK)
    plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
    plt.savefig(os.path.join(GRAPHS_DIR, f"daily_returns_distribution_{ticker}.png"), dpi=300)
    plt.close()

# 3. Volatility Over Time
plt.figure(figsize=(10, 6))
for idx, ticker in enumerate(data['ticker'].unique()):
    ticker_data = data[data['ticker'] == ticker]
    plt.plot(ticker_data['Date'], ticker_data['Volatility'], label=ticker, color=COLORS[idx % len(COLORS)])
plt.title("Volatility Over Time", color=BLACK)
plt.xlabel("Date", color=BLACK)
plt.ylabel("Volatility", color=BLACK)
plt.legend()
plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
plt.savefig(os.path.join(GRAPHS_DIR, "volatility_over_time.png"), dpi=300)
plt.close()

# 4. Sharpe Ratio Trends
plt.figure(figsize=(10, 6))
for idx, ticker in enumerate(data['ticker'].unique()):
    ticker_data = data[data['ticker'] == ticker]
    plt.plot(ticker_data['Date'], ticker_data['Sharpe Ratio'], label=ticker, color=COLORS[idx % len(COLORS)], linewidth=1.5)
plt.title("Sharpe Ratio Trends", color=BLACK)
plt.xlabel("Date", color=BLACK)
plt.ylabel("Sharpe Ratio", color=BLACK)
plt.legend()
plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
plt.savefig(os.path.join(GRAPHS_DIR, "sharpe_ratio_trends.png"), dpi=300)
plt.close()

# 5. Correlation Matrix
# Create a copy of data without the 'Date' column
df = data.copy().drop(columns=['Date'])

# Define custom colormap
custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", [ORANGE, "white", BLUE])

# Helper function for Cramér's V
def cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    return np.sqrt(phi2 / min(k - 1, r - 1))

# Check for constant columns
constant_columns = [col for col in df.columns if df[col].nunique() <= 1]

if constant_columns:
    print(f"Excluding constant columns from correlation matrix: {constant_columns}")

# Drop constant columns from the dataframe for correlation calculation
df_corr = df.drop(columns=constant_columns, errors='ignore')

# Compute correlation matrix for mixed data types
def compute_correlation_matrix(df):
    cols = df.columns
    corr_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)

    for col1 in cols:
        for col2 in cols:
            if df[col1].dtype == 'object' and df[col2].dtype == 'object':
                # Categorical vs Categorical: Cramér's V
                corr_matrix.loc[col1, col2] = cramers_v(df[col1], df[col2])
            elif df[col1].dtype != 'object' and df[col2].dtype != 'object':
                # Numerical vs Numerical: Pearson correlation
                try:
                    corr_matrix.loc[col1, col2] = pearsonr(df[col1], df[col2])[0]
                except Exception as e:
                    print(f"Error computing Pearson correlation between {col1} and {col2}: {e}")
                    corr_matrix.loc[col1, col2] = np.nan
            else:
                # Mixed types: Use ANOVA F-statistic correlation
                try:
                    if df[col1].dtype == 'object':
                        cat_col, num_col = col1, col2
                    else:
                        cat_col, num_col = col2, col1
                    le = LabelEncoder()
                    encoded = le.fit_transform(df[cat_col])
                    corr_matrix.loc[col1, col2] = pearsonr(encoded, df[num_col])[0]
                except Exception as e:
                    print(f"Error computing mixed correlation between {col1} and {col2}: {e}")
                    corr_matrix.loc[col1, col2] = np.nan

    return corr_matrix

# Generate the correlation matrix
correlation_matrix = compute_correlation_matrix(df_corr)

# Plot the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(
    correlation_matrix.astype(float),
    annot=True,
    fmt=".2f",
    cmap=custom_cmap,
    cbar_kws={'label': 'Correlation'},
    linewidths=0.5,
    linecolor=GRAY
)
plt.title("Correlation Matrix (Numerical & Categorical Features)", color=BLACK)
plt.savefig(os.path.join(GRAPHS_DIR, "correlation_matrix_mixed.png"), dpi=300)
plt.close()

# 6. Sector-Wise Average Metrics (Updated Colors)
plt.figure(figsize=(10, 6))
avg_metrics = data.groupby('ticker')[['ROI', 'Volatility', 'Sharpe Ratio']].mean()
avg_metrics.plot(kind='bar', figsize=(10, 6), color=[BLACK, BLUE, ORANGE])
plt.title("Sector-Wise Average Metrics", color=BLACK)
plt.xlabel("Ticker", color=BLACK)
plt.ylabel("Average Value", color=BLACK)
plt.legend(loc='upper right')
plt.grid(color=GRAY, linestyle="--", linewidth=0.5)
plt.savefig(os.path.join(GRAPHS_DIR, "sector_wise_metrics.png"), dpi=300)
plt.close()

print("High-resolution graphs generated and saved in the 'graphs' folder!")
