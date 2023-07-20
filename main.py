from flask import Flask, render_template
import requests
import os
import openai

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

# Function to generate weather advice using the gpt-3.5-turbo model
def generate_weather_advice(weather_data):
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    openai.api_key = openai_api_key

    # Construct the prompt using the weather data
    prompt = f"The weather in {weather_data['name']} is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']} degrees Celsius. It feels like {weather_data['main']['feels_like']} degrees Celsius. The humidity is {weather_data['main']['humidity']}%. Based on the weather conditions, I would suggest the following activities:"

    # Generate weather advice using gpt-3.5-turbo model
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can use gpt-3.5-turbo model
        prompt=prompt,
        max_tokens=500,  # Adjust the number of tokens as per your desired length
        stop=["."]  # Stop generation at the end of a sentence
    )

    return response['choices'][0]['text']

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

        # Generate dynamic weather description using the OpenAI API
        weather_description_ai = generate_weather_description(weather_data)

        # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
        openai.api_key = openai_api_key

        # Construct the prompt using the weather data
        prompt = f"The weather in {city} is {weather_description_json} with a temperature of {temperature_celsius} degrees Celsius. It feels like {feels_like_celsius} degrees Celsius. The minimum temperature today is {temp_min_celsius} degrees Celsius, and the maximum temperature is {temp_max_celsius} degrees Celsius. The atmospheric pressure is {pressure_hpa} hPa, visibility is {visibility_meters} meters, and wind speed is {wind_speed} m/s coming from {wind_degrees} degrees. Cloudiness is at {cloudiness_percent}%."

        # Generate dynamic weather description using gpt-3.5-turbo model
        response = openai.Completion.create(
            engine="text-davinci-002",  # You can use gpt-3.5-turbo model
            prompt=prompt,
            max_tokens=500,  # Adjust the number of tokens as per your desired length
            stop=["."]  # Stop generation at the end of a sentence
        )

        # Get the generated weather description from the API response
        weather_description_ai = response['choices'][0]['text']
        # Generate weather advice using the OpenAI API
        weather_advice = generate_weather_advice(weather_data)

        # Render the template with weather data and separate descriptions
        return render_template('weather.html', city=city, temperature=temperature_celsius,
                               weather_description_json=weather_description_json,
                               weather_description_ai=weather_description_ai,
                               humidity=humidity, wind_speed=wind_speed,
                               feels_like_celsius=feels_like_celsius,
                               temp_min_celsius=temp_min_celsius,
                               temp_max_celsius=temp_max_celsius,
                               pressure_hpa=pressure_hpa,
                               visibility_meters=visibility_meters,
                               wind_degrees=wind_degrees,
                               cloudiness_percent=cloudiness_percent,
                               sunrise_timestamp=sunrise_timestamp,
                               sunset_timestamp=sunset_timestamp,
                               weather_advice=weather_advice)
    else:
        return "Weather data not available."

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)