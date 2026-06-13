import requests

API_KEY = "your_api_key"

def get_weather(city):

    try:

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"
            f"&appid={API_KEY}"
            f"&units=metric"
        )

        data = requests.get(
            url,
            timeout=5
        ).json()

        if "main" not in data:

            return {
                "temp": "N/A",
                "humidity": "N/A",
                "weather": "Weather API Not Configured"
            }

        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }

    except Exception:

        return {
            "temp": "N/A",
            "humidity": "N/A",
            "weather": "Service Unavailable"
        }
