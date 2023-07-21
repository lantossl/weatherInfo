# main.py
from flask import Flask, render_template
from weather_api import weather_api_bp
import os

# Create the Flask app
app = Flask(__name__, template_folder="templates/")

# Enable debug mode
app.debug = True

# Set your OpenAI API key and OpenWeatherMap API key here
app.config['OPENWEATHERMAP_API_KEY'] = os.environ['OPENWEATHERMAP_API_KEY']
app.config['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']

# Register the weather_api_bp blueprint
app.register_blueprint(weather_api_bp)

# Flask app route to show the index page
@app.route('/')
def index():
    # Render the index.html page that contains the geolocation button
    return render_template('index.html')

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)