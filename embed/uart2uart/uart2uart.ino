#include <avr/io.h>
#include <avr/interrupt.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(11, 10); // TX, RX
String str="";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (mySerial.available()) {
    //char c = mySerial.read();
    //str = mySerial.read();
    //str = mySerial.readString();
    str = mySerial.readStringUntil('a');
    //blink();
    if(str == "90,90,90,90,90,1"){
      blink();
      }
    //Serial.println(str);
  }
  }

void blink(){
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
  }
