# weather_advice.py
import openai
import os

def generate_weather_advice(weather_data):
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Construct the prompt using the weather data
    prompt = f"The weather in {weather_data['name']} today is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']} degrees Celsius. The minimum temperature today is {weather_data['main']['temp_min']} degrees Celsius, and the maximum temperature is {weather_data['main']['temp_max']} degrees Celsius. It feels like {weather_data['main']['feels_like']} degrees Celsius. The atmospheric pressure is {weather_data['main']['pressure']} hPa, visibility is {weather_data['visibility']} meters, and wind speed is {weather_data['wind']['speed']} m/s coming from {weather_data['wind']['deg']} degrees. Cloudiness is at {weather_data['clouds']['all']}. How cold you describe the weather in details today? Could you please advise activities that is fits perfectly for the weather? What would be the perfect dress to wear regarding the weather? Finally, please share a nice thought and wish something good regarding your previous answers!%"

    # Generate weather advice using gpt-3.5-turbo model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        stop=["%"]
    )

    return response['choices'][0]['text']