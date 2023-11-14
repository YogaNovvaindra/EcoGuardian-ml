import datetime
import pandas as pd
from app.db import use_engine
from exponen.engine import triple_exponential_smoothing

def get_forecast_temperature(esp_id):

    engine = use_engine()

    query = f"SELECT temperature FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 10080"
    # query = f"SELECT temperature FROM mean ORDER BY createdAt DESC LIMIT 1440"
    df = pd.read_sql(query, engine)
    data = df["temperature"]

    # reverse data but dont reverse index
    data = data[::-1].reset_index(drop=True)
    print(data)

    forecast_temperature = triple_exponential_smoothing(data, 7, 0.2, 0.2, 0.2, 360)
    utc_datetime = datetime.datetime.utcnow()

    # forecast_remperature = triple_exponential_smoothing(data, 12, 0.2, 0.2, 0.2, 60)
    return forecast_temperature

