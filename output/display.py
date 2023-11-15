import pandas as pd
from app.db import use_engine


def get_display():
    engine = use_engine()
    query = "SELECT * FROM esp"
    df = pd.read_sql(query, engine)

    # get id for each  esp
    esp_id = df["id"].unique()

    # get latest data for each esp
    latest_data = []
    for i in esp_id:
        query = f"SELECT temperature, humidity FROM data WHERE esp_id = '{i}' ORDER BY createdAt DESC LIMIT 1"
        df = pd.read_sql(query, engine)
        latest_data.append(df)

    if latest_data:
        # Combine all the latest data into a single DataFrame
        combined_data = pd.concat(latest_data)
        # Calculate overall average temperature and humidity
        overall_avg_temperature = combined_data["temperature"].mean()
        overall_avg_humidity = combined_data["humidity"].mean()

        # give me only 1 number after comma
        overall_avg_temperature = round(overall_avg_temperature, 1)
        overall_avg_humidity = round(overall_avg_humidity, 1)

    else:
        # Handle the case when latest_data is empty
        combined_data = pd.DataFrame()  # or any other appropriate action
        overall_avg_temperature = (
            overall_avg_humidity
        ) = 0  # or any other appropriate values

    # print(combined_data)
    overall_avg_polution = "Baik"

    return overall_avg_temperature, overall_avg_humidity, overall_avg_polution
