"""Core classes ported from the Arduino sketch: NuTimer, NuRange, House, HOA, colors."""
from enum import Enum
import time
import random
from typing import List

# Time helpers
def millis():
    return int(time.monotonic() * 1000)

# Color helpers
def CRGB(r, g, b):
    return (r << 16) + (g << 8) + b

COLOR_WHITE = CRGB(255, 255, 255)
COLOR_AQUA = CRGB(0, 255, 255)
COLOR_ORCHID = CRGB(153, 50, 204)
COLOR_YELLOW = CRGB(255, 255, 0)
COLOR_GREEN_SPRING = CRGB(0, 255, 127)
COLOR_ORANGE = CRGB(255, 165, 0)
COLOR_BLUE_ROYAL = CRGB(65, 105, 255)
COLOR_PURPLE_DARK = CRGB(76, 0, 153)
COLOR_PINK_HOT = CRGB(255, 105, 180)
COLOR_GREEN_DARK = CRGB(0, 128, 0)
COLOR_RED = CRGB(255, 0, 0)
COLOR_GREEN = CRGB(0, 255, 0)
COLOR_BLUE = CRGB(0, 0, 255)

# Arduino constants
HOUSE_COLOR = CRGB(255, 145, 25)

PARTY_TIME = 8000
PARTY_RATE = 200
PARTY_PROB = 80
PARTY_MIN_COOL = 1000
PARTY_MAX_COOL = 30000
POLICE_RATE = 100
DEBUG_RATE = 1000

NUM_PARTY_COLORS = 10
PartyColors = [
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_AQUA,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_GREEN_DARK,
    COLOR_GREEN_SPRING,
    COLOR_BLUE_ROYAL,
    COLOR_PINK_HOT,
]

PoliceColors = [COLOR_RED, COLOR_BLUE]

class NuTimer:
    def __init__(self, duration: int = 0):
        self._duration = duration
        self._start = millis()

    def reset(self, duration: int = None):
        if duration is not None:
            self._duration = duration
        self._start = millis()

    def is_expired(self):
        return millis() > (self._start + self._duration)

class NuRange:
    def __init__(self, start=0, count=0):
        self.m_start = start
        self.m_count = count

class HouseMode(Enum):
    NormalMode = 0
    PartyMode = 1
    PoliceMode = 2
    ArrestedMode = 3
    DebugMode = 4

class House(NuRange):
    def __init__(self, start=0, count=0, color=HOUSE_COLOR):
        super().__init__(start, count)
        self.m_color = color
        self.m_mode = HouseMode.NormalMode
        self.m_lastPolice = 0
        self.m_debugColor = 0
        self.m_partyTimer = NuTimer(0)
        self.m_modeDelay = NuTimer(0)

    def set_mode(self, mode: HouseMode):
        if mode == self.m_mode:
            return

        # leaving modes
        if self.m_mode == HouseMode.PartyMode:
            self.m_partyTimer.reset(random.randrange(PARTY_MIN_COOL, PARTY_MAX_COOL))

        # entering modes
        if mode == HouseMode.PoliceMode:
            self.m_lastPolice = 0
        elif mode == HouseMode.PartyMode:
            self.m_partyTimer.reset(random.randrange(PARTY_TIME >> 1, PARTY_TIME))

        self.m_mode = mode

    def update(self, leds):
        if self.m_mode == HouseMode.NormalMode:
            self._update_normal(leds)
        elif self.m_mode == HouseMode.PartyMode:
            self._update_party(leds)
        elif self.m_mode == HouseMode.PoliceMode:
            self._update_police(leds)
        elif self.m_mode == HouseMode.DebugMode:
            self._update_debug(leds)

    def _update_normal(self, leds):
        for jj in range(self.m_count):
            leds.set_pixel(self.m_start + jj, self.m_color)

    def _update_party(self, leds):
        if self.m_modeDelay.is_expired():
            self.m_modeDelay.reset(PARTY_RATE)
            for jj in range(self.m_count):
                c = random.choice(PartyColors)
                leds.set_pixel(self.m_start + jj, c)

        if self.m_partyTimer.is_expired():
            self.set_mode(HouseMode.NormalMode)

    def _update_police(self, leds):
        c = PoliceColors[self.m_lastPolice % 2]
        if self.m_modeDelay.is_expired():
            self.m_lastPolice = (self.m_lastPolice + 1) % 2
            c = PoliceColors[self.m_lastPolice]
            self.m_modeDelay.reset(POLICE_RATE)
        for jj in range(self.m_count):
            leds.set_pixel(self.m_start + jj, c)

    def _update_debug(self, leds):
        if self.m_modeDelay.is_expired():
            self.m_debugColor += 1
            self.m_color = PartyColors[self.m_debugColor % NUM_PARTY_COLORS]
            self.m_modeDelay.reset(DEBUG_RATE)
            # Note: Serial prints removed in Python port

class HOA:
    def __init__(self, houses: List[House], num_houses: int, police_house: int):
        self.m_allHouses = houses
        self.m_numHouses = num_houses
        self.m_policeHouseIndex = police_house
        self.m_partyTime = False
        self.m_partyTimer = NuTimer(random.randrange(0, PARTY_MAX_COOL))
        self.m_partyHouse = 0
        self.m_policeTimer = NuTimer(0)
        self.m_policeHouse = police_house
        self.m_partyDirection = 1

    def update(self, leds):
        if self.m_partyTime:
            # police reached party?
            if self.m_policeHouse == self.m_partyHouse:
                if self.m_policeTimer.is_expired():
                    self.m_partyTime = False
                    self.m_allHouses[self.m_partyHouse].set_mode(HouseMode.NormalMode)
                    self.m_allHouses[self.m_policeHouseIndex].set_mode(HouseMode.NormalMode)
                    self.m_partyTimer.reset(random.randrange(0, PARTY_MAX_COOL))
            elif self.m_policeTimer.is_expired():
                if self.m_policeHouse != self.m_policeHouseIndex:
                    self.m_allHouses[self.m_policeHouse].set_mode(HouseMode.NormalMode)

                self.m_policeHouse += self.m_partyDirection
                self.m_allHouses[self.m_policeHouse].set_mode(HouseMode.PoliceMode)

                if self.m_policeHouse == self.m_partyHouse:
                    self.m_policeTimer.reset(2000)  # ARREST_TIME
                else:
                    self.m_policeTimer.reset(200)
        elif self.m_partyTimer.is_expired():
            partyTime = random.randrange(0, 100) < PARTY_PROB
            if partyTime:
                self.m_partyTimer.reset(random.randrange(PARTY_TIME >> 1, PARTY_TIME))
                self.m_partyTime = True

                partyHouse = self.m_policeHouseIndex
                while partyHouse == self.m_policeHouseIndex:
                    partyHouse = random.randrange(0, self.m_numHouses)

                self.m_partyHouse = partyHouse
                self.m_allHouses[partyHouse].set_mode(HouseMode.PartyMode)
                self.m_allHouses[self.m_policeHouseIndex].set_mode(HouseMode.PoliceMode)

                self.m_policeHouse = self.m_policeHouseIndex
                self.m_policeTimer.reset(200)  # POLICE_COOL
                self.m_partyDirection = 1 if self.m_policeHouseIndex < partyHouse else -1
            else:
                self.m_partyTimer.reset(random.randrange(0, PARTY_MAX_COOL))

        for i in range(self.m_numHouses):
            self.m_allHouses[i].update(leds)
