// TARS-Lite Biped Add-on v1.0 — ESP32-S3 head/gripper/sensor controller.
// Lower-body gait stays on the stock ROBOTIS OpenCM controller.
// Neck-only bus: one XL-320 on a separate data line through DXL-Neck-Interface.
// Required libraries: Dynamixel2Arduino, ESP32Servo, Adafruit_VL53L0X,
// Adafruit_MPU6050, Adafruit Unified Sensor.
// Safety: 2S actuator power is separately fused; 5V hand-servos use an external 5V rail.
#include <Wire.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <Dynamixel2Arduino.h>
#include <ESP32Servo.h>
#include <Adafruit_VL53L0X.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

static constexpr int DXL_TX=17, DXL_RX=18, DXL_DIR=16;
static constexpr int FACE_TX=15, FACE_RX=14;
static constexpr int I2C_SDA=8, I2C_SCL=9;
static constexpr int GRIP_L_PIN=4, GRIP_R_PIN=5;
static constexpr uint8_t HEAD_ID=1, AS5600_ADDR=0x36;
static constexpr uint32_t DXL_BAUD=1000000;
static constexpr float MAX_HEAD_RPM=4.0f;
static constexpr float Kp=0.10f;   // rpm per degree; tune only on a supported fixture
static constexpr float STOP_DEG=3.0f;
static constexpr uint32_t CMD_TIMEOUT_MS=10000;
HardwareSerial DxlSerial(1);
HardwareSerial FaceSerial(2);
Dynamixel2Arduino dxl(DxlSerial, DXL_DIR);
Servo gripL, gripR;
Adafruit_VL53L0X tof;
Adafruit_MPU6050 imu;
bool headReady=false, armed=false, tofReady=false, imuReady=false;
bool gripLReady=false, gripRReady=false;
float targetDeg=0;
uint32_t lastCommandMs=0, lastControlMs=0, lastTelemetryMs=0;
char cmd[80]; size_t cmdLen=0;

float wrap180(float d) { while(d>180) d-=360; while(d<-180) d+=360; return d; }
bool readHeading(float &deg) {
  Wire.beginTransmission(AS5600_ADDR); Wire.write(0x0C); // RAW ANGLE MSB
  if (Wire.endTransmission(false)!=0) return false;
  if (Wire.requestFrom((int)AS5600_ADDR,2)!=2) return false;
  uint16_t raw=((uint16_t)(Wire.read()&0x0F)<<8) | Wire.read();
  deg=(raw*360.0f)/4096.0f; return true;
}
void stopHead() { if(headReady) dxl.setGoalVelocity(HEAD_ID,0.0f,UNIT_RPM); }
void disarm() { stopHead(); if(headReady) dxl.torqueOff(HEAD_ID); armed=false; }
void reply(const char *s) { Serial.println(s); }
void processLine(char *s) {
  lastCommandMs=millis();
  if (!strcmp(s,"ARM")) {
    if (!headReady) { reply("ERR NO_HEAD"); return; }
    float now; if(!readHeading(now)) { reply("ERR NO_ENCODER"); return; }
    targetDeg=now; dxl.torqueOn(HEAD_ID); armed=true; reply("OK ARMED"); return;
  }
  if (!strcmp(s,"DISARM")) { disarm(); reply("OK DISARMED"); return; }
  if (!strcmp(s,"STOP")) { float now; stopHead(); if(readHeading(now)) targetDeg=now; reply("OK STOPPED"); return; }
  if (!strncmp(s,"HEAD ",5)) {
    if(!armed) { reply("ERR DISARMED"); return; }
    char *end=nullptr; float a=strtof(s+5,&end);
    if(end==s+5 || *end!='\0' || a<0 || a>=360) { reply("ERR RANGE_0_359"); return; }
    targetDeg=a; reply("OK HEAD_TARGET"); return;
  }
  if (!strncmp(s,"GRIP L ",7) || !strncmp(s,"GRIP R ",7)) {
    char side=s[5]; char *end=nullptr; long a=strtol(s+7,&end,10);
    if(end==s+7 || *end!='\0' || a<0 || a>180) { reply("ERR GRIP_RANGE_0_180"); return; }
    if(side=='L') { if(!gripLReady) { gripL.setPeriodHertz(50); gripL.attach(GRIP_L_PIN,1000,2000); gripLReady=true; } gripL.write((int)a); }
    else { if(!gripRReady) { gripR.setPeriodHertz(50); gripR.attach(GRIP_R_PIN,1000,2000); gripRReady=true; } gripR.write((int)a); }
    reply("OK GRIP"); return;
  }
  reply("ERR COMMAND");
}
void readCommands() {
  while(Serial.available()) {
    char c=(char)Serial.read();
    if(c=='\r') continue;
    if(c=='\n') { cmd[cmdLen]='\0'; if(cmdLen) processLine(cmd); cmdLen=0; }
    else if(cmdLen<sizeof(cmd)-1) cmd[cmdLen++]=c;
    else cmdLen=0;
  }
}
void setup() {
  Serial.begin(115200); delay(300);
  DxlSerial.begin(DXL_BAUD,SERIAL_8N1,DXL_RX,DXL_TX);
  FaceSerial.begin(115200,SERIAL_8N1,FACE_RX,FACE_TX);
  Wire.begin(I2C_SDA,I2C_SCL); Wire.setClock(100000);
  tofReady=tof.begin(0x29,false,&Wire);
  imuReady=imu.begin(0x68,&Wire);
  if(imuReady) { imu.setAccelerometerRange(MPU6050_RANGE_4_G); imu.setGyroRange(MPU6050_RANGE_250_DEG); imu.setFilterBandwidth(MPU6050_BAND_21_HZ); }
  dxl.begin(DXL_BAUD); dxl.setPortProtocolVersion(2.0);
  headReady=dxl.ping(HEAD_ID);
  if(headReady) {
    dxl.torqueOff(HEAD_ID);
    dxl.setOperatingMode(HEAD_ID,OP_VELOCITY); // XL-320 wheel mode
    dxl.setGoalVelocity(HEAD_ID,0.0f,UNIT_RPM);
    // Torque remains off until explicit ARM; no head motion on power-up.
  }
  float h; bool encoder=readHeading(h); if(encoder) targetDeg=h;
  lastCommandMs=millis();
  Serial.printf("BOOT head=%s encoder=%s ToF=%s IMU=%s state=DISARMED\n",headReady?"OK":"MISSING",encoder?"OK":"MISSING",tofReady?"OK":"MISSING",imuReady?"OK":"MISSING");
}
void loop() {
  readCommands();
  uint32_t now=millis();
  if(armed && now-lastCommandMs>CMD_TIMEOUT_MS) { disarm(); reply("WATCHDOG DISARM"); }
  if(armed && headReady && now-lastControlMs>=50) {
    lastControlMs=now; float current;
    if(!readHeading(current)) { disarm(); reply("FAULT ENCODER"); return; }
    float err=wrap180(targetDeg-current);
    if(fabsf(err)<=STOP_DEG) stopHead();
    else {
      float rpm=Kp*err;
      if(fabsf(rpm)<0.8f) rpm=(err>0?0.8f:-0.8f);
      rpm=constrain(rpm,-MAX_HEAD_RPM,MAX_HEAD_RPM);
      // Confirm direction sign on a supported stand; invert rpm if target error grows.
      dxl.setGoalVelocity(HEAD_ID,rpm,UNIT_RPM);
    }
  }
  if(now-lastTelemetryMs>=500) {
    lastTelemetryMs=now; float h=0; bool encOK=readHeading(h);
    int distanceMm=-1; bool tofOK=false;
    if(tofReady) { VL53L0X_RangingMeasurementData_t m; tof.rangingTest(&m,false); if(m.RangeStatus!=4) {distanceMm=(int)m.RangeMilliMeter; tofOK=true;} }
    float ax=0,ay=0,az=0,gx=0,gy=0,gz=0;
    if(imuReady) { sensors_event_t a,g,t; imu.getEvent(&a,&g,&t); ax=a.acceleration.x; ay=a.acceleration.y; az=a.acceleration.z; gx=g.gyro.x; gy=g.gyro.y; gz=g.gyro.z; }
    Serial.printf("TEL head_deg=%.1f encoder=%d armed=%d tof_mm=%d imu_accel=%.2f,%.2f,%.2f gyro=%.2f,%.2f,%.2f\n",h,encOK?1:0,armed?1:0,distanceMm,ax,ay,az,gx,gy,gz);
    FaceSerial.println(tofOK?(distanceMm<500?"NEAR":"CLEAR"):"UNKNOWN");
    while(FaceSerial.available()) if(FaceSerial.read()=='B') Serial.println("EVENT BUTTON");
  }
}
