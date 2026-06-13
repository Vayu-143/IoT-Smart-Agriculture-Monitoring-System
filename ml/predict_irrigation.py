import joblib

model = joblib.load(
    "ml/irrigation_model.pkl"
)

def predict_pump(
        soil,
        temp,
        humidity,
        water
):

    result = model.predict(
        [[soil,temp,humidity,water]]
    )[0]

    return "ON" if result == 1 else "OFF"