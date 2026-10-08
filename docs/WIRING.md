# TARS-Lite wiring and assembly notes (v0.3)

## Controller roles

- **Raspberry Pi 5 1 GB:** headless Raspberry Pi OS Lite telemetry logger, connected by USB to ESP32. This memory tier is not for local vision/LLM workloads.
- **ESP32-S3:** six servo PWM outputs and I2C polling for the front ToF and torso IMU; sends sensor text over USB serial to Pi and `NEAR/CLEAR/UNKNOWN` over UART to Arduino.
- **Arduino UNO R4 Minima:** face-eye LEDs and local button event input. It does not drive servos or act as a safety-rated controller.

## Pin assignment proposal

| Function | Controller pin | Notes |
|---|---:|---|
| Servo shoulder L / elbow L / gripper L | ESP32 GPIO 4 / 5 / 6 | PWM only, via JPWM1-3 |
| Servo shoulder R / elbow R / gripper R | ESP32 GPIO 7 / 15 / 16 | PWM only, via JPWM4-6 |
| I2C SDA / SCL | ESP32 GPIO 8 / 9 | ToF and IMU share bus; verify exposed/free pins on board |
| Face UART ESP32 TX / RX | ESP32 GPIO 17 / 18 | Cross to Arduino D0 RX / D1 TX; level-shift Arduino TX toward ESP32 RX |
| Left / right eye LED | Arduino D4 / D5 | One 330-ohm-class resistor per LED |
| Local button | Arduino D2 | Button to GND; firmware enables internal pull-up |
| Pi data | Pi USB-A ↔ ESP32 USB | USB CDC serial; Pi script reads `/dev/ttyACM0` by default |
| Servo supply | External regulated 5 V | Fused source to J_PWR; never power servos from controller pins |

## Power and signal precautions

1. Pi has its own 5.1 V / 5 A USB-C supply; servo rail is separately regulated/fused. Arduino may be powered from Pi USB only if port limits permit; check total USB current.
2. Estimate/measure servo peak/stall current. Six small servos may exceed 5 A if stalled together; actual supply, wiring and PCB copper must be sized for the real load.
3. Connect servo source positive/ground to J_PWR; servo headers are GND, +5 V, PWM. Check connector orientation from the board specification because Gerber silkscreen is blank.
4. ESP32 GND, servo supply GND and Arduino GND must be common. Pi ground joins through its USB cable.
5. Arduino UNO R4 uses 5 V logic. Use a level shifter on Arduino TX → ESP32 RX (or a documented divider); do not let a 5 V TX signal reach ESP32 GPIO. ESP32 3.3 V TX to Arduino RX is expected but test against board logic thresholds.
6. Disconnect power before wiring. Meter-check +5 V-to-GND shorts before first power-up. PCB has no onboard fuse, reverse protection or regulator.

## Sensors and placement

- Face-mounted VL53L0X-class module: J_I2C 3V3/GND/SDA/SCL; align its optical aperture with the face window.
- Torso MPU6050-class IMU: share the same I2C bus, using a short Y lead. Check voltage, address and pullups.
- Mount IMU rigidly on rear torso panel and record axes. Sensors provide telemetry only, not collision safety or balance control.
- Keep power wiring away from I2C leads; add strain relief. Fix both legs; test on a stable level surface.
- Support arms during servo tests and calibrate each unit before fitting horns/grippers.
