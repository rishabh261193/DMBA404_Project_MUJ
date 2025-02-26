import os
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Directories
evaluation_results_dir = "evaluation_results"
plots_dir = os.path.join(evaluation_results_dir, "hypothesis_plots")
os.makedirs(plots_dir, exist_ok=True)

# Load combined evaluation metrics
combined_metrics_file = os.path.join(evaluation_results_dir, "combined_evaluation_metrics.csv")
metrics_data = pd.read_csv(combined_metrics_file)

# Hypothesis H1: LSTM and Hybrid models outperform ARIMA
# Group data by models
lstm_data = metrics_data[metrics_data["Model"] == "LSTM"]
hybrid_data = metrics_data[metrics_data["Model"] == "Hybrid"]
arima_data = metrics_data[metrics_data["Model"] == "ARIMA"]

# Combine LSTM and Hybrid for comparison against ARIMA
advanced_models_data = pd.concat([lstm_data, hybrid_data])

# T-test for MAE
ttest_mae = ttest_ind(advanced_models_data["MAE"], arima_data["MAE"], equal_var=False)

# T-test for RMSE
ttest_rmse = ttest_ind(advanced_models_data["RMSE"], arima_data["RMSE"], equal_var=False)

# Display H1 results
print("\nH1 Results: Advanced Models vs ARIMA")
print(f"MAE T-test p-value: {ttest_mae.pvalue:.5f}")
print(f"RMSE T-test p-value: {ttest_rmse.pvalue:.5f}")

# Hypothesis H2: Seasonal and trend components influence forecast accuracy
# Compare Hybrid vs LSTM for MAE and RMSE
ttest_hybrid_lstm_mae = ttest_ind(hybrid_data["MAE"], lstm_data["MAE"], equal_var=False)
ttest_hybrid_lstm_rmse = ttest_ind(hybrid_data["RMSE"], lstm_data["RMSE"], equal_var=False)

# Display H2 results
print("\nH2 Results: Hybrid vs LSTM")
print(f"MAE T-test p-value: {ttest_hybrid_lstm_mae.pvalue:.5f}")
print(f"RMSE T-test p-value: {ttest_hybrid_lstm_rmse.pvalue:.5f}")

# Visualizations for Hypotheses
# H1: MAE and RMSE comparison (Advanced Models vs ARIMA)
def plot_h1(metric):
    plt.figure(figsize=(10, 6))
    plt.boxplot([
        advanced_models_data[metric],
        arima_data[metric]
    ], labels=["Advanced Models (LSTM + Hybrid)", "ARIMA"])
    plt.title(f"H1: {metric} Comparison")
    plt.ylabel(metric)
    plt.savefig(os.path.join(plots_dir, f"H1_{metric}_comparison.png"))
    plt.close()

# H2: MAE and RMSE comparison (Hybrid vs LSTM)
def plot_h2(metric):
    plt.figure(figsize=(10, 6))
    plt.boxplot([
        hybrid_data[metric],
        lstm_data[metric]
    ], labels=["Hybrid", "LSTM"])
    plt.title(f"H2: {metric} Comparison")
    plt.ylabel(metric)
    plt.savefig(os.path.join(plots_dir, f"H2_{metric}_comparison.png"))
    plt.close()

# Generate plots
plot_h1("MAE")
plot_h1("RMSE")
plot_h2("MAE")
plot_h2("RMSE")

# Summary
print("\nHypothesis testing completed. Results and plots saved.")
