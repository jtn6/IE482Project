#include <Servo.h>

Servo sorterServo;
String command = "";

void setup() {
  Serial.begin(9600);
  sorterServo.attach(9);
  sorterServo.write(90);  // start centered
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LEFT") {
      sorterServo.write(30);
    }
    else if (command == "RIGHT") {
      sorterServo.write(150);
    }
  }
}