import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Directories
selected_data_dir = "selected_stock_data"
eda_results_dir = "eda_results"
arima_results_dir = "arima_results"
os.makedirs(eda_results_dir, exist_ok=True)
os.makedirs(arima_results_dir, exist_ok=True)

warnings.filterwarnings("ignore")

# Function to perform EDA and save visualizations
def perform_eda(data, stock_name):
    try:
        # Plot closing price trends
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Close'], label='Closing Price', color='blue')
        plt.title(f"Closing Price Trend for {stock_name}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(eda_results_dir, f"{stock_name}_trend.png"))
        plt.close()

        # Plot rolling mean for smoothing trends
        rolling_mean = data['Close'].rolling(window=30).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Close'], label='Closing Price', color='blue')
        plt.plot(data['Date'], rolling_mean, label='30-Day Rolling Mean', color='orange')
        plt.title(f"Rolling Mean for {stock_name}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(eda_results_dir, f"{stock_name}_rolling_mean.png"))
        plt.close()

        print(f"EDA visualizations saved for {stock_name}.")
    except Exception as e:
        print(f"Error in EDA for {stock_name}: {e}")

# Function to apply ARIMA and save results
def apply_arima(data, stock_name):
    try:
        # ARIMA modeling requires the 'Close' column as a time series
        ts = data['Close']

        # Fit ARIMA model
        model = ARIMA(ts, order=(5, 1, 0))  # (p, d, q) parameters
        model_fit = model.fit()

        # Save model summary
        summary_file = os.path.join(arima_results_dir, f"{stock_name}_arima_summary.txt")
        with open(summary_file, 'w') as f:
            f.write(model_fit.summary().as_text())

        # Plot actual vs fitted values
        plt.figure(figsize=(12, 6))
        plt.plot(ts, label='Actual', color='blue')
        plt.plot(model_fit.fittedvalues, label='Fitted', color='red')
        plt.title(f"ARIMA Model Fit for {stock_name}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(arima_results_dir, f"{stock_name}_arima_fit.png"))
        plt.close()

        print(f"ARIMA results saved for {stock_name}.")
    except Exception as e:
        print(f"Error in ARIMA modeling for {stock_name}: {e}")

# Process each stock in the selected data directory
for file in os.listdir(selected_data_dir):
    if file.endswith(".csv"):
        stock_name = file.replace(".csv", "")
        file_path = os.path.join(selected_data_dir, file)
        
        try:
            # Load the data
            data = pd.read_csv(file_path)
            data['Date'] = pd.to_datetime(data['Date'])

            # Perform EDA
            perform_eda(data, stock_name)

            # Apply ARIMA
            apply_arima(data, stock_name)

        except Exception as e:
            print(f"Error processing {file}: {e}")