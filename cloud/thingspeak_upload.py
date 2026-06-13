import requests

CHANNEL_API_KEY = "YOUR_WRITE_API_KEY"

def upload_data(
        soil,
        temp,
        humidity,
        light,
        water
):

    url = "https://api.thingspeak.com/update"

    payload = {
        "api_key": CHANNEL_API_KEY,
        "field1": soil,
        "field2": temp,
        "field3": humidity,
        "field4": light,
        "field5": water
    }

    requests.get(
        url,
        params=payload
    )