from flask import Flask, render_template, request
import requests
from conditions import conditions


app = Flask(__name__)

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city):
    location_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    location_response = requests.get(location_url)
    location_data = location_response.json()

    if location_data['results']:
        lat = location_data['results'][0]['latitude']
        lon = location_data['results'][0]['longitude']

        weather_params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True,
        }

        weather_response = requests.get(WEATHER_API_URL, params=weather_params)
        weather_data = weather_response.json()
    try:
        if weather_data['current_weather']['weathercode'] in conditions:
            weather_data['current_weather']['weathercode'] = conditions[weather_data['current_weather']['weathercode']]
            return weather_data
    except Exception:
        return {'error': "No weather condition available"}


@app.route('/')
def index():
    default_city = "New York"
    weather = get_weather(default_city)
    return render_template('index.html', weather=weather, city=default_city)


@app.route('/weather')
def weather_by_city():
    city = request.args.get('city')
    weather = get_weather(city)
    if weather:
        return render_template('weather.html', weather=weather, city=city)
    else:
        return f"City '{city}' not found.", 404


if __name__ == '__main__':
    app.run(debug=True)
