import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import datetime
from app.db import use_engine
import uuid


def get_ispu_co2():

    engine = use_engine()
    connection = engine.connect()
    
    try:
        count_esp = "SELECT id FROM esp"
        df_esp = pd.read_sql(count_esp, engine)
        esp_ids = df_esp['id'].unique()

        for esp_id in esp_ids:
            query = f"SELECT * FROM data WHERE esp_id = '{esp_id}' ORDER BY createdAt DESC LIMIT 60;"
            df_data = pd.read_sql(query, engine)

            average_co2 = df_data['mq135_co2'].mean()
            average_co = df_data['mq2_co'].mean()

            # average_pm25 = df['pm25'].mean()
            # print(average_pm25)

            if 0 <= average_co2 <= 50:
                Ia = 100
                Ib = 50
                Xa = 8000
                Xb = 4000
                color = 'green'
                health_status = 'Good'
            elif 51 <= average_co2 <= 100:
                Ia = 200
                Ib = 100
                Xa = 15000
                Xb = 8000
                color = 'blue'
                health_status = 'Average'
            elif 101 <= average_co2 <= 200:
                Ia = 300
                Ib = 200
                Xa = 30000
                Xb = 15000
                color = 'yellow'
                health_status = 'Unhealthy'
            elif 201 <= average_co2 <= 300:
                Ia = 400
                Ib = 300
                Xa = 45000
                Xb = 30000
                color = 'red'
                health_status = 'Very Unhealthy'
            else:
                Ia = 500
                Ib = 500
                Xa = 50000
                Xb = 45000
                color = 'black'
                health_status = 'Dangerous'

            # if 0 <= average_pm25 <= 50:
            #     Iapm25 = 100
            #     Ibpm25 = 50
            #     Xapm25 = 55.4
            #     Xbpm25 = 15.5
            #     color = 'green'
            #     health_statuspm25 = 'Good'
            # elif 51 <= average_pm25 <= 100:
            #     Iapm25 = 200
            #     Ibpm25 = 100
            #     Xapm25 = 150.4
            #     Xbpm25 = 55.4
            #     color = 'blue'
            #     health_statuspm25 = 'Average'
            # elif 101 <= average_pm25 <= 200:
            #     Iapm25 = 300
            #     Ibpm25 = 200
            #     Xapm25 = 250.4
            #     Xbpm25 = 150.4
            #     color = 'yellow'
            #     health_statuspm25 = 'Unhealthy'
            # elif 201 <= average_pm25 <= 300:
            #     Iapm25 = 400
            #     Ibpm25 = 300
            #     Xapm25 = 500
            #     Xbpm25 = 250.4
            #     color = 'red'
            #     health_statuspm25 = 'Very Unhealthy'
            # else:
            #     Iapm25 = 500
            #     Ibpm25 = 500
            #     Xapm25 = 500
            #     Xbpm25 = 500
            #     color = 'black'
            #     health_statuspm25 = 'Dangerous'

            if 0 <= average_co <= 50:
                Iaco = 100
                Ibco = 50
                Xaco = 8000
                Xbco = 4000
                color = 'green'
                health_statusco = 'Good'
            elif 51 <= average_co <= 100:
                Iaco = 200
                Ibco = 100
                Xaco = 15000
                Xbco = 8000
                color = 'blue'
                health_statusco = 'Average'
            elif 101 <= average_co <= 200:
                Iaco = 300
                Ibco = 200
                Xaco = 30000
                Xbco = 15000
                color = 'yellow'
                health_statusco = 'Unhealthy'
            elif 201 <= average_co <= 300:
                Iaco = 400
                Ibco = 300
                Xaco = 45000
                Xbco = 30000
                color = 'red'
                health_statusco = 'Very Unhealthy'
            else:
                Iaco = 500
                Ibco = 500
                Xaco = 50000
                Xbco = 45000
                color = 'black'
                health_statusco = 'Dangerous'
                
            Xxco2 = average_co2
            Xxco = average_co
            # Xxpm25 = average_pm25
            Ico2 = ((Ia - Ib) / (Xa - Xb)) * (Xxco2 - Xb) + Ib
            Ico = ((Iaco - Ibco)/ (Xaco - Xbco))* (Xxco - Xbco) +Ibco
            # Ipm25 = ((Iapm25 - Ibpm25)/ (Xapm25 - Xbpm25))* (Xxpm25 - Xbpm25) +Ibpm25
            utc_datetime = datetime.datetime.utcnow()
            
            try:
                # generate id using uuid
                ispu_id = str(uuid.uuid4())
                query = text("INSERT INTO ispu (id, esp_id, nilai_ispu, text_ispu, jenis_gas, createdAt, updatedAt) VALUES (:ispu_id, :esp_id, :nilai_ispu, :text_ispu, :jenis_gas, :utc_datetime, :utc_datetime)")
                connection.execute(query, {
                    'ispu_id': ispu_id,
                    'esp_id': esp_id,
                    'nilai_ispu': Ico2,
                    'text_ispu': health_status,
                    'jenis_gas': 'mq135_co2',
                    'utc_datetime': utc_datetime,
                })
            except SQLAlchemyError as e:
                logging.error(f"Error inserting data into the database: {e}")

            try:
                # generate id using uuid
                ispu_id = str(uuid.uuid4())
                query = text("INSERT INTO ispu (id, esp_id, nilai_ispu, text_ispu, jenis_gas, createdAt, updatedAt) VALUES (:ispu_id, :esp_id, :nilai_ispu, :text_ispu, :jenis_gas, :utc_datetime, :utc_datetime)")
                connection.execute(query, {
                    'ispu_id': ispu_id,
                    'esp_id': esp_id,
                    'nilai_ispu': Ico,
                    'text_ispu': health_statusco,
                    'jenis_gas': 'mq2_co',
                    'utc_datetime': utc_datetime,
                })
            except SQLAlchemyError as e:
                logging.error(f"Error inserting data into the database: {e}")
            
        # try:
        #     # generate id using uuid
        #     ispu_id = str(uuid.uuid4())
        #     query = text("INSERT INTO ispu (id, esp_id, nilai_ispu, text_ispu, jenis_gas, createdAt, updatedAt) VALUES (:ispu_id, :esp_id, :nilai_ispu, text_ispu, :jenis_gas, :utc_datetime, :utc_datetime)")
        #     connection.execute(query, {
        #         'ispu_id': ispu_id,
        #         'esp_id' : {esp_id},
        #         'nilai_ispu' : Ipm25,
        #         'text_ispu' : health_statuspm25,
        #         'jenis_gas' : 'pm25',
        #         'utc_datetime': utc_datetime,
        #     })
        # except SQLAlchemyError as e:
        #             logging.error(f"Error inserting data into the database: {e}")
    finally:
        connection.close()
    return Ico2, Ico