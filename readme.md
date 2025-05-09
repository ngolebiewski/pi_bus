# Pi MTA Bus Stop Alerter for Raspberry Pi
Will display on a Sensehat LED display (or other display) realtime information for your local MTA bustop and favored direction. Great for those catching a bus to school/work daily.

# Set up
1. Setup virtual environment and acitvate
2. Get an API key from the MTA `https://register.developer.obanyc.com/`
3. Add MTA_API_KEY to .env
4. pip install -r requirements.txt

# Plans
1. Use Adafruit PiTFT Plus 320x240 2.8" TFT + Capacitive Touchscreen
2. Design PyGame graphics to show data -- like a bus moving around! Pixel/8-bit art.
3. Use the Lon/Lat from the bus stop data to bring up current weather from NOAA. Can also have the user set the Zip code.

# Tech
- Raspberry Pi Zero 2W
- Adafruit PiTFT Plus 320x240 2.8" TFT + Capacitive Touchscreen
- Python
    - Requests -> API Calls to MTA, NOAA, and Open Street Map.
    - PyGame

# Source:
https://github.com/ngolebiewski/pi_bus
