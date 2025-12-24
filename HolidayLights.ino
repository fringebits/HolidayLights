#include "src/NeoHouse/neo_hoa.h"

#define DATA_PIN      7  	// this is the data pin connected to the LED strip.  If using WS2801 you also need a clock pin
#define NUM_LIGHTS  200	// change this for the number of LEDs in the strip

#define NUM_HOUSES 27
#define FIRST_HOUSE 0

#define POLICE_HOUSE 22

#define HOUSE_COLOR CRGB(255, 145, 25)

// Create an instance of the Adafruit_NeoPixel class called "leds".
// RGB color order, 800 KHz
Adafruit_NeoPixel all_leds = Adafruit_NeoPixel( NUM_LIGHTS, DATA_PIN, NEO_RGB + NEO_KHZ800 );

House all_houses[NUM_HOUSES] = {
    House(  0, 1), 
    House(  8, 2),
    House( 13, 2),
    House( 19, 2),
    House( 24, 2),
      
    House( 34, 2),  
    House( 39, 2),
    House( 44, 2),  
    House( 50, 2),
    
    House( 64, 1), // lighthoues
    //House( 67, 2),
    House( 71, 2), // winery
    House( 77, 2), // toystore

    House( 88, 2),
    House( 95, 2),
    House(100, 2),

    House(108, 2),
    House(113, 2),
    House(119, 2),
    
    House(130, 2),
    House(138, 2),
    House(144, 2), // gift shop
    
    House(154, 2),
    House(159, 2),
    House(164, 2),
    House(171, 2),

    House(183, 2),
    House(197, 3),
};

HOA hoa = HOA(all_houses, NUM_HOUSES, POLICE_HOUSE);

void update_hoa(Adafruit_NeoPixel* leds) 
{
    leds->clear();

    hoa.update(leds);

    leds->show();
}

void update_leds(Adafruit_NeoPixel* leds)
{
    leds->clear();
    static int index = 0;

    index = (index + 1) % NUM_LIGHTS;

    leds->setPixelColor(index, HOUSE_COLOR);
    
    leds->show();

    delay(100);
}

void setup()
{
    Serial.begin(9600); // 57600);  // print for debug
    Serial.println("setup()");
    randomSeed(analogRead(A0));

    all_leds.begin();
    update_hoa(&all_leds);
    all_houses[0].set_mode(DebugMode);
}

void loop()
{
    update_hoa(&all_leds);
}
