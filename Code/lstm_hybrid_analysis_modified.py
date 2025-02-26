import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Directories
selected_data_dir = "selected_stock_data"
lstm_results_dir = "lstm_results"
hybrid_results_dir = "hybrid_results"
os.makedirs(lstm_results_dir, exist_ok=True)
os.makedirs(hybrid_results_dir, exist_ok=True)

# LSTM Model Parameters
look_back = 60  # Number of previous days to consider for prediction

# Function to create LSTM dataset
def create_dataset(data, look_back):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i + look_back])
        Y.append(data[i + look_back])
    return np.array(X), np.array(Y)

# Function to build and train LSTM model
def apply_lstm(data, stock_name):
    try:
        # Normalize the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Prepare dataset for LSTM
        X, Y = create_dataset(scaled_data, look_back)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        # Build the LSTM model
        model = Sequential()
        model.add(Input(shape=(X.shape[1], 1)))  # Updated to use Input layer
        model.add(LSTM(units=50, return_sequences=True))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X, Y, epochs=20, batch_size=32, verbose=0)

        # Make predictions
        predicted_prices = model.predict(X)
        predicted_prices = scaler.inverse_transform(predicted_prices)

        # Save results
        lstm_file = os.path.join(lstm_results_dir, f"{stock_name}_lstm_predictions.csv")
        pd.DataFrame({"Date": data['Date'][look_back:].values, "Actual": data['Close'][look_back:].values, "Predicted": predicted_prices.flatten()}).to_csv(lstm_file, index=False)
        
        print(f"LSTM results saved for {stock_name}.")
    except Exception as e:
        print(f"Error in LSTM modeling for {stock_name}: {e}")

# Function to combine ARIMA and LSTM predictions (Hybrid Model)
def apply_hybrid(data, stock_name):
    try:
        # ARIMA modeling
        ts = data['Close']
        arima_model = ARIMA(ts, order=(5, 1, 0))
        arima_fit = arima_model.fit()
        arima_predictions = arima_fit.fittedvalues

        # Normalize the data for LSTM
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Prepare dataset for LSTM
        X, Y = create_dataset(scaled_data, look_back)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        # Build and train the LSTM model
        lstm_model = Sequential()
        lstm_model.add(Input(shape=(X.shape[1], 1)))  # Updated to use Input layer
        lstm_model.add(LSTM(units=50, return_sequences=True))
        lstm_model.add(LSTM(units=50))
        lstm_model.add(Dense(units=1))
        lstm_model.compile(optimizer='adam', loss='mean_squared_error')
        lstm_model.fit(X, Y, epochs=20, batch_size=32, verbose=0)

        # Make LSTM predictions
        lstm_predictions = lstm_model.predict(X)
        lstm_predictions = scaler.inverse_transform(lstm_predictions)

        # Combine ARIMA and LSTM predictions
        hybrid_predictions = 0.5 * arima_predictions[look_back:] + 0.5 * lstm_predictions.flatten()

        # Save results
        hybrid_file = os.path.join(hybrid_results_dir, f"{stock_name}_hybrid_predictions.csv")
        pd.DataFrame({"Date": data['Date'][look_back:].values, "Actual": data['Close'][look_back:].values, "Hybrid_Predicted": hybrid_predictions}).to_csv(hybrid_file, index=False)

        print(f"Hybrid model results saved for {stock_name}.")
    except Exception as e:
        print(f"Error in Hybrid modeling for {stock_name}: {e}")

# Process each stock in the selected data directory
for file in os.listdir(selected_data_dir):
    if file.endswith(".csv"):
        stock_name = file.replace(".csv", "")
        file_path = os.path.join(selected_data_dir, file)

        try:
            # Load the data
            data = pd.read_csv(file_path)
            data['Date'] = pd.to_datetime(data['Date'])

            # Apply LSTM
            apply_lstm(data, stock_name)

            # Apply Hybrid Model
            apply_hybrid(data, stock_name)

        except Exception as e:
            print(f"Error processing {file}: {e}")
