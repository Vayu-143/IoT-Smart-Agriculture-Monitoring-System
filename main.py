import random
import pandas as pd
from datetime import datetime
import time
import os

from cloud.thingspeak_upload import upload_data

SOIL_THRESHOLD = 30
TEMP_THRESHOLD = 35
WATER_THRESHOLD = 20

csv_file = "data/sensor_data.csv"

os.makedirs("data", exist_ok=True)

while True:

    soil = random.randint(10,100)
    temp = random.randint(20,45)
    humidity = random.randint(30,90)
    light = random.randint(100,1000)
    water = random.randint(10,100)

    alerts = []
    pump = "OFF"

    if soil < SOIL_THRESHOLD:
        alerts.append("Low Soil Moisture")
        pump = "ON"

    if temp > TEMP_THRESHOLD:
        alerts.append("High Temperature")

    if water < WATER_THRESHOLD:
        alerts.append("Low Water Level")

    row = pd.DataFrame([{
        "Time": datetime.now(),
        "Soil": soil,
        "Temperature": temp,
        "Humidity": humidity,
        "Light": light,
        "Water": water,
        "Pump": pump,
        "Alerts": ",".join(alerts)
    }])

    if os.path.exists(csv_file):
        row.to_csv(
            csv_file,
            mode="a",
            header=False,
            index=False
        )
    else:
        row.to_csv(
            csv_file,
            index=False
        )

    upload_data(
        soil,
        temp,
        humidity,
        light,
        water
    )

    print("="*50)
    print(row)
    print("="*50)

    time.sleep(5)