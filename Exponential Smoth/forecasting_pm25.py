import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_csv('../Dataset/processed_data.csv')

time_series = df['PM 2.5']  
seasonality_period = 12
alpha = 0.12
beta = 0.012
gamma = 0.12

model = ExponentialSmoothing(
    time_series,
    trend='add',
    seasonal='add',
    seasonal_periods=seasonality_period,
)

model_fit = model.fit(
    smoothing_level=alpha,
    smoothing_trend=beta,
    smoothing_seasonal=gamma,
)

forecast_period = 12
forecast = model_fit.forecast(steps=forecast_period)

print("Triple Exponential Smoothing Forecast:")
print(forecast)

import matplotlib.pyplot as plt

plt.figure(figsize=(5, 6))
plt.plot(time_series, label='Actual Data')
plt.plot(model_fit.fittedvalues, label='Fitted Values', color='orange')
forecast_values = model_fit.forecast(steps=forecast_period)
plt.plot(forecast_values, label='Forecast', color='green')
plt.legend()
plt.title('Triple Exponential Smoothing Forecast for Humidity')
plt.show()
