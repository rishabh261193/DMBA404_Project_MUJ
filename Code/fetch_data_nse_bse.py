import os
import pandas as pd
import yfinance as yf
from datetime import datetime

# List of stock tickers (NSE and BSE)
stock_tickers = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
    "HINDUNILVR.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "AXISBANK.NS", "WIPRO.NS", "HCLTECH.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "TATAMOTORS.NS",
    "SUNPHARMA.NS", "ULTRACEMCO.NS", "ADANIENT.NS", "NTPC.NS", "POWERGRID.NS", "TATASTEEL.NS",
    "JSWSTEEL.NS", "HDFCLIFE.NS", "TECHM.NS", "MARICO.NS", "BRITANNIA.NS", "DRREDDY.NS", 
    "DIVISLAB.NS", "EICHERMOT.NS", "DMART.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS",
    "BHARATFORG.NS", "UPL.NS", "HINDALCO.NS", "INDUSINDBK.NS", "GRASIM.NS", "BAJAJFINSV.NS", 
    "BPCL.NS", "IOC.NS", "CIPLA.NS", "LUPIN.NS", "M&M.NS", "SBILIFE.NS", "ZEEL.NS"
]

# Directory to store stock data
output_dir = "stock_data"
os.makedirs(output_dir, exist_ok=True)

# Function to download stock data and save it to a CSV file
def download_stock_data(ticker):
    try:
        print(f"Downloading data for {ticker}...")
        # Download historical data
        stock_data = yf.download(ticker, start="2015-01-01", end=datetime.today().strftime('%Y-%m-%d'))
        
        # Add 'Date' column at the start
        stock_data.reset_index(inplace=True)
        stock_data.insert(0, 'Date', stock_data.pop('Date'))
        
        # Save to CSV file
        file_path = os.path.join(output_dir, f"{ticker}.csv")
        stock_data.to_csv(file_path, index=False)
        print(f"Data for {ticker} saved to {file_path}.")
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")

# Loop through all stock tickers and download their data
for ticker in stock_tickers:
    download_stock_data(ticker)
