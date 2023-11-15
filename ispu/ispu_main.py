import pandas as pd
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
        esp_ids = df_esp['id'].unique()

        for i in esp_ids:
            query = f"SELECT * FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
            df = pd.read_sql(query, engine)

            if df['pm10'].isnull().values.any() == True:
                get_ispu_co(i)

            else:
                get_ispu_co(i)
                get_ispu_pm25(i)
                get_ispu_pm10(i)
            
    except SQLAlchemyError as e:
        logging.error(e)
        return "Error when updating forecast table : " + str(e)
    else:
        return "Success calculating ISPU"
    finally:
        connection.close()