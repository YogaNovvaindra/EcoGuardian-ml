import datetime
import logging
import uuid
import numpy as np
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine import triple_exponential_smoothing


def reset_forecast():
    engine = use_engine()
    connection = engine.connect()

    try:
        delete_time = datetime.datetime.utcnow()
        delete_time = delete_time + datetime.timedelta(minutes=10)
        delete_future = delete_time + datetime.timedelta(hours=6)
        # query_delete = f"DELETE FROM forecast WHERE esp_id = '{esp_id}' AND createdAt BETWEEN '{delete_time}' AND '{delete_future}'"
        query_delete = text(
            f"DELETE FROM forecast WHERE createdAt BETWEEN :delete_time AND :delete_future"
        )
        result = connection.execute(
            query_delete,
            {
                # "esp_id": esp_id,
                "delete_time": delete_time,
                "delete_future": delete_future,
            },
        )

        connection.commit()
    except SQLAlchemyError as e:
        logging.error(f"Error deleting data from the database: {e}")

    else:
        result = "success delete forecast data"
        return True
    finally:
        connection.close()


def reset_mean_forecast():
    engine = use_engine()
    connection = engine.connect()

    try:
        delete_time = datetime.datetime.utcnow()
        delete_time = delete_time + datetime.timedelta(minutes=10)
        delete_future = delete_time + datetime.timedelta(hours=6)
        query_delete = text(
            f"DELETE FROM forecast_mean WHERE createdAt BETWEEN :delete_time AND :delete_future"
        )
        result = connection.execute(
            query_delete,
            {
                # "esp_id": esp_id,
                "delete_time": delete_time,
                "delete_future": delete_future,
            },
        )

        connection.commit()
    except SQLAlchemyError as e:
        logging.error(f"Error deleting data from the database: {e}")

    else:
        result = "success delete forecast data"
        return True
    finally:
        connection.close()


def reset_ispu_forecast():
    engine = use_engine()
    connection = engine.connect()

    try:
        delete_time = datetime.datetime.utcnow()
        delete_time = delete_time + datetime.timedelta(minutes=10)
        delete_future = delete_time + datetime.timedelta(hours=6)
        query_delete = text(
            f"DELETE FROM ispu_mean_forecast WHERE createdAt BETWEEN :delete_time AND :delete_future"
        )
        result = connection.execute(
            query_delete,
            {
                # "esp_id": esp_id,
                "delete_time": delete_time,
                "delete_future": delete_future,
            },
        )

        connection.commit()
    except SQLAlchemyError as e:
        logging.error(f"Error deleting data from the database: {e}")

    else:
        result = "success delete forecast data"
        return True
    finally:
        connection.close()
