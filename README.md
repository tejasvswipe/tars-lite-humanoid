# TARS-Lite — biped prototype and stationary baseline

A TARS-inspired robotics project organized into exactly four top-level categories: **`PCB/`, `CAD/`, `Firmware/`, and `Docs/`**. The root README and `.gitignore` remain at repository root.

## Repository structure

- [`PCB/`](PCB/) — KiCad source, PCB notes, Gerber/drill manufacturing files and previews.
- [`CAD/`](CAD/) — editable OpenSCAD models, exported STL meshes and print guides.
- [`Firmware/`](Firmware/) — ESP32-S3/Arduino firmware and Raspberry Pi utilities.
- [`Docs/`](Docs/) — build guides, engineering journals, BOMs, wiring maps and visuals, separated into `Biped/`, `Stationary/` and `Media/`.

Each category has its own README index. Files are grouped by design and function within those four folders.

## Biped / 360° head prototype

- [Integrated build guide](Docs/Biped/COMPLETE_BIPED_BUILD.md)
- [Engineering journal](Docs/Biped/BIPED_ENGINEERING_JOURNAL.md)
- [Walking and 360° BOM](Docs/Biped/WALKING_360_BOM.csv) — estimated **$1,128.53–$1,353.93 with 15% contingency**, before shipping/tax.
- [Wiring map](Docs/Biped/BIPED_WIRING.md)
- [Editable add-on CAD](CAD/Biped/biped_tarslite.scad), [print guide](CAD/Biped/BIPED_PRINT_GUIDE.md), and [STL meshes](CAD/Biped/biped_stl/)
- [Neck-interface KiCad board](PCB/DXL-Neck/TARS-Lite-DXL-Neck.kicad_pcb) and [Gerber/drill ZIP](PCB/DXL-Neck/gerber/TARS-Lite-DXL-Neck-Gerbers.zip)
- [ESP32-S3 head/gripper firmware](Firmware/ESP32-Arduino/esp32_biped_head.ino) and [Raspberry Pi console](Firmware/Raspberry-Pi/head_console.py)

The biped lower body relies on a compatible ROBOTIS MINI/Darwin-Mini reference platform and its stock gait controller; vendor CAD and motion files are linked from the [official e-Manual](https://emanual.robotis.com/docs/en/edu/mini/) and are not redistributed here. The add-on design has not been physically assembled or fit-checked. The hand grippers are for very light objects; this is not a general-purpose human-task robot.

The neck uses one additional XL-320 on a separate data bus with AS5600 absolute heading feedback. The neck PCB is not a leg-bus power board. The ESP32-S3 firmware compiles for the `esp32-s3-devkitc-1` PlatformIO target, but has not been flashed or tested on physical hardware. Full PCB DRC/DFM and walking tests remain outstanding. Review the safety gates in the build guide before fabrication or motion.

## Stationary v0.3 baseline

The original tabletop design has fixed support legs and does **not** walk. Its files are kept separate from the biped package:

- [Stationary engineering journal](Docs/Stationary/ENGINEERING_JOURNAL.md)
- [Stationary BOM](Docs/Stationary/BOM.csv)
- [Stationary wiring](Docs/Stationary/WIRING.md)
- [Stationary CAD/STLs](CAD/Stationary/)
- [ServoBus-6 board specification and Gerbers](PCB/ServoBus-6/)

## Repository

Public GitHub repository: [tejasvswipe/tars-lite-humanoid](https://github.com/tejasvswipe/tars-lite-humanoid).
