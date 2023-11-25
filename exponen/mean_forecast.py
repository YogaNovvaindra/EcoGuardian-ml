import datetime
import logging
import uuid
import numpy as np
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine import triple_exponential_smoothing


def mean_forecast(forecast_period):
    engine = use_engine()
    connection = engine.connect()

    query = "SELECT temperature, humidity, mq135_co, mq135_co2 FROM mean ORDER BY createdAt DESC LIMIT 10080"
    df = pd.read_sql(query, engine)

    temperature = df["temperature"]
    temperature = temperature.groupby(np.arange(len(temperature)) // 10).mean()
    temperature = temperature[::-1].reset_index(drop=True)
    forecast_temperature = triple_exponential_smoothing(
        temperature, 7, 0.2, 0.2, 0.2, forecast_period
    )

    humidity = df["humidity"]
    humidity = humidity.groupby(np.arange(len(humidity)) // 10).mean()
    humidity = humidity[::-1].reset_index(drop=True)
    forecast_humidity = triple_exponential_smoothing(
        humidity, 7, 0.8, 0.1, 0.1, forecast_period
    )

    mq135_co = df["mq135_co"]
    mq135_co = mq135_co.groupby(np.arange(len(mq135_co)) // 10).mean()
    mq135_co = mq135_co[::-1].reset_index(drop=True)
    forecast_mq135_co = triple_exponential_smoothing(
        mq135_co, 7, 0.9, 0.015, 0.6,forecast_period
    )

    mq135_co2 = df["mq135_co2"]
    mq135_co2 = mq135_co2.groupby(np.arange(len(mq135_co2)) // 10).mean()
    mq135_co2 = mq135_co2[::-1].reset_index(drop=True)
    forecast_mq135_co2 = triple_exponential_smoothing(
        mq135_co2,  7, 0.4, 0.08, 0.04,  forecast_period
    )

    now = datetime.datetime.utcnow()

    for i in range(forecast_period):
        try:
            m_id = str(uuid.uuid4())
            now = now + datetime.timedelta(minutes=10)
            query = text(
                """
                INSERT INTO forecast_mean (id, temperature, humidity, mq135_co, mq135_co2, createdAt, updatedAt)
                VALUES (:id, :temperature, :humidity, :mq135_co, :mq135_co2, :now, :now)
            """
            )
            connection.execute(
                query,
                {
                    "id": m_id,
                    "temperature": forecast_temperature[i],
                    "humidity": forecast_humidity[i],
                    "mq135_co": forecast_mq135_co[i],
                    "mq135_co2": forecast_mq135_co2[i],
                    "now": now,
                },
            )
            connection.commit()
        except SQLAlchemyError as e:
            logging.error(e)
            result = f"Error when inserting forecast table : {str(e)}"
        else:
            result = "Success inserting forecast mean"
            # finally:
            #     connection.close()
    connection.close()
    return result
