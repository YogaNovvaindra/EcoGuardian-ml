import numpy as np

def triple_exponential_smoothing(data, seasonality_period, alpha, beta, gamma, forecast_period):
    # Initialization of level, trend, and seasonal
    level = data[0]
    trend = 0
    seasonal = np.array(data[:seasonality_period])

    # Initialization of result variables
    fitted_values = []
    forecast_values = []
    actual_values = []  

    for i in range(len(data) + forecast_period):
        # Update level, trend, and seasonal
        if i < len(data):
            value = data[i]
            last_level = level
            last_trend = trend
            last_seasonal = seasonal[i % seasonality_period]
            
            # Update level
            level = alpha * (value - last_seasonal) + (1 - alpha) * (last_level + last_trend)
            
            # Update trend
            trend = beta * (level - last_level) + (1 - beta) * last_trend
            
            # Update seasonal
            seasonal[i % seasonality_period] = gamma * (value - level) + (1 - gamma) * last_seasonal
            
            # Save fitted values
            fitted_values.append(level + trend + seasonal[i % seasonality_period])

            # Save actual values
            actual_values.append(value)
        else:
            # Forecasting
            # Update level, trend, and seasonal for the forecast period
            last_level = level
            last_trend = trend
            last_seasonal = seasonal[i % seasonality_period]
            
            # Forecast value initialization
            forecast_value = level + trend + seasonal[i % seasonality_period]
            forecast_values.append(forecast_value)
            
            # Update level, trend, and seasonal for the forecast period
            level = last_level + last_trend
            trend = beta * (level - last_level) + (1 - beta) * last_trend
            seasonal[i % seasonality_period] = gamma * (value - level) + (1 - gamma) * last_seasonal

            # Save forecasted values
            fitted_values.append(forecast_value)

    # Calculate Mean Squared Deviation (MSD)
    if len(actual_values) > 0:
        msd = sum((actual - fitted) ** 2 for actual, fitted in zip(actual_values, fitted_values[:len(actual_values)])) / len(actual_values)
    else:
        msd = 0  # or handle this case according to your requirements

    actual_values = np.array(actual_values)
    fitted_values = np.array(fitted_values[:len(actual_values)])

    # Calculate Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual_values - fitted_values) / actual_values)) * 100

    # Calculate Mean Absolute Deviation (MAD)
    mad = np.mean(np.abs(actual_values - fitted_values))

    forecast_values = [round(float(i), 3) for i in forecast_values]

    return forecast_values, msd, mape, mad

# Example usage:
# forecast_values, msd, mape, mad = triple_exponential_smoothing(data, seasonality_period, alpha, beta, gamma, forecast_period)
