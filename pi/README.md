# Raspberry Pi 5 1 GB monitor

Use Raspberry Pi OS Lite, no desktop or heavy ML. Connect the ESP32-S3 USB data port to a Pi USB port; identify the port with `ls /dev/ttyACM*`. A Pi 5 1 GB is sufficient for lightweight telemetry logging, not for local vision/LLM workloads.

Install `python3-serial` (`sudo apt install python3-serial`) and run:

```bash
python3 monitor.py --port /dev/ttyACM0 --log ~/tarslite-telemetry.log
```

The Pi has its own 5.1 V / 5 A USB-C supply, separate from the servo rail. The Arduino may be connected to Pi USB for its supply only if port current limits are respected; UART with ESP32 is the designated data link. Avoid powering servos from either computer board.