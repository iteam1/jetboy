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
bool in_run = true; // step motor is running, stop = false 

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
  else{
    Serial.println("Communicate via mySerial");
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
  // read count
  count = EEPROM.read(0);
  // accumulate count and store in pulse
  if(dir){
    count -= pulses;
    }
  else{
    count += pulses;
    }
  EEPROM.write(0,count);
  
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

void flip_up(){
  rotate(400,1200,0);// forward
  while(in_run); // while step motor is runing don't run servo rc
  sv2.write(150);
  rotate(300,1200,0);
  while(in_run);
  sv2.write(180);
  rotate(500,1200,0);
  while(in_run);
  sv3.write(180);
  }

void lay_down(){
  
  sv3.write(90);
  delay(50);
  sv2.write(160);
  delay(50);
  rotate(200,1200,1);
  while(in_run);
  sv2.write(130);
  delay(100);
  rotate(200,1200,1);
  while(in_run);
  sv2.write(100);
  delay(100);
  rotate(200,1200,1);
  while(in_run);
  sv2.write(80);
  rotate(500,1200,1);
  }

void grip(){
  for(size_t i = 20;i<=60;i++){
    sv1.write(i);
    delay(5);
    }
  delay(1000);
  for(size_t i = 60;i>=20;i--){
    sv1.write(i);
    delay(5);
    }
  }
void say_hello(){
  flip_up();
  delay(2000);
  test_grip();
  delay(100);
  test_grip();
  delay(3000);
  grip();
  delay(3000);
  lay_down();
  delay(100);
  stand_by();
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
    else if(Val=="forward"){
      forward();
      }
    else if(Val=="backward"){
      backward();
      }
    else if(Val=="up"){
      flip_up();
      }
    else if(Val=="down"){
      lay_down();
      }
    else if(Val=="hello"){
      say_hello();
      }
    else if(Val=="count"){
      count = EEPROM.read(0);
      Serial.println(count); // query the count value of step motor
      }
    else{
      Serial.println(Val);
      }
    }
  }

void mycomm(){
  /*
   * communicate with robot's arm by serial built-in port 
   */
   if (mySerial.available()){
    // get the serial string until q
    Val = mySerial.readStringUntil('q'); // Accept 'q' not accept "q"??
    if(Val=="who"){
      mySerial.println("arm");
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
    else if(Val=="forward"){
      forward();
      }
    else if(Val=="backward"){
      backward();
      }
    else if(Val=="up"){
      flip_up();
      }
    else if(Val=="down"){
      lay_down();
      }
    else if(Val=="hello"){
      say_hello();
      }
    else if(Val=="count"){
      count = EEPROM.read(0);
      mySerial.println(count); // query the count value of step motor
      }
    else{
      mySerial.println(Val);
      }
    }
  }
