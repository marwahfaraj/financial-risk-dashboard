import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
from mlflow.models.signature import infer_signature

# Paths
RAW_DATA_PATH = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/raw/complaints.csv"
PROCESSED_DATA_PATH = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/processed/combined_stock_metrics.csv"
SAVED_PROCESSED_PATH = "/Users/marwahfaraj/Desktop/ms_degree_application_and_doc/final_projects/507_final_project/financial-risk-dashboard/data/processed/processed_stock_metrics.csv"
MODEL_DIR = "../models/"
GRAPHS_DIR = "../graphs/"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

# Load stock data
stock_data = pd.read_csv(PROCESSED_DATA_PATH)

# Load consumer complaints data
complaints_data = pd.read_csv(RAW_DATA_PATH, low_memory=False)

# Convert company names to lowercase for uniformity
complaints_data["Company"] = complaints_data["Company"].str.lower()

# Define Apple and Meta company name mappings from consumer complaints
apple_variants = [
    "apple financial holdings, inc.", "apple recovery, llc", "apple recovery services corp",
    "apple law group, inc.", "apple financing llc", "apple auto sales, inc.", "applewood funding corporation"
]
meta_variants = ["meta payments inc.", "metacorp llc"]

# Count complaints per company
apple_complaints_count = complaints_data[complaints_data["Company"].isin(apple_variants)].shape[0]
meta_complaints_count = complaints_data[complaints_data["Company"].isin(meta_variants)].shape[0]

# Create a DataFrame to store complaint counts per ticker
complaints_df = pd.DataFrame({
    "ticker": ["AAPL", "META"],  # Using tickers from Yahoo Finance dataset
    "Complaint_Count": [apple_complaints_count, meta_complaints_count]
})

# Merge complaint data with stock data
stock_data = stock_data.merge(complaints_df, on="ticker", how="left").fillna({"Complaint_Count": 0})

# Save the merged dataset to use for anomaly analysis
stock_data.to_csv(SAVED_PROCESSED_PATH, index=False)
print(f"✅ Processed stock data with complaints saved to {SAVED_PROCESSED_PATH}")

# Print debug information
print(f"Columns in dataset after merging complaints: {stock_data.columns}")
print(f"Complaint Count Value Distribution:\n{stock_data['Complaint_Count'].value_counts()}")

# Feature Selection
features = ["Close", "Daily Return", "Volatility", "Sharpe Ratio", "Complaint_Count", "ticker"]
target = "ROI"

# Check target variable distribution
stock_data[target] = np.log1p(stock_data[target])  # Log transform if skewed

# Preprocessing
X = stock_data[features]
y = stock_data[target]

# Handle missing values
X = X.fillna(0)

# Feature Selection: Remove highly correlated features
selector = SelectKBest(score_func=f_regression, k=4)  # Adjusted k to include Complaint_Count
X_selected = selector.fit_transform(X.drop(columns=['ticker']), y)

# Scale numerical features
scaler = StandardScaler()
X_selected = scaler.fit_transform(X_selected)

# Encode categorical variables (ticker)
encoder = LabelEncoder()
X_ticker_encoded = encoder.fit_transform(X["ticker"]).reshape(-1, 1)
X_final = np.hstack((X_selected, X_ticker_encoded))

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.3, random_state=42)

# Define models and hyperparameter search space
param_distributions = {
    "Random Forest Regressor": {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 5, 10],
        "min_samples_split": [2, 5, 10]
    },
    "Gradient Boosting Regressor": {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.05, 0.1]
    },
    "Ridge Regression": {"alpha": [0.01, 0.1, 1.0, 10.0]},
    "Lasso Regression": {"alpha": [0.01, 0.1, 1.0]},
    "ElasticNet Regression": {"alpha": [0.01, 0.1, 1.0]},
}

models = {
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "ElasticNet Regression": ElasticNet(),
    "Random Forest Regressor": RandomForestRegressor(random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
    "Decision Tree Regressor": DecisionTreeRegressor(max_depth=3, random_state=42),
}

# Initialize MLflow
mlflow.set_experiment("Stock ROI Prediction")

# Evaluate models with Randomized Grid Search and Cross Validation
model_performance = []
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        if model_name in param_distributions:
            search = RandomizedSearchCV(model, param_distributions[model_name], n_iter=10, cv=5, scoring='r2', n_jobs=-1, random_state=42)
            search.fit(X_train, y_train)
            best_model = search.best_estimator_
        else:
            best_model = model
            best_model.fit(X_train, y_train)
        
        y_pred = best_model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        model_performance.append((model_name, r2, rmse))
        
        # Log parameters, metrics, and model
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("rmse", rmse)
        
        # Infer signature and input example
        signature = infer_signature(X_train, best_model.predict(X_train))
        input_example = X_train[:1]
        
        # Log the model with signature and input example
        mlflow.sklearn.log_model(best_model, model_name, signature=signature, input_example=input_example)

# Convert model performance to DataFrame
performance_df = pd.DataFrame(model_performance, columns=["Model", "R-Squared", "RMSE"])
performance_df = performance_df.sort_values(by="R-Squared", ascending=False)

# Save model performance metrics
performance_file = os.path.join(MODEL_DIR, "model_performance.csv")
performance_df.to_csv(performance_file, index=False)
print(f"Model performance saved to {performance_file}")

# Generate and save model comparison graph
plt.figure(figsize=(12, 6))
plt.barh(performance_df["Model"], performance_df["R-Squared"], color=["#FF8F46", "#0F3166", "#FF8F46", "#0F3166"])
plt.xlabel("R-Squared Score")
plt.ylabel("Model")
plt.title("Model Comparison by R-Squared")
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", linewidth=0.5)
graph_path = os.path.join(GRAPHS_DIR, "model_comparison_r2.png")
plt.tight_layout()
plt.savefig(graph_path, dpi=300)
plt.close()
print(f"Model comparison graph saved to {graph_path}")

print("✅ Model evaluation complete with consumer complaints integrated and graph generated.")
