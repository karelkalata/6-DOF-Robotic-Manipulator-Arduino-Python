#include <Servo.h>

Servo myservo0;  
Servo myservo1; 
Servo myservo2; 
Servo myservo3; 
Servo myservo4; 
Servo myservo5; 

void setup() {
  Serial.begin(115200);
  myservo0.attach(2);
  myservo1.attach(3);
  myservo2.attach(4);
  myservo3.attach(5);
  myservo4.attach(6);
  myservo5.attach(7);
}

void loop() {
  if( Serial.available())
  {
    int numEngine = Serial.parseInt();
    int valEngine = Serial.parseInt();
    if (Serial.read() == '\n') {
      switch(numEngine)
      {
        case 0:
          myservo0.write(valEngine);
        break;
        case 1:
          myservo1.write(valEngine);
        break;
        case 2:
          myservo2.write(valEngine);
        break;
        case 3:
          myservo3.write(valEngine);
        break;
        case 4:
          myservo4.write(valEngine);
        break;
        case 5:
          myservo5.write(valEngine);
        break;
      }
    }
    delay(15);  
  }

}

/*
example 0,50
0 - number Engine
0-1023  - val Engine



*/