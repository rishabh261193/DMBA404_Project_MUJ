import os
import pandas as pd

# Directories
raw_data_dir = "stock_data"
clean_data_dir = "clean_stock_data"
os.makedirs(clean_data_dir, exist_ok=True)

# Function to clean and preprocess stock data
def clean_and_preprocess(file_name):
    try:
        # Load raw data
        file_path = os.path.join(raw_data_dir, file_name)
        data = pd.read_csv(file_path)

        # Check if required columns exist
        required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        if not all(column in data.columns for column in required_columns):
            print(f"Skipping {file_name}: Missing required columns.")
            return

        # Drop rows with missing values
        data.dropna(inplace=True)

        # Ensure 'Date' column is in datetime format
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

        # Remove rows with invalid dates
        data.dropna(subset=['Date'], inplace=True)

        # Sort data by date
        data.sort_values(by='Date', inplace=True)

        # Reset index after cleaning
        data.reset_index(drop=True, inplace=True)

        # Save cleaned data to new folder
        clean_file_path = os.path.join(clean_data_dir, file_name)
        data.to_csv(clean_file_path, index=False)
        print(f"Cleaned data for {file_name} saved to {clean_file_path}.")
    except Exception as e:
        print(f"Error cleaning {file_name}: {e}")

# Process all CSV files in the raw data directory
for file in os.listdir(raw_data_dir):
    if file.endswith(".csv"):
        clean_and_preprocess(file)
