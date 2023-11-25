import datetime
import logging
import uuid
import numpy as np
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine import triple_exponential_smoothing
from exponen.reset_forecast import reset_ispu_forecast


def get_ispu_forecast(forecast_period):
    
    del_ispu_forecast = reset_ispu_forecast()
    engine = use_engine()
    connection = engine.connect()

    query = "SELECT ispu FROM ispu_mean ORDER BY createdAt DESC LIMIT 10080"
    df = pd.read_sql(query, engine)
    
    ispu = df["ispu"]
    ispu = ispu.groupby(np.arange(len(ispu)) // 10).mean()
    ispu = ispu[::-1].reset_index(drop=True)
    forecast_ispu = triple_exponential_smoothing(
        ispu, 7, 0.4, 0.1, 0.1, forecast_period
    )

    now = datetime.datetime.utcnow()

    for i in range(forecast_period):
        try:
            m_id = str(uuid.uuid4())
            now = now + datetime.timedelta(minutes=10)
            query = text(
                """
                INSERT INTO ispu_mean_forecast (id, ispu, createdAt, updatedAt) 
                VALUES (:id, :ispu, :createdAt, :updatedAt)
            """
            )
            connection.execute(
                query,
                {
                    "id": m_id,
                    "ispu": forecast_ispu[i],
                    "createdAt": now,
                    "updatedAt": now,
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
