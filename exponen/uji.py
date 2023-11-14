import pandas as pd
import numpy as np
from app.db import use_engine
from sklearn.metrics import mean_squared_error

# def triple_exponential_smoothing(data, seasonality_period, alpha, beta, gamma, forecast_period):
#     # Inisialisasi level, trend, dan seasonal
#     level = data[0]
#     trend = 0
#     seasonal = np.array(data[:seasonality_period])

#     # Inisialisasi variabel hasil
#     fitted_values = []
#     forecast_values = []

#     for i in range(len(data) + forecast_period):
#         # Update level, trend, dan seasonal
#         if i < len(data):
#             value = data[i]
#             last_level = level
#             last_trend = trend
#             level = alpha * (value - seasonal[i % seasonality_period]) + (1 - alpha) * (last_level + last_trend)
#             trend = beta * (level - last_level) + (1 - beta) * last_trend
#             seasonal[i % seasonality_period] = gamma * (value - level) + (1 - gamma) * seasonal[i % seasonality_period]
#             fitted_values.append(level + trend + seasonal[i % seasonality_period])
#         else:
#             # Forecasting
#             forecast_values.append(level + trend + seasonal[i % seasonality_period])
#             # Update level, trend, dan seasonal untuk periode forecast
#             last_level = level
#             last_trend = trend
#             level = last_level + last_trend
#             trend = beta * (level - last_level) + (1 - beta) * last_trend
#             seasonal[i % seasonality_period] = gamma * (forecast_values[-1] - level) + (1 - gamma) * seasonal[i % seasonality_period]

#     return fitted_values, forecast_values

def evaluate_model(data, seasonality_period, alpha, beta, gamma, forecast_period):
    fitted_values, forecast_values = triple_exponential_smoothing(data, seasonality_period, alpha, beta, gamma, forecast_period)
    mse = mean_squared_error(data, fitted_values[:len(data)])
    return mse

# Baca data
engine = use_engine()
query = "SELECT temperature FROM data WHERE esp_id = 'clotgwdgf0000pfmghz30qjlz' ORDER BY createdAt DESC LIMIT 2880 "
df = pd.read_sql(query, engine)

time_series = df['temperature']
time_series = time_series[::-1].reset_index(drop=True)

# Example for daily seasonality
seasonality_period = 28

# Experiment with different parameter values
alpha_values = [0.1, 0.2, 0.3]
beta_values = [0.1, 0.2, 0.3]
gamma_values = [0.1, 0.2, 0.3]

# Set forecast_period
forecast_period = 360

best_mse = float('inf')
best_params = {}

for alpha in alpha_values:
    for beta in beta_values:
        for gamma in gamma_values:
            mse = evaluate_model(time_series, seasonality_period, alpha, beta, gamma, forecast_period)
            if mse < best_mse:
                best_mse = mse
                best_params = {'alpha': alpha, 'beta': beta, 'gamma': gamma}

print("Best Parameters:", best_params)
print("Best MSE:", best_mse)
# Best Parameters
best_alpha = best_params['alpha']
best_beta = best_params['beta']
best_gamma = best_params['gamma']

# Triple Exponential Smoothing with Best Parameters
fitted_values, forecast_values = triple_exponential_smoothing(time_series, seasonality_period, best_alpha, best_beta, best_gamma, forecast_period)

# Print and Plot Forecasted Values
print("Triple Exponential Smoothing Forecast:")
print(forecast_values)
