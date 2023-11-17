import datetime
import uuid
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.db import use_engine
from ispu.ispu_co import get_ispu_co
from ispu.ispu_pm25 import get_ispu_pm25
from ispu.ispu_pm10 import get_ispu_pm10


def get_ispu():
    engine = use_engine()
    connection = engine.connect()

    try:
        count_esp = "SELECT id FROM esp"
        df_esp = pd.read_sql(count_esp, engine)
        esp_ids = df_esp["id"].unique()

        now = datetime.datetime.utcnow()
        for i in esp_ids:
            query = f"SELECT * FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
            df = pd.read_sql(query, engine)

            if df["pm10"].isnull().values.any() == True:
                co = get_ispu_co(i)

                ispu_id = str(uuid.uuid4())

                try:
                    query_send = text(
                        """
                        INSERT INTO ispu (id, esp_id, mq135_co, createdAt, updatedAt) 
                        VALUES (:id, :esp_id, :mq135_co, :createdAt, :updatedAt)
                        """
                    )
                    connection.execute(
                        query_send,
                        {
                            "id": ispu_id,
                            "esp_id": i,
                            "mq135_co": co[0],
                            "createdAt": now,
                            "updatedAt": now,
                        },
                    )
                    connection.commit()
                except SQLAlchemyError as e:
                    logging.error(e)
                    result = f"Error when inserting ispu table : {str(e)}"
                else :
                    result = "Success calculating ISPU"

            else:
                co = get_ispu_co(i)
                pm25 = get_ispu_pm25(i)
                pm10 = get_ispu_pm10(i)

                ispu_id = str(uuid.uuid4())

                try:
                    query_send = text(
                        """
                        INSERT INTO ispu (id, esp_id, mq135_co, pm25, pm10, createdAt, updatedAt) 
                        VALUES (:id, :esp_id, :mq135_co, :pm25, :pm10, :createdAt, :updatedAt)
                        """
                    )
                    connection.execute(
                        query_send,
                        {
                            "id": ispu_id,
                            "esp_id": i,
                            "mq135_co": co[0],
                            "pm25": pm25[0],
                            "pm10": pm10[0],
                            "createdAt": now,
                            "updatedAt": now,
                        },
                    )
                    connection.commit()
                except SQLAlchemyError as e:
                    logging.error(e)
                    result = f"Error when inserting ispu table : {str(e)}"
                else :
                    result = "Success calculating ISPU"

    except SQLAlchemyError as e:
        logging.error(e)
        return f"Error when updating forecast table : {str(e)}"
    else:
        return f"Success calculating ISPU: {str(result)}"
    finally:
        connection.close()
        
