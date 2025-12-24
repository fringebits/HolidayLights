#pragma once

#include "../Adafruit_NeoPixel/Adafruit_NeoPixel.h"
#include "../Nutron/nu_range.h"
#include "../Nutron/nu_color.h"
#include "../Nutron/nu_timer.h"

#define HOUSE_COLOR CRGB(255, 145, 25)

#define PARTY_TIME       8000  // 10s of house party time
#define PARTY_RATE        200  // how frequently to change lights during the party
#define PARTY_PROB         80  // probability of starting a party
#define PARTY_MIN_COOL   1000  // min house party cooldown (before considering a new party)
#define PARTY_MAX_COOL  30000  // max house party cooldown (before considering a new party)
#define POLICE_RATE       100  //
#define DEBUG_RATE       1000  // how often to change debug colors

#define NUM_PARTY_COLORS 10
static uint32_t PartyColors[NUM_PARTY_COLORS] =
{
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_AQUA,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_GREEN_DARK,
    COLOR_GREEN_SPRING,
    COLOR_BLUE_ROYAL,
    COLOR_PINK_HOT
};

static uint32_t PoliceColors[2] =
{
    COLOR_RED,
    COLOR_BLUE
};

enum HouseMode 
{
    NormalMode,
    PartyMode,
    PoliceMode,
    ArrestedMode,
    DebugMode
};

class House : public NuRange
{
public:
    House(int _start = 0, int _count = 0, uint32_t _color = HOUSE_COLOR)
        : NuRange(_start, _count)
        , m_color(_color)
        , m_mode(NormalMode)
    {
    }

    void set_mode(HouseMode mode)
    {
        if (mode == m_mode)
        {
            // don't do anything if we're already in this mode
            return;
        }

        switch(m_mode)
        {
            case PartyMode: // leaving the party mode
                m_partyTimer.Reset(random(PARTY_MIN_COOL, PARTY_MAX_COOL));
                break;
        }

        switch(mode)
        {
            case PoliceMode: // start police!
                m_lastPolice = 0;
                break;

            case PartyMode:  // start a party!
                m_partyTimer.Reset(random(PARTY_TIME>>1, PARTY_TIME));
                break;
        }
        
        m_mode = mode;
    }

    void update(Adafruit_NeoPixel* leds)
    {
        switch(m_mode)
        {
            case NormalMode:
                update_normal(leds);
                break;
            case PoliceMode:
                update_police(leds);
                break;
            case PartyMode:
                update_party(leds);
                break;
            case DebugMode:
                update_debug(leds);
                break;
        }
    }

private:
    void update_normal(Adafruit_NeoPixel *leds)
    {
        for (int jj = 0; jj < m_count; jj++)
        {
            leds->setPixelColor(m_start + jj, m_color);
        }
    }

    void update_party(Adafruit_NeoPixel *leds)
    {        
        if (m_modeDelay.IsExpired())
        {
            m_modeDelay.Reset(PARTY_RATE);

            for (int jj = 0; jj < m_count; jj++)
            {
                auto c = PartyColors[random(NUM_PARTY_COLORS)];
                leds->setPixelColor(m_start + jj, c);
            }
        }

        if (m_partyTimer.IsExpired())
        {
            set_mode(NormalMode);
        }
    }

    void update_police(Adafruit_NeoPixel *leds)
    {
        auto c = PoliceColors[(m_lastPolice) % 2];

        if (m_modeDelay.IsExpired())
        {
            c = PoliceColors[(++m_lastPolice) % 2];
            m_modeDelay.Reset(POLICE_RATE);
        }

        for (int jj = 0; jj < m_count; jj++)
        {
            leds->setPixelColor(m_start + jj, c);
        }
    }

    void update_debug(Adafruit_NeoPixel *leds)
    {
        if (m_modeDelay.IsExpired())
        {
            m_debugColor += 1;
            m_color = PartyColors[m_debugColor % NUM_PARTY_COLORS];
            m_modeDelay.Reset(DEBUG_RATE);
            Serial.print("Debug house: ");
            Serial.println(m_debugColor);
        }
    }

    uint32_t  m_color;
    uint32_t  m_last_color;
    HouseMode m_mode;
	int       m_lastPolice;	
    int       m_debugColor;
    NuTimer   m_partyTimer;
    NuTimer   m_modeDelay; // flash rate (party/police)
};
