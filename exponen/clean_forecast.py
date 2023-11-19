import logging
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


def get_clean_forecast():
    all_clean = clean_forecast()
    all_clean_mean = clean_forecast_mean()
    return all_clean, all_clean_mean


def clean_forecast():
    engine = use_engine()
    connection = engine.connect()

    # update table forecast with state = false and time between now and older
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
        return f"Error when updating forecast table : {str(e)}"
    else:
        return "Success updating forecast table"
    finally:
        connection.close()


def clean_forecast_mean():
    engine = use_engine()
    connection = engine.connect()

    # update table forecast with state = false and time between now and older
    try:
        query = text(
            """
            UPDATE forecast_mean
            SET state = 0
            WHERE state = 1
            AND createdAt < NOW() - INTERVAL 7 HOUR
        """
        )
        connection.execute(query)

        query_del = text(
            "DELETE FROM forecast_mean WHERE createdAt < NOW() - INTERVAL 7 DAY"
        )
        connection.execute(query_del)
        connection.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        return f"Error when updating forecast_mean table : {str(e)}"
    else:
        return "Success updating forecast_mean table"
    finally:
        connection.close()
