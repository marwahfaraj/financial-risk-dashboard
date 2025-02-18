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

# Define relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH = os.path.join(BASE_DIR, "financial_risk_dashboard", "data", "raw", "complaints.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "financial_risk_dashboard", "data", "processed", "combined_stock_metrics.csv")
SAVED_PROCESSED_PATH = os.path.join(BASE_DIR, "financial_risk_dashboard", "data", "processed", "processed_stock_metrics.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")

# Ensure directories exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

# Load stock data
if not os.path.exists(PROCESSED_DATA_PATH):
    raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}. Ensure the data processing pipeline has run successfully.")
stock_data = pd.read_csv(PROCESSED_DATA_PATH)

# Load consumer complaints data
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}. Ensure the file exists.")
complaints_data = pd.read_csv(RAW_DATA_PATH, low_memory=False)

# Convert company names to lowercase for uniformity
complaints_data["Company"] = complaints_data["Company"].str.lower()

# Define company name mappings for complaints
apple_variants = [
    "apple financial holdings, inc.", "apple recovery, llc", "apple recovery services corp",
    "apple law group, inc.", "apple financing llc", "apple auto sales, inc.", "applewood funding corporation"
]
meta_variants = ["meta payments inc.", "metacorp llc"]

# Count complaints per company
apple_complaints_count = complaints_data[complaints_data["Company"].isin(apple_variants)].shape[0]
meta_complaints_count = complaints_data[complaints_data["Company"].isin(meta_variants)].shape[0]

# Create DataFrame to store complaint counts
complaints_df = pd.DataFrame({
    "ticker": ["AAPL", "META"],
    "Complaint_Count": [apple_complaints_count, meta_complaints_count]
})

# Merge complaint data with stock data
stock_data = stock_data.merge(complaints_df, on="ticker", how="left").fillna({"Complaint_Count": 0})

# Save the merged dataset
stock_data.to_csv(SAVED_PROCESSED_PATH, index=False)
print(f"Processed stock data with complaints saved to {SAVED_PROCESSED_PATH}")

# Feature Selection
features = ["Close", "Daily Return", "Volatility", "Sharpe Ratio", "Complaint_Count", "ticker"]
target = "ROI"

# Preprocessing
stock_data[target] = np.log1p(stock_data[target])
X = stock_data[features]
y = stock_data[target]
X = X.fillna(0)

# Feature Selection
selector = SelectKBest(score_func=f_regression, k=4)
X_selected = selector.fit_transform(X.drop(columns=['ticker']), y)

# Scaling
scaler = StandardScaler()
X_selected = scaler.fit_transform(X_selected)

# Encode categorical variables
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

# Set MLflow tracking
mlflow.set_tracking_uri("file://" + os.path.abspath("./mlruns"))
mlflow.set_experiment("Stock ROI Prediction")

# Variable to store the best ElasticNet model
best_elastic_net_model = None
model_performance = []

# Train and evaluate models
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        if model_name in param_distributions:
            search = RandomizedSearchCV(model, param_distributions[model_name], n_iter=10, cv=5, scoring='r2', n_jobs=-1, random_state=42)
            search.fit(X_train, y_train)
            best_model = search.best_estimator_
        else:
            best_model = model
            best_model.fit(X_train, y_train)

        # Store the best ElasticNet model
        if model_name == "ElasticNet Regression":
            best_elastic_net_model = best_model

        # Predictions
        y_pred = best_model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        model_performance.append((model_name, r2, rmse))

        # Log parameters, metrics, and model
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("rmse", rmse)

        # Log the model
        model_path = model_name.replace(" ", "_")
        mlflow.sklearn.log_model(best_model, model_path)

# Save model performance
performance_df = pd.DataFrame(model_performance, columns=["Model", "R-Squared", "RMSE"])
performance_df = performance_df.sort_values(by="R-Squared", ascending=False)
performance_file = os.path.join(MODEL_DIR, "model_performance.csv")
performance_df.to_csv(performance_file, index=False)
print(f"Model performance saved to {performance_file}")

# Save ElasticNet predictions
if best_elastic_net_model is not None:
    y_pred_elasticnet = best_elastic_net_model.predict(X_test)
    results_df = pd.DataFrame({
        'Ticker': stock_data.iloc[y_test.index]['ticker'].values,
        'Actual_ROI': y_test.values,
        'Predicted_ROI': y_pred_elasticnet,
        'Prediction_Error': y_test.values - y_pred_elasticnet
    })
    PREDICTIONS_FILE = os.path.join(MODEL_DIR, "elastic_net_predictions.csv")
    results_df.to_csv(PREDICTIONS_FILE, index=False)
    print(f"ElasticNet predictions saved to {PREDICTIONS_FILE}")
else:
    print("ElasticNet model was not trained. No predictions were saved.")
