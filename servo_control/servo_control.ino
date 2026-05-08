#include <Servo.h>

Servo sorterServo;
String command = "";

const int REST_POS = 90;
const int LEFT_POS = 30;
const int RIGHT_POS = 150;

const int TRAVEL_DELAY = 2000;  // time from camera ROI to servo
const int TAP_TIME = 300;       // time servo stays out to hit object

void setup() {
  Serial.begin(9600);
  sorterServo.attach(9);
  sorterServo.write(REST_POS);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LEFT") {
      delay(TRAVEL_DELAY);
      sorterServo.write(LEFT_POS);
      delay(TAP_TIME);
      sorterServo.write(REST_POS);
    }

    else if (command == "RIGHT") {
      delay(TRAVEL_DELAY);
      sorterServo.write(RIGHT_POS);
      delay(TAP_TIME);
      sorterServo.write(REST_POS);
    }
  }
}