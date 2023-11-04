import os
import pandas as pd
import pymysql
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from dotenv import load_dotenv

load_dotenv()

def get_forecast_co2(esp_id):
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

    query = "SELECT mq135 FROM dummy"
    # query = f"SELECT mq135 FROM dummy WHERE esp_id = '{esp_id}' ORDER BY timestamp DESC"
    df = pd.read_sql(query, connection)

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

    connection.close()
    return forecast.tolist()