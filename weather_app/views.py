import datetime
import requests
from django.shortcuts import render

def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forcast_url = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    
    if request.method == "POST":
        city = request.POST['city']

        weather_data, daily_forcasts = fetch_weather_and_forcast(city, API_KEY, current_weather_url, forcast_url)

        context = {
            "weather_data": weather_data,
            "daily_forcasts": daily_forcasts
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")
    
def fetch_weather_and_forcast(city, api_key, current_weather_url, forcast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forcast_response = requests.get(forcast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 272.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    daily_forcasts = []
    for daily_data in forcast_response['daily'][:5]:
        daily_forcasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })
    return weather_data, daily_forcasts