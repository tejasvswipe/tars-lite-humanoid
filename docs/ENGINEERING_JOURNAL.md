# TARS-Lite Engineering Journal

**Revision:** 0.3 prototype pack  
**Date:** 2026-10-08  
**Budget ceiling:** USD 250, indicative parts cost  
**Status:** Design files and STL meshes generated; not physically built, fabricated, or electrically validated.

## 1. Design brief and scope interpretation

Requested: a TARS-inspired humanoid with one face/two eyes, hands, legs, rear-mounted electronics, ESP32-S3 / Raspberry Pi 5 / Arduino options, sensors, and PCB/Gerber and 3D-print files. The revised budget ceiling is $250.

The initial build is a **stationary desktop robot** with rigid legs and six low-cost servo axes. This preserves the visual and interactive concept without making unsafe claims about walking. The revised BOM includes all three requested controllers: a low-cost 1 GB Pi 5, ESP32-S3, and Arduino UNO R4 Minima. The sensor set is a front VL53L0X-class time-of-flight range module and an MPU6050-class torso IMU.

## 2. Architecture

- **Head/face:** one face plate, two fixed diffused LED eyes, one front ToF range sensor. No eye rotation servos in v0.3.
- **Torso:** central compact chassis; electronics mounted on the rear internal panel, along the spine side, with ventilation and service access.
- **Arms/hands:** each arm has shoulder pitch + elbow pitch + one-servo two-finger gripper. Limited range; no human-scale payload handling.
- **Legs:** two rigid printed leg shells/struts with broad feet. Supports only, not actuated. Center of mass must remain over feet.
- **Compute stack:** Raspberry Pi 5 1 GB in rear electronics bay runs a minimal headless monitor/logger via USB serial; its 1 GB RAM is not a vision/LLM target. ESP32-S3 performs servo PWM and I2C sensor polling. Arduino UNO R4 Minima drives the two face LEDs and reports local button events via a 3.3/5 V-safe UART link. Keep Arduino away from servo power control; it is not a safety controller.
- **Distance sensor:** front-facing VL53L0X-class ToF module on I2C. It gives short-range distance readings for a supervised stationary demo; it is not a certified collision-avoidance system.
- **IMU:** MPU6050-class module fixed rigidly in torso, on shared I2C. It measures acceleration/angular rate; this stationary design does not use it for balance control.
- **Servo signals:** six ESP32-S3 PWM channels to signal-only headers. PCA9685 may be added if PWM timing needs offload; not required for v0.3.
- **Power:** separate regulated 5 V supply for servo rail, fused and wired for actual worst-case current. Controller may use USB supply. Grounds must be common. Do not route servo current through MCU/logic traces.

## 3. PCB intent

The fabrication set describes a passive two-layer through-hole servo power/signal distribution board: two-wire external regulated 5 V input; shared servo power/ground; six 3-pin servo outputs; controller I2C and six PWM input pads; plus a 4-pin 3V3/GND/SDA/SCL sensor header. Servo power is routed on top copper and PWM signals on bottom copper. It has no active motor driver, regulator, fuse, reverse-polarity protection, or level shifter.

Use an inline fuse on 5 V servo supply. Because low-cost servos can collectively draw high stall current, check power bus, connector and wiring current capacity against exact components. Sensor modules must be 3.3 V logic-compatible. The PCB has not been manufacturer-DRC checked or physically tested; inspect every Gerber layer and perform electrical design review before fabrication.

## 4. Indicative budget

`docs/BOM.csv` currently totals **$223 estimated parts** before shipping/tax/tools, leaving $27 under the $250 cap. It includes a $45 Pi 5 1 GB (official launch pricing), a $20 Arduino UNO R4 Minima (official Arduino US store listing), and estimates for the Pi power supply, microSD, and cooling. It assumes an existing 3D printer/computer and excludes shipping/tax, battery and charger. Price references: https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/ and https://store-usa.arduino.cc/products/uno-r4-minima. Raspberry Pi 5 requires a separate 5 V/5 A USB-C supply: https://www.raspberrypi.com/products/27w-power-supply/. These are planning estimates, not checkout prices; local tax/shipping can exceed the $250 cap.

## 5. Mechanical plan

OpenSCAD model uses adjustable dimensions and separate printable parts: head shell/face insert, torso, arms, grippers, support legs and feet. Individual STL exports were rendered and passed a watertight mesh check; physical fit remains unverified. Add a ToF sensor behind the face aperture and locate the IMU on a rigid torso mount. CAD needs detailed fit iteration against the chosen sensor, boards, servo horns and screws. A typical hobby micro servo is nominally about 23 x 12 x 29 mm; verify the exact part. Suggested PLA for fit/appearance, PETG for repeated-use brackets. Use metal screws/nuts at joints; do not rely on printed threads.

## 6. Bring-up and validation log

No hardware has been assembled or tested in this session.

| Check | Status | Notes |
|---|---|---|
| CAD fit against exact servo/controller/sensor | NOT RUN | Measure purchased parts first |
| Gerber viewer layer/outline review | NOT RUN | Check units and drill mapping |
| PCB continuity/short check | NOT RUN | Test unpowered before connecting controller |
| I2C address scan and sensor orientation | NOT RUN | Confirm both modules share bus without address conflict |
| 5 V supply fuse/current test | NOT RUN | No servo attached initially |
| One-servo PWM test | NOT RUN | External 5 V; common ground |
| Six-servo no-load test | NOT RUN | Add channels gradually; monitor resets/heat |
| Enclosure/center-of-mass test | NOT RUN | Legs fixed; stable surface only |

## 7. Safety and limitations

- Stationary and supervised only; not a walking robot, not for carrying people/objects, not for unsupervised children.
- Micro servos pinch. Limit speed, travel and torque; keep gripper force low.
- Disconnect power before wiring. Stalled servos can overheat, reset control or damage traces/connectors.
- Use a regulated supply, fuse, insulated wiring, strain relief and ventilation. No battery pack or charger design is included.
- Confirm sensor board I/O voltage; never connect 5 V signal to ESP32 GPIO without level conversion.
- Sensor readings are not safety interlocks. Printed parts are unvalidated; inspect layer adhesion/fasteners.

## 8. References

- Espressif, ESP32-S3 DevKitC-1 listing: https://www.espressif.com/en/products/devkits (accessed 2026-10-08; sample reference $15 for DevKitC-1-N8R8).
- Raspberry Pi, Pi 5 1 GB launch price: https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/ (official announced price $45; accessed 2026-10-08).
- Arduino, UNO R4 Minima: https://store-usa.arduino.cc/products/uno-r4-minima (official US store listed $20; accessed 2026-10-08).
- Raspberry Pi 27 W USB-C supply: https://www.raspberrypi.com/products/27w-power-supply/ (5.1 V, 5 A output; price estimate in BOM is not official retail quote).
- KiCad/JLCPCB Gerber/drill export guide: https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-9.

References inform architecture/manufacturing conventions. Requote all items before purchasing; the budget margin is narrow and shipping/tax are excluded.
