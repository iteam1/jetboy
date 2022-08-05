# include <Servo.h> // Servo lib

Servo sv1; // create rc servo object for join1

void setup() {
  // put your setup code here, to run once:
  sv1.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  sv1.write(180); // raise the arm before rotate step motor

}
