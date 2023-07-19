from flask import Flask, render_template
import requests
import os
api_key = os.environ['OPENWEATHERMAP_API_KEY']

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
    url= f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to generate weather description using OpenAI
def generate_weather_description(weather_data):
    # Use OpenAI API here to generate weather description
    # Replace this placeholder code with actual OpenAI API call
    description = "Weather description will be generated here."
    return description

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
    
    # Update the API URL to request data in metric units directly
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data:
        city = weather_data['name']  # Extract the city name from the JSON data
        temperature_celsius = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # Render the template with weather data
        return render_template('weather.html', city=city, temperature=temperature_celsius,
                               weather_description=weather_description,
                               humidity=humidity, wind_speed=wind_speed)
    else:
        return "Weather data not available."

# Run the Flask application
app.run(host='0.0.0.0', port=81)