import os
import pandas as pd
import matplotlib.pyplot as plt

# Directories
evaluation_results_dir = "evaluation_results"
plots_dir = os.path.join(evaluation_results_dir, "plots")
os.makedirs(plots_dir, exist_ok=True)

# Files containing evaluation metrics
lstm_metrics_file = os.path.join(evaluation_results_dir, "lstm_evaluation_metrics.csv")
hybrid_metrics_file = os.path.join(evaluation_results_dir, "hybrid_evaluation_metrics.csv")
arima_metrics_file = os.path.join(evaluation_results_dir, "arima_evaluation_metrics.csv")

# Function to clean stock names
def clean_stock_name(stock_name):
    return stock_name.replace(".NS_lstm_predictions", "").replace(".NS_hybrid_predictions", "").replace(".NS_arima_predictions", "")

# Function to load evaluation metrics
def load_metrics(file_path, model_name):
    try:
        data = pd.read_csv(file_path)
        data["Model"] = model_name
        data["Stock"] = data["Stock"].apply(clean_stock_name)
        return data
    except Exception as e:
        print(f"Error loading metrics from {file_path}: {e}")
        return pd.DataFrame()

# Load metrics from all models
lstm_metrics = load_metrics(lstm_metrics_file, "LSTM")
hybrid_metrics = load_metrics(hybrid_metrics_file, "Hybrid")
arima_metrics = load_metrics(arima_metrics_file, "ARIMA")

# Combine all metrics into a single DataFrame
all_metrics = pd.concat([lstm_metrics, hybrid_metrics, arima_metrics], ignore_index=True)

# Display combined metrics in the terminal
print("\nCombined Evaluation Metrics:\n")
print(all_metrics)

# Save combined metrics to a CSV file
combined_metrics_file = os.path.join(evaluation_results_dir, "combined_evaluation_metrics.csv")
all_metrics.to_csv(combined_metrics_file, index=False)
print(f"Combined evaluation metrics saved to {combined_metrics_file}")

# Plotting function for each metric
def plot_metric(metric_name, title, ylabel):
    try:
        plt.figure(figsize=(12, 6))

        # Pivot data to plot grouped bars
        pivot_data = all_metrics.pivot(index="Stock", columns="Model", values=metric_name)
        pivot_data.plot(kind="bar", figsize=(14, 8))

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel("Stocks")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Model")
        plt.tight_layout()

        # Save the plot
        plot_path = os.path.join(plots_dir, f"{metric_name}_comparison.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved: {plot_path}")

    except Exception as e:
        print(f"Error plotting {metric_name}: {e}")

# Generate plots for MAE, RMSE, and MAPE
plot_metric("MAE", "Mean Absolute Error (MAE) Comparison", "Mean Absolute Error")
plot_metric("RMSE", "Root Mean Squared Error (RMSE) Comparison", "Root Mean Squared Error")
plot_metric("MAPE", "Mean Absolute Percentage Error (MAPE) Comparison", "Mean Absolute Percentage Error (%)")
