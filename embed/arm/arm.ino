/*
 * https://nshopvn.com/product/mach-dieu-khien-dong-co-buoc-tb6600-4-0a-942vdc/
 * Kết nối:
          TB6600                  Arduino
           ENA+                     8-enPin
           DIR+                     7-dirPin
           PUL+                     4-stepPin
           ENA-                     GND
           DIR-                     GND
           PUL-                     GND

  A+ A- B+ B- kết nối với động cơ

  Nguồn đầu vào là 9V - 42V.
 */
# include <Servo.h> // Servo lib
# include <SoftwareSerial.h> // External serial port

SoftwareSerial mySerial(11,10); // create a serial object for uart communicate 11=Rx,10=Tx
Servo sv1,sv2,sv3,sv4;  // robot's arm have 4 rc servo

const int BT = 12; // button on board
const int RES = A0; // the potential meter
const int BZ = A5; // buzzer
const int stepPin = 4; // make pulse for step motor
const int dirPin = 7; // direction for step motor pin
const int enPin = 8; //brake step motor pin
const int rev = 1600;

void setup() {

  // button, potential, buzzer
  pinMode(BT,INPUT); // button on board
  pinMode(RES,INPUT); // the potential meter
  pinMode(BZ,OUTPUT); // buzzer

  // init servo
  sv1.attach(9);  // attaches the servo on pin 9 to the servo object
  sv2.attach(6);
  sv3.attach(5);
  sv4.attach(3);
  
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);

  // stand by postion
  stand_by();
  
  // peep check
  peeps(5);
}
void loop() {
}

void peep(){
  digitalWrite(BZ,HIGH);
  delay(100);
  digitalWrite(BZ,LOW);
  }

void peeps(int t){
  for(int i=0;i<t;i++){
    peep();
    delay(100);
    }
  }

void stand_by(){
  sv1.write(20); // raise the arm before rotate step motor
  sv2.write(80);
  sv3.write(90);
  sv4.write(130); 
  }

void rotate(int pulses,int microTime,bool dir){
  // set limit for pulses
  if(pulses >1100){
    pulses = 1100;
    }
  digitalWrite(dirPin,dir);
  for(int x = 0; x < pulses; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(microTime); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(microTime); 
  }
  }
