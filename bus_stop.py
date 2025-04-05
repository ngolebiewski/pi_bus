import os
import requests
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()
API_KEY = os.getenv("MTA_API_KEY")
STOP_ID = "401220"

url = "https://bustime.mta.info/api/siri/stop-monitoring.json"
params = {
    "key": API_KEY,
    "MonitoringRef": STOP_ID
}

response = requests.get(url, params=params)
data = response.json()
# import json
# print(json.dumps(data, indent=2))

# Print out the next few buses
visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]

for visit in visits[:3]:  # limit to first 3 for brevity
    journey = visit["MonitoredVehicleJourney"]
    line = journey["LineRef"]
    destination = journey["DestinationName"]
    location = journey["VehicleLocation"]
    eta = journey["MonitoredCall"].get("ExpectedArrivalTime")

    print(f"Bus {line} to {destination}")
    print(f" → Location: {location}")
    print(f" → ETA: {eta}\n")

