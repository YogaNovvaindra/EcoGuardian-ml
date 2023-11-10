import pandas as pd
import matplotlib.pyplot as plt
from app.db import use_engine


def get_ispu_pm25(esp_id):

    engine = use_engine()
    query = "SELECT pm25 FROM dummy LIMIT 60"
        # query = f"SELECT mq135 FROM dummy WHERE esp_id = '{esp_id}' ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)
    average_pm25 = df['pm25'].mean()

    if 0 <= average_pm25 <= 50:
        Ia = 100
        Ib = 50
        Xa = 55.4
        Xb = 15.5
        color = 'green'
        health_status = 'Baik'
    elif 51 <= average_pm25 <= 100:
        Ia = 200
        Ib = 100
        Xa = 150.4
        Xb = 55.4
        color = 'blue'
        health_status = 'Sedang'
    elif 101 <= average_pm25 <= 200:
        Ia = 300
        Ib = 200
        Xa = 250.4
        Xb = 150.4
        color = 'yellow'
        health_status = 'Tidak Sehat'
    elif 201 <= average_pm25 <= 300:
        Ia = 400
        Ib = 300
        Xa = 500
        Xb = 250.4
        color = 'red'
        health_status = 'Sangat Tidak Sehat'
    else:
        Ia = 500
        Ib = 500
        Xa = 500
        Xb = 500
        color = 'black'
        health_status = 'Berbahaya'


    Xx = average_pm25
    I = ((Ia - Ib) / (Xa - Xb)) * (Xx - Xb) + Ib

    return I

