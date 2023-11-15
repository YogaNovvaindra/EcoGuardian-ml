import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_csv('../Dataset/smoke_detection_iot.csv')

time_series = df['Humidity[%]']  
seasonality_period = 5
alpha = 0.8
beta = 0.1
gamma = 0.1

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

forecast_period = 5
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
