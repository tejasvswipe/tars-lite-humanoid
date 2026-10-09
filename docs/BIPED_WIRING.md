# Biped v1.0 — Wiring and Power Map

This wiring plan is for the **biped add-on package only**. The older [`WIRING.md`](WIRING.md) describes the stationary prototype and its PWM arms; do not use its six-servo map for the walking joints.

## Controller and signal map

| Function | From → to | Signal / notes |
|---|---|---|
| Walking joints | Stock OpenCM9.04-C → 16 stock XL-320s | Keep the manufacturer controller, bus, IDs, battery input and gait files; do not connect a second data master |
| Neck servo UART | ESP32-S3 GPIO17 TX / GPIO18 RX → DXL-Neck PCB J1 pins 3/4 | 1 Mbps, Protocol 2.0, neck-only bus; set the neck XL-320 to ID 1 |
| Neck direction | ESP32 GPIO16 → DXL-Neck PCB J1 pin 5 | Active high while transmitting; board inverter drives 74HCT125 `/OE` low |
| Neck logic supply | ESP32 5V and GND → PCB J1 pins 1/2 | 5 V powers the logic ICs only; never connect this to actuator VDD |
| Neck actuator supply | 2S pack branch → PCB J3 pins 1/2 → F1 → J2 pins 2/1 | 6–8.4 V at the XL-320; J2 pin 2 is fused VDD, pin 1 GND, pin 3 DATA |
| Neck angle | AS5600 VCC/GND/SDA/SCL → ESP32 3V3/GND/GPIO8/GPIO9 | I²C address 0x36; sensor fixed to base, magnet fixed to rotor |
| Front distance / torso attitude | ToF + MPU6050-class module → same ESP32 3V3 I²C bus | Typical addresses 0x29 / 0x68; confirm voltage, pull-ups and exact board variants |
| Left/right grippers | ESP32 GPIO4/GPIO5 → existing ServoBus-6 PWM1/PWM2 → 9 g microservos | Separate regulated 5 V 3 A rail on the board's servo-power input; common ground only |
| Pi high-level commands | Raspberry Pi 5 USB → ESP32 USB CDC | `ARM`, `HEAD n`, `GRIP L/R n`, `STOP`, `DISARM`; Pi does not control the stock gait bus |
| Eye LEDs / face button | Arduino UNO R4 D4/D5 LEDs; D2 button | Arduino D0/D1 UART to ESP32 GPIO15/GPIO14; use verified bidirectional 3.3↔5 V level shifting unless both input thresholds are confirmed compatible |
| Rotating face | Arduino LED outputs → 6-wire slip ring → eye LEDs | Use 4 conductors for 5 V/GND/left/right; one 330 Ω-class resistor per LED; no actuator or battery rail through ring |

## Power-domain rules

- The **leg actuator bus** remains on the stock platform's manufacturer supply/controller wiring. Do not assume its battery, board or connector can accept added actuator loads without checking the exact manual.
- The neck XL-320 uses a separate DATA bus and a separately fused branch. It can share the 2S pack only after confirming the battery, emergency stop, connectors and harness can support the added load. XL-320 spec lists 1.1 A stall current at 7.4 V; one head servo alone can demand that at stall.
- A rough simultaneous-stall upper bound for 16 leg/reference XL-320s plus one neck XL-320 is **17 × 1.1 A = 18.7 A**. It is not normal operating draw, but demonstrates why the battery, main fuse, e-stop and wiring cannot be selected from average current or a 5 V breadboard rail. Measure actual transients and check manufacturer guidance.
- The hand servo board has a separate regulated 5 V input. Do not tie its positive output to the 2S actuator rail or ESP32 3V3 rail. Use common GND where signals cross; do not tie separate regulated +5 V sources together.
- The Pi 5 uses its own compliant 5.1 V / 5 A USB-C power supply. The Arduino and ESP32 use their own approved logic supplies/USB; signal-ground connection does not mean positive rails should be paralleled.
- Hardwired e-stop must cut actuator battery positive upstream of both leg and neck power branches. It must be DC-rated for the final measured current; software STOP is not an emergency stop.

## First-power checklist

1. With batteries removed, verify connector pin order with the XL-320 manufacturer connector diagram; do not trust wire color.
2. Check no continuity short exists between 2S VDD, logic 5 V and GND where not intended. Verify the neck PCB's fuse only feeds J2 VDD.
3. Power the logic board with no actuators attached; verify +5 V rails, UART direction and RX divider levels.
4. Power the neck branch from a current-limited 7.4 V bench supply, verify polarity and current limit, then connect one XL-320.
5. Confirm no motion on reset. Arm only while the robot is held in a fixture, verify the angle sensor and movement sign, then test STOP/DISARM/watchdog.
6. Keep walking tests separate until stock gait and e-stop have passed with the unmodified base platform.
