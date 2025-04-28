import requests
from datetime import datetime, timedelta

# URLs
hourly_url = "https://api.weather.gov/gridpoints/OKX/33,35/forecast/hourly"
daily_url = "https://api.weather.gov/gridpoints/OKX/33,35/forecast"

# Fetch hourly and daily data
hourly_resp = requests.get(hourly_url)
daily_resp = requests.get(daily_url)

hourly_data = hourly_resp.json()
daily_data = daily_resp.json()

# Get current period (usually periods[0])
current = hourly_data['properties']['periods'][0]

current_temp = current['temperature']
current_wind = current['windSpeed']
current_precip = current['probabilityOfPrecipitation']['value'] or 0  # sometimes it's None

# Get today's and tomorrow's daytime and nighttime forecast
periods = daily_data['properties']['periods']

today_date = datetime.now().date()
tomorrow_date = today_date + timedelta(days=1)

daytime = None
nighttime = None
tomorrow_daytime = None
tomorrow_nighttime = None

# Loop to find the appropriate periods for today and tomorrow
for period in periods:
    period_time = datetime.fromisoformat(period['startTime']).astimezone()
    if period_time.date() == today_date:
        if period['isDaytime'] and not daytime:
            daytime = period
        elif not period['isDaytime'] and not nighttime:
            nighttime = period
    elif period_time.date() == tomorrow_date:
        if period['isDaytime'] and not tomorrow_daytime:
            tomorrow_daytime = period
        elif not period['isDaytime'] and not tomorrow_nighttime:
            tomorrow_nighttime = period

def get_weather_emoji(forecast):
    forecast = forecast.lower()
    if "sunny" in forecast or "clear" in forecast:
        return "☀️"
    elif "cloud" in forecast:
        return "☁️"
    elif "rain" in forecast or "showers" in forecast:
        return "🌧️"
    elif "snow" in forecast:
        return "❄️"
    elif "thunder" in forecast:
        return "⛈️"
    elif "fog" in forecast:
        return "🌫️"
    else:
        return "🌡️"

# Output
print("🌎 Current Weather")
print(f"🌡️ Temperature: {current_temp}°F")
print(f"💨 Wind: {current_wind}")
print(f"🌧️ Chance of Rain: {current_precip}%")
print("")

if daytime:
    day_emoji = get_weather_emoji(daytime['shortForecast'])
    print(f"📅 Today")
    print(f"{day_emoji} Forecast: {daytime['shortForecast']}")
    print(f"🔥 High: {daytime['temperature']}°F")
    print(f"📝 {daytime['detailedForecast']}")
    print("")

if nighttime:
    night_emoji = get_weather_emoji(nighttime['shortForecast'])
    print(f"🌙 Tonight")
    print(f"{night_emoji} Forecast: {nighttime['shortForecast']}")
    print(f"❄️ Low: {nighttime['temperature']}°F")
    print(f"📝 {nighttime['detailedForecast']}")
    print("")

if tomorrow_daytime:
    tomorrow_day_emoji = get_weather_emoji(tomorrow_daytime['shortForecast'])
    print(f"📅 Tomorrow")
    print(f"{tomorrow_day_emoji} Forecast: {tomorrow_daytime['shortForecast']}")
    print(f"🔥 High: {tomorrow_daytime['temperature']}°F")
    print(f"📝 {tomorrow_daytime['detailedForecast']}")
    print("")

if tomorrow_nighttime:
    tomorrow_night_emoji = get_weather_emoji(tomorrow_nighttime['shortForecast'])
    print(f"🌙 Tomorrow Night")
    print(f"{tomorrow_night_emoji} Forecast: {tomorrow_nighttime['shortForecast']}")
    print(f"❄️ Low: {tomorrow_nighttime['temperature']}°F")
    print(f"📝 {tomorrow_nighttime['detailedForecast']}")

