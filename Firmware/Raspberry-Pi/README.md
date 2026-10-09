# Raspberry Pi 5 1 GB support

Use Raspberry Pi OS Lite, without a desktop or heavy ML. A Pi 5 1 GB is sufficient for the command console and lightweight telemetry logging, not local vision/LLM workloads. Give the Pi its own compliant 5.1 V / 5 A USB-C supply; do not power any servo from Pi pins.

## Stationary telemetry logger

Install the serial package (`sudo apt install python3-serial`) and run:

```bash
python3 monitor.py --port /dev/ttyACM0 --log ~/tarslite-telemetry.log
```

## Biped add-on console

Connect the ESP32-S3 USB CDC port and install the same serial dependency. Run:

```bash
python3 head_console.py --port /dev/ttyACM0
```

Commands: `arm`, `head 0..359`, `left 0..180`, `right 0..180`, `stop`, `disarm`, `quit`. The firmware limits head speed and disarms after 10 seconds without a command. This console controls only the neck/grippers; the supported walking gait remains on the ROBOTIS platform controller/app. Keep the physical latching actuator emergency stop reachable during tests.
