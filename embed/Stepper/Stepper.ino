# include <Servo.h> // Servo lib
Servo sv1; // create rc servo object for join1
# include <SoftwareSerial.h> // create a new serial port
# include <avr/io.h>
# include <avr/interrupt.h>
byte reload = 50; //set 100us period for interrupt timer
int count = 0; //make a pulse for step motor if count = 8
unsigned long T_delay; // T_delay for delay function
int STmoi = 0; // the value of angle calculated by set pulse - current
int STcu = 0; // the old value angle of step motor for comparing with new current value angle
int Xung_Xoay = 0; // the set pulse value
const int stepPin = 4; // make pulse for step motor
const int dirPin = 7; // direction for step motor pin
const int enPin = 8; //brake step motor pin
const int BZ = A5; // buzzer pin
const int LED = 13; // led built-in
void setup() {
  // init serial communication
  Serial.begin(9600); // Arduino internal serial
  Serial.println("step1: init serial -> DONE");
  // init servo
  sv1.attach(3);
  Serial.println("step2: init RC servo -> DONE");
  // init pin mode
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(BZ,OUTPUT);
  pinMode(LED,OUTPUT);
  Serial.println("step3: init pins -> DONE");
  // init timer
  cli(); // disable all interrupt before you done setting up
  Serial.println("step4: init timer -> DOING...");
}

void loop() {
  // put your main code here, to run repeatedly:
  sv1.write(90); // raise the arm before rotate step motor

}
