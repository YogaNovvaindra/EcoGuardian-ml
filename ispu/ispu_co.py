import pandas as pd
import matplotlib.pyplot as plt
from app.db import use_engine


def get_ispu_co(esp_id):

    engine = use_engine()
    query = "SELECT mq7 FROM dummy LIMIT 60"
        # query = f"SELECT mq135 FROM dummy WHERE esp_id = '{esp_id}' ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)

    average_co = df['mq7'].mean()

    if 0 <= average_co <= 50:
        Ia = 100
        Ib = 50
        Xa = 8000
        Xb = 4000
        color = 'green'
        health_status = 'Baik'
    elif 51 <= average_co <= 100:
        Ia = 200
        Ib = 100
        Xa = 15000
        Xb = 8000
        color = 'blue'
        health_status = 'Sedang'
    elif 101 <= average_co <= 200:
        Ia = 300
        Ib = 200
        Xa = 30000
        Xb = 15000
        color = 'yellow'
        health_status = 'Tidak Sehat'
    elif 201 <= average_co <= 300:
        Ia = 400
        Ib = 300
        Xa = 45000
        Xb = 30000
        color = 'red'
        health_status = 'Sangat Tidak Sehat'
    else:
        Ia = 500
        Ib = 500
        Xa = 50000
        Xb = 45000
        color = 'black'
        health_status = 'Berbahaya'


    Xx = average_co
    I = ((Ia - Ib) / (Xa - Xb)) * (Xx - Xb) + Ib
    return I