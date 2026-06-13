def predict_pump(
    soil,
    temperature,
    humidity,
    water
):
    if soil < 30:
        return "ON"

    return "OFF"