import requests
# Read all about it: https://requests.readthedocs.io/en/latest/
# NOAA API: https://api.weather.gov/openapi.json
# This is good: https://weather-gov.github.io/api/general-faqs


noaa_hourly = 'https://api.weather.gov/gridpoints/OKX/33,36/forecast/hourly'
noaa_forecast = 'https://api.weather.gov/gridpoints/OKX/33,36/forecast'

r = requests.get(noaa_hourly)

print(r.json(), '\nServer status code:', r.status_code)