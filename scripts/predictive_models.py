import os
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import subprocess
from mlflow.models.signature import infer_signature

# Start MLflow UI automatically
mlflow_ui_command = ["mlflow", "ui", "--host", "127.0.0.1", "--port", "5000"]
subprocess.Popen(mlflow_ui_command)

# Paths
PROCESSED_DATA_DIR = "../data/processed/"
MODEL_DIR = "../models/"
GRAPHS_DIR = "../graphs/"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

# Load data
file_path = os.path.join(PROCESSED_DATA_DIR, "combined_stock_metrics.csv")
data = pd.read_csv(file_path)

# Feature Selection
features = ["Close", "Volume", "Daily Return", "Volatility", "Sharpe Ratio", "ticker"]
target = "ROI"

# Preprocessing
X = data[features]
y = data[target]

# Handle missing values
X = X.fillna(0)

# Scale numerical features
numerical_features = ["Close", "Volume", "Daily Return", "Volatility", "Sharpe Ratio"]
scaler = StandardScaler()
X.loc[:, numerical_features] = scaler.fit_transform(X[numerical_features]).astype(float)

# Convert integer columns to float to avoid schema enforcement issues
X["ticker"] = X["ticker"].astype(str)  # Ensure it's a string for encoding
encoder = LabelEncoder()
X["ticker"] = encoder.fit_transform(X["ticker"]).astype(float)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to evaluate
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "ElasticNet Regression": ElasticNet(alpha=0.1),
    "Random Forest Regressor": RandomForestRegressor(random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
    "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
    "Support Vector Regressor (SVR)": SVR(kernel='linear'),
}

# Initialize MLflow
mlflow.set_experiment("Stock ROI Prediction")

# Evaluate models
model_performance = []
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate performance metrics
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)  # Compute MSE
        rmse = mse ** 0.5  # Calculate RMSE manually
        model_performance.append((model_name, r2, rmse))
        
        # Log parameters, metrics, and model
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("rmse", rmse)
        
        # Infer signature and input example
        signature = infer_signature(X_train, model.predict(X_train))
        input_example = X_train.iloc[:1]

        # Log the model with signature and input example
        mlflow.sklearn.log_model(model, model_name, signature=signature, input_example=input_example)

# Convert performance metrics to a DataFrame
performance_df = pd.DataFrame(model_performance, columns=["Model", "R-Squared", "RMSE"])
performance_df = performance_df.sort_values(by="R-Squared", ascending=False)
performance_file = os.path.join(MODEL_DIR, "model_performance.csv")
performance_df.to_csv(performance_file, index=False)
print(f"Model performance metrics saved to {performance_file}")

# Plot and save top models' R² scores
plt.figure(figsize=(12, 8))
plt.barh(performance_df["Model"], performance_df["R-Squared"], color="#FF8F46", edgecolor="#0F3166")
plt.xlabel("R-Squared", color="#000000", fontsize=12)
plt.ylabel("Model", color="#000000", fontsize=12)
plt.title("Model Comparison by R-Squared", color="#000000", fontsize=14)
plt.gca().invert_yaxis()
plt.grid(color="#D3D3D3", linestyle="--", linewidth=0.5)
graph_path = os.path.join(GRAPHS_DIR, "model_comparison_r2.png")
plt.tight_layout()
plt.savefig(graph_path, dpi=300)
print(f"Model comparison graph saved to {graph_path}")
plt.close()

# Print the best model
best_model = performance_df.iloc[0]
print(f"The best model is {best_model['Model']} with R²: {best_model['R-Squared']:.4f} and RMSE: {best_model['RMSE']:.4f}")

print("Model comparison complete.")
