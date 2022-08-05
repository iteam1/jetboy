/*
 * https://nshopvn.com/product/mach-dieu-khien-dong-co-buoc-tb6600-5a-hy-div268n/?gclid=Cj0KCQjw_7KXBhCoARIsAPdPTfi90oOPmzix3mB6K9zfVeSNNHptESnVxldMXMKFD_zgTHs-L6sKvdsaAnjvEALw_wcB
  Kết nối:
          TB6600                  Arduino
           ENA+                      enPin
           DIR+                      dirPin
           PUL+                      stepPin
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
  
}
void loop() {
  
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 800; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay

  digitalWrite(dirPin,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 800; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(500);
  }
  delay(1000);
  
}

void stand_by(){
  sv1.write(50); // raise the arm before rotate step motor
  sv2.write(90);
  sv3.write(0);
  sv4.write(170); 
  }
