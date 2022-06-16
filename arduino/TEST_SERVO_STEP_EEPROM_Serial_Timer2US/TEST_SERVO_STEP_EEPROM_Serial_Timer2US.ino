//#include <MsTimer2.h>
#include <avr/io.h>
#include <avr/interrupt.h>
byte reload = 50;  //100us
int count = 0;
unsigned long Tmoi,T_delay;
//#include <AccelStepper.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(11, 10); // RX, TX
#include <Servo.h>
#include <string.h>
//#include <TimerOne.h>
Servo sv4,sv3, sv2, sv1;  // create servo object to control a servo
// twelve servo objects can be created on most boards
//#define dirPin 7
//#define stepPin 4
#define motorInterfaceType 1
// Create a new instance of the AccelStepper class:
//AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
String s="";
int g1,g2,g3,g4;
float tdcu[5], tdmoi[5], h[4], denta[5],tdcu1[5], tdmoi1[5], h1[5], denta1[5];
//int k,x,j,f;
//int i=0;
//int dl=2000;
//int f1=200;
int S1,S2,S3,S4,ST1, STmoi = 0,STcu = 0, EN = 0;

int Xung_Xoay = 0, dem = 0;
int S = 0;
byte Home = 0;
//byte Phu = 0;
boolean s1 = false;
byte Run_Step = 0;
String str;
char buf[100];
int  chuoi[] = {
    20,90,90,90, //trang thai mat dinh
    110, 20,45, 140,   //Dua ra phia truoc
//    20, 90, 90, 90,    
//    110, 20,45, 140,   
//    20, 90, 90, 90
};
//unsigned long timer, timer1;
const int BT =  12;
const int RES =  A0;
const int BZ =  A5;
const int stepPin = 4; 
const int dirPin = 7; 
const int enPin = 8;

void setgoc();
void Run(int G1, int G2, int G3, int G4, int T, int Dir);
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(BZ,OUTPUT);
  pinMode(BT,INPUT);
  pinMode(RES,INPUT);
  pinMode(13, OUTPUT);
  digitalWrite(13,0);
  attachInterrupt(0, Ngat, FALLING);
  Serial.println("1");
  cli();
  Serial.println("2");
  TCCR0B = 0; 
  OCR2A = reload;
  TCCR2A = 1<<WGM21;
  TCCR2B = ((1<<CS21) | (1<<CS20));//1<<CS22)
  TIMSK2 = (1<<OCIE2A);
  Serial.println("3");
  sei();
  Serial.println("4");
  //Timer1.initialize(500); // khởi tạo timer 1 đến 1 mili giây
  //Timer1.attachInterrupt(Blink); // khai báo ngắt timer 1
  //MsTimer2::set(1, Blink); // 500ms period
  //MsTimer2::start();
  digitalWrite(enPin,1); //0 la thang, 1 la nha
  digitalWrite(BZ,0);
//  stepper.setMaxSpeed(2000);
//  stepper.setAcceleration(2000);
  sv4.attach(3);  // goc tang la kep lai
  sv3.attach(5);  // goc tang la gap vao
  sv2.attach(6);  //goc giam la dua ra
  sv1.attach(9);  //goc tang la dua ra
  Serial.println("5");
//  sv4.write(90); //kep goc lon dan
//  sv3.write(90); // 
//  sv2.write(90); //
//  sv1.write(20); //nhat tay len khi goc lon dan
  setgoc();
  Serial.println("6");
  if(digitalRead(BT) == 0)
  {
    digitalWrite(BZ,1);
    Delay(1000);
    digitalWrite(BZ,0);
    Delay(2000);
    digitalWrite(BZ,1);
    Delay(1000);
    digitalWrite(BZ,0);
    Delay(10000);
    while(digitalRead(BT) == 0);
    while(1)
    {
      int Val = analogRead(RES);
      S = map(Val, 0, 1024, 0, 180);
      Serial.println(S);
      sv4.write(S);
      Delay(1000);
      if(digitalRead(BT) == 0)
      {
        EEPROM.write(0,S);
        Delay(100);
        break;
      }
     }
  }
  Serial.print("GT GOC: ");
  S = EEPROM.read(0);
  Serial.println(S);
  setgoc();
  digitalWrite(BZ,1);
  Delay(10000); //1s
  digitalWrite(BZ,0);
}

//------------------
void loop() {
  if (Serial.available()) {
    Serial.println("RX....");
    //90,20,80,90,90,1
    str = Serial.readStringUntil('\n');
      Serial.println(str);

      ST1 = atof(strtok(str.c_str(),","));
      S1 = atof(strtok(NULL,","));
      S2 = atoi(strtok(NULL,","));
      S3 = atoi(strtok(NULL,","));
      S4 = atoi(strtok(NULL,","));
      EN = atoi(strtok(NULL,","));
      Serial.println(EN);
      if(ST1 > 350 || ST1 < 0) {
          Serial.println("angle Step is over the limit");
          ST1 = STcu;
        }
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
    }
  }


  if(digitalRead(BT) == 0)
  {
    
    Run(160,70,80,90,90,600);
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,70,160,90,90,600);//190,70,160,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,90,600);//190,40,136,90,90,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(190,40,136,90,135,600);//190,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
//    Delay(5000); 
    Run(195,40,136,90,135,600);//195,40,136,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(195,70,120,90,135,600);//195,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
//    
    Run(210,70,120,90,135,600);//210,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
    Run(170,70,120,90,135,600); //170,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
//    Delay(5000);
    Run(190,70,120,90,135,600);//190,70,120,90,135,1,A
    while(Xung_Xoay >= dem){Serial.print(dem);Serial.print(" ");Serial.println(Xung_Xoay);}
//    
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
    //setgoc();
    Serial.println(" Xong-----------------------");
    Delay(50000); 
    digitalWrite(enPin,1);
    Serial.println(" Xong........................");
  }
}
//--------------------
ISR(TIMER2_COMPA_vect)
{
//if(count > 10000) {digitalWrite(13, !digitalRead(13)); count = 0;}
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
//=====================
//void Blink()
//{
//  if( Run_Step == 1 && dem <= Xung_Xoay) {
//    digitalWrite(stepPin,!digitalRead(stepPin)); 
//    
//  }
//  dem++;
//}

//----------------------------------------
void Run(int ST, int G1, int G2, int G3, int G4, int F)
{
  
  digitalWrite(enPin,0);
  Run_Step = 1;
  count = 0;
  dem = 0;
  
  //Goc_Xoay = map(ST, 0, 360, 0, 8288);  //xung = độ x 23
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
  //tdmoi[4]=Goc_Xoay;
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
            //tdcu[4]=tdcu[4]+h[4];
            //Serial.println(tdcu[0]);
            sv1.write(tdcu[0]);
            sv2.write(tdcu[1]);
            sv3.write(tdcu[2]);
            sv4.write(tdcu[3]);
            Delay(10);
           
    }
      //Serial.println(tdcu[0]);
    //if(tdcu[3] == G4) Run_Step = 0;
    Serial.println(Xung_Xoay);
}
//--------------------------------------------
void setgoc()
{ 
    STcu=90;
  
   tdcu[0]=20;          //nhin tu trc, ben phai
   sv1.write(tdcu[0]);
   Serial.println("7");
   //
   tdcu[1]=80;
   sv2.write(tdcu[1]);
   //
   tdcu[2]=90;
   sv3.write(tdcu[2]);
   //
   tdcu[3]=90;
   sv4.write(tdcu[3]); 
        //f=200;  
   
//    stepper.setCurrentPosition(0);
Serial.println("8");
  Delay(10000);
    //delay(2000);
    Serial.println("9");
}
void Ngat()
{
  //digitalWrite(enPin,1);
  if(Home == 1){ digitalWrite(enPin,1); Home = 0;}
}
void Delay(unsigned int T)  //T = 10000 = 1s
{
  T_delay = 0;
  while(T_delay < T){Serial.println(T_delay);}
}
