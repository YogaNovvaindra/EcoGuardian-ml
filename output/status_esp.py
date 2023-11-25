from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import datetime
import pandas as pd
from app.db import use_engine
import uuid

def get_status_esp():
    engine = use_engine()
    connection = engine.connect()
    
    query = "SELECT id, status FROM esp"
    espdata = pd.read_sql(query, engine)
    esp_id = espdata["id"].unique()
    
    result = []
    
    for esp in esp_id:
        query = f"SELECT * FROM data WHERE esp_id = '{esp}' ORDER BY createdAt DESC LIMIT 1"
        df = pd.read_sql(query, engine)
        
        now = datetime.datetime.utcnow()
        now -= datetime.timedelta(minutes=5)
        
        if pd.to_datetime(df["createdAt"].values[0]) < now:
            if espdata.loc[espdata["id"] == esp, "status"].values[0] == 0:
                result.append(f"ESP {esp} is OFF")
            else:
                try:
                    query_send = text(
                        """
                        UPDATE esp SET status = :status WHERE id = :id
                        """
                    )
                    connection.execute(
                        query_send,
                        {
                            "id": esp,
                            "status": 0,
                        },
                    )
                    connection.commit()
                except SQLAlchemyError as e:
                    logging.error(e)
                    result.append(f"Error when updating esp table : {str(e)}")
                else:
                    result.append(f"Success updating esp table: {esp} to OFF")
                # finally:
                #     connection.close()
        else:
            if espdata.loc[espdata["id"] == esp, "status"].values[0] == 1:
                result.append(f"ESP {esp} is ON")
            else:
                try:
                    query_send = text(
                        """
                        UPDATE esp SET status = :status WHERE id = :id
                        """
                    )
                    connection.execute(
                        query_send,
                        {
                            "id": esp,
                            "status": 1,
                        },
                    )
                    connection.commit()
                except SQLAlchemyError as e:
                    logging.error(e)
                    result.append(f"Error when updating esp table : {str(e)}")
                else:
                    result.append(f"Success updating esp table: {esp} to ON")
                # finally:
                #     connection.close()
    
    connection.close()
    return result
    
        