from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import datetime
import pandas as pd
from app.db import use_engine
import uuid

def get_mean():
    engine, connection = use_engine()
    
    try:
        count_esp = "SELECT id FROM esp"
        df = pd.read_sql(count_esp, engine)
        esp_id = df['id'].unique()

        latest_data = []
        for i in esp_id:
            query = f"SELECT * FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
            df = pd.read_sql(query, engine)
            latest_data.append(df)

        if latest_data:
            combined_data = pd.concat(latest_data)
            avg_temperature = combined_data['temperature'].mean()
            avg_temperature = round(float(avg_temperature), 3)
            avg_humidity = combined_data['humidity'].mean()
            avg_humidity = round(float(avg_humidity), 3)
            avg_mq135_co = combined_data['mq135_co'].mean()
            avg_mq135_co = round(float(avg_mq135_co), 3)
            avg_mq135_alcohol = combined_data['mq135_alcohol'].mean()
            avg_mq135_alcohol = round(float(avg_mq135_alcohol), 3)
            avg_mq135_co2 = combined_data['mq135_co2'].mean()
            avg_mq135_co2 = round(float(avg_mq135_co2), 3)
            avg_mq135_toluen = combined_data['mq135_toluen'].mean()
            avg_mq135_toluen = round(float(avg_mq135_toluen), 3)
            avg_mq135_nh4 = combined_data['mq135_nh4'].mean()
            avg_mq135_nh4 = round(float(avg_mq135_nh4), 3)
            avg_mq135_aceton = combined_data['mq135_aceton'].mean()
            avg_mq135_aceton = round(float(avg_mq135_aceton), 3)
            avg_mq2_h2 = combined_data['mq2_h2'].mean()
            avg_mq2_h2 = round(float(avg_mq2_h2), 3)
            avg_mq2_lpg = combined_data['mq2_lpg'].mean()
            avg_mq2_lpg = round(float(avg_mq2_lpg), 3)
            avg_mq2_co = combined_data['mq2_co'].mean()
            avg_mq2_co = round(float(avg_mq2_co), 3)
            avg_mq2_alcohol = combined_data['mq2_alcohol'].mean()
            avg_mq2_alcohol = round(float(avg_mq2_alcohol), 3)
            avg_mq2_propane = combined_data['mq2_propane'].mean()
            avg_mq2_propane = round(float(avg_mq2_propane), 3)
            avg_mq7_h2 = combined_data['mq7_h2'].mean()
            avg_mq7_h2 = round(float(avg_mq7_h2), 3)
            avg_mq7_lpg = combined_data['mq7_lpg'].mean()
            avg_mq7_lpg = round(float(avg_mq7_lpg), 3)
            avg_mq7_ch4 = combined_data['mq7_ch4'].mean()
            avg_mq7_ch4 = round(float(avg_mq7_ch4), 3)
            avg_mq7_co = combined_data['mq7_co'].mean()
            avg_mq7_co = round(float(avg_mq7_co), 3)
            avg_mq7_alcohol = combined_data['mq7_alcohol'].mean()
            avg_mq7_alcohol = round(float(avg_mq7_alcohol), 3)
            utc_datetime = datetime.datetime.utcnow()

            try:
                # generate id using uuid
                mean_id = str(uuid.uuid4())
                query = text("INSERT INTO mean (id, temperature, humidity, mq135_co, mq135_alcohol, mq135_co2, mq135_toluen, mq135_nh4, mq135_aceton, mq2_h2, mq2_lpg, mq2_co, mq2_alcohol, mq2_propane, mq7_h2, mq7_lpg, mq7_ch4, mq7_co, mq7_alcohol, createdAt, updatedAt) VALUES (:mean_id, :avg_temperature, :avg_humidity, :avg_mq135_co, :avg_mq135_alcohol, :avg_mq135_co2, :avg_mq135_toluen, :avg_mq135_nh4, :avg_mq135_aceton, :avg_mq2_h2, :avg_mq2_lpg, :avg_mq2_co, :avg_mq2_alcohol, :avg_mq2_propane, :avg_mq7_h2, :avg_mq7_lpg, :avg_mq7_ch4, :avg_mq7_co, :avg_mq7_alcohol, :utc_datetime, :utc_datetime)")
                connection.execute(query, {
                    'mean_id': mean_id,
                    'avg_temperature': avg_temperature,
                    'avg_humidity': avg_humidity,
                    'avg_mq135_co': avg_mq135_co,
                    'avg_mq135_alcohol': avg_mq135_alcohol,
                    'avg_mq135_co2': avg_mq135_co2,
                    'avg_mq135_toluen': avg_mq135_toluen,
                    'avg_mq135_nh4': avg_mq135_nh4,
                    'avg_mq135_aceton': avg_mq135_aceton,
                    'avg_mq2_h2': avg_mq2_h2,
                    'avg_mq2_lpg': avg_mq2_lpg,
                    'avg_mq2_co': avg_mq2_co,
                    'avg_mq2_alcohol': avg_mq2_alcohol,
                    'avg_mq2_propane': avg_mq2_propane,
                    'avg_mq7_h2': avg_mq7_h2,
                    'avg_mq7_lpg': avg_mq7_lpg,
                    'avg_mq7_ch4': avg_mq7_ch4,
                    'avg_mq7_co': avg_mq7_co,
                    'avg_mq7_alcohol': avg_mq7_alcohol,
                    'utc_datetime': utc_datetime,
                })

                # delete data older that 7 days
                delete = text("DELETE FROM mean WHERE createdAt < NOW() - INTERVAL 7 DAY")
                connection.execute(delete)
                connection.commit()
            except SQLAlchemyError as e:
                logging.error(f"Error inserting data into the database: {e}")
            else:
                result = "success get mean data"
                return result
        else:
            result = "error get mean data"
            return result
    finally:
        connection.close()


