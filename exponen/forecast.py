import datetime
import logging
import time
import uuid
import numpy as np
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine import triple_exponential_smoothing


def forecast(esp_id, forecast_period):
    engine = use_engine()
    connection = engine.connect()

    query = f"SELECT * FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 10080"
    # query = f"SELECT temperature FROM mean ORDER BY createdAt DESC LIMIT 1440"
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
        mq135_co, 7, 0.2, 0.2, 0.2, forecast_period
    )

    # mq135_alcohol = df["mq135_alcohol"]
    # mq135_alcohol = mq135_alcohol[::-1].reset_index(drop=True)
    # forecast_mq135_alcohol = triple_exponential_smoothing(mq135_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    mq135_co2 = df["mq135_co2"]
    mq135_co2 = mq135_co2.groupby(np.arange(len(mq135_co2)) // 10).mean()
    mq135_co2 = mq135_co2[::-1].reset_index(drop=True)
    forecast_mq135_co2 = triple_exponential_smoothing(
        mq135_co2, 7, 0.2, 0.15, 0.3, forecast_period
    )

    # mq135_toluen = df["mq135_toluen"]
    # mq135_toluen = mq135_toluen[::-1].reset_index(drop=True)
    # forecast_mq135_toluen = triple_exponential_smoothing(mq135_toluen, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq135_nh4 = df["mq135_nh4"]
    # mq135_nh4 = mq135_nh4[::-1].reset_index(drop=True)
    # forecast_mq135_nh4 = triple_exponential_smoothing(mq135_nh4, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq135_aceton = df["mq135_aceton"]
    # mq135_aceton = mq135_aceton[::-1].reset_index(drop=True)
    # forecast_mq135_aceton = triple_exponential_smoothing(mq135_aceton, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_h2 = df["mq2_h2"]
    # mq2_h2 = mq2_h2[::-1].reset_index(drop=True)
    # forecast_mq2_h2 = triple_exponential_smoothing(mq2_h2, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_lpg = df["mq2_lpg"]
    # mq2_lpg = mq2_lpg[::-1].reset_index(drop=True)
    # forecast_mq2_lpg = triple_exponential_smoothing(mq2_lpg, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_co = df["mq2_co"]
    # mq2_co = mq2_co.groupby(np.arange(len(mq2_co)) // 10).mean()
    # mq2_co = mq2_co[::-1].reset_index(drop=True)
    # forecast_mq2_co = triple_exponential_smoothing(
    #     mq2_co, 7, 0.8, 0.2, 0.1, forecast_period
    # )

    # mq2_alcohol = df["mq2_alcohol"]
    # mq2_alcohol = mq2_alcohol[::-1].reset_index(drop=True)
    # forecast_mq2_alcohol = triple_exponential_smoothing(mq2_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_propane = df["mq2_propane"]
    # mq2_propane = mq2_propane[::-1].reset_index(drop=True)
    # forecast_mq2_propane = triple_exponential_smoothing(mq2_propane, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_h2 = df["mq7_h2"]
    # mq7_h2 = mq7_h2[::-1].reset_index(drop=True)
    # forecast_mq7_h2 = triple_exponential_smoothing(mq7_h2, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_lpg = df["mq7_lpg"]
    # mq7_lpg = mq7_lpg[::-1].reset_index(drop=True)
    # forecast_mq7_lpg = triple_exponential_smoothing(mq7_lpg, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_ch4 = df["mq7_ch4"]
    # mq7_ch4 = mq7_ch4[::-1].reset_index(drop=True)
    # forecast_mq7_ch4 = triple_exponential_smoothing(mq7_ch4, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_co = df["mq7_co"]
    # mq7_co = mq7_co[::-1].reset_index(drop=True)
    # forecast_mq7_co = triple_exponential_smoothing(mq7_co, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_alcohol = df["mq7_alcohol"]
    # mq7_alcohol = mq7_alcohol[::-1].reset_index(drop=True)
    # forecast_mq7_alcohol = triple_exponential_smoothing(mq7_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    utc_datetime = datetime.datetime.utcnow()
    # utc_datetime = utc_datetime - datetime.timedelta(minutes=30)
    for i in range(forecast_period):
        try:
            # delete data forecast between now+1min and now+3hours

            forecast_id = str(uuid.uuid4())
            utc_datetime = utc_datetime + datetime.timedelta(minutes=10)
            query = text(
                """
                INSERT INTO forecast (id, esp_id, temperature, humidity, mq135_co, mq135_co2, createdAt, updatedAt) 
                VALUES (:forecast_id, :esp_id, :forecast_temperature, :forecast_humidity, :forecast_mq135_co, :forecast_mq135_co2, :utc_datetime, :utc_datetime)
            """
            )
            connection.execute(
                query,
                {
                    "forecast_id": forecast_id,
                    "esp_id": esp_id,
                    "forecast_temperature": forecast_temperature[i],
                    "forecast_humidity": forecast_humidity[i],
                    "forecast_mq135_co": forecast_mq135_co[i],
                    # "forecast_mq135_alcohol": forecast_mq135_alcohol[i],
                    "forecast_mq135_co2": forecast_mq135_co2[i],
                    # "forecast_mq135_toluen": forecast_mq135_toluen[i],
                    # "forecast_mq135_nh4": forecast_mq135_nh4[i],
                    # "forecast_mq135_aceton": forecast_mq135_aceton[i],
                    # "forecast_mq2_h2": forecast_mq2_h2[i],
                    # "forecast_mq2_lpg": forecast_mq2_lpg[i],
                    # "forecast_mq2_co": forecast_mq2_co[i],
                    # "forecast_mq2_alcohol": forecast_mq2_alcohol[i],
                    # "forecast_mq2_propane": forecast_mq2_propane[i],
                    # "forecast_mq7_h2": forecast_mq7_h2[i],
                    # "forecast_mq7_lpg": forecast_mq7_lpg[i],
                    # "forecast_mq7_ch4": forecast_mq7_ch4[i],
                    # "forecast_mq7_co": forecast_mq7_co[i],
                    # "forecast_mq7_alcohol": forecast_mq7_alcohol[i],
                    "utc_datetime": utc_datetime,
                },
            )
            connection.commit()

        except SQLAlchemyError as e:
            logging.error(f"Error inserting data into the database: {e}")
            result = "error forecast data"
        else:
            result = "success forecast data"
        # finally:
        #     connection.close()
    return result


def forecast_withpm(esp_id, forecast_period):
    engine = use_engine()
    connection = engine.connect()

    query = f"SELECT * FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 10080"
    # query = f"SELECT temperature FROM mean ORDER BY createdAt DESC LIMIT 1440"
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
        mq135_co, 7, 0.2, 0.2, 0.2, forecast_period
    )

    # mq135_alcohol = df["mq135_alcohol"]
    # mq135_alcohol = mq135_alcohol[::-1].reset_index(drop=True)
    # forecast_mq135_alcohol = triple_exponential_smoothing(mq135_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    mq135_co2 = df["mq135_co2"]
    mq135_co2 = mq135_co2.groupby(np.arange(len(mq135_co2)) // 10).mean()
    mq135_co2 = mq135_co2[::-1].reset_index(drop=True)
    forecast_mq135_co2 = triple_exponential_smoothing(
        mq135_co2, 7, 0.2, 0.15, 0.3, forecast_period
    )

    # mq135_toluen = df["mq135_toluen"]
    # mq135_toluen = mq135_toluen[::-1].reset_index(drop=True)
    # forecast_mq135_toluen = triple_exponential_smoothing(mq135_toluen, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq135_nh4 = df["mq135_nh4"]
    # mq135_nh4 = mq135_nh4[::-1].reset_index(drop=True)
    # forecast_mq135_nh4 = triple_exponential_smoothing(mq135_nh4, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq135_aceton = df["mq135_aceton"]
    # mq135_aceton = mq135_aceton[::-1].reset_index(drop=True)
    # forecast_mq135_aceton = triple_exponential_smoothing(mq135_aceton, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_h2 = df["mq2_h2"]
    # mq2_h2 = mq2_h2[::-1].reset_index(drop=True)
    # forecast_mq2_h2 = triple_exponential_smoothing(mq2_h2, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_lpg = df["mq2_lpg"]
    # mq2_lpg = mq2_lpg[::-1].reset_index(drop=True)
    # forecast_mq2_lpg = triple_exponential_smoothing(mq2_lpg, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_co = df["mq2_co"]
    # mq2_co = mq2_co.groupby(np.arange(len(mq2_co)) // 10).mean()
    # mq2_co = mq2_co[::-1].reset_index(drop=True)
    # forecast_mq2_co = triple_exponential_smoothing(
    #     mq2_co, 7, 0.8, 0.2, 0.1, forecast_period
    # )

    # mq2_alcohol = df["mq2_alcohol"]
    # mq2_alcohol = mq2_alcohol[::-1].reset_index(drop=True)
    # forecast_mq2_alcohol = triple_exponential_smoothing(mq2_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq2_propane = df["mq2_propane"]
    # mq2_propane = mq2_propane[::-1].reset_index(drop=True)
    # forecast_mq2_propane = triple_exponential_smoothing(mq2_propane, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_h2 = df["mq7_h2"]
    # mq7_h2 = mq7_h2[::-1].reset_index(drop=True)
    # forecast_mq7_h2 = triple_exponential_smoothing(mq7_h2, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_lpg = df["mq7_lpg"]
    # mq7_lpg = mq7_lpg[::-1].reset_index(drop=True)
    # forecast_mq7_lpg = triple_exponential_smoothing(mq7_lpg, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_ch4 = df["mq7_ch4"]
    # mq7_ch4 = mq7_ch4[::-1].reset_index(drop=True)
    # forecast_mq7_ch4 = triple_exponential_smoothing(mq7_ch4, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_co = df["mq7_co"]
    # mq7_co = mq7_co[::-1].reset_index(drop=True)
    # forecast_mq7_co = triple_exponential_smoothing(mq7_co, 7, 0.2, 0.2, 0.2, forecast_period)

    # mq7_alcohol = df["mq7_alcohol"]
    # mq7_alcohol = mq7_alcohol[::-1].reset_index(drop=True)
    # forecast_mq7_alcohol = triple_exponential_smoothing(mq7_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    pm10 = df["pm10"]
    pm10 = pm10.groupby(np.arange(len(pm10)) // 10).mean()
    pm10 = pm10[::-1].reset_index(drop=True)
    forecast_pm10 = triple_exponential_smoothing(
        pm10, 7, 0.2, 0.2, 0.2, forecast_period
    )

    pm25 = df["pm25"]
    pm25 = pm25.groupby(np.arange(len(pm25)) // 10).mean()
    pm25 = pm25[::-1].reset_index(drop=True)
    forecast_pm25 = triple_exponential_smoothing(
        pm25, 7, 0.2, 0.2, 0.2, forecast_period
    )

    utc_datetime = datetime.datetime.utcnow()
    # utc_datetime = utc_datetime - datetime.timedelta(minutes=30)
    # delete data forecast between now+1min and now+3hours
    for i in range(forecast_period):
        try:
            forecast_id = str(uuid.uuid4())
            utc_datetime = utc_datetime + datetime.timedelta(minutes=10)
            query = text(
                """
                INSERT INTO forecast (id, esp_id, temperature, humidity, mq135_co, mq135_co2,  pm10, pm25, createdAt, updatedAt) 
                VALUES (:forecast_id, :esp_id, :forecast_temperature, :forecast_humidity, :forecast_mq135_co, :forecast_mq135_co2, :forecast_pm10, :forecast_pm25, :utc_datetime, :utc_datetime)
            """
            )
            connection.execute(
                query,
                {
                    "forecast_id": forecast_id,
                    "esp_id": esp_id,
                    "forecast_temperature": forecast_temperature[i],
                    "forecast_humidity": forecast_humidity[i],
                    "forecast_mq135_co": forecast_mq135_co[i],
                    # "forecast_mq135_alcohol": forecast_mq135_alcohol[i],
                    "forecast_mq135_co2": forecast_mq135_co2[i],
                    # "forecast_mq135_toluen": forecast_mq135_toluen[i],
                    # "forecast_mq135_nh4": forecast_mq135_nh4[i],
                    # "forecast_mq135_aceton": forecast_mq135_aceton[i],
                    # "forecast_mq2_h2": forecast_mq2_h2[i],
                    # "forecast_mq2_lpg": forecast_mq2_lpg[i],
                    # "forecast_mq2_co": forecast_mq2_co[i],
                    # "forecast_mq2_alcohol": forecast_mq2_alcohol[i],
                    # "forecast_mq2_propane": forecast_mq2_propane[i],
                    # "forecast_mq7_h2": forecast_mq7_h2[i],
                    # "forecast_mq7_lpg": forecast_mq7_lpg[i],
                    # "forecast_mq7_ch4": forecast_mq7_ch4[i],
                    # "forecast_mq7_co": forecast_mq7_co[i],
                    # "forecast_mq7_alcohol": forecast_mq7_alcohol[i],
                    "forecast_pm10": forecast_pm10[i],
                    "forecast_pm25": forecast_pm25[i],
                    "utc_datetime": utc_datetime,
                },
            )
            connection.commit()

        except SQLAlchemyError as e:
            logging.error(f"Error inserting data into the database: {e}")
            result = "error forecast data"
        else:
            result = "success forecast data"
        # finally:
        #     connection.close()
    return result


def del_forecast():
    engine = use_engine()
    connection = engine.connect()

    try:
        delete_time = datetime.datetime.utcnow()
        delete_time = delete_time + datetime.timedelta(minutes=10)
        delete_3h = delete_time + datetime.timedelta(hours=6)
        # query_delete = f"DELETE FROM forecast WHERE esp_id = '{esp_id}' AND createdAt BETWEEN '{delete_time}' AND '{delete_3h}'"
        query_delete = text(
            f"DELETE FROM forecast WHERE createdAt BETWEEN :delete_time AND :delete_3h"
        )
        result = connection.execute(
            query_delete,
            {
                # "esp_id": esp_id,
                "delete_time": delete_time,
                "delete_3h": delete_3h,
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


def get_forecast():
    engine = use_engine()
    # query esp include data
    count_esp = "SELECT id FROM esp"
    df = pd.read_sql(count_esp, engine)
    esp_id = df["id"].unique()

    delete = del_forecast()
    # print(delete)

    # if delete == True:
    for i in esp_id:
        query = (
            f"SELECT * FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
        )
        df = pd.read_sql(query, engine)

        if df["pm10"].isnull().values.any() == True:
            result = forecast(i, 18)
            # print(result)
        else:
            result = forecast_withpm(i, 18)
            # print(result)

    return "success forecast data"
