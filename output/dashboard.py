import pandas as pd
from app.db import use_engine

def get_dashboard():
    
    engine = use_engine()

    result = []
    # select latest from mean
    query = "SELECT * FROM mean ORDER BY createdAt DESC LIMIT 1"
    df = pd.read_sql(query, engine)

    temperature = df.iloc[0]["temperature"]
    humidity = df.iloc[0]["humidity"]

    if temperature < 15:
        result.append(
            f"Temperature right now is {str(temperature)}°C, it's cold outside. Please wear a jacket"
        )
    elif temperature <= 25:
        result.append(
            f"Temperature right now is {str(temperature)}°C, it's normal outside. Have a nice day"
        )
    elif temperature <= 30:
        result.append(
            f"Temperature right now is {str(temperature)}°C, it's little hot outside. Please drink more water"
        )
    else:
        result.append(
            f"Temperature right now is {str(temperature)}°C, it's hot outside. Please drink more water and stay inside when possible"
        )
        
    if humidity <= 40:
        result.append(
            f"Humidity right now is {str(humidity)}%, it's dry outside. Please drink more water"
        )
    elif humidity <= 60:
        result.append(
            f"Humidity right now is {str(humidity)}%, it's normal outside. Have a nice day"
        )
    elif humidity <= 80:
        result.append(
            f"Humidity right now is {str(humidity)}%, it's little wet outside. Please wear comfortable clothes when outside"
        )
    else:
        result.append(
            f"Humidity right now is {str(humidity)}%, it's really humid outside. Please wear comfortable clothes when outside"
        )