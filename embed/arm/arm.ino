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
# include <avr/io.h>
# include <avr/interrupt.h>
# include <EEPROM.h>
# include <Servo.h> // Servo lib
# include <SoftwareSerial.h> // External serial port

SoftwareSerial mySerial(11,10); // create a serial object for uart communicate 11=Rx,10=Tx
Servo sv1,sv2,sv3,sv4;  // robot's arm have 4 rc servo

int count = 0; // make counter count pulse of step motor

unsigned long Tdelay; // count tick-value of timer for delay function

const int BT = 12; // button on board
const int RES = A0; // the potential meter
const int BZ = A5; // buzzer
const int LED = 13; // buildtin led

const int stepPin = 4; // make pulse for step motor
const int dirPin = 7; // direction for step motor pin
const int enPin = 8; //brake step motor pin
const int rev = 1600;
bool in_run = false; // step motor is running, stop = false 

String Val = "";

bool myserial = false; // option to choice builtin serial or mySerial port

void setup() {

  //Serial setup
  Serial.begin(9600);
  mySerial.begin(9600);

  // init servo
  sv1.attach(9);  // attaches the servo on pin 9 to the servo object
  sv2.attach(6);
  sv3.attach(5);
  sv4.attach(3);

  // button, potential, buzzer
  pinMode(BT,INPUT); // button on board
  pinMode(RES,INPUT); // the potential meter
  pinMode(BZ,OUTPUT); // buzzer
  pinMode(LED,OUTPUT); // Led build in
  
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);

  // brake and buzzer setup
  digitalWrite(enPin,1); // 0 is realse, 1 is brake
  digitalWrite(BZ,0); // 0 is off, 1 is buzz

  //store the value of counter into EEPROM
  EEPROM.write(0,count); // store in the position 0 value of count,  Read count = EEPROM.read(0);

  // stand by postion
  stand_by();
  
  // peep check
  peeps(3);

  // what kind of serial you are using?
  if(not myserial){
    Serial.println("From Serial: Robot Arm Hello!");
    }
}
void loop() {
  if(myserial){
    mycomm();
    }
  else{
    comm();
    }
  }

void peep(){
  /*
   * a single peep function
   */
  digitalWrite(BZ,HIGH);
  delay(100); // delay 100 ms by sleep function
  digitalWrite(BZ,LOW);
  }

void peeps(int t){
  /*
   * multi peep function
   */
  for(int i=0;i<t;i++){
    peep();
    delay(100); // delay 100 ms by sleep function
    }
  }

void stand_by(){
  /*
  robot's arm go to standby posture
  */
  sv1.write(20);
  sv2.write(80);
  sv3.write(90);
  sv4.write(130); 
  }

void rotate(int pulses,int microTime,bool dir){
  /*
  robot's arm rotate a setup angle
  */
  // set limit for pulses
  if(pulses >1100){
    pulses = 1100;
    }
  in_run = true;
  digitalWrite(enPin,0); // realse brake and go
  digitalWrite(dirPin,dir);
  
  for(int x = 0; x < pulses; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(microTime); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(microTime); 
   }

   digitalWrite(enPin,1); // brake
   delay(1000);
   in_run = false;
  }

void test_grip(){
  /*test servo grip*/
  sv4.write(150);
  delay(100);
  sv4.write(130);
  }
  
void test_step(){
  /*
   * test step motor function
  */
  rotate(100,1200,0);// forward
  delay(1000);
  rotate(100,1200,1);// backward      
  }

void forward(){
  /*
   * go forward 100 pulses
   */
   rotate(100,1200,0);// forward
  }

void backward(){
  /*
   * go backward 100 pulses
   */
   rotate(100,1200,1);// backward
  }
  
void say_hello(){
  rotate(100,1200,0);// forward
  while(in_run);
  test_grip();
  }

void comm(){
  /*
   * communicate with robot's arm by serial built-in port 
   */
   if (Serial.available()){
    // get the serial string until q
    Val = Serial.readStringUntil('q'); // Accept 'q' not accept "q"??
    if(Val=="who"){
      Serial.println("arm");
      }
    else if(Val=="peeps"){
      peeps(5);
      }
    else if(Val=="grip"){
      test_grip();
      }
    else if(Val=="step"){
      test_step();
      }
    else if(Val=="hello"){
      say_hello();
      }
    else{
      Serial.println(Val);
      }
    }
  }

 void mycomm(){}
