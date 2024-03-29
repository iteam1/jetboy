/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep

 sv4 attach pin 3 # griping tool
 sv3 attach pin 5 # join3
 sv2 attach pin 6 # join2
 sv1 attach pin 9 # join1
*/

#include <Servo.h>

Servo sv1,sv2,sv3,sv4;  // robot's arm have 4 rc servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int min_angle = 30; // minimum angle
int max_angle = 70; // maximum angle
void setup() {
  sv1.attach(9);  // attaches the servo on pin 9 to the servo object
  sv2.attach(6);
  sv3.attach(5);
  sv4.attach(3);
}

void loop() {
  //sv3.write(90);
    
  for (pos = min_angle; pos <= max_angle; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    sv3.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = max_angle; pos >= min_angle; pos -= 1) { // goes from 180 degrees to 0 degrees
    sv3.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
