from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timezone

load_dotenv()
API_KEY = os.getenv("MTA_API_KEY")
STOP_ID = "401220"

# --- Step 1: Get real-time bus info ---
stop_monitoring_url = "https://bustime.mta.info/api/siri/stop-monitoring.json"
monitoring_params = {
    "key": API_KEY,
    "MonitoringRef": STOP_ID
}

response = requests.get(stop_monitoring_url, params=monitoring_params)
data = response.json()

stop_name = None

try:
    delivery = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]
    visits = delivery.get("MonitoredStopVisit", [])

    if visits:
        for visit in visits[:3]:  # Limit to first 3
            journey = visit["MonitoredVehicleJourney"]
            line = journey["LineRef"]
            destination = journey["DestinationName"]
            location = journey["VehicleLocation"]
            eta_raw = journey["MonitoredCall"].get("ExpectedArrivalTime")

            # Format ETA (if available)
            if eta_raw:
                eta_dt = datetime.fromisoformat(eta_raw)
                now = datetime.now(eta_dt.tzinfo)  # respect timezone from MTA
                eta_str = eta_dt.strftime("%B %-d, %Y %-I:%M %p")  # or use %d, %I for Windows
                minutes_left = int((eta_dt - now).total_seconds() / 60)

                red = "\033[91m"
                reset = "\033[0m"
                print(f"🚌 Bus {line} to {destination}")
                print(f" → Location: {location}")
                print(f" → ETA: {eta_str}")
                print(f" ⏳ Arrival in: {red}{minutes_left} minute(s){reset}\n")
            else:
                print(f"🚌 Bus {line} to {destination}")
                print(f" → Location: {location}")
                print(" → ETA: Unknown\n")

        # Try to get stop name from live data
        stop_name = visits[0]["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"]
    else:
        print("✅ No buses currently being tracked for this stop.")

except KeyError as e:
    print(f"❌ Could not process real-time API response. Missing key: {e}")

# --- Step 2: Fallback to get stop name via static stop metadata API ---
if not stop_name:
    stop_lookup_url = f"https://bustime.mta.info/api/where/stop.json"
    stop_params = {
        "key": API_KEY,
        "stopId": f"MTA_{STOP_ID}"
    }
    stop_response = requests.get(stop_lookup_url, params=stop_params)
    stop_data = stop_response.json()

    try:
        stop_name = stop_data["data"]["stop"]["name"]
    except KeyError:
        stop_name = "Unknown Stop Name"

# --- Final Output ---
print(f"📍 Stop Name: {stop_name}")

