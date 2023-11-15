import datetime
import logging
import uuid
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine import triple_exponential_smoothing


def get_clean_forecast():
    engine = use_engine()
    connection = engine.connect()

    # update table forecast with state = false and time between now and older
    utc_now = datetime.datetime.utcnow()
    try:
        query = text(
            """
            UPDATE forecast
            SET state = 0
            WHERE state = 1
            AND createdAt < NOW() - INTERVAL 7 HOUR
        """
        )
        connection.execute(query)

        query_del = text(
            "DELETE FROM forecast WHERE createdAt < NOW() - INTERVAL 7 DAY"
        )
        connection.execute(query_del)
        connection.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        return "Error when updating forecast table : " + str(e)
    else:
        return "Success updating forecast table"
    finally:
        connection.close()
