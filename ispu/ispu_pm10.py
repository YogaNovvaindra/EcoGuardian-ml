import datetime
import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import pandas as pd
from app.db import use_engine


def get_ispu_pm10(esp_id):
    engine = use_engine()
    connection = engine.connect()

    # query = f"SELECT pm10 FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 60"
    query = f"SELECT pm10 FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 1440"
    df = pd.read_sql(query, engine)
    average_pm10 = df["pm10"].mean()
    # print('rata', average_pm10)

    if 0 <= average_pm10 <= 50:
        Ia = 100
        Ib = 50
        Xa = 150
        Xb = 50
        color = "green"
        health_status = "Baik"
    elif 51 <= average_pm10 <= 150:
        Ia = 200
        Ib = 100
        Xa = 350
        Xb = 150
        color = "blue"
        health_status = "Sedang"
    elif 151 <= average_pm10 <= 350:
        Ia = 300
        Ib = 200
        Xa = 420
        Xb = 350
        color = "yellow"
        health_status = "Tidak Sehat"
    elif 351 <= average_pm10 <= 420:
        Ia = 400
        Ib = 300
        Xa = 500
        Xb = 420
        color = "red"
        health_status = "Sangat Tidak Sehat"
    else:
        Ia = 500
        Ib = 500
        Xa = 500
        Xb = 500
        color = "black"
        health_status = "Berbahaya"

    Xx = average_pm10
    I = 500 if Xa == Xb else ((Ia - Ib) / (Xa - Xb)) * (Xx - Xb) + Ib
    
    I = float(I)
    return I, health_status
