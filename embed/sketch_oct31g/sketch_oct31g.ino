/*
 * arduino nano control driver BTS960
*/
int L_PWM = A1;
int R_PWM = A2;
int L_EN = 3;
int R_EN = 4;
int L_IS = 5;
int  R_IS = 6;
int M_RUN = 10;
int M_DIR = 11;

void setup() {
  // put your setup code here, to run once:
  pinMode(M_RUN,INPUT);
  pinMode(M_DIR,INPUT);
  
  pinMode(L_IS,OUTPUT);
  pinMode(R_IS,OUTPUT);
  pinMode(L_EN,OUTPUT);
  pinMode(R_EN,OUTPUT);
  pinMode(L_PWM,OUTPUT);
  pinMode(R_PWM,OUTPUT);
  
  digitalWrite(R_IS,LOW);
  digitalWrite(L_IS,LOW);
  digitalWrite(L_EN,HIGH);
  digitalWrite(R_EN,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(M_RUN) == HIGH){
    if(digitalRead(M_DIR) == HIGH){
      analogWrite(L_PWM,129);
      analogWrite(R_PWM,0);
      }
    else{
      analogWrite(L_PWM,0);
      analogWrite(R_PWM,129);
      }
  }
  else{
  analogWrite(L_PWM,0);
  analogWrite(R_PWM,0);
    }
}
