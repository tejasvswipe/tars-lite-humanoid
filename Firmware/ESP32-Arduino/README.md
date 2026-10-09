# Firmware bring-up

This folder contains two separate firmware tracks. Do not mix their pin maps or power assumptions.

## Stationary v0.3 baseline

`tarslite.ino` is the original ESP32-S3 stationary scaffold. Install ESP32Servo, Adafruit_VL53L0X, Adafruit_MPU6050 and Adafruit Unified Sensor. It drives at most one PWM channel by default and only reports sensor telemetry. `eyes_button.ino` is the Arduino UNO R4 Minima face indicator. For the original stationary setup, see [`../../Docs/Stationary/WIRING.md`](../../Docs/Stationary/WIRING.md).

## Biped add-on v1.0

`esp32_biped_head.ino` is for an ESP32-S3 DevKitC-1-class board. It controls a **separate, neck-only XL-320 bus**, reads an AS5600 absolute angle sensor plus the ToF/IMU, and drives two small gripper servos through the existing ServoBus-6 board. The stock ROBOTIS OpenCM controller remains responsible for the 16 leg/arm gait actuators.

Required Arduino libraries: Dynamixel2Arduino, ESP32Servo, Adafruit_VL53L0X, Adafruit_MPU6050, and Adafruit Unified Sensor. A dependency manifest is in `platformio-biped.ini`. The current source **compiled successfully** with PlatformIO for `esp32-s3-devkitc-1` (6.6% RAM, 11.0% flash); it has not been flashed to or tested on physical hardware. Confirm the exact ESP32-S3 board variant and review library versions before deployment.

The proposed pin map is in [`../../Docs/Biped/BIPED_WIRING.md`](../../Docs/Biped/BIPED_WIRING.md). Confirm every pin against the purchased DevKit. The custom DXL interface board level-shifts UART and passes a separately fused 6–8.4 V branch for **one** XL-320 only. Keep it off the 16-joint bus power distribution.

At boot, neck torque is off and no head motion is commanded. Send `ARM`, then `HEAD <0..359>`; `STOP` stops; `DISARM` turns neck torque off. A 10-second command timeout disarms the neck. Verify direction and the encoder magnet gap on a supported bench fixture before mounting the head. These controls are not a safety-rated emergency stop.

Grippers accept `GRIP L <0..180>` and `GRIP R <0..180>`. The hand servos must have their own regulated 5 V supply, separate from GPIO and actuator power. Their initial mechanical center must be set so the first commanded position does not bind.

The Arduino eye/button firmware remains the face indicator; route only low-current LED conductors through the slip ring, with a resistor per LED. Level-shift Arduino TX toward ESP32 RX. A button event is informational and is not a safety function.
