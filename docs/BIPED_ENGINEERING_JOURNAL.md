# TARS-Lite Biped / 360° Head Engineering Journal

**Revision:** 1.0 — design package, not a completed physical robot
**Status:** CAD, source firmware, BOM, KiCad neck interface, Gerbers and STL add-ons are prepared. Physical assembly, fit checks, electrical DRC/DFM and gait testing remain outstanding.

## Design brief

Build a small TARS-inspired two-legged robot with a face, two eyes, hands/grippers, a continuously rotating head, and electronics concentrated in a rear/spinal tray. Use the requested Raspberry Pi 5, ESP32-S3 and Arduino, while keeping the existing budget warning visible. The earlier $127 cap cannot cover a safe walking platform with the requested computers and actuators; the current reference BOM is about **$1,128.53–$1,353.93 including 15% contingency**, before shipping/tax and subject to stock and kit contents.

## Decision log

### 1. Use a proven gait base rather than inventing balance control

The walking lower body is based on the 16-DOF ROBOTIS MINI / Darwin-Mini reference system, with its stock XL-320 joints, OpenCM9.04-C gait controller and manufacturer motion package. This intentionally avoids claiming that a newly improvised ESP32 gait can balance a biped. The official lower-body CAD and gait resources are linked, not redistributed. The kit listing was shown backordered during the research snapshot; verify availability and exact included battery/charger before purchase.

### 2. Separate the three requested computers by role

- **Raspberry Pi 5 1 GB:** high-level USB command console and logging only; it is not sized or programmed here for local vision or language-model work.
- **ESP32-S3:** neck angle loop, sensors and two light gripper servos; starts unarmed and keeps the neck stopped until explicitly armed.
- **Arduino UNO R4 Minima:** two face/eye LED channels and a local button event; the button is not an emergency stop.
- **OpenCM9.04-C:** remains the stock gait controller for the reference base.

The positive power rails remain separate by function. Signals share a common return where required; battery/actuator current never travels through a logic board or slip ring.

### 3. Correct the neck actuator voltage mismatch

An early proposal named an XL-430. That actuator is not appropriate for the XL-320 2S rail. The compatible design uses one extra XL-320 on a **separate neck-only DATA bus**, with a 2S-fused actuator branch. It operates in continuous wheel mode; wheel mode does not provide accumulated travel position, so an AS5600 absolute magnetic sensor provides the 0–360° head heading. A bearing carries the head load independently of the servo horn. Keep the head light and validate torque, temperature, cable routing and stops before use.

### 4. Keep the hands intentionally simple

Two lightweight printed grippers use one 9 g-class microservo each and are intended only for very light, soft objects. They are not human-safe dexterous hands. Their supply is an independent regulated 5 V rail sized for servo peaks; ESP32 GPIO is signal-only.

### 5. Produce a separate single-servo neck interface PCB

The KiCad board translates 3.3 V ESP32 UART to the XL-320's 5 V TTL half-duplex bus with 74HCT logic, receive division and disabled-by-default direction control. A separately fused 2S branch feeds only one neck servo. It is not a leg controller or high-current distribution PCB.

For reproducibility, run `generate_board.py` with the KiCad 7 `pcbnew` module, then `export_gerbers.sh`. The export helper calls `fill_zones.py` as a separate process, saves the filled B.Cu GND plane, and exports Gerbers, PTH/NPTH drills, drill-map PDFs and a ZIP. On the current revision, KiCad connectivity reported **0 unconnected items** after zone fill. A supplementary geometric trace/pad precheck reported **0 flags**. A full KiCad DRC, manufacturer DFM check and powered test have **not** been completed; run them before fabrication or connection to a servo.

## Package contents

- `docs/COMPLETE_BIPED_BUILD.md` — integrated build, power, pin map, gates and limitations.
- `docs/WALKING_360_BOM.csv` — line items, status/source notes, subtotals and 15% reserve.
- `docs/BIPED_WIRING.md` — the connector and power-domain map.
- `mechanical/biped_tarslite.scad` and `mechanical/biped_stl/` — editable shells/neck/gripper add-ons and exported meshes.
- `electronics/dxl_neck/` — KiCad source, fill/export helpers, component BOM, schematic notes and fabrication pack.
- `firmware/esp32_biped_head.ino` — guarded neck, sensor and gripper scaffold; `firmware/eyes_button.ino` remains the Arduino face sketch.
- `pi/head_console.py` — serial command console.

## Validation snapshot

| Area | Result | Still required |
|---|---|---|
| BOM | Parsed line items and totals reconcile: $981.33–$1,177.33 before reserve; $1,128.53–$1,353.93 with 15% reserve | Confirm live stock, final kit contents, regional price, shipping/tax and actual power draw |
| PCB connectivity | KiCad reports 0 open items after zone fill | Full KiCad GUI DRC; inspect connector orientation and Gerber/drill layers; DFM review |
| PCB trace precheck | 0 different-net track/pad flags in supplementary geometric screen | Not a substitute for KiCad DRC or fab-house checks |
| Firmware | Source and configuration are included; default state is unarmed | Compile for exact ESP32-S3 board, verify library/API versions, serial levels, actuator ID/baud and bench test |
| Mechanical | Parametric model and STL add-ons are included | Fit coupons to the exact host kit; measure printed mass/CG, horn geometry and 360° clearance |
| Walking | Uses the manufacturer's stock gait package | Tethered/padded-floor test with shell removed, then incremental mass additions; no autonomous balance or fall recovery |

## Safety and intended task envelope

Treat the robot as a supervised educational prototype. Use a tether, a clear padded test area and an accessible hardwired latching actuator-power stop; lift/support the body during first actuator tests. Begin with the bare stock gait, then add printed parts one at a time. Stop if it falls, oscillates, overheats, draws excessive current, binds or strains cables. Do not use it around people, stairs, hot/sharp/heavy objects, tools or unsupervised household tasks.

## Next build gates

1. Confirm a genuine compatible reference kit and inspect its included battery, charger, controller and instructions.
2. Run the full KiCad DRC and review the Gerber ZIP in a separate viewer; resolve every reported issue before board ordering.
3. Print low-mass fit coupons; measure the actual XL-320 horn, bearing, frame slots, fasteners and cable/slip-ring route.
4. Populate and bench-test the neck board with a current-limited supply and one XL-320; verify safe reset state and angle sensor readings.
5. Compile each controller sketch for the exact board variant; verify bidirectional UART level compatibility and servo limits.
6. Validate hands and all power rails separately; meter polarity and continuity before connecting any motor.
7. Run the manufacturer bare-base gait under supervision, then re-test after each incremental shell/head/arm addition.
