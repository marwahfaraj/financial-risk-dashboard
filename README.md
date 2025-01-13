# Financial Risk Dashboard 📊

A dashboard for tracking, analyzing, and visualizing financial risks and metrics for stocks and mutual funds.

![Python](https://img.shields.io/badge/Python-3.9-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-blue) ![Docker](https://img.shields.io/badge/Docker-✔️-brightgreen) ![Terraform](https://img.shields.io/badge/Terraform-✔️-purple)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Folder Structure](#folder-structure)
4. [How to Run the Project](#how-to-run-the-project)
5. [Contributing](#contributing)
6. [License](#license)

---

## Introduction

The Financial Risk Dashboard is an analytical platform designed to provide actionable insights into financial risks and key metrics for stocks and mutual funds. The project integrates real-time and historical data from robust APIs, processes it using SQL transformations, and visualizes it using Tableau, ensuring users can make informed investment decisions.

---

## Features 📊

- **Data Integration**:

  - [Yahoo Finance](https://finance.yahoo.com/): Historical stock prices and financial metrics via `yfinance`.
  - [Quandl](https://www.quandl.com/): Mutual funds and economic indicators.
  - [Morningstar](https://www.morningstar.com/): ETF and stock data.

- **Data Processing**:

  - SQL transformations for financial calculations like ROI, P/E Ratio, Volatility, and Sharpe Ratio.

- **Visualization**:

  - Interactive dashboards built with [Tableau](https://www.tableau.com/).

- **Deployment**:

  - Infrastructure as Code using [Docker](https://www.docker.com/) and [Terraform](https://www.terraform.io/).

- **Monitoring**:
  - Robust pipeline monitoring using [Grafana](https://grafana.com/).

---

## Folder Structure

```plaintext
financial-risk-dashboard/
│
├── data/                   # Raw and processed data files
│   ├── raw/                # Raw data from APIs
│   └── processed/          # Processed and cleaned data
│
├── scripts/                # Python scripts for data collection and processing
│   ├── data_collection.py  # Scripts to fetch data from APIs
│   ├── data_processing.py  # Scripts to process and transform data
│   └── utils.py            # Utility functions
│
├── sql/                    # SQL queries for data transformation
│   └── create_tables.sql   # SQL script for database schema
│
├── visualizations/         # Tableau dashboard files or screenshots
│   └── tableau_project.twbx
│
├── infrastructure/         # Docker and Terraform files
│   ├── Dockerfile          # Docker configuration
│   ├── docker-compose.yml  # Docker Compose setup
│   └── terraform/          # Terraform scripts for deployment
│
├── monitoring/             # Grafana configuration files
│   ├── grafana_dashboard.json
│   └── alerts/             # Custom alert rules
│
├── requirements.txt        # Python dependencies
├── README.md               # Project overview and instructions
└── .gitignore              # Files to ignore in version control
```
