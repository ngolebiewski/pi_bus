from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
import math

###############
# Globals     #
###############

load_dotenv()
API_KEY = os.getenv("MTA_API_KEY")
STOP_ID = "401220" # This should become a user settable field!!!!!!! Maybe make an argparser with this number as the default.

STOP_MONITORING_URL = "https://bustime.mta.info/api/siri/stop-monitoring.json"
MONITORING_PARAMS = {
    "key": API_KEY,
    "MonitoringRef": STOP_ID
}

###############
# Class       #
###############

class BusData:
    def __init__(self, line, destination, eta_raw, distance_away, stops_away, bus_id, stop_name):
        self.line = line
        self.destination = destination
        self.eta = self.eta_parser(eta_raw) # gives you a response like 8:30 AM
        self.minutes_away = self.compute_minutes_away(eta_raw)
        self.distance_away = distance_away
        self.stops_away = stops_away
        self.bus_id = bus_id
        self.stop_name = stop_name

    def eta_parser(self, eta_raw):
        try:
            eta_dt = datetime.fromisoformat(str(eta_raw))
            eta_str = eta_dt.strftime("%-I:%M %p") 
            return eta_str  
        except ValueError:
            return None
        
    def compute_minutes_away(self, eta_raw):
        try:
            eta_dt = datetime.fromisoformat(eta_raw)
            now = datetime.now(eta_dt.tzinfo) if eta_dt.tzinfo else datetime.now()
            delta = eta_dt - now
            return max(math.ceil(delta.total_seconds() / 60), 0)  # avoid negative minutes + round up, i.e. is is 12:45:02 and the bus arrives at 12:46, it makes no sense to say the bus arrives in 0 minutes.
        except Exception:
            return -1 
    
    def bus_ticket_string(self):
        match self.eta:
            case None:
                return f"Next {self.line} bus at {self.stop_name} is {self.distance_away}" 
            case _:  
                return f"Next {self.line} bus at {self.stop_name} is {self.minutes_away} minutes away, arriving at {self.eta}"
            
    def bus_string_short(self):
        match self.eta:
            case None:
                return f"Next {self.line} is {self.distance_away}" 
            case _:  
                return f"Next {self.line} is {self.minutes_away} minutes away, arriving at {self.eta}"
    
    def stop_info(self):
        return f"{self.line} at {self.stop_name} to {self.destination}"
    
    def __repr__(self):
        return (
            f"<BusData>\n"
            f"  line={self.line}\n"
            f"  destination={self.destination}\n"
            f"  eta={self.eta}\n"
            f"  minutes_away={self.minutes_away}\n"
            f"  distance_away={self.distance_away}\n"
            f"  stops_away={self.stops_away}\n"
            f"  bus_id={self.bus_id}\n"
            f"  stop_name={self.stop_name}\n"
        )

###############
# Function    #
###############

def get_realtime_bus_updates():
# --- Get real-time bus info ---
    response = requests.get(STOP_MONITORING_URL, params=MONITORING_PARAMS)
    data = response.json()
    pretty_json = json.dumps(data, indent=4)
    # print(pretty_json) # Shows an indent formatted debug statement of the json data from the MTA.
    stop_name = None # Will get overwritten, hopefully, weird way to catch an error.
    
    busses = [] # Drop in bus objects

    try:
        delivery = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]
        visits = delivery.get("MonitoredStopVisit", [])

        if visits:
            for visit in visits[:3]:  # Limit to first 3
                journey = visit["MonitoredVehicleJourney"]
                line = journey["PublishedLineName"]
                destination = journey["DestinationName"]
                location = journey["VehicleLocation"]
                eta_raw = journey["MonitoredCall"].get("ExpectedArrivalTime")
                distance_away = journey["MonitoredCall"]["Extensions"]["Distances"]["PresentableDistance"]
                stops_away = journey["MonitoredCall"]["Extensions"]["Distances"]["StopsFromCall"]
                bus_id = journey["VehicleRef"]
                stop_name = journey["MonitoredCall"]["StopPointName"]

                # create a BusData object and append to Busses list
                busses.append(BusData(line, destination, eta_raw, distance_away, stops_away, bus_id, stop_name))

    except KeyError as e:
        print(f"❌ Could not process real-time API response. Missing key: {e}")
        return

    return busses

###############
# Debug       #
###############

if __name__ == "__main__":
    from api_py_weather import current_weather
    
    busses = get_realtime_bus_updates()
    print(busses[0].stop_info())
    # print([m.bus_ticket_string() for m in busses])
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    print(current_weather())
    print("Current Time:", current_time)
    print([m.bus_string_short() for m in busses])

    # print(busses)