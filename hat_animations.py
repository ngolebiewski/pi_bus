# from sense_emu import SenseHat
from sense_hat import SenseHat
import time
import colorsys
import random

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

def realistic_fire(duration=3, speed=0.05):
    """
    Display a realistic flickering fire effect on the Sense HAT.
    `duration`: total time to show the animation (in seconds)
    `speed`: delay between frames
    """
    width, height = 8, 8
    palette = [
        (0, 0, 0),              # black
        (32, 0, 0),             # deep red
        (128, 0, 0),            # red
        (255, 64, 0),           # bright red-orange
        (255, 128, 0),          # orange
        (255, 200, 0),          # yellow-orange
        (255, 255, 64),         # yellow
        (255, 255, 200),        # pale yellow (hot)
    ]

    fire_grid = [[0 for _ in range(width)] for _ in range(height)]

    start_time = time.time()

    while time.time() - start_time < duration:
        # Update bottom row with random "fuel"
        for x in range(width):
            fire_grid[height - 1][x] = random.randint(5, 7)

        # Propagate the fire upward with randomness
        for y in range(height - 2, -1, -1):
            for x in range(width):
                below = fire_grid[y + 1][x]
                drift = random.randint(-1, 1)
                decay = random.randint(0, 2)
                new_x = min(width - 1, max(0, x + drift))
                fire_grid[y][x] = max(0, fire_grid[y + 1][new_x] - decay)

        # Convert grid to pixel colors
        pixels = []
        for y in range(height):
            for x in range(width):
                color_index = fire_grid[y][x]
                color = palette[color_index]
                pixels.append(color)

        sense.set_pixels(pixels)
        time.sleep(speed)

    sense.clear()
