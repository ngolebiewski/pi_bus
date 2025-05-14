from api_bus_stop import BusData, get_realtime_bus_updates
from hat_animations import smooth_rainbow_wave, realistic_fire
# from sense_emu import SenseHat
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

last_bus_ids = set()

def flash_red():
    for i in range(2):
        sense.clear((255, 0, 0))
        time.sleep(0.3)
        sense.clear()
        time.sleep(0.3)

def display_messages(messages):
    for msg in messages:
        sense.show_message(msg, scroll_speed=0.05, text_color=(255, 255, 0))

while True:
    try:
        busses = get_realtime_bus_updates()
        if not busses:
            sense.show_message("No data", scroll_speed=0.05)
            time.sleep(5)
            continue

        current_ids = set(bus.bus_id for bus in busses)

        if current_ids != last_bus_ids:
            smooth_rainbow_wave(duration=3)

        for bus in busses:
            if bus.minutes_away <= 3:
                flash_red()
                realistic_fire(5)

        display_messages([b.bus_ticket_string() for b in busses])
        time.sleep(5)

    except Exception as e:
        sense.show_message(f"Error: {str(e)}", scroll_speed=0.05, text_colour=(255, 0, 0))
        time.sleep(10)
