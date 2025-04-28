import requests
import json
from dotenv import load_dotenv
import os

# Hiding my email address from Github for some reason...
load_dotenv()
EMAIL = os.getenv("EMAIL")

zip_code = int(input('What is your zip code?:'))

url = f'https://nominatim.openstreetmap.org/search?q={zip_code}+us&format=jsonv2'
headers = {
        'User-Agent': f'Pi Bus Time/0.1 ({EMAIL})' 
    }
print(headers)
r = requests.get(url, headers=headers)
print(r.status_code)
data = r.json()
print(json.dumps(data, indent=4))   # Pretty Print

place_name = data[0]['display_name']
lat, lon = float(data[0]['lat']), float(data[0]['lon'])
print(place_name)
print(lat)
print(lon)

# def get_lat_lon_from_zip(zip_code=10001):
#     url = f"https://nominatim.openstreetmap.org/search.php?q={zip_code}+us&format=jsonv2"
    
#     response = requests.get(url)
#     print(response)
#     data = response.json()
    
#     if data:
#         latitude = float(data[0]['lat'])
#         longitude = float(data[0]['lon'])
#         return latitude, longitude
#     else:
#         return None, None

# def main():
#     zip_code = 10001
#     lat, lon = get_lat_lon_from_zip(zip_code)

#     if lat and lon:
#         print(f"Latitude: {lat}, Longitude: {lon}")
#     else:
#         print("Could not retrieve coordinates.")
    
# if __name__ == "__main__":
#     main()



# Data we're working with below.
'''
python3 zip_code_tool.py

200
[
    {
        "place_id": 353632576,
        "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
        "lat": "40.7484723",
        "lon": "-73.9941186",
        "category": "place",
        "type": "postcode",
        "place_rank": 21,
        "importance": 0.12000999999999995,
        "addresstype": "postcode",
        "name": "10001",
        "display_name": "10001, Manhattan, New York County, City of New York, New York, United States",
        "boundingbox": [
            "40.6984723",
            "40.7984723",
            "-74.0441186",
            "-73.9441186"
        ]
    }
]
'''