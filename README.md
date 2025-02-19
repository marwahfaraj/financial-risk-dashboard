# 📊 Financial Risk Dashboard

A comprehensive analytical platform that tracks, evaluates, and visualizes financial risks and key metrics for stocks, ETFs, and mutual funds, enhanced with predictive insights using machine learning.

## 🏷️ Technologies Used

![Python](https://img.shields.io/badge/Python-3.9-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-blue) ![Tableau](https://img.shields.io/badge/Tableau-✔️-orange) ![Docker](https://img.shields.io/badge/Docker-✔️-brightgreen) ![Terraform](https://img.shields.io/badge/Terraform-✔️-purple) ![Machine Learning](https://img.shields.io/badge/ML-✔️-yellow) ![LLM](https://img.shields.io/badge/LLM-Groq,%20Phi%20Models-red)

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Machine Learning Model Training](#machine-learning-model-training)
4. [Model Evaluation & Performance Tracking](#model-evaluation--performance-tracking)
5. [Anomaly Detection & Risk Assessment](#anomaly-detection--risk-assessment)
6. [How to Run the Project](#how-to-run-the-project)
7. [Contributing](#contributing)
8. [License](#license)

## 🔹 Introduction

The **Financial Risk Dashboard** is a state-of-the-art tool designed for retail investors, analysts, and portfolio managers. It integrates real-time and historical financial data, advanced SQL transformations, and machine learning to deliver actionable insights into stock and mutual fund performance. Users can explore interactive dashboards built in Tableau, monitor real-time portfolio risks, and view predictive trends for informed decision-making.

## 🚀 Features

### 📊 Data Sources

- **Yahoo Finance API**:
  - Fetches historical stock prices, returns, volatility, and Sharpe Ratios for stocks such as AAPL, MSFT, GOOGL, and META.
  - Uses the `yfinance` Python library for seamless integration.
- **Consumer Complaint Database (data.gov)**:
  - Provides insights into market risks and reputational issues based on consumer sentiment data.
  - Enables analysis of complaint trends and their correlation with stock volatility and ROI.
- **Relational MySQL Database**:
  - Stores and links financial market data with consumer sentiment analysis for efficient querying and long-term trend analysis.
  - Enhances financial risk assessment by integrating historical performance metrics with real-time sentiment-driven risks.

### 🛠️ Data Preprocessing

Effective data preprocessing ensures data quality and consistency for ROI prediction and financial risk assessment. This study applies data cleaning, normalization, aggregation, and integration techniques to prepare stock and consumer complaint data.

- **Handling Missing Values**:
  - Missing stock values are addressed using forward and backward filling techniques.
  - Missing consumer complaint data is replaced with "Unknown."

- **Standardization & Normalization**:
  - Date fields are standardized to `YYYY-MM-DD` format for consistency.
  - Company names in complaints are normalized and mapped to stock tickers to resolve variations.

- **Data Aggregation & Merging**:
  - Consumer complaints are aggregated using a six-month rolling window to detect trends.
  - Stock and complaint data are merged by ticker, linking financial metrics (closing price, returns, volatility) with sentiment indicators (complaint frequency, regulatory concerns).

This integration enables machine learning models to identify anomalous stock behavior influenced by market sentiment, supporting predictive modeling and real-time anomaly detection.

## 🏆 Machine Learning Model Training

### 📊 Models Implemented

- **Linear Models**: Ridge Regression, Lasso Regression, and ElasticNet Regression.
- **Tree-Based Models**: Decision Tree Regressor, Random Forest Regressor, and Gradient Boosting Regressor.

### 🔍 Training & Testing Split

- The dataset was split into **70% for training** and **30% for testing**.

### 🎯 Hyperparameter Tuning

- **RandomizedSearchCV** was applied to fine-tune key hyperparameters.

## 📊 Model Evaluation & Performance Tracking

- **R-Squared (R²) Score**: Measures variance in ROI.
- **Root Mean Squared Error (RMSE)**: Measures prediction deviation.
- **MLflow** integrated for experiment logging and hyperparameter tracking.

## 🚨 Anomaly Detection & Risk Assessment

- **Visualization-Based Detection**:
  - **Box plots** of ROI distribution identified stocks with high variability.
  - **3D scatter plots** mapped ROI, volatility, and complaint trends.

- **Red-Flagging Criteria**:
  - Stocks experiencing a **surge in consumer complaints** were flagged.
  - **META and GOOGL** displayed heightened market instability.

## 📌 How to Run the Project

### Prerequisites

Ensure that the following dependencies are installed:

- Python (>=3.9)
- Docker
- Terraform
- AWS CLI (configured with necessary credentials)
- Tableau (for advanced data visualization)

### Installation Steps

```sh
git clone https://github.com/your-username/financial-risk-dashboard.git
cd financial-risk-dashboard
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py

