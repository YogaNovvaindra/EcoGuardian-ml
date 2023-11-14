import pandas as pd
from app.db import use_engine
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def get_forecast_temperature(esp_id):

    engine = use_engine()
    query = "SELECT temperature FROM data"
    # query = f"SELECT mq135 FROM dummy WHERE esp_id = '{esp_id}' ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)

    time_series = df['temperature']

    seasonality_period = 12

    alpha = 0.2
    beta = 0.2
    gamma = 0.2

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

    return forecast.tolist()
