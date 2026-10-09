# TARS-Lite — stationary baseline + biped prototype

This repository contains two clearly separated designs:

1. **Stationary v0.3 baseline:** a tabletop TARS-inspired robot with fixed support legs, six 5 V PWM servos, sensor breakout PCB and the original $223 estimated BOM. It does **not** walk.
2. **Biped / 360° head package v1.0:** a complete *prototype design package* using a proven 16-DOF ROBOTIS MINI/Darwin-Mini gait base, custom TARS-style add-ons, a voltage-compatible XL-320 neck, head-angle sensor, grippers, firmware, wiring and a new neck-interface PCB. It is not yet physically fit-checked or gait-tested.

## Biped package (latest)

- [`docs/COMPLETE_BIPED_BUILD.md`](docs/COMPLETE_BIPED_BUILD.md) — integrated architecture, wiring domains, staged build/acceptance gates, safety and realistic task scope.
- [`docs/BIPED_ENGINEERING_JOURNAL.md`](docs/BIPED_ENGINEERING_JOURNAL.md) — design decisions, compatibility correction, validation snapshot and next gates.
- [`docs/WALKING_360_BOM.csv`](docs/WALKING_360_BOM.csv) — reconciled line-item cost estimate: $981.33–$1,177.33 before contingency; $1,128.53–$1,353.93 with 15% contingency, before shipping/tax.
- [`docs/WALKING_360_UPGRADE_PLAN.md`](docs/WALKING_360_UPGRADE_PLAN.md) — selected platform, compatibility correction, budget and source links.
- [`docs/BIPED_WIRING.md`](docs/BIPED_WIRING.md) — connector/pin and power-domain wiring map.
- [`mechanical/biped_tarslite.scad`](mechanical/biped_tarslite.scad) — editable parametric torso/head/neck/forearm/gripper add-ons.
- [`mechanical/BIPED_PRINT_GUIDE.md`](mechanical/BIPED_PRINT_GUIDE.md) and [`mechanical/biped_stl/`](mechanical/biped_stl/) — print notes and exported STL parts.
- [`electronics/dxl_neck/`](electronics/dxl_neck/) — KiCad PCB source generator, one-servo interface design notes, component BOM and Gerber/Excellon export pack.
- [`firmware/esp32_biped_head.ino`](firmware/esp32_biped_head.ino) — guarded XL-320 head loop, absolute heading, sensor telemetry and two microservo grippers.
- [`pi/head_console.py`](pi/head_console.py) — Raspberry Pi USB command console.

## Critical compatibility correction

The earlier XL-430 neck suggestion is **not compatible with the XL-320 7.4 V actuator rail**. The biped package instead uses one additional XL-320 on a separate data bus and the same voltage class, with an AS5600 absolute angle sensor for continuous heading. Verify stock first: the reference kit and an extra XL-320 were shown backordered/sold out in the research snapshot. The head-interface PCB is for one neck servo only; it is not a walking-leg power distribution board.

The manufacturer lower-body STL/STEP and gait examples are linked from the [official ROBOTIS MINI e-Manual](https://emanual.robotis.com/docs/en/edu/mini/). Vendor models are not redistributed in this repository.

## Original stationary package

- `docs/ENGINEERING_JOURNAL.md` — original stationary design decisions and bring-up plan.
- `docs/BOM.csv` — original stationary prototype BOM.
- `electronics/gerber/` — original ServoBus-6 PWM/sensor board fabrication files (not a DYNAMIXEL leg controller).
- `mechanical/tarslite.scad`, `mechanical/stl/` — original stationary CAD/STLs.
- `firmware/` and `pi/` — original stationary firmware and telemetry logger.
- `media/` — concept and system-architecture visuals.

## Scope and safety

The biped package is a prototype design, not a validated product and not a general household robot. Begin with supervised, stock-platform gaits on a clear, padded floor; hold it on a tether; keep a hardwired actuator-power emergency stop reachable; and retest after every change in mass or center of gravity. The custom software does not implement balance, fall recovery, collision avoidance or autonomous human-level tasks. See the complete build guide before wiring or motion.

## Repository

Published privately at [github.com/tejasvswipe/tars-lite-humanoid](https://github.com/tejasvswipe/tars-lite-humanoid).
