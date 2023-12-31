import datetime
import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import pandas as pd
from app.db import use_engine


def get_ispu_co(esp_id):
    engine = use_engine()
    connection = engine.connect()
    # query = f"SELECT mq135_co FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 60"
    query = f"SELECT mq135_co FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 1440"
    df = pd.read_sql(query, engine)

    average = df["mq135_co"].mean()

    # print(average)
    berat_molekul_CO = 28.01  # Berat molekul CO dalam g/mol
    volume_molar_CO = 24.5  # Volume molar CO dalam L/mol
    pangkat = 1000
    average_co = ((average * berat_molekul_CO) / volume_molar_CO) * pangkat
    # print(average_co)

    if 0 <= average_co <= 4000:
        Ia = 100
        Ib = 50
        Xa = 8000
        Xb = 4000
        color = "green"
        health_status = "Baik"

    elif 4000 <= average_co <= 8000:
        Ia = 200
        Ib = 100
        Xa = 15000
        Xb = 8000
        color = "blue"
        health_status = "Sedang"
    elif 8000 <= average_co <= 15000:
        Ia = 300
        Ib = 200
        Xa = 30000
        Xb = 15000
        color = "yellow"
        health_status = "Tidak Sehat"
    elif 15000 <= average_co <= 30000:
        Ia = 400
        Ib = 300
        Xa = 45000
        Xb = 30000
        color = "red"
        health_status = "Sangat Tidak Sehat"
    else:
        Ia = 500
        Ib = 500
        Xa = 50000
        Xb = 45000
        color = "black"
        health_status = "Berbahaya"

    Xx = average_co
    I = 500 if Xa == Xb else ((Ia - Ib) / (Xa - Xb)) * (Xx - Xb) + Ib
    
    I = float(I)

    return I, health_status
