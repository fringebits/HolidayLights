#pragma once

#include "neo_house.h"

// #define HOUSE_COLOR CRGB(255, 145, 25)

#define PARTY_TIME 8000  // 10s of house party time
#define PARTY_RATE 200   // how frequently to change lights during the party
#define PARTY_PROB 100   // probability of starting a party
#define PARTY_COOL 10000 // 30s of house party cooldown (before considering a new party)

#define POLICE_COOL 200  // 200ms before the police move to the next house
#define ARREST_TIME 2000 // 2s of arrest time

class HOA
{
public:
    HOA(House* houses, int numHouses, int policeHouse)
    {
        m_allHouses = houses;
        m_partyTimer.Reset(random(PARTY_COOL));
    }

    void update(Adafruit_NeoPixel *leds)
    {
        if (m_partyTime)
        {
            if (m_policeHouse == m_partyHouse) // check if police reached the house
            {
                if (m_policeTimer.IsExpired())
                {
                    m_partyTime = false;
                    m_allHouses[m_partyHouse].set_mode(NormalMode);
                    m_allHouses[m_policeHouseIndex].set_mode(NormalMode);
                    m_partyTimer.Reset(random(PARTY_COOL));
                }
            }
            else if (m_policeTimer.IsExpired()) // move the police towards the party house
            {
                if (m_policeHouse != m_policeHouseIndex)
                {
                    m_allHouses[m_policeHouse].set_mode(NormalMode);
                }

                m_policeHouse += m_partyDirection;
                m_allHouses[m_policeHouse].set_mode(PoliceMode);

                if (m_policeHouse == m_partyHouse)
                {
                    m_policeTimer.Reset(ARREST_TIME);
                }
                else
                {
                    m_policeTimer.Reset(POLICE_COOL);
                }
            }
        }
        else if (m_partyTimer.IsExpired())
        {
            auto partyTime = random(100) < PARTY_PROB;
            if (partyTime)
            {
                m_partyTimer.Reset(random(PARTY_TIME >> 1, PARTY_TIME));
                m_partyTime = true;

                int partyHouse = m_policeHouseIndex;
                while (partyHouse == m_policeHouseIndex)
                {
                    partyHouse = random(m_numHouses);
                }

                m_partyHouse = partyHouse;
                m_allHouses[partyHouse].set_mode(PartyMode);
                m_allHouses[m_policeHouseIndex].set_mode(PoliceMode);

                m_policeHouse = m_policeHouseIndex;
                m_policeTimer.Reset(POLICE_COOL);
                m_partyDirection = m_policeHouseIndex < partyHouse ? 1 : -1;
            }
            else
            {
                m_partyTimer.Reset(random(PARTY_COOL));
            }
        }

        for (int i = 0; i < m_numHouses; i++)
        {
            m_allHouses[i].update(leds);
        }
    }

private:
    int m_numHouses;
    int m_policeHouseIndex;

    House* m_allHouses;
    bool m_partyTime;
    NuTimer m_partyTimer;
    int m_partyHouse;

    NuTimer m_policeTimer;
    int m_policeHouse;
    int m_partyDirection;
};