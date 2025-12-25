"""Hardware adapters for HolidayLights Python port.

Provides a Mock adapter (works on any platform) and skeletons for RPi and CircuitPython.
"""
from typing import List

class MockLEDs:
    def __init__(self, num_pixels: int):
        self.num_pixels = num_pixels
        self.pixels = [0] * num_pixels

    def clear(self):
        self.pixels = [0] * self.num_pixels

    def set_pixel(self, index: int, color: int):
        if 0 <= index < self.num_pixels:
            self.pixels[index] = color

    def show(self):
        # Print a compact summary: show runs of identical colors
        out = []
        if not self.pixels:
            print("<no pixels>")
            return
        last = self.pixels[0]
        count = 1
        for c in self.pixels[1:]:
            if c == last:
                count += 1
            else:
                out.append(f"{count}x{last:#06x}")
                last = c
                count = 1
        out.append(f"{count}x{last:#06x}")
        print(" ".join(out))

    def get_pixels(self) -> List[int]:
        return list(self.pixels)

class RPiWS281xAdapter:
    def __init__(self, num_pixels: int, pin=18, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0):
        try:
            from rpi_ws281x import PixelStrip
        except Exception as e:
            raise RuntimeError("rpi_ws281x library is required for RPi adapter: " + str(e))
        self.strip = PixelStrip(num_pixels, pin, freq_hz, dma, invert, brightness, channel)
        self.strip.begin()
        self.num_pixels = num_pixels

    def clear(self):
        for i in range(self.num_pixels):
            self.strip.setPixelColor(i, 0)

    def set_pixel(self, index: int, color: int):
        # color is 24-bit RGB int
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        # rpi_ws281x Color order is GRB or according to library - we keep RGB
        from rpi_ws281x import Color
        self.strip.setPixelColor(index, Color(r, g, b))

    def show(self):
        self.strip.show()

class CircuitPythonAdapter:
    def __init__(self, num_pixels: int, pin=None, brightness=0.5, auto_write=False):
        try:
            import board
            import neopixel
        except Exception as e:
            raise RuntimeError("CircuitPython adafruit_neopixel is required: " + str(e))

        # default pin logic left to the caller; using board.D18 when available
        if pin is None:
            pin = getattr(board, 'D18', None)
            if pin is None:
                raise RuntimeError('No default pin found for CircuitPython adapter; pass pin explicitly')

        self.np = neopixel.NeoPixel(pin, num_pixels, brightness=brightness, auto_write=auto_write)
        self.num_pixels = num_pixels

    def clear(self):
        for i in range(self.num_pixels):
            self.np[i] = (0, 0, 0)

    def set_pixel(self, index: int, color: int):
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        self.np[index] = (r, g, b)

    def show(self):
        # NeoPixel may auto-write depending on constructor
        if hasattr(self.np, 'show'):
            self.np.show()
