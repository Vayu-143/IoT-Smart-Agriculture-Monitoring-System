import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

csv_file = "data/sensor_data.csv"

if not os.path.exists(csv_file):
    print("ERROR: sensor_data.csv not found.")
    print("Run: python main.py")
    exit()

df = pd.read_csv(csv_file)

if len(df) < 10:
    print("Not enough training data.")
    print("Run main.py longer.")
    exit()

df["PumpLabel"] = df["Pump"].map({
    "OFF": 0,
    "ON": 1
})

X = df[
    [
        "Soil",
        "Temperature",
        "Humidity",
        "Water"
    ]
]

y = df["PumpLabel"]

model = DecisionTreeClassifier()

model.fit(X, y)

joblib.dump(
    model,
    "ml/irrigation_model.pkl"
)

print("Model Saved Successfully")