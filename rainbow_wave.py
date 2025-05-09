from sense_hat import SenseHat
import time
import colorsys

sense = SenseHat()

def hsv_to_rgb(h, s, v):
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

def smooth_rainbow_wave(duration=3, speed=0.05):
    """
    Show a smooth, animated rainbow wave scrolling across the Sense HAT.
    `duration`: total time to show the animation (in seconds)
    `speed`: delay between frames
    """
    width, height = 8, 8
    start_time = time.time()

    while time.time() - start_time < duration:
        pixels = []
        t = time.time() * 0.5  # Controls animation speed
        for y in range(height):
            for x in range(width):
                hue = (x + t * 10) % width / width
                rgb = hsv_to_rgb(hue, 1.0, 1.0)
                pixels.append(rgb)
        sense.set_pixels(pixels)
        time.sleep(speed)

    sense.clear()
