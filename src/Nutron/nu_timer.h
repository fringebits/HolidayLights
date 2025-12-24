
 #pragma once

class NuTimer
{
public:
    NuTimer(uint32_t duration = 0)
        : m_debug(false)
        , m_duration(duration) 
    { 
        Reset(duration);
    }

    void Reset()
    {
        m_startTime = millis();
        if (m_debug)
        {
        Serial.print("NuTimer: dur=");
        Serial.print(m_duration);
        Serial.print(", start=");
        Serial.println(m_startTime);
        }
    }

    void Reset(uint32_t duration) 
    {
        m_duration = duration;
        Reset();
    }

    bool IsExpired()
    {
        auto runTime = millis();

        if (runTime > (m_startTime + m_duration))
        {
            return true;
        }

        return false;
    }

    void SetDebug(bool flag)
    {
        m_debug = flag;
    }

private:
    uint32_t m_duration;     // how long this timer lasts
    uint32_t m_startTime;    // current value
    bool m_debug;
}; 