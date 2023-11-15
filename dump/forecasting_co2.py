import pandas as pd
from app.db import use_engine
from exponen.engine import triple_exponential_smoothing

def get_forecast_co2(esp_id):

    engine = use_engine()
    query = f"SELECT mq135_co2 FROM data WHERE esp_id = '{esp_id}'"
    df = pd.read_sql(query, engine)
    