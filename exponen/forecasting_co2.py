import os
import pandas as pd
import numpy as np
import pymysql
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL database connection using environment variables
connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)

# Query to retrieve data from the 'sensor' table
query = "SELECT mq135 FROM dummy"
df = pd.read_sql(query, connection)
connection.close()

time_series = df['mq135']

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
