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

        response = requests.get(url)

        data = response.json()

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

    except:

        return {
            "temp": "N/A",
            "humidity": "N/A",
            "weather": "Weather API Not Configured"
        }
