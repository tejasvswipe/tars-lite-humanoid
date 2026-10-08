// TARS-Lite auxiliary face I/O for Arduino UNO R4 Minima.
// Serial1 receives NEAR/CLEAR/UNKNOWN from ESP32 and sends BTN input events (D0/D1).
// Use a 3.3V/5V bidirectional level shifter (or verified divider on Arduino TX -> ESP32 RX).
const int LEFT_EYE = 4;
const int RIGHT_EYE = 5;
const int MODE_BUTTON = 2;
String line;
unsigned long lastPress=0;
bool nearObject=false;
bool sensorKnown=false;
unsigned long lastBlink=0;
bool blinkState=false;

void setup() {
  pinMode(LEFT_EYE, OUTPUT);
  pinMode(RIGHT_EYE, OUTPUT);
  pinMode(MODE_BUTTON, INPUT_PULLUP);
  Serial1.begin(115200); // D0 RX, D1 TX
  Serial.begin(115200);  // optional USB diagnostics
}
void loop() {
  while (Serial1.available()) {
    char c=(char)Serial1.read();
    if (c=='\n' || c=='\r') {
      line.trim();
      if (line=="NEAR") { nearObject=true; sensorKnown=true; }
      else if (line=="CLEAR") { nearObject=false; sensorKnown=true; }
      else if (line=="UNKNOWN") sensorKnown=false;
      line="";
    } else if (line.length()<24) line+=c;
  }
  // Simple, non-safety display cue; eye LEDs only.
  unsigned long now=millis();
  unsigned long interval = !sensorKnown ? 1000 : (nearObject ? 180 : 700);
  if (now-lastBlink>=interval) {
    lastBlink=now; blinkState=!blinkState;
    digitalWrite(LEFT_EYE, blinkState ? HIGH : LOW);
    digitalWrite(RIGHT_EYE, sensorKnown && nearObject ? (blinkState ? HIGH : LOW) : LOW);
  }
  if (digitalRead(MODE_BUTTON)==LOW && now-lastPress>350) {
    lastPress=now;
    Serial1.println("BTN");
    Serial.println("Button event sent");
  }
}
