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
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    //char c = mySerial.read();
    //Serial.println(c);
    str = Serial.readStringUntil('a');
      mySerial.println(str);
  }
  }
