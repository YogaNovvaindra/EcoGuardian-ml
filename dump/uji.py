# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from app.db import use_engine

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

# # Baca data
# engine = use_engine()
# query = "SELECT temperature FROM data"
#     # query = f"SELECT mq135 FROM dummy WHERE esp_id = '{esp_id}' ORDER BY timestamp DESC"
# df = pd.read_sql(query, engine)

# time_series = df['temperature']

# # Parameter triple exponential smoothing
# seasonality_period = 12

# alpha = 0.2
# beta = 0.2
# gamma = 0.2

# # Periode forecast
# forecast_period = 12

# # Triple Exponential Smoothing
# fitted_values, forecast_values = triple_exponential_smoothing(time_series, seasonality_period, alpha, beta, gamma, forecast_period)

# print("Triple Exponential Smoothing Forecast:")
# print(forecast_values)
