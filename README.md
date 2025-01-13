# Financial Risk Dashboard

A dashboard for tracking, analyzing, and visualizing financial risks and metrics for stocks and mutual funds.

## Features

- Integrates data from Yahoo Finance, Quandl, and Morningstar APIs.
- Processes data using SQL transformations.
- Interactive visualizations built with Tableau.
- Scalable deployment using Docker and Terraform.
- Monitoring via Grafana.

## Folder Structure

financial-risk-dashboard/
│
├── data/ # Raw and processed data files
│ ├── raw/ # Raw data from APIs
│ └── processed/ # Processed and cleaned data
│
├── scripts/ # Python scripts for data collection and processing
│ ├── data_collection.py # Scripts to fetch data from APIs
│ ├── data_processing.py # Scripts to process and transform data
│ └── utils.py # Utility functions
│
├── sql/ # SQL queries for data transformation
│ └── create_tables.sql # SQL script for database schema
│
├── visualizations/ # Tableau dashboard files or screenshots
│ └── tableau_project.twbx
│
├── infrastructure/ # Docker and Terraform files
│ ├── Dockerfile # Docker configuration
│ ├── docker-compose.yml # Docker Compose setup
│ └── terraform/ # Terraform scripts for deployment
│
├── monitoring/ # Grafana configuration files
│ ├── grafana_dashboard.json
│ └── alerts/ # Custom alert rules
│
├── requirements.txt # Python dependencies
├── README.md # Project overview and instructions
└── .gitignore # Files to ignore in version control
