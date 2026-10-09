# DXL Neck Interface — Circuit Netlist Notes

This is the reviewable circuit description corresponding to the editable KiCad PCB. It is a **single neck-actuator channel**, not a walking-bus or multi-servo power board.

```text
ESP32-S3 UART TX ── U1A 74HCT125 (5V, /OE) ── 220Ω ── XL-320 DATA
ESP32-S3 UART RX ◀── 10kΩ ──┬────────────────── XL-320 DATA (5V TTL)
                            └── 20kΩ ── GND
ESP32 DXL_DIR (HIGH=TX) ── U2A 74HCT14 inverter ── U1A /OE (LOW=TX)
                            └── 10kΩ pulldown to GND

ESP32 +5V_LOGIC ── U1/U2 VCC, 100nF decoupling each
2S battery + ── F1 PTC 2A hold ── XL-320 VDD (one servo only)
Battery GND ─────────────────────── XL-320 GND / ESP32 GND
```

## Pin connections

- U1 = 74HCT125N: pin 1 `/OE1` ← U2 pin 2; pin 2 `1A` ← ESP32 TX; pin 3 `1Y` → R1 220 Ω → DXL DATA; pin 7 GND; pin 14 +5V. Pins 4/10/13 (`/OE2..4`) tied high; unused inputs 5/9/12 tied low; outputs 6/8/11 left open.
- U2 = 74HCT14N: pin 1 ← ESP32 DXL_DIR; pin 2 → U1 `/OE1`; pin 7 GND; pin 14 +5V. Unused gate inputs tied low; unused outputs open.
- R4 10 kΩ pulls DXL_DIR low at boot. Since U2 inverts it, U1 output stays disabled (receive state) until the library asserts transmit.
- R2 = 10 kΩ from bus DATA to RX node; R3 = 20 kΩ from RX node to GND. Divider output is nominally 3.3 V when DATA is 5 V.
- F1 is a 2 A-hold resettable fuse in the **single XL-320 branch**. Verify the exact selected component's datasheet/derating and match the battery wire and connector ratings.
- Ground plane is B.Cu. Servo VDD is a separate `V_SERVO` net and is not connected to the logic 5V net.

Check this circuit against the exact XL-320 documentation and the final chosen library/firmware direction-pin semantics. Do not fabricate from the diagram alone: inspect the KiCad board, run DRC, and test the physical board with a current-limited bench supply.
