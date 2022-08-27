//#include <SoftwareSerial.h>
//SoftwareSerial mySerial(10, 11); // RX, TX 
// Arduino nano
#include <Adafruit_NeoPixel.h>
#define PIN 4

Adafruit_NeoPixel strip = Adafruit_NeoPixel(128, PIN, NEO_GRB + NEO_KHZ800);
byte Smile[] = {3,4,10,11,12,13,17,18,21,22,25,26,29,30,32,33,38,39,40,41,46,47,48,55}; 
byte Nomal[] = {2,3,4,5,9,10,13,14,17,22,25,30,33,38,41,46,49,50,53,54,58,59,60,61};
byte Sad[] = {6,7,13,14,15,20,21,22,27,28,29,34,35,36,41,42,43,48,49,50,56,57};
byte Sad1[] = {64,65,72,73,74,81,82,83,90,91,92,99,100,101,108,109,110,117,118,119,126,127};
byte Angry[] = {0,1,8,9,10,17,18,19,26,27,28,35,36,37,44,45,46,53,54,55,62,63};
byte Angry1[] = {70,71,77,78,79,84,85,86,91,92,93,98,99,100,105,106,107,112,113,114,120,121};
byte Suprised[] = {1,4,7,9,10,12,14,15,18,19,20,21,22,27,28,29,35,36,37,42,43,44,45,46,49,50,52,54,55,57,60,63};
byte Sleep[] = {24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39};

String str = "";
String Val = "";

void setup(){
    // initialize led and serial
    Serial.begin(9600);
    //mySerial.begin(9600);   
    strip.begin();  
    strip.show();
    Serial.println("ok");
    //mySerial.println("ok");
    // warm up
    Warm_Up();
}

void loop(){
  if(Serial.available()){
    //str = Serial.read();
    str = Serial.readStringUntil('q');
    Val = str; //strtok(str.c_str(),",");
    Serial.println(Val);
//    int R = atof(strtok(NULL,","));
//    int G = atof(strtok(NULL,","));
//    int B = atof(strtok(NULL,","));
    if (Val == "who"){
      Serial.println("emoled");
      }
    else if(Val == "smile"){
      Write_Smile(5,5,5);
    }
    else if(Val == "normal"){
      Write_Nomal(5,5,5);
    }
    else if(Val == "sad"){
      Write_Sad(0,0,5);
    }
    else if(Val == "angry"){
      Write_Angry(5,0,0);
    }
    else if(Val == "suprised"){
      Write_Suprised(5,5,5);
    }
    else if(Val == "sleep"){
      Write_Sleep(0,0,5);
    }
    else if(Val == "off"){
      OFF();
    }
//    else{
//      Write_Nomal(5,5,5);
//    }
  }
}

void Warm_Up(){
    Write_Smile(5,5,5);
    delay(1000);
    Write_Nomal(5,5,5);
    delay(1000);
    Write_Sad(5,5,5);
    delay(1000);
    Write_Angry(5,0,0);
    delay(1000);
    Write_Suprised(0,5,0);
    delay(1000);
    Write_Sleep(0,0,5);
    delay(1000);
  }

void Write_Smile(int R, int G, int B){
    for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100);
  for(int i =0;i<24;i++)
    {
      strip.setPixelColor(Smile[i],R,G,B);
      strip.setPixelColor(Smile[i]+64,R,G,B);
    }
    strip.show();    
}

void Write_Nomal(int R, int G, int B){
  for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100);
  for(int i =0;i<24;i++)
    {
      strip.setPixelColor(Nomal[i],R,G,B);
      strip.setPixelColor(Nomal[i]+64,R,G,B);
    }
    strip.show(); 
    
}

 void Write_Sad(int R, int G, int B){
  for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100);
    for(int i =0;i<22;i++)
    {
      strip.setPixelColor(Sad[i],R,G,B);
      strip.setPixelColor(Sad1[i],R,G,B);
    }
    strip.show(); 
    
 }

void Write_Angry(int R, int G, int B){
  for(int i =0;i<128;i++)
  {
    strip.setPixelColor(i,0,0,0);
  }
  strip.show(); 
  delay(100);
  for(int i =0;i<22;i++)
  {
    strip.setPixelColor(Angry[i],R,G,B);
    strip.setPixelColor(Angry1[i],R,G,B);
  }
  strip.show(); 
  
}

void Write_Suprised(int R, int G, int B){
  for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100);
    for(int i =0;i<32;i++)
    {
      strip.setPixelColor(Suprised[i],R,G,B);
      strip.setPixelColor(Suprised[i]+64,R,G,B);
    }
    strip.show(); 
    
 }

void Write_Sleep(int R, int G, int B){
  for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100);
    for(int i =0;i<16;i++)
    {
      strip.setPixelColor(Sleep[i],R,G,B);
      strip.setPixelColor(Sleep[i]+64,R,G,B);
    }
    strip.show(); 
    
 }

void OFF(){
  for(int i =0;i<128;i++)
    {
      strip.setPixelColor(i,0,0,0);
    }
    strip.show(); 
    delay(100); 
 }
