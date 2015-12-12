// This #include statement was automatically added by the Particle IDE.
#include "adafruit-led-backpack/adafruit-led-backpack.h"

    // static String t = "";
    // /***************************************************
    //   This is a library for our I2C LED Backpacks

    //   Designed specifically to work with the Adafruit LED Matrix backpacks
    //   ----> http://www.adafruit.com/products/872
    //   ----> http://www.adafruit.com/products/871
    //   ----> http://www.adafruit.com/products/870

    //   These displays use I2C to communicate, 2 pins are required to
    //   interface. There are multiple selectable I2C addresses. For backpacks
    //   with 2 Address Select pins: 0x70, 0x71, 0x72 or 0x73. For backpacks
    //   with 3 Address Select pins: 0x70 thru 0x77

    //   Adafruit invests time and resources providing this open source code,
    //   please support Adafruit and open-source hardware by purchasing
    //   products from Adafruit!

    //   Written by Limor Fried/Ladyada for Adafruit Industries.
    //   BSD license, all text above must be included in any redistribution
    //  ****************************************************/

    // // #include "adafruit-led-backpack/adafruit-led-backpack.h"

Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

int x;               // x axis variable
int y;               // y axis variable
int z;               // z axis variable
float filterVal;     // this determines smoothness  - .0001 is max  1 is off (no
                     // smoothing)
float smoothedValy;  // this holds the last loop value just use a unique
                     // variable for every different sensor that needs smoothing
float smoothedValx;  // this would be the buffer value for another sensor if you
                     // needed to smooth two different sensors - not used in
                     // this sketch
float smoothedValz;  // this would be the buffer value for another sensor if you
                     // needed to smooth two different sensors - not used in
                     // this sketch
String accel;
int i, j;  // loop counters or demo
int pos = 0;  // 1 for upright and 0 for facing down
int shapeIdx = 0;

void setup() {
  Serial.begin(9600);  // opens serial port, sets data rate to 9600 bps
  //   pinMode(0, OUTPUT);
  // Spark.variable("accel", accel);
  Particle.variable("getpos", &pos, INT);

  matrix.begin(0x70);  // pass in the address
  Particle.function("tile", changeTile);
}

static const uint8_t shapes[22][8] = {

    //the following is NSEW [0-3]
    {B00000000, B10000100, B11000100, B10100100, B10010100, B10001100,
     B10000100, B00000000},

    {B00000000, B11111100, B10000000, B11111100, B10000000, B10000000,
     B11111100, B00000000},

    {B00000000, B01111000, B10000100, B01111000, B00000100, B10000100,
     B01111000, B00000000},

    {B00000000, B10000100, B10000100, B10000100, B10110100, B11001100,
     B11001100, B00000000},
    // the following is circle suit [4-12]
    {B00000000, B00110000, B01111000, B11111100, B11111100, B01111000,
     B00110000, B00000000},

    {B00110000, B01111000, B00110000, B00000000, B00000000, B00110000,
     B01111000, B00110000},

    {B10000001, B10000001, B00000000, B00110000, B00110000, B00000000,
     B00000110, B00000110},

    {B10000111, B10000111, B00000000, B00000000, B00000000, B00000000,
     B10000111, B10000111},

    {B10000111, B10000111, B00000000, B00110000, B00110000, B00000000,
     B10000111, B10000111},

    {B11001100, B11001100, B00000000, B11001100, B11001100, B00000000,
     B11001100, B11001100},

    {B00110000, B00110000, B00000000, B10110111, B10110111, B00000000,
     B10110111, B10110111},

    {B11001100, B11001100, B00000000, B10110111, B10110111, B00000000,
     B10110111, B10110111},

    {B10110111, B10110111, B00000000, B10110111, B10110111, B00000000,
     B10110111, B10110111},

    // the following is number suit [13-21]
    {B00000000, B00010000, B00110000, B00010000, B00010000, B00010000,
     B00010000, B01111100},

    {B00000000, B00111000, B00100100, B00000100, B00001000, B00010000,
     B00100000, B01111100},

    {B00000000, B01111100, B00001000, B00010000, B00001000, B00000100,
     B01000100, B00111000},

    {B00000000, B00001000, B00011000, B00101000, B01001000, B01111100,
     B00001000, B00001000},

    {B00000000, B01111100, B01000000, B01111000, B00000100, B00000100,
     B00000100, B01111000},

    {B00000000, B00011000, B00100000, B01000000, B01111000, B01000100,
     B01000100, B00111000},

    {B00000000, B01111100, B00000100, B00001000, B00010000, B00100000,
     B00100000, B00100000},

    {B00000000, B00111000, B01000100, B01000100, B00111000, B01000100,
     B01000100, B00111000},

    {B00000000, B00111000, B01000100, B01000100, B00111100, B00000100,
     B00001000, B00110000}};
void loop() {
  //   digitalWrite(0, HIGH);

  for (i = 0; i < 1; i++) {  // substitute some different filter values
    filterVal = i * .15;
    x = analogRead(2);  // read A5 input pin
    y = analogRead(1);  // read A4 input pin
    z = analogRead(0);  // read A3 input pin
    // sensVal = analogRead(0);   this is what one would do normally
    smoothedValx = smooth(x, filterVal, smoothedValx);  // second parameter
                                                        // determines smoothness
                                                        // - 0 is off,  .9999 is
                                                        // max smooth
    smoothedValy = smooth(y, filterVal, smoothedValy);  // second parameter
                                                        // determines smoothness
                                                        // - 0 is off,  .9999 is
                                                        // max smooth
    smoothedValz = smooth(z, filterVal, smoothedValz);  // second parameter
                                                        // determines smoothness
                                                        // - 0 is off,  .9999 is
                                                        // max smooth

    Serial.print(x);
    Serial.print("   ");
    Serial.print(smoothedValx, DEC);
    Serial.print("      ");
    Serial.print(y);
    Serial.print("   ");
    Serial.print(smoothedValy, DEC);
    Serial.print("      ");
    Serial.print(z);
    Serial.print("   ");
    Serial.print(smoothedValz, DEC);
    Serial.print("      ");
    Serial.print("filterValue * 100 =  ");  // print doesn't work with floats
    Serial.println(filterVal * 100, DEC);
    //   if((1570<smoothedValx<1470) && (1300<smoothedValy<1200) &&
    //   (2050<smoothedValz<1950)){
    if (smoothedValx < 1250 || smoothedValy < 800) {
      pos = 1;
      matrix.clear();
      matrix.drawBitmap(0, 0, shapes[shapeIdx], 8, 8, LED_GREEN);
      // matrix.drawBitmap(0, 0, shapes[0], 8, 8, LED_GREEN);

      matrix.writeDisplay();
      delay(100);
    }
    //   if(smoothedValx < 1520 && smoothedValy < 1250 ){
    else {
      pos = 0;
      matrix.clear();
      // matrix.drawBitmap(0, 0, north, 8, 8, LED_GREEN);
      matrix.writeDisplay();
      delay(100);
    }
    delay(200);
  } // end for loop

}



// PUBLISH STUFF TO OUR SERVER
#define publish_delay 5000
unsigned int lastPublish = 0;


void photonPublishUpdates(float x, float y, float z) {
    String payload = "";

    unsigned long now = millis();

    if ((now - lastPublish) < publish_delay) {
        // it hasn't been 10 seconds yet...
        return;
    }

    payload = payload + "{";
    payload = payload + "\"endpoint\": \"photonUpdate\","
    payload = payload + "\"x\":\"" + String(x) + "\","
    payload = payload + "\"y\":\"" + String(y) + "\","
    payload = payload + "\"z\":\"" + String(z) + "\","
    payload = payload + "\"orientation\":\"" + String(pos) + "\","
    payload = payload + "\"tile\":\"" + String(shapeIdx) + "\","
    payload = payload + "\"timestamp\":\"" + String(now) + "\""
    payload = payload + "}";

    Spark.publish("custom_publish_event", payload, 60, PRIVATE);

    lastPublish = now;
}

int smooth(int data, float filterVal, float smoothedVal) {
  if (filterVal > 1) {  // check to make sure param's are within range
    filterVal = .99;
  } else if (filterVal <= 0) {
    filterVal = 0;
  }

  smoothedVal = (data * (1 - filterVal)) + (smoothedVal * filterVal);

  return (int)smoothedVal;
}

int changeTile(String command) {
  shapeIdx = command.toInt();
  return shapeIdx;
}
