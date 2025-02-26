import os
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Directories
selected_data_dir = "selected_stock_data"
arima_results_dir = "arima_prediction_results"
os.makedirs(arima_results_dir, exist_ok=True)

# ARIMA Model Parameters
arima_order = (5, 1, 0)  # (p, d, q) order for ARIMA model

# Function to apply ARIMA model
def apply_arima(data, stock_name):
    try:
        # Extract the time series data (e.g., closing prices)
        ts = data['Close']

        # Fit the ARIMA model
        arima_model = ARIMA(ts, order=arima_order)
        arima_fit = arima_model.fit()

        # Generate predictions
        predictions = arima_fit.fittedvalues

        # Save results
        arima_file = os.path.join(arima_results_dir, f"{stock_name}_arima_predictions.csv")
        pd.DataFrame({"Date": data['Date'], "Actual": ts, "Predicted": predictions}).to_csv(arima_file, index=False)

        print(f"ARIMA results saved for {stock_name}.")

        # Plot results
        plt.figure(figsize=(10, 6))
        plt.plot(data['Date'], ts, label="Actual")
        plt.plot(data['Date'], predictions, label="Predicted", linestyle="--")
        plt.title(f"ARIMA Prediction for {stock_name}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.savefig(os.path.join(arima_results_dir, f"{stock_name}_arima_plot.png"))
        plt.close()

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

            # Apply ARIMA model
            apply_arima(data, stock_name)

        except Exception as e:
            print(f"Error processing {file}: {e}")
