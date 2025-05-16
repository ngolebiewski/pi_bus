import requests

# URLs
hourly_url_manhattan = "https://api.weather.gov/gridpoints/OKX/33,36/forecast/hourly"
hourly_url_brooklyn = "https://api.weather.gov/gridpoints/OKX/35,35/forecast/hourly"

def current_weather():
    try:
        hourly_resp = requests.get(hourly_url_manhattan)
        hourly_data = hourly_resp.json()
        current = hourly_data['properties']['periods'][0]
        
        current_temp = current['temperature']
        current_precip = current['probabilityOfPrecipitation']['value'] or 0  # sometimes it's None
        
        return f"Current Weather: {current_temp}F, Chance Rain: {current_precip}%"
    except:
        return ("No weather data")