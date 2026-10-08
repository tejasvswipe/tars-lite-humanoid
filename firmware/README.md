# Firmware bring-up

Target: ESP32-S3 DevKitC-1-class board, Arduino framework. Install libraries: ESP32Servo, Adafruit_VL53L0X, Adafruit_MPU6050, Adafruit Unified Sensor. The exact GPIO choices must be checked against the purchased board and selected USB/flash configuration. The scaffold uses 6 PWM channels; do not assume every ESP32-S3 pin is free on every board variant.

The companion `eyes_button.ino` is for an Arduino UNO R4 Minima and uses `Serial1` on D0/D1 for `NEAR`, `CLEAR`, `UNKNOWN` and `BTN` messages. Fit a level shifter on Arduino TX to ESP32 RX. The ESP32 USB serial text stream is intended for the Raspberry Pi monitor under `pi/`.

## Power and signal

Use a separate regulated 5 V servo supply and inline fuse. Servo GND and ESP32 GND must be connected together. Never feed servo power into the 3V3 pin. Connect the six PWM signals to the passive PCB's PWM1–PWM6. Start with one servo only, unloaded and mechanically disconnected.

Suggested starting GPIOs (verify board variant): servo PWM 4, 5, 6, 7, 15, 16; I2C SDA 8/SCL 9; UART to Arduino TX 17/RX 18. Modules use 3.3 V-compatible I/O. Connect ToF and IMU in parallel on the same I2C bus; verify addresses and pullups. Firmware reports range and IMU acceleration/gyro over serial but does not use readings for motion or safety. At 50 Hz, calibrate each servo and slowly test around neutral; stop immediately if buzzing, heating, binding, brownout, or unexpected travel occurs. The source intentionally commands neutral pulses only.

For a Pi 5 upgrade, run high-level UI/vision on Pi and communicate desired bounded targets over USB serial/UART. Keep servo timing and any future emergency-stop handling on the ESP32. No Pi 5 is needed to test v0.1.
