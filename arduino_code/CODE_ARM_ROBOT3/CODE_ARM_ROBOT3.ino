#include <avr/io.h>
#include <avr/interrupt.h>
byte reload = 50;  //100us for interupt timer
int count = 0; //make a pulse for step motor if count == 8
unsigned long Tmoi,T_delay; // T_delay for delay function
#include <EEPROM.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(11, 10); // create a serial object for uart communicate 11 = RX, 10 = TX
#include <Servo.h>
#include <string.h>
Servo sv4,sv3, sv2, sv1;  // create servo object to control a servo
#define motorInterfaceType 1
String s=""; // the framework string to communicate with main control board
int g1,g2,g3,g4; // useless
float tdcu[5]; // for storage previous RC angle 
float tdmoi[5]; // for storage new RC angle 
float h[4]; // for storage previous RC angle 
float denta[5]; // for storage the distance between set value of RC servo angle and previous one
// float tdcu1[5];
// float tdmoi1[5];
// float h1[5];
// float denta1[5];
int S1; // the value angle of servo 1 you received from framework
int S2; // the value angle of servo 2 you received from framework
int S3; // the value angle of servo 3 you received from framework
int S4; // the value angle of servo 4 you received from framework
int ST1; // the value angle of step motor you received from the framework
int STmoi = 0; // the new value of angle calculated by set pulse - current pulse
int STcu = 0; // the old value angle of step motor for comparing with new current value angle
int EN = 0; // working mode received from framework
int Xung_Xoay = 0; // the set pulse value
int dem = 0; // the current pulse value for comparing with Xung_Xoay
int S = 0; // the set value of gripping angle
byte Home = 0; // get 1 value if robot go home
boolean s1 = false; // limit switch
byte Run_Step = 0; // get value 1 if step motor is running, 0 if step stopped
String str; // the string framework
char buf[100]; // useless
//unsigned long timer, timer1;
const int BT =  12; // button 
const int RES =  A0; // the potential meter
const int BZ =  A5; // buzzer
const int stepPin = 4; // make pulse for step motor
const int dirPin = 7; // direction for step motor pin
const int enPin = 8; // brake step motor pin

void setgoc();

void Run(int G1, int G2, int G3, int G4, int T, int Dir);

void setup() {

  // STEP1: Serial setup
  Serial.begin(9600); // Arduino internal serial
  mySerial.begin(9600); // your custom serial
  
  // STEP2: Pinmode setup
  pinMode(stepPin,OUTPUT); // init stepPin for step motor is output
  pinMode(dirPin,OUTPUT); // init dirPin for step motor direction is output
  pinMode(enPin,OUTPUT); // init enable for step motor is output, BRAKE control
  pinMode(BZ,OUTPUT); // buzzer
  pinMode(BT,INPUT); // button
  pinMode(RES,INPUT); // potential resistor
  pinMode(13, OUTPUT); // led builtin
  digitalWrite(13,0);
  attachInterrupt(0, Ngat, FALLING);
  Serial.println("1");
  
  // STEP3: Timer setup
  cli(); // init timer, disable all interupt before you done setup
  Serial.println("2");
  TCCR0B = 0; 
  OCR2A = reload;
  TCCR2A = 1<<WGM21;
  TCCR2B = ((1<<CS21) | (1<<CS20));//1<<CS22)
  TIMSK2 = (1<<OCIE2A);
  Serial.println("3zzzzz");
  sei();
  Serial.println("4xxxxx");
  
  // STEP4: brake and buzzer setup
  digitalWrite(enPin,1); //0 la thang, 1 la nha
  digitalWrite(BZ,0);
  
  // STEP5: RC servo setup
  sv4.attach(3);  // goc tang la kep lai
  sv3.attach(5);  // goc tang la gap vao
  sv2.attach(6);  //goc giam la dua ra
  sv1.attach(9);  //goc tang la dua ra
  setgoc();
  
  Serial.println("dddd");
   
  // STEP6: set grip angle, push the button 
  if(digitalRead(BT) == 0)
  {
    // activate the buzzer 2 time for announcement
    digitalWrite(BZ,1);
    Delay(1000); // delay by custom function
    digitalWrite(BZ,0);
    Delay(2000);
    digitalWrite(BZ,1);
    Delay(1000);
    digitalWrite(BZ,0);
    Delay(10000);
    // wait until you release the button
    while(digitalRead(BT) == 0); // if the condition is true, continue loop
    // starting set the grip angle
    while(1)
    {
      int Val = analogRead(RES); // read the analog value of potential metter
      S = map(Val, 0, 1024, 0, 180); // map to range (0,180)
      Serial.println(S); // print out the value of grip angle
      sv4.write(S); // write the angle to gripping servo
      Delay(1000); // delay 1000ms 
      // if you have a correct angle, press the button to release
      if(digitalRead(BT) == 0)
      {
        EEPROM.write(0,S); // save the value to arduino eeprom, make sure this
        Delay(100);
        break; // jump out the while
      }
     }
  }
  // print out the gripping angle
  Serial.print("GT GOC: ");
  S = EEPROM.read(0);
  Serial.println(S);
  // return robot to zero position again
  setgoc();

  Serial.println("-------....");
  // Run(180,20,80,90,90,600); //robot go to ready position from begining
  // while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
  // Run_Step = 0;
  Serial.println("++++--....");

  // announcement by buzzer that all setup is done
  beep_long();
}

//LOOP--------------------------------------------------------
void loop() {
  // if you received someting
  if (Serial.available()) {
    // print out the content you received
    Serial.println("RX....");

    beep_3();

    //str = Serial.readStringUntil('a');
    //str = Serial.read();
    //str = Serial.readString();
    str = Serial.readStringUntil('\n');
    Serial.println(str);
    /*
      convert a character string to double precision floating point value,
      get the sub string then convert it into integer
      */ 
    
    beep_4();
    /*
      convert a character string to double precision floating point value,
      get the sub string then convert it into integer
      */
    ST1 = atof(strtok(str.c_str(),","));
    S1 = atof(strtok(NULL,","));
    S2 = atoi(strtok(NULL,","));
    S3 = atoi(strtok(NULL,","));
    S4 = atoi(strtok(NULL,","));
    EN = atoi(strtok(NULL,","));
    Serial.println(EN);  // print out the working mode
    
    /*
      Check the angle of step motor if it get over the limit then set it as the previous value
      */
    if(ST1 > 350 || ST1 < 0) {
        Serial.println("angle Step is over the limit");
        ST1 = STcu;
      }
    
    /*
      Check the working mode
      1: for go to specific position
      2: for go home
      3: robot go forward
      4: robot grip
      5: robot release
      */
    switch (EN) {
    case 1:    
      Run(ST1,S1,S2,S3,S4,600);
      while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
      Run_Step = 0;
    break;
    case 2:   // TT mac dinh
      Home = 1;
      Run(80,20,80,90,90,600);
      STcu = 90;
      while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
      Run_Step = 0;
      Serial.println("2");
    break;
    case 3:    
      Serial.println("3");
      
    break;
    case 4:    
      Serial.println("4");
      
    break;
    case 5:    
      Serial.println("5");
      
    break;
    case 7:
      beep_5();
    }
  }


  if(digitalRead(BT) == 0)
  {
    Serial.println("-----============--....");
    Run(160,70,80,90,90,600);
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,70,160,90,90,600);//190,70,160,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,90,600);//190,40,136,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,135,600);//190,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(195,40,136,90,135,600);//195,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(195,70,120,90,135,600);//195,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(210,70,120,90,135,600);//210,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(170,70,120,90,135,600); //170,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,70,120,90,135,600);//190,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,70,120,110,135,600); //190,70,120,110,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,70,120,70,135,600); //    190,70,120,170,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(195,40,136,90,135,600); //195,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,135,600); //190,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,90,600); //190,40,136,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,80,136,90,90,600); //190,80,160,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(90,20,80,90, 90,600);//90,20,80,90, 90,600
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    
    Run_Step = 0;
    Delay(50000); 
    digitalWrite(enPin,1);
  }
}

//INTERUPT----------------------------------------------------
ISR(TIMER2_COMPA_vect)
{
  count++;
  T_delay++;
  if(count >= 8)
  {
    if( Run_Step == 1 && dem <= Xung_Xoay) {
      digitalWrite(stepPin,!digitalRead(stepPin)); 
    }
    dem++;
    count = 0;
  }
  OCR2A = reload;
}

//RUN robot function------------------------------------------
void Run(int ST, int G1, int G2, int G3, int G4, int F)
{
  
  digitalWrite(enPin,0);
  Run_Step = 1;
  count = 0;
  dem = 0;
 
  STmoi= ST - STcu;
  Serial.print(ST);
  Serial.print("  ");
  Serial.print(STmoi);
  Serial.print("  ");
  Serial.println(STcu);
  if(STmoi > 0) {
    digitalWrite(dirPin,0);
    Xung_Xoay = STmoi * 89; // 89 = 16000/360*2 vi 2 lan ngat moi dc 1 xung
    STcu = ST;
    Serial.println(" 1 ");
  }
  else if(STmoi < 0) {
    Home = 1;
    digitalWrite(dirPin,1);
    Xung_Xoay = abs(STmoi) * 89; // 46 = 23*2 vi 2 lan ngat moi dc 1 xung
    STcu = ST;
    Serial.println(" 2 ");
  }
  else {Xung_Xoay = -1; Run_Step = 0;Serial.println(" 3 ");}
  Serial.println(Xung_Xoay);
  
  tdmoi[0]=G1;
  tdmoi[1]=G2;
  tdmoi[2]=G3;
  tdmoi[3]=G4;
  Serial.println(Xung_Xoay);
  for(char r1=0; r1<4; r1++)
      {
        denta[r1] = tdmoi[r1]-tdcu[r1];
        h[r1] = denta[r1]*1.00/F;
      }
      Serial.println(Xung_Xoay);
      for(int r2=0; r2<F; r2++)
      {
            tdcu[0]=tdcu[0]+h[0];
            //
            tdcu[1]=tdcu[1]+h[1];
            //
            tdcu[2]=tdcu[2]+h[2];
            //
            tdcu[3]=tdcu[3]+h[3];
            sv1.write(tdcu[0]);
            sv2.write(tdcu[1]);
            sv3.write(tdcu[2]);
            sv4.write(tdcu[3]);
            Delay(10);
           
    }
    Serial.println(Xung_Xoay);
}

//GO HOME function--------------------------------------------
void setgoc()
{ 
    STcu=90;
  
    tdcu[0]=20;          //nhin tu trc, ben phai
    sv1.write(tdcu[0]);
    Serial.println("7kkkkk");
    //
    tdcu[1]=80;
    sv2.write(tdcu[1]);
    //
    tdcu[2]=90;
    sv3.write(tdcu[2]);
    //
    tdcu[3]=90;
    sv4.write(tdcu[3]); 
    Serial.println("8yyyyy");
    Delay(10000);
    Serial.println("9fffff");
}

// OVER LIMIT STOP function----------------------------------
void Ngat()
{
  if(Home == 1){ digitalWrite(enPin,1); Home = 0;}
}

// DELAY by interupt ----------------------------------------
void Delay(unsigned int T)  //T = 10000 = 1s
{
  T_delay = 0;
  while(T_delay < T){Serial.println(T_delay);}
}

// BEEP functions--------------------------------------------
void beep_long(){
  digitalWrite(BZ,1);
  Delay(20000); //2s
  digitalWrite(BZ,0);
  }

void beep_2(){
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  }

void beep_3(){
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  }

void beep_4(){
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  }

void beep_5(){
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  Delay(1000); //100ms
  digitalWrite(BZ,1);
  Delay(1000); //100ms
  digitalWrite(BZ,0);
  }

