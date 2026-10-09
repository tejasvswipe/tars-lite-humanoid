# PCB designs

This folder contains two distinct boards. They serve different purposes and their power/data domains must not be confused.

## DXL-Neck

[`DXL-Neck/`](DXL-Neck/) contains the editable KiCad single-servo interface board for the ESP32-S3 and one separate XL-320 neck bus, plus design notes, preview, Gerber/Excellon drills and fabrication ZIP. It is **not** a leg-bus controller or high-current distribution board. Run a full KiCad DRC and inspect the fabrication outputs before ordering.

## ServoBus-6

[`ServoBus-6/`](ServoBus-6/) contains the passive PWM/sensor breakout's Gerber generator, board specification and fabrication files. In this project it is limited to low-current hand servos and sensors; it is not for the walking actuators.
