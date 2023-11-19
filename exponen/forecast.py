import datetime
import logging
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.reset_forecast import reset_forecast, reset_mean_forecast
from exponen.all_forecast import all_forecast, all_forecast_withpm
from exponen.mean_forecast import mean_forecast


def get_forecast():

    engine = use_engine()
    result = []
    # query esp include data
    count_esp = "SELECT id FROM esp"
    df = pd.read_sql(count_esp, engine)
    esp_id = df["id"].unique()

    delete = reset_forecast()
    delete_mean = reset_mean_forecast()

    # print(delete)

    res = mean_forecast(36)
    result.append(res)
    # if delete == True:
    for i in esp_id:
        query = (
            f"SELECT * FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
        )
        df = pd.read_sql(query, engine)

        if df["pm10"].isnull().values.any() == True:
            res = all_forecast(i, 36)
                    # print(result)
        else:
            res = all_forecast_withpm(i, 36)
                    # print(result)
        result.append(res)
    return result