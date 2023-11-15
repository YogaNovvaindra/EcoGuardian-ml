import pandas as pd
from app.db import use_engine
from exponen.engine import triple_exponential_smoothing

def get_forecast_temperature(esp_id):

    # engine = use_engine()

    # query = f"SELECT temperature FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 12"
    # df = pd.read_sql(query, engine)
    # data = df["data"].tolist()
    # print(data)

    engine = use_engine()
    query = "SELECT * FROM esp"
    df = pd.read_sql(query, engine)
    print(df)


    # forecast_remperature = triple_exponential_smoothing(data, 12, 0.2, 0.2, 0.2, 60)
    # return forecast_remperature

