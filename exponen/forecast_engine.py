import datetime
import logging
import uuid
import numpy as np
import pandas as pd
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from exponen.engine_msd import triple_exponential_smoothing


def get_forecast_engine(esp_id= 'closr23sr0002o90jflxpzrlf', forecast_period=36):
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
        mq135_co, 7, 0.8, 0.01, 0.8, forecast_period
    )

    # mq135_alcohol = df["mq135_alcohol"]
    # mq135_alcohol = mq135_alcohol[::-1].reset_index(drop=True)
    # forecast_mq135_alcohol = triple_exponential_smoothing(mq135_alcohol, 7, 0.2, 0.2, 0.2, forecast_period)

    mq135_co2 = df["mq135_co2"]
    mq135_co2 = mq135_co2.groupby(np.arange(len(mq135_co2)) // 10).mean()
    mq135_co2 = mq135_co2[::-1].reset_index(drop=True)
    forecast_mq135_co2 = triple_exponential_smoothing(
        mq135_co2, 7, 0.8, 0.01, 0.8, forecast_period
    )
    return forecast_temperature, forecast_humidity, forecast_mq135_co, forecast_mq135_co2

def forecast_withpm(esp_id= 'cloodu0dk0000pff06r0pacus', forecast_period=36):
    engine = use_engine()
    connection = engine.connect()

    query = f"SELECT * FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 10080"
    # query = f"SELECT temperature FROM mean ORDER BY createdAt DESC LIMIT 1440"
    df = pd.read_sql(query, engine)
    pm10 = df["pm10"]
    pm10 = pm10.groupby(np.arange(len(pm10)) // 10).mean()
    pm10 = pm10[::-1].reset_index(drop=True)
    forecast_pm10 = triple_exponential_smoothing(
        pm10, 7,  0.9, 0.009, 0.6, forecast_period
    )

    pm25 = df["pm25"]
    pm25 = pm25.groupby(np.arange(len(pm25)) // 10).mean()
    pm25 = pm25[::-1].reset_index(drop=True)
    forecast_pm25 = triple_exponential_smoothing(
        pm25, 7, 0.8, 0.016, 0.8, forecast_period
    )
    
    return forecast_pm10, forecast_pm25

def get_ispu_forecast_engine(forecast_period=36):
    

    engine = use_engine()
    connection = engine.connect()

    query = "SELECT ispu FROM ispu_mean ORDER BY createdAt DESC LIMIT 10080"
    df = pd.read_sql(query, engine)
    
    ispu = df["ispu"]
    ispu = ispu.groupby(np.arange(len(ispu)) // 10).mean()
    ispu = ispu[::-1].reset_index(drop=True)
    forecast_ispu = triple_exponential_smoothing(
        ispu, 7, 0.8, 0.01, 0.8, forecast_period
    )
    return forecast_ispu