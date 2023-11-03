import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_csv('../Dataset/Gas_Sensors_Measurements1.csv')

time_series = df['MQ135']

seasonality_period = 12

alpha = 0.2
beta = 0.15
gamma = 0.3
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

plt.figure(figsize=(12, 6))
plt.plot(time_series, label='Actual Data')
plt.plot(model_fit.fittedvalues, label='Fitted Values', color='orange')
forecast_values = model_fit.forecast(steps=forecast_period)
plt.plot(forecast_values, label='Forecast', color='green')
plt.legend()
plt.title('Triple Exponential Smoothing Forecast')
plt.show()
