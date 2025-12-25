# Arduino
Sample arduino sketches

LedHouse
* Lighting up some of the holiday houses using a WS2811 light strip.


Dependencies
* Set IDE sketch directory to top-level Arduino folder
* Install Adafruit NeoPixel, 1.15.2

## Python port

A Python port of the HolidayLights sketch lives in the `python/` directory and provides:

- Core classes ported from the Arduino sketch (`House`, `HOA`, timers, colors).
- A **mock** adapter for desktop testing (`run_mock.py`).
- Adapters/skeletons for **Raspberry Pi** using `rpi_ws281x` and **CircuitPython** using `adafruit_neopixel`.

See `python/README.md` for installation and usage instructions.
