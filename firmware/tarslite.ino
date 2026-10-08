// TARS-Lite v0.3 safe idle + sensor telemetry scaffold (Arduino framework, ESP32-S3)
// Libraries: ESP32Servo, Adafruit_VL53L0X, Adafruit_MPU6050, Adafruit Unified Sensor.
// External fused 5 V servo supply required; share its ground with ESP32 GND.
// Verify GPIO availability on the exact ESP32-S3 board before wiring.
#include <Wire.h>
#include <ESP32Servo.h>
#include <Adafruit_VL53L0X.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

static const int SERVO_COUNT = 6;
static const int ACTIVE_SERVO_COUNT = 1; // Increase only after each joint is independently checked.
static const int SERVO_PINS[SERVO_COUNT] = {4, 5, 6, 7, 15, 16};
static const int I2C_SDA_PIN = 8; // Verify against the purchased board/module
static const int I2C_SCL_PIN = 9; // Verify against the purchased board/module
static const int FACE_UART_RX = 18; // from Arduino TX through level shifter
static const int FACE_UART_TX = 17; // to Arduino RX
Servo servos[SERVO_COUNT];
HardwareSerial faceSerial(1);
Adafruit_VL53L0X tof;
Adafruit_MPU6050 imu;
bool tofReady=false, imuReady=false;
uint32_t lastRead=0;

void setup() {
  Serial.begin(115200);
  faceSerial.begin(115200, SERIAL_8N1, FACE_UART_RX, FACE_UART_TX);
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  Wire.setClock(100000); // conservative shared sensor bus
  tofReady=tof.begin(0x29, false, &Wire);
  imuReady=imu.begin(0x68, &Wire);
  if (imuReady) {
    imu.setAccelerometerRange(MPU6050_RANGE_4_G);
    imu.setGyroRange(MPU6050_RANGE_250_DEG);
    imu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }
  Serial.printf("ToF=%s IMU=%s\n", tofReady?"OK":"NOT FOUND", imuReady?"OK":"NOT FOUND");
  // Safe, neutral-only initialization; only the first channel is enabled by default.
  for (int i=0; i<ACTIVE_SERVO_COUNT; ++i) {
    servos[i].setPeriodHertz(50);
    servos[i].attach(SERVO_PINS[i], 1000, 2000);
    servos[i].writeMicroseconds(1500); // Not guaranteed mechanical midpoint.
    delay(250);
  }
  Serial.printf("Stationary safe-idle. Active servo channels: %d/%d.\n", ACTIVE_SERVO_COUNT, SERVO_COUNT);
}

void loop() {
  if (millis()-lastRead < 250) return;
  lastRead=millis();
  if (tofReady) {
    VL53L0X_RangingMeasurementData_t m;
    tof.rangingTest(&m, false);
    if (m.RangeStatus != 4) {
      Serial.printf("ToF_mm=%u ", m.RangeMilliMeter);
      faceSerial.println(m.RangeMilliMeter < 500 ? "NEAR" : "CLEAR");
    } else {
      Serial.print("ToF=out_of_range ");
      faceSerial.println("UNKNOWN");
    }
  } else {
    faceSerial.println("UNKNOWN");
  }
  if (imuReady) {
    sensors_event_t a,g,t;
    imu.getEvent(&a,&g,&t);
    Serial.printf("accel_mps2=(%.2f,%.2f,%.2f) gyro_rads=(%.2f,%.2f,%.2f)",
      a.acceleration.x,a.acceleration.y,a.acceleration.z,
      g.gyro.x,g.gyro.y,g.gyro.z);
  }
  Serial.println();
  while (faceSerial.available()) {
    char c=(char)faceSerial.read();
    if (c=='B') Serial.println("Arduino button event");
  }
}
