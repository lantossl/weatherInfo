# weather_api.py
from flask import Blueprint, render_template, request, current_app
import datetime
import weather_data
import weather_advice

weather_api_bp = Blueprint('weather_api', __name__)

# Flask app route to show weather information
@weather_api_bp.route('/weather')
def get_weather():
    # Get the latitude and longitude from the query parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    # Pass the api_key to the get_weather_data function
    openWeatherMap_api_key = current_app.config['OPENWEATHERMAP_API_KEY']

    # Retrieve weather data from OpenWeatherMap API
    weather_data_result = weather_data.get_weather_data(lat, lon, openWeatherMap_api_key)

    if weather_data_result:
        # Generate weather advice using the weather data
        city = weather_data_result['name']  # Extract the city name from the JSON data
        temperature_celsius = weather_data_result['main']['temp']
        weather_description = weather_data_result['weather'][0]['description']
        humidity = weather_data_result['main']['humidity']
        wind_speed = weather_data_result['wind']['speed']
        
        # Extract additional data from the JSON
        feels_like_celsius = weather_data_result['main']['feels_like']
        temp_min_celsius = weather_data_result['main']['temp_min']
        temp_max_celsius = weather_data_result['main']['temp_max']
        pressure_hpa = weather_data_result['main']['pressure']
        visibility_meters = weather_data_result['visibility']
        wind_degrees = weather_data_result['wind']['deg']
        cloudiness_percent = weather_data_result['clouds']['all']
        sunrise_timestamp = weather_data_result['sys']['sunrise']
        sunset_timestamp = weather_data_result['sys']['sunset']
        timezone_offset_seconds = weather_data_result['timezone']
        weather_advice_text = weather_advice.generate_weather_advice(weather_data_result)

      # Convert sunrise and sunset timestamps to local timezone
        sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp + timezone_offset_seconds).strftime('%H:%M')
        sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp + timezone_offset_seconds).strftime('%H:%M')

        # Render the template with weather data and advice
        return render_template('weather.html', city=weather_data_result['name'],
                               temperature=weather_data_result['main']['temp'],
                               feels_like_celsius=weather_data_result['main']['feels_like'],
                               temp_min_celsius=weather_data_result['main']['temp_min'],
                               temp_max_celsius=weather_data_result['main']['temp_max'],
                               humidity=weather_data_result['main']['humidity'],
                               visibility_meters=weather_data_result['visibility'],
                               wind_speed=weather_data_result['wind']['speed'],
                               wind_degrees=weather_data_result['wind']['deg'],
                               cloudiness_percent=weather_data_result['clouds']['all'],
                               sunrise_time=sunrise_time,
                               sunset_time=sunset_time,
                               weather_description=weather_data_result['weather'][0]['description'],
                               weather_advice=weather_advice_text)
      
    else:
        return "Weather data not available."