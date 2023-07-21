# weather_data.py
import requests

def get_weather_data(lat, lon, openWeatherMap_api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={openWeatherMap_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
