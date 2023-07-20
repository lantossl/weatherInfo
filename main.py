from flask import Flask, render_template
import requests
import os
import openai
import datetime

# Set your OpenAI API key here
api_key = os.environ['OPENWEATHERMAP_API_KEY']
openai_api_key = os.environ['OPENAI_API_KEY']

# Static geographical coordinates for Budapest, Hungary
BUDAPEST_LAT = 47.4979
BUDAPEST_LON = 19.0402

# Flag to determine whether to use current coordinates or static coordinates
USE_CURRENT_COORDINATES = False

# Create the Flask app
app = Flask(__name__, template_folder="templates/")

# Enable debug mode
app.debug = True

# Function to get weather data from OpenWeatherMap API
def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to generate weather description using the gpt-3.5-turbo model
def generate_weather_description(weather_data):
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    openai.api_key = openai_api_key

    # Construct the prompt using the weather data
    prompt = f"The weather in {weather_data['name']} is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']} degrees Celsius. It feels like {weather_data['main']['feels_like']} degrees Celsius. The minimum temperature today is {weather_data['main']['temp_min']} degrees Celsius, and the maximum temperature is {weather_data['main']['temp_max']} degrees Celsius. The atmospheric pressure is {weather_data['main']['pressure']} hPa, visibility is {weather_data['visibility']} meters, and wind speed is {weather_data['wind']['speed']} m/s coming from {weather_data['wind']['deg']} degrees. Cloudiness is at {weather_data['clouds']['all']}%."

    # Generate dynamic weather description using gpt-3.5-turbo model
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can use gpt-3.5-turbo model
        prompt=prompt,
        max_tokens=500,  # Adjust the number of tokens as per your desired length
        stop=["."]  # Stop generation at the end of a sentence
    )

    return response['choices'][0]['text']

# Function to generate weather advice for activities and clothing
def generate_weather_advice(weather_data):
    # Convert sunrise and sunset timestamps to human-readable format
    sunrise_timestamp = weather_data['sys']['sunrise']
    sunset_timestamp = weather_data['sys']['sunset']
    sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
    sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')

    # Generate weather advice based on the weather conditions
    advice = f"For today's weather in {weather_data['name']}, the weather is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']} degrees Celsius. The minimum temperature today is {weather_data['main']['temp_min']} degrees Celsius, and the maximum temperature is {weather_data['main']['temp_max']} degrees Celsius. It feels like {weather_data['main']['feels_like']} degrees Celsius. The atmospheric pressure is {weather_data['main']['pressure']} hPa, visibility is {weather_data['visibility']} meters, and wind speed is {weather_data['wind']['speed']} m/s coming from {weather_data['wind']['deg']} degrees. Cloudiness is at {weather_data['clouds']['all']}%."

    # Add advice for activities and clothing based on weather conditions
    if 'rain' in weather_data['weather'][0]['description'].lower():
        advice += " It may rain today, so don't forget to bring an umbrella or raincoat with you!"
    else:
        advice += " It's a good day for outdoor activities. Enjoy the weather!"

    if weather_data['main']['temp'] > 25:
        advice += " The temperature is quite warm today. Wear light and breathable clothing to stay comfortable."
    else:
        advice += " The temperature is moderate today. Dress accordingly and bring a light jacket if needed."

    # Return the weather advice
    return advice

# Flask app route to show weather information
@app.route('/')
def show_weather():
    # Replace 'OPENWEATHERMAP_API_KEY' with the name of your environment variable
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    
    # If USE_CURRENT_COORDINATES is True, use the current coordinates (to be implemented later)
    # Otherwise, use the static coordinates for Budapest
    if USE_CURRENT_COORDINATES:
        lat, lon = get_current_coordinates()
    else:
        lat, lon = BUDAPEST_LAT, BUDAPEST_LON
    
    # Get weather data from OpenWeatherMap API
    weather_data = get_weather_data(lat, lon, api_key)

    if weather_data:
        city = weather_data['name']  # Extract the city name from the JSON data
        temperature_celsius = weather_data['main']['temp']
        weather_description_json = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # Extract additional data from the JSON
        feels_like_celsius = weather_data['main']['feels_like']
        temp_min_celsius = weather_data['main']['temp_min']
        temp_max_celsius = weather_data['main']['temp_max']
        pressure_hpa = weather_data['main']['pressure']
        visibility_meters = weather_data['visibility']
        wind_degrees = weather_data['wind']['deg']
        cloudiness_percent = weather_data['clouds']['all']
        sunrise_timestamp = weather_data['sys']['sunrise']
        sunset_timestamp = weather_data['sys']['sunset']
        timezone_offset_seconds = weather_data['timezone']

        # Generate dynamic weather description using the OpenAI API
        weather_description_ai = generate_weather_description(weather_data)

        # Generate weather advice for activities and clothing
        weather_advice = generate_weather_advice(weather_data)

        # Convert sunrise and sunset timestamps to local timezone
        sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp + timezone_offset_seconds).strftime('%H:%M')
        sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp + timezone_offset_seconds).strftime('%H:%M')
      
        # Render the template with weather data and separate descriptions
        return render_template('weather.html', city=city, temperature=temperature_celsius,
                               weather_description_json=weather_description_json,
                               weather_description_ai=weather_description_ai,
                               feels_like_celsius=feels_like_celsius,
                               temp_min_celsius=temp_min_celsius,
                               temp_max_celsius=temp_max_celsius,
                               pressure_hpa=pressure_hpa,
                               visibility_meters=visibility_meters,
                               wind_degrees=wind_degrees,
                               cloudiness_percent=cloudiness_percent,
                               sunrise_time=sunrise_time,
                               sunset_time=sunset_time,
                               weather_advice=weather_advice,
                               humidity=humidity, wind_speed=wind_speed)
    else:
        return "Weather data not available."

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)