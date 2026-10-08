# TARS-Lite — budget tabletop humanoid prototype

A buildable, **stationary** TARS-inspired desktop robot: two structural support legs, a torso, two articulated arms ending in simple two-finger grippers, and one head with two fixed LED eyes. Revision 0.3 includes a front time-of-flight distance sensor, internal IMU, ESP32-S3, Pi 5 and Arduino. This is an educational prototype, not a walking or load-bearing robot.

## Scope and budget decisions

- Target ceiling: **USD $250**, indicative parts budget before local shipping/tax. Current all-three-controller estimate is **$223**, including a $25 contingency; shipping/tax may exceed the cap.
- Controllers: **ESP32-S3** handles servo PWM and sensor polling; **Raspberry Pi 5 1 GB** runs a lightweight headless logger over USB serial; **Arduino UNO R4 Minima** handles the two eye LEDs and reports a local button event over UART. The 1 GB Pi is not a vision/LLM machine.
- The first build does **not** walk. Legs are rigid, wide-set supports; do not install leg joints or allow it to stand unsupported until separately engineered and tested.
- Six micro servos: shoulder/elbow/gripper on each side. Eyes are fixed LEDs. Sensors: VL53L0X-class front distance ToF module + MPU6050-class IMU. Both share I2C; the IMU measures tilt/acceleration, not safe balance control.
- Servos use a separate regulated 5 V supply. Do not power servos from the ESP32 3.3 V pin or the Pi. Join supply ground and controller ground.
- The custom PCB is a low-voltage breakout/distribution board, not a motor driver or power supply. It routes PWM signals and distributes externally regulated servo power; sensor header carries 3.3 V, GND, SDA and SCL.
- Reuse a 3D printer and soldering tools. The Pi 5 supply/storage/cooling are included as estimates; paid 3D-print service, tools, shipping and tax are excluded.

## Package map

- `docs/ENGINEERING_JOURNAL.md` — design choices, assumptions, assembly and bring-up plan.
- `docs/BOM.csv` — indicative line-item budget and exclusions.
- `electronics/gerber/` — fabrication layers and drill files for the servo/sensor breakout PCB.
- `electronics/kicad/` — PCB interface specification (editable geometry source in `generate_gerbers.py`).
- `electronics/generate_gerbers.py` — deterministic generator for the simple through-hole board files.
- `mechanical/tarslite.scad` — parametric OpenSCAD assembly and print geometry.
- `mechanical/PRINT_GUIDE.md` — part quantities, fit checks, and slicer starting points.
- `mechanical/stl/` — rendered STL meshes for the individual parts.
- `firmware/` — pin map, ESP32-S3 servo/sensor scaffold, and Arduino eye/button sketch.
- `pi/` — lightweight serial telemetry monitor for Raspberry Pi OS Lite.

## First build limits

This is a concept-to-prototype package, **not a certified product**. The hand-built PCB should be visually inspected and checked for shorts before power. Confirm footprints, controller pins and sensor modules against the exact parts bought. Servos require external power and a common ground. Do not connect 5 V sensor outputs to ESP32 GPIO unless level-shifted. Keep pinch points clear; use low torque/speed and current-limited supply for first tests. A printed part, breakout, or servo failure could cause damage.

## Recommended build sequence

1. Inspect BOM, measure selected controller, servos and fasteners.
2. Print structural parts; fit-test one joint before printing duplicates.
3. Assemble PCB and inspect continuity/shorts.
4. Test the ESP32 alone, then I2C sensors, then one servo with external 5 V, then add servos one at a time.
5. Mount servos and tune neutral angles with arms supported; never command hard against a stop.
6. Mount ToF sensor in the face; mount IMU rigidly in the torso; validate sensor axes.
7. Add eyes and enclosure. Legs remain fixed supports.

## Publishing status

Local Git commit created. GitHub publication is pending because the GitHub account connector is disabled in this session; no credential bypass was attempted.
