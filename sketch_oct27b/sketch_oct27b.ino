#include <EEPROM.h>
#include "TimerOne.h"
#include <Wire.h>
#include "MultiFuncShield.h"
#include "GravityTDS.h"
#include "TM1637.h"
#define CLK 2
#define DIO 3
#define TdsSensorPin A5

TM1637 tm1637(CLK,DIO);
GravityTDS gravityTds;

float temperature = 25;
int tdsValue = 0;
int a = 1;
int b = 1;

void setup()
{
    Serial.begin(115200);
    pinMode(9,OUTPUT);
    pinMode(6,OUTPUT);
    pinMode(5,OUTPUT);
    Timer1.initialize();
    MFS.initialize(&Timer1);
    tm1637.set();
    tm1637.init(); 
    tm1637.set(BRIGHT_TYPICAL);
    gravityTds.setPin(TdsSensorPin);
    gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds.begin();  //initialization
}

void loop()
{
    //temperature = readTemperature();  //add your temperature sensor and read it
    gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
    gravityTds.update();  //sample and calculate
    tdsValue = gravityTds.getTdsValue();  // then get the value
    MFS.write(tdsValue);
    b = analogRead(A4);
    Serial.println(b);
    if (b >= 1000 and a >= 1000){MFS.beep(15,0,1,1,0);}
    a = analogRead(A4);
    if (tdsValue <= 10){digitalWrite(6,1);digitalWrite(9,0);digitalWrite(5,0);}
    else if(tdsValue <= 20){digitalWrite(6,0);digitalWrite(9,0);digitalWrite(5,1);}
    else {digitalWrite(6,0);digitalWrite(9,1);digitalWrite(5,0);}
    delay(1000);
}