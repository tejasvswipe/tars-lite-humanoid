# Firmware and software

## ESP32-S3 and Arduino

[`ESP32-Arduino/`](ESP32-Arduino/) contains both firmware tracks. `tarslite.ino` and the stationary pin map belong to the fixed-support baseline. `esp32_biped_head.ino`, `eyes_button.ino` and `platformio-biped.ini` belong to the biped add-on design. Do not mix their wiring or power assumptions.

## Raspberry Pi 5

[`Raspberry-Pi/`](Raspberry-Pi/) contains the serial telemetry logger, biped neck/gripper console and setup notes. The Pi is a high-level console/logger in this design, not a gait controller or local vision/AI computer.
