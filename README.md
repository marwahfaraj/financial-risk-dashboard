# Financial Risk Dashboard 📊

A comprehensive analytical platform that tracks, evaluates, and visualizes financial risks and key metrics for stocks, ETFs, and mutual funds, now enhanced with predictive insights using machine learning.

![Python](https://img.shields.io/badge/Python-3.9-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-blue) ![Tableau](https://img.shields.io/badge/Tableau-✔️-orange) ![Docker](https://img.shields.io/badge/Docker-✔️-brightgreen) ![Terraform](https://img.shields.io/badge/Terraform-✔️-purple) ![Machine Learning](https://img.shields.io/badge/ML-✔️-yellow)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [How to Run the Project](#how-to-run-the-project)
4. [Folder Structure](#folder-structure)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction

The Financial Risk Dashboard is a state-of-the-art tool designed for retail investors, analysts, and portfolio managers. It integrates real-time and historical financial data, advanced SQL transformations, and machine learning to deliver actionable insights into stock and mutual fund performance. Users can explore interactive dashboards built in Tableau, monitor real-time portfolio risks, and view predictive trends for informed decision-making.

## Features 📊

### **Data Sources**:

- **Yahoo Finance API**: Fetch historical stock prices, dividends, and financial metrics.
- **Quandl API**: Provides data on stocks, mutual funds, and economic indicators.
- **Morningstar API**: Supplies ETF, mutual fund, and stock data.

### **Data Processing**:

- SQL transformations for key financial metrics:
  - ROI, Volatility, Sharpe Ratio, and P/E Ratio.
- Data stored in a relational MySQL database for efficiency.

### **Predictive Analysis**:

- Machine Learning Models:
  - **Linear Regression**: ROI prediction.
  - **Time Series Models** (ARIMA, Prophet): Trend forecasting.
  - **Clustering**: Group stocks and ETFs by risk-return profiles.
- Predicted metrics stored in the database and visualized in Tableau.

### **Visualization**:

- Interactive dashboards in Tableau:
  - Historical and predicted trends for key metrics.
  - Risk-return analysis through clustering visualizations.

### **Deployment**:

- Automated using Docker and Terraform.
- Scalable infrastructure ensures reliable real-time monitoring.

## How to Run the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/username/financial-risk-dashboard.git
   cd financial-risk-dashboard

   ```

2. **Set Up the Environment**:

- Install Python dependencies:

```bash
  pip install -r requirements.txt
```

- Configure .env file with your MySQL credentials and API keys.

3. **Run Data Pipeline**:

- Fetch raw data:

```bash
  python scripts/data_collection.py
```

- Process data and store it in the database:

```bash
python scripts/data_processing.py
```

4. **Train ML Models**:

- Train models and generate predictions:

```bash
python scripts/predictive_models.py
```

5. **Visualize the Dashboard**:

Open the Tableau workbook (visualizations/tableau_project.twbx) to view the interactive dashboard.

## Folder Structure

```plaintext
financial-risk-dashboard/
│
├── data/                   # Raw and processed data files
│   ├── raw/                # Raw data from APIs
│   └── processed/          # Processed and cleaned data
│
├── scripts/                # Python scripts for data collection, processing, and ML
│   ├── data_collection.py  # Fetches data from APIs
│   ├── data_processing.py  # Cleans and processes data
│   ├── predictive_models.py # Trains and runs ML models
│   └── utils.py            # Utility functions
│
├── sql/                    # SQL queries for data schema and transformations
│   └── create_tables.sql   # Schema for relational database
│
├── visualizations/         # Tableau dashboard files or screenshots
│   └── tableau_project.twbx
│
├── infrastructure/         # Docker and Terraform files
│   ├── Dockerfile          # Docker configuration
│   ├── docker-compose.yml  # Docker Compose setup
│   └── terraform/          # Terraform scripts for deployment
│
├── requirements.txt        # Python dependencies
├── README.md               # Project overview and instructions
└── .gitignore              # Files to ignore in version control
```
