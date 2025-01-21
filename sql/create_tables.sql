CREATE DATABASE IF NOT EXISTS financial_dashboard;

USE financial_dashboard;


CREATE TABLE IF NOT EXISTS stock_metrics ( ticker VARCHAR(10) NOT NULL, date DATE NOT NULL,
                                                                                  close_price DECIMAL(10, 2),
                                                                                              daily_return DECIMAL(10, 4),
                                                                                                           roi DECIMAL(10, 2),
                                                                                                               volatility DECIMAL(10, 4),
                                                                                                                          sharpe_ratio DECIMAL(10, 4),
                                                                                                                                       PRIMARY KEY (ticker, date));

