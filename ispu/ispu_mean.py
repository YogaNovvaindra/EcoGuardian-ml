import datetime
import uuid
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.db import use_engine


def get_ispu_mean():
    engine = use_engine()
    connection = engine.connect()

    count_esp = "SELECT id FROM esp"
    df_esp = pd.read_sql(count_esp, engine)
    esp_ids = df_esp["id"].unique()

    ispu = []
    for esp in esp_ids:
        query = f"SELECT mq135_co, pm10, pm25 FROM ispu WHERE esp_id = '{esp}' ORDER BY createdAt DESC LIMIT 1"
        df = pd.read_sql(query, engine)

        ispu.append(df["mq135_co"].values[0])
        # if df pm10 is not null then
        if df["pm10"].isnull().values.any() == False:
            ispu.extend((df["pm10"].values[0], df["pm25"].values[0]))
    mean = sum(ispu) / len(ispu)
    mean = float(mean)

    try:
        now = datetime.datetime.utcnow()
        query_send = text(
            """
            INSERT INTO ispu_mean (id, ispu, createdAt, updatedAt) 
            VALUES (:id, :ispu, :createdAt, :updatedAt)
            """
        )
        connection.execute(
            query_send,
            {
                "id": str(uuid.uuid4()),
                "ispu": mean,
                "createdAt": now,
                "updatedAt": now,
            },
        )
        connection.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        result = f"Error when inserting ispu_mean table : {str(e)}"
    else:
        result = "Success calculating ISPU mean"
    finally:
        connection.close()

    return result
