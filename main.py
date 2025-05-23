from api_bus_stop import BusData, get_realtime_bus_updates, current_time
from hat_animations import smooth_rainbow_wave, realistic_fire
# from sense_emu import SenseHat
from sense_hat import SenseHat
import time
from api_py_weather import current_weather
from json_img_getter import bus_scroller

sense = SenseHat()
# sense.set_rotation(180)  # Adjust if text still looks wrong
sense.clear()

SCROLL_SPEED = 0.05

last_bus_ids = set()

def flash_red():
    for i in range(2):
        sense.clear((255, 0, 0))
        time.sleep(0.3)
        sense.clear()
        time.sleep(0.3)

def display_messages(messages):
    for msg in messages:
        print(msg)
        sense.show_message(msg, scroll_speed=SCROLL_SPEED, text_colour=(255, 255, 0))

count = -1

bus_scroller()

while True:
    count +=1
    if count % 5 == 0:
        try:
            weather = current_weather()
            sense.show_message(weather, scroll_speed=SCROLL_SPEED)
        except Exception as e:
            sense.show_message("Weather error")
        
    try:
        busses = get_realtime_bus_updates()
        if not busses:
            sense.show_message("No data", scroll_speed=SCROLL_SPEED)
            time.sleep(5)
            continue

        current_ids = set(bus.bus_id for bus in busses)

        if current_ids != last_bus_ids:
            smooth_rainbow_wave(duration=3)

        for bus in busses:
            if bus.minutes_away <= 3:
                flash_red()
                realistic_fire(5)
                
        sense.show_message(f"Current time: {current_time()}", scroll_speed=SCROLL_SPEED)

        display_messages([b.bus_ticket_string() for b in busses])
        time.sleep(5)

    except Exception as e:
        sense.show_message(f"Error: {str(e)}", scroll_speed=SCROLL_SPEED, text_colour=(255, 0, 0))
        time.sleep(10)
