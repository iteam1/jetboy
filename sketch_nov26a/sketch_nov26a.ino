/*
For Arduino nano handles obstacle awaring
*/

#include<NewPing.h>
#define max_distance 500 // max distance 500 cm, out of range 1183 cm
#define trig_front 2 // Trigger pin of front sensor
#define echo_front 3 // Echo pin of front sensor
#define trig_back 4 // Trigger pin of back sensor
#define echo_back 5 // Echo pin of back sensor
#define trig_left 6 // Trigger pin of left sensor
#define echo_left 7 // Echo pin of left sensor
#define trig_right 8 // Trigger pin of right sensor
#define echo_right 9 // Echo pin of right sensor
#define ledpin 13 // Led builtin pin for warning

NewPing sonar_front(trig_front,echo_front,max_distance); // create sonar front sensor
NewPing sonar_back(trig_back,echo_back,max_distance); // create sonar back sensor
NewPing sonar_left(trig_left,echo_left,max_distance); // create sonar left sensor
NewPing sonar_right(trig_right,echo_right,max_distance); // create sonar right sensor

// Define some variables
float duration_front; // Stores front HC-SR04 pulse duration value in microseconds
float distance_front; // Stores front HC-SR04 distance value in centimeter
float duration_back; // Stores back HC-SR04 pulse duration value in microseconds
float distance_back; // Stores back HC-SR04 distance value in centimeter
float duration_left; // Srores left HC-SR04 pulse duration value in microseconds
float distance_left; // Stores left HC-SR04 distance value in centimeter
float duration_right; // Stores right HC-SR04 pulse duration value in microseconds
float distance_right; // Stores right HC-SR04 distance value in centimeter
float soundsp = 34000; // cm/s
int iterations = 5; // The iteration for ping median function
float min_distance = 10;

int front_warning = A0; // Warning out pin for obstacle
int back_warning = A1; // Warning out pin for obstacle
int left_warning = A2; // Warning out pin for obstacle
int right_warning = A3; // Warning out pin for obstacle
int read_warning = A4; // For reading warning output value
int val; // Stores analog output value

void setup() {
  // put your setup code here, to run once:
  // Initialize your serial
  // Serial.begin(9600);
  pinMode(ledpin,OUTPUT);
  digitalWrite(ledpin,LOW);
  pinMode(front_warning,OUTPUT);
  analogWrite(front_warning,0);
  pinMode(back_warning,OUTPUT);
  analogWrite(back_warning,0);
  pinMode(left_warning,OUTPUT);
  analogWrite(left_warning,0);
  pinMode(right_warning,OUTPUT);
  analogWrite(right_warning,0);
  pinMode(read_warning,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  duration_front = sonar_front.ping_median(iterations);
  distance_front = (duration_front/2000000) * soundsp;
  duration_back = sonar_back.ping_median(iterations);
  distance_back = (duration_back/2000000) * soundsp;
  duration_left = sonar_left.ping_median(iterations);
  distance_left = (duration_left/2000000) * soundsp;
  duration_right = sonar_right.ping_median(iterations);
  distance_right = (duration_right/2000000) * soundsp;

//  Serial.print("front: ");
//  Serial.print(distance_front);
//  Serial.print(" cm ");
//
//  Serial.print("back: ");
//  Serial.print(distance_back);
//  Serial.print(" cm ");
//
//  Serial.print("left: ");
//  Serial.print(distance_left);
//  Serial.print(" cm ");
//
//  Serial.print("right: ");
//  Serial.print(distance_right);
//  Serial.print(" cm ");
//
//  Serial.println(".");

//  val = analogRead(read_warning);
//  Serial.println(val);
  
  if(distance_front <= min_distance){
    analogWrite(front_warning,255);
    }
  else{
    analogWrite(front_warning,0);
    }

  if(distance_back <= min_distance){
    analogWrite(back_warning,255);
    }
  else{
    analogWrite(back_warning,0);
    }

  if(distance_left <= min_distance){
    analogWrite(left_warning,255);
    }
  else{
    analogWrite(left_warning,0);
    }

  if(distance_right <= min_distance){
    analogWrite(right_warning,255);
    }
  else{
    analogWrite(right_warning,0);
    }
  
  if (distance_front <= min_distance || distance_back <= min_distance || distance_left <= min_distance || distance_right <= min_distance){
    digitalWrite(ledpin,HIGH);
  }
  else{
    digitalWrite(ledpin,LOW);
    }
    
  delay(100);
}
