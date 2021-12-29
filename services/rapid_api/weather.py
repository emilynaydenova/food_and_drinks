import json

import requests
from decouple import config

town = "Pleven,bg"
latitude = "43.4167"
longitude = "24.6167"


class CurrentWeatherService:
    def __init__(self):
        self.headers = {
            "x-rapidapi-host": config("WEATHER_API_HOST"),
            "x-rapidapi-key": config("WEATHER_API_KEY"),
        }
        self.querystring = {
            "q": town,
            "lat": latitude,
            "lon": longitude,
            "lang": "en",
            "units": "metric",
            "mode": "json",
        }

    def get_weather(self):
        url = config("WEATHER_API_URL")
        resp = requests.request(
            "GET", url, headers=self.headers, params=self.querystring
        )
        return json.loads(resp.text)["main"]

    # {'temp': 0.97, 'feels_like': -2.41, 'temp_min': 0.97, 'temp_max': 0.97, 'pressure': 1015, 'humidity': 100}


#
# if __name__ == "__main__":
#     weather = CurrentWeatherService()
#     resp = weather.get_weather()
#     print(resp)

"""
{"coord":{"lon":24.6167,"lat":43.4167},
"weather":[{"id":701,"main":"Mist","description":"mist","icon":"50n"}],
"base":"stations",
"main":{"temp":1.97,"feels_like":-0.23,"temp_min":1.97,"temp_max":1.97,"pressure":1014,"humidity":87},
"visibility":8000,
"wind":{"speed":2.06,"deg":90},
"clouds":{"all":90},"dt":1640573916,
"sys":{"type":1,"id":6369,
"country":"BG",
"sunrise":1640584402,
"sunset":1640616697},
"timezone":7200,
"id":728203,
"name":"Pleven",
"cod":200}

"""
