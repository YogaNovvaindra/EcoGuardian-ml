import numpy as np

def triple_exponential_smoothing(data, seasonality_period, alpha, beta, gamma, forecast_period):
    # Inisialisasi level, trend, dan seasonal
    level = data[0]
    trend = 0
    seasonal = np.array(data[:seasonality_period])

    # Inisialisasi variabel hasil
    fitted_values = []
    forecast_values = []
    # round forecast value to 3 decimal places and make it float

    for i in range(len(data) + forecast_period):
        # Update level, trend, dan seasonal
        if i < len(data):
            value = data[i]
            last_level = level
            last_trend = trend
            level = alpha * (value - seasonal[i % seasonality_period]) + (1 - alpha) * (last_level + last_trend)
            trend = beta * (level - last_level) + (1 - beta) * last_trend
            seasonal[i % seasonality_period] = gamma * (value - level) + (1 - gamma) * seasonal[i % seasonality_period]
            fitted_values.append(level + trend + seasonal[i % seasonality_period])
        else:
            # Forecasting
            forecast_values.append(level + trend + seasonal[i % seasonality_period])
            # Update level, trend, dan seasonal untuk periode forecast
            last_level = level
            last_trend = trend
            level = last_level + last_trend
            trend = beta * (level - last_level) + (1 - beta) * last_trend
            seasonal[i % seasonality_period] = gamma * (forecast_values[-1] - level) + (1 - gamma) * seasonal[i % seasonality_period]

    forecast_values = [round(float(i), 3) for i in forecast_values]
    
    return forecast_values