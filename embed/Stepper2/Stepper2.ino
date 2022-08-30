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
Servo sv1,sv2,sv3,sv4;  // robot's arm have 4 rc servo

const int stepPin = 4; // make pulse for step motor
const int dirPin = 7; // direction for step motor pin
const int enPin = 8; //brake step motor pin
const int rev = 1600;

void setup() {

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
  // stepper
  rotate(300,800,0); // 0 = forward, 1 = backward, 1100 pulses = 90 degree  
}
void loop() {
  test();
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

void test(){
  rotate(300,800,0);
  delay(1000); // One second delay
  rotate(300,800,1);
  delay(1000);
  }
