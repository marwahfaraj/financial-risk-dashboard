CREATE DATABASE IF NOT EXISTS financial_dashboard;

USE financial_dashboard;

-- Create companies table

CREATE TABLE IF NOT EXISTS companies ( ticker VARCHAR(10) PRIMARY KEY,
                                                                  name VARCHAR(100) NOT NULL,
                                                                                    sector VARCHAR(50),
                                                                                           description TEXT);

-- Create categories table

CREATE TABLE IF NOT EXISTS categories ( category_id INT AUTO_INCREMENT PRIMARY KEY,
                                                                               name VARCHAR(50) NOT NULL UNIQUE);

-- Create stock_categories table to link stocks to categories

CREATE TABLE IF NOT EXISTS stock_categories
    ( ticker VARCHAR(10) NOT NULL,
                         category_id INT NOT NULL,
                                         PRIMARY KEY (ticker,
                                                      category_id),
     FOREIGN KEY (ticker) REFERENCES companies(ticker) ON DELETE CASCADE,
     FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE);

-- Create stock_metrics table with a foreign key to companies

CREATE TABLE IF NOT EXISTS stock_metrics
    ( ticker VARCHAR(10) NOT NULL, date DATE NOT NULL,
                                             close_price DECIMAL(10, 2),
                                                         daily_return DECIMAL(10, 4),
                                                                      roi DECIMAL(10, 2),
                                                                          volatility DECIMAL(10, 4),
                                                                                     sharpe_ratio DECIMAL(10, 4),
                                                                                                  PRIMARY KEY (ticker, date), CONSTRAINT fk_ticker_companies
     FOREIGN KEY (ticker) REFERENCES companies(ticker) ON DELETE CASCADE);

-- Insert default categories

INSERT INTO categories (name)
VALUES ('Technology'), ('Energy'), ('Finance'), ('Healthcare'), ('Consumer Discretionary') ON DUPLICATE KEY
UPDATE name =
VALUES(name);

