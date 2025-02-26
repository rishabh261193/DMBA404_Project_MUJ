import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Directories
lstm_results_dir = "lstm_results"
hybrid_results_dir = "hybrid_results"
arima_results_dir = "arima_prediction_results"
evaluation_results_dir = "evaluation_results"
os.makedirs(evaluation_results_dir, exist_ok=True)

# Function to calculate evaluation metrics
def evaluate_model(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return mae, rmse, mape

# Function to evaluate results and save metrics
def evaluate_results(results_dir, evaluation_file):
    evaluation_data = []

    for file in os.listdir(results_dir):
        if file.endswith(".csv"):
            stock_name = file.replace(".csv", "")
            file_path = os.path.join(results_dir, file)

            try:
                # Load the results
                data = pd.read_csv(file_path)
                actual = data['Actual'].values

                if 'Predicted' in data.columns:
                    predicted = data['Predicted'].values
                elif 'Hybrid_Predicted' in data.columns:
                    predicted = data['Hybrid_Predicted'].values
                else:
                    print(f"No prediction column found in {file}")
                    continue

                # Evaluate the model
                mae, rmse, mape = evaluate_model(actual, predicted)

                # Append results
                evaluation_data.append({
                    "Stock": stock_name,
                    "MAE": mae,
                    "RMSE": rmse,
                    "MAPE": mape
                })

            except Exception as e:
                print(f"Error evaluating {file}: {e}")

    # Save evaluation results
    evaluation_df = pd.DataFrame(evaluation_data)
    evaluation_df.to_csv(evaluation_file, index=False)
    print(f"Evaluation results saved to {evaluation_file}")

# Evaluate LSTM Results
lstm_evaluation_file = os.path.join(evaluation_results_dir, "lstm_evaluation_metrics.csv")
evaluate_results(lstm_results_dir, lstm_evaluation_file)

# Evaluate Hybrid Model Results
hybrid_evaluation_file = os.path.join(evaluation_results_dir, "hybrid_evaluation_metrics.csv")
evaluate_results(hybrid_results_dir, hybrid_evaluation_file)

# Evaluate ARIMA Results
arima_evaluation_file = os.path.join(evaluation_results_dir, "arima_evaluation_metrics.csv")
evaluate_results(arima_results_dir, arima_evaluation_file)
