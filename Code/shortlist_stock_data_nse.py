import os
import pandas as pd

# Directories
clean_data_dir = "clean_stock_data"
selected_data_dir = "selected_stock_data"
os.makedirs(selected_data_dir, exist_ok=True)

# List of selected stocks and their tickers
selected_stocks = [
    "M&M.NS", "MARUTI.NS", "TATAMOTORS.NS",  # Automobiles
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",  # Banking and Financial Services
    "LT.NS", "ULTRACEMCO.NS", "GRASIM.NS",  # Cement and Construction
    "HINDUNILVR.NS", "ITC.NS", "ASIANPAINT.NS",  # Consumer Goods
    "RELIANCE.NS", "NTPC.NS", "ADANIENT.NS",  # Energy
    "SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS",  # Healthcare and Pharmaceuticals
    "TCS.NS", "INFY.NS", "HCLTECH.NS",  # Information Technology
    "JSWSTEEL.NS", "TATASTEEL.NS", "HINDALCO.NS",  # Metals and Mining
    "BHARTIARTL.NS"  # Telecommunications
]

# Function to filter and copy selected stock data
def filter_selected_stocks(file_name):
    try:
        ticker = file_name.replace(".csv", "")
        if ticker in selected_stocks:
            # Load clean data
            file_path = os.path.join(clean_data_dir, file_name)
            data = pd.read_csv(file_path)

            # Save to selected data folder
            selected_file_path = os.path.join(selected_data_dir, file_name)
            data.to_csv(selected_file_path, index=False)
            print(f"Selected data for {ticker} saved to {selected_file_path}.")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Process all files in the clean data directory
for file in os.listdir(clean_data_dir):
    if file.endswith(".csv"):
        filter_selected_stocks(file)
