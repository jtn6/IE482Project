void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LEFT") {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(200);
      digitalWrite(LED_BUILTIN, LOW);
    }
    else if (command == "RIGHT") {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(600);
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}