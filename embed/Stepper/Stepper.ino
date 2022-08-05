# include <Servo.h> // Servo lib
# include <SoftwareSerial.h> // create a new serial port
# include <avr/io.h>
# include <avr/interrupt.h>
byte reload = 50; //set 100us period for interrupt timer
int count = 0; //make a pulse for step motor if count = 8
unsigned long T_delay; // T_delay for delay function
int STmoi = 0; // the value of angle calculated by set pulse - current
int STcu = 0;
Servo sv1; // create rc servo object for join1

void setup() {
  // put your setup code here, to run once:
  sv1.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  sv1.write(50); // raise the arm before rotate step motor

}
