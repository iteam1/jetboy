/*
This function for testing uart communicate
send out what the chip received
*/
String str;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    //Serial.println("Received: ");
    //str = Serial.read();
    str = Serial.readStringUntil('a');
    if(str == "90,90,90,90,90,1"){
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(1000);                       // wait for a second
      }
    }
}
