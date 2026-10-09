# TARS-Lite Complete Biped Prototype — Build Package v1.0

**Status:** a complete, editable *prototype design package* for a small biped using a proven commercial gait base plus custom TARS-style add-ons. It is not a finished or safety-certified robot, and no physical fit or walking test has yet been performed in this workspace.

## What this version is

- **Two-legged walking base:** ROBOTIS MINI / Darwin-Mini reference platform, using its 16 stock XL-320 joints, OpenCM9.04-C controller and manufacturer motion package. This avoids inventing an unverified small-biped gait from scratch.
- **TARS-like body:** custom printed torso shell, head with two eyes, rear “spinal” electronics tray, forearm shells and simple two-finger grippers. The official lower-body files remain the platform's own printable frame.
- **360° head:** one additional XL-320 in a separate neck-only bus, configured for continuous wheel mode. A stationary AS5600 absolute angle sensor measures head heading; a 608 bearing supports the head. This is a voltage-compatible choice for the XL-320 biped rail.
- **Three requested computers:** Raspberry Pi 5 (high-level command console/logging), ESP32-S3 (head angle loop, distance/IMU telemetry and gripper PWM), and Arduino UNO R4 Minima (eye LEDs and local button). The reference kit's OpenCM remains the gait controller; its stock gait is not replaced.
- **Two PCBs:** reuse the existing `ServoBus-6` PCB only for low-current sensors / two 5 V hand servos; add the separate `DXL-Neck-Interface` signal-level interface for the neck XL-320. Neither board is a substitute for the biped kit's actuator controller or high-current battery harness.

## Important correction to the earlier upgrade proposal

The earlier proposal named an XL-430 neck actuator. **Do not connect an XL-430 to the XL-320 7.4 V servo rail**: the XL-430 is a different voltage class. This revision instead uses one extra XL-320 (6–8.4 V input; 7.4 V recommended) on a separate data line. It shares only the appropriately rated 2S actuator power source, through its own inline fuse. The XL-320 wheel mode is continuous; its internal position feedback does not track travel in wheel mode, so the separate AS5600 provides absolute 0–360° heading feedback.

Manufacturer data: [XL-320 specification and communication circuit](https://docs.robotis.com/docs/dxl/model_reference/x_series/xl_series/xl320). ROBOTIS lists 0.39 N·m stall torque at 7.4 V / 1.1 A and advises stable motions at no more than about one-fifth of stall torque. Use a light head (target ≤150 g) and a low-friction bearing; test loads and temperatures before use.

## Architecture and wiring boundaries

### Motion and power domains

1. **Leg bus:** stock OpenCM controller → existing 16 XL-320 actuators and stock manufacturer harness. Keep the original motion firmware and stock power connection until its specifications are checked.
2. **Neck bus:** ESP32-S3 `Serial1` → `DXL-Neck-Interface` level shifter → one XL-320, ID 1 at the configured baud. Its **DATA line is separate** from the 16-joint leg bus; only the power return/ground is common. Use the specified 2S actuator voltage (6–8.4 V at the actuator) and an independent inline fuse on the neck branch. Do not hot-plug DYNAMIXEL cables.
3. **Hand servos / sensors:** ESP32 PWM and I²C → existing `ServoBus-6` breakout. Power the two microservos from an independent regulated 5 V rail (budget for at least 3 A peak); do not power them from ESP32/Pi GPIO. I²C sensors use 3.3 V only.
4. **Logic:** Pi 5 uses its own compliant 5.1 V / 5 A supply; ESP32 and Arduino use their board USB/5 V inputs. Grounds are common where signals cross; keep the separate positive supply rails isolated.
5. **Face:** Arduino drives two LED channels through the slip ring. Use four of its conductors for 5 V, GND, left-eye and right-eye (330 Ω-class current-limiting resistor per LED); spare conductors remain unconnected. Slip ring is not for actuator or battery current.
6. **Sensors:** front ToF and torso IMU use the ESP32's shared I²C bus. AS5600 (0x36), MPU6050-class IMU (0x68) and VL53L0X-class ToF (0x29) share SDA/SCL only if pull-ups and voltage are compatible. Place the ToF sensor on the torso, not on the rotating head.
7. **Emergency stop:** use a hardwired latching switch that interrupts actuator battery positive upstream of both leg and neck branches. A software STOP is not an emergency stop.

### Proposed ESP32-S3 pins

| Function | ESP32-S3 pin | Notes |
|---|---:|---|
| Neck DYNAMIXEL UART TX / RX | GPIO17 / GPIO18 | `Serial1`; verify against the exact DevKitC-1 revision |
| DYNAMIXEL direction | GPIO16 | The new board inverts this logic for the half-duplex driver |
| I²C SDA / SCL | GPIO8 / GPIO9 | AS5600, ToF and IMU; check exact board pinout |
| Face UART TX / RX | GPIO15 / GPIO14 | `Serial2` to Arduino D0/D1; use a verified bidirectional level shifter for 3.3 V ↔ 5 V logic |
| Left / right gripper PWM | GPIO4 / GPIO5 | Through existing ServoBus-6 channels; external regulated 5 V |
| Pi connection | USB CDC | Pi sends `ARM`, `HEAD <0..359>`, `GRIP L <0..180>`, `GRIP R <0..180>`, `STOP`, `DISARM` |

**Never** connect a 5 V Arduino TX pin directly to an ESP32-S3 GPIO; also verify that the Arduino accepts the ESP32's 3.3 V TX HIGH level. Use a bidirectional level shifter unless the exact boards' input thresholds are confirmed. Confirm the bus baud and XL-320 ID before powering the neck. Assign no duplicate ID on the neck-only bus.

## PCB package

- `electronics/gerber/` is the earlier ServoBus-6 low-voltage PWM/sensor board. For this biped build it is restricted to two low-current 5 V microservos and 3.3 V sensors; it does not drive the walking legs.
- `electronics/dxl_neck/` contains the new editable KiCad neck-interface PCB and exported Gerber/Excellon fabrication files. It converts ESP32 3.3 V UART to the XL-320 TTL half-duplex bus with a 74HCT buffer and direction inversion, and provides a separately fused, single-servo power branch. The PCB is **not** the 16-actuator leg power distribution board.
- Inspect the board in KiCad/Gerber viewer and **run KiCad DRC locally before fabrication**; a full PCB DRC has not been executed in this package. The generated revision has 0 open KiCad connectivity items after zone fill and 0 flags in a supplementary geometric trace/pad screen; that screen is not a DRC substitute. Check fuse orientation, connector polarity/adapter wiring, track widths and all power-net clearances. Bench-test the first board with one XL-320 and a current-limited supply.

## Mechanical package

- Editable add-on source: `mechanical/biped_tarslite.scad`.
- Printable STL outputs: `mechanical/biped_stl/`.
- Vendor lower-body STEP/STL and stock assembly guide are linked from the [ROBOTIS MINI e-Manual](https://emanual.robotis.com/docs/en/edu/mini/); vendor files are not republished here.
- The 6-mm-grid host slots and XL-320 horn adapter are deliberately adjustable. Print coupons and measure your actual kit before printing the full set. Do not assume the TARS shell fits without adjustment.

## Firmware and operation

1. Flash `firmware/esp32_biped_head.ino` to an ESP32-S3 using the Arduino framework, after installing the listed libraries. Its default state is **unarmed** and the head velocity is zero.
2. Start the Pi console with `python3 pi/head_console.py --port /dev/ttyACM0`. Commands are clamped to the firmware's safe operating range; use `DISARM` when finished.
3. Load `firmware/eyes_button.ino` on the Arduino. Its eyes are an indicator only; its button sends an event and is not a safety switch.
4. Run stock biped motions only through the manufacturer-supported controller/app. First verify actuator IDs, pose and all joints with the robot lifted and supported. Do not run a walking motion until the shell, battery, center of gravity, and cable clearance have been checked.
5. The custom software does **not** implement biped balance, fall recovery, collision avoidance, voice recognition, or autonomous household task planning. The stock reference gait is not guaranteed after changing robot mass or center of gravity.

## Bring-up and acceptance gates

1. **Fit check:** verify every kit mounting point and XL-320 horn. Confirm head mass ≤150 g target and full 360° clearance with all cables/rotor parts installed.
2. **Power check:** disconnect every actuator; inspect fuse, connector, polarity and grounds with a meter. Use a current-limited bench supply for the neck branch. Do not use a breadboard for actuator current.
3. **Neck-only test:** bench-test one XL-320, direction control, AS5600 reading, command parser, watchdog and STOP/DISARM. Confirm no rotation at boot, correct direction, measured full-turn angle, and safe motor temperature.
4. **Hands-only test:** power the 5 V microservos from their own supply; confirm travel limits, no binding and less than 3 A peak for the selected parts.
5. **Stock gait test:** remove all shell/hand add-ons; use manufacturer initial pose and stock motions on a tethered/padded floor with a spotter and accessible physical emergency stop.
6. **Incremental integration:** add the torso shell, then the head, then each arm/hand, retesting gait and temperature after every mass/CG change.
7. **Do not proceed to unsupervised walking** if the robot falls, oscillates, overheats, draws excessive current, or has loose/strained wires.

## Realistic task envelope

This is a small educational biped, not a general home assistant. Initial tasks should be limited to supervised walking on a clear, level surface and opening/closing the grippers around very light, soft objects. It must not carry hot/sharp/heavy items, operate tools, touch people, climb stairs, or run unattended. The original gait platform's stability may be reduced by the new torso and head; the robot must be tested with its actual printed mass.

## Cost and availability

The revised source-based planning BOM is `WALKING_360_BOM.csv`. Current planning estimate is about **USD 1.13k–1.35k before shipping/tax**, including 15% contingency, subject to exact kit contents and power requirements. The ROBOTIS MINI listing and extra XL-320 reference were shown backordered/sold out during the research snapshot; the XL-320 source price is not a promise of availability. The BOM explicitly marks estimates and price references. Do not purchase an alternative actuator until voltage, protocol, dimensions, torque and gait compatibility have been rechecked.
