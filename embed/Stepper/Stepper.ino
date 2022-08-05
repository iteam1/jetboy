# include <Servo.h> // Servo lib
Servo sv1,sv2,sv3,sv4;  // robot's arm have 4 rc servo
# include <SoftwareSerial.h> // create a new serial port
#include <avr/io.h>
#include <avr/interrupt.h>
#include <EEPROM.h>
byte reload = 50;  //100us for interupt timer
int count = 0; //make a pulse for step motor if count == 8
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
  // init RC servos
  sv1.attach(9);  // attaches the servo on pin 9 to the servo object
  sv2.attach(6);
  sv3.attach(5);
  sv4.attach(3);
  Serial.println("step2: init RC servo -> DONE");
  // init pin mode
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(BZ,OUTPUT);
  pinMode(LED,OUTPUT);
  Serial.println("step3: init pins -> DONE");
  // init timer
  Serial.println("step4: init timer -> DOING...");
//  cli(); // disable all interrupt before you done setting up
//  TCCR0B = 0; 
//  OCR2A = reload;
//  TCCR2A = 1<<WGM21;
//  TCCR2B = ((1<<CS21) | (1<<CS20));//1<<CS22)
//  TIMSK2 = (1<<OCIE2A);
//  sei();
  // init stepper motor
  digitalWrite(enPin,0); //0 la BRAKE, 1 la REALSE
  digitalWrite(dirPin,0);
  digitalWrite(stepPin,0);
  // sound out
  beep(5,100);
  stand_by();
  rotate();
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void rotate(){
  digitalWrite(enPin,1); //0 la BRAKE, 1 la REALSE
  digitalWrite(dirPin,0);
  digitalWrite(stepPin,0);
  
  for(int i = 0; i <= 300; i++){
    digitalWrite(stepPin,1);
    delayMicroseconds(500);
    digitalWrite(stepPin,1);
    delayMicroseconds(500);
    }
  
  digitalWrite(dirPin,1);
  
  for(int i = 0; i <= 300; i++){
    digitalWrite(stepPin,1);
    delayMicroseconds(500);
    digitalWrite(stepPin,1);
    delayMicroseconds(500);
    }
  }

void stand_by(){
  sv1.write(50); // raise the arm before rotate step motor
  sv2.write(90);
  sv3.write(0);
  sv4.write(170); 
  }

void beep(int times,int sleep){
  for(int i = 0;i<=times;i++){
    digitalWrite(BZ,1);
    delay(sleep);
    digitalWrite(BZ,0);
    delay(sleep);
    }
  }
