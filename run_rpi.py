"""Example runner for Raspberry Pi using rpi_ws281x adapter.

Edit `PIN` and other parameters as needed for your hardware.
"""
import time
from holidaylights.core import House, HOA, HouseMode
from holidaylights.adapters import RPiWS281xAdapter

NUM_LIGHTS = 200
NUM_HOUSES = 27
POLICE_HOUSE = 22

# Build houses as in Arduino sketch
all_houses = [
    House(0, 1), House(8, 2), House(13, 2), House(19, 2), House(24, 2),
    House(34, 2), House(39, 2), House(44, 2), House(50, 2), House(64, 1),
    House(71, 2), House(77, 2), House(88, 2), House(95, 2), House(100, 2),
    House(108, 2), House(113, 2), House(119, 2), House(130, 2), House(138, 2),
    House(144, 2), House(154, 2), House(159, 2), House(164, 2), House(171, 2),
    House(183, 2), House(197, 3),
]

hoa = HOA(all_houses, NUM_HOUSES, POLICE_HOUSE)

# Configure for your hardware
PIN = 18
leds = RPiWS281xAdapter(NUM_LIGHTS, pin=PIN)

# initial state
hoa.update(leds)
all_houses[0].set_mode(HouseMode.DebugMode)

try:
    while True:
        leds.clear()
        hoa.update(leds)
        leds.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting")
