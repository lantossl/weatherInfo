from flask import Flask, render_template, request
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

# Function to generate weather advice for activities and clothing using the gpt-3.5-turbo model
def generate_weather_advice(weather_data):
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    openai.api_key = openai_api_key

    # Construct the prompt using the weather data
    prompt = f"The weather in {weather_data['name']} today is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']} degrees Celsius. The minimum temperature today is {weather_data['main']['temp_min']} degrees Celsius, and the maximum temperature is {weather_data['main']['temp_max']} degrees Celsius. It feels like {weather_data['main']['feels_like']} degrees Celsius. The atmospheric pressure is {weather_data['main']['pressure']} hPa, visibility is {weather_data['visibility']} meters, and wind speed is {weather_data['wind']['speed']} m/s coming from {weather_data['wind']['deg']} degrees. Cloudiness is at {weather_data['clouds']['all']}. How cold you describe the weather in details today? Could you please advise activities that is fits perfectly for the weather? What would be the perfect dress to wear regarding the weather? Finally, please share a nice thought and wish something good regarding your previous answers!%"

    # Generate weather advice using gpt-3.5-turbo model
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can use gpt-3.5-turbo model
        prompt=prompt,
        max_tokens=1000,  # Adjust the number of tokens as per your desired length
        stop=["%"]  # Stop generation at the end of a sentence
    )

    return response['choices'][0]['text']

# Flask app route to show weather information
@app.route('/')
def index():
    # Render the index.html page that contains the geolocation button
    return render_template('index.html')
  
def show_weather():
    # Replace 'OPENWEATHERMAP_API_KEY' with the name of your environment variable
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    
    # If USE_CURRENT_COORDINATES is True, use the current coordinates (to be implemented later)
    # Otherwise, use the static coordinates for Budapest

    # Get the latitude and longitude from the query parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

@app.route('/weather')
def get_weather():
    # Get the latitude and longitude from the query parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
  
    # Get weather data from OpenWeatherMap API
    weather_data = get_weather_data(lat, lon, api_key)

    if weather_data:
        city = weather_data['name']  # Extract the city name from the JSON data
        temperature_celsius = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
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

        # Convert sunrise and sunset timestamps to local timezone
        sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp + timezone_offset_seconds).strftime('%H:%M')
        sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp + timezone_offset_seconds).strftime('%H:%M')

        # Generate weather advice for activities and clothing
        weather_advice = generate_weather_advice(weather_data)

        # Render the template with weather data and separate descriptions
        return render_template('weather.html', city=city, temperature=temperature_celsius,
        		           weather_description=weather_description,
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
