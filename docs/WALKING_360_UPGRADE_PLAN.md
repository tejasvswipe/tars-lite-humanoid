# TARS-Lite — Walking + 360° Neck Plan

**Status:** Complete editable prototype design package is now in [`COMPLETE_BIPED_BUILD.md`](COMPLETE_BIPED_BUILD.md). It has not been physically assembled, fit-checked, or gait-tested. The stationary v0.3 design remains a separate baseline.

## Selected architecture

- Use the manufacturer-supported 16-DOF ROBOTIS MINI/Darwin-Mini platform and its stock OpenCM controller/motion files for the two-legged gait base. The kit listing was observed at $593.89 and marked backordered; check exact kit contents and availability.
- Keep the ESP32-S3, Raspberry Pi 5 1GB and Arduino UNO R4 Minima for the add-on functions: ESP32 head control/sensors/gripper PWM, Pi command console/logging, Arduino eye LEDs/button events. The reference kit's controller stays responsible for gait; no two controllers drive one DYNAMIXEL bus.
- Use a spare/additional XL-320 for the neck, not the earlier XL-430 proposal. The XL-320 is rated for 6–8.4 V (7.4 V recommended), supports wheel mode/endless turn, and is the same voltage class as the biped kit's joints. Its wheel mode does not track absolute turn count; the separate AS5600 sensor provides 0–360° heading.
- Carry head weight on a 608 bearing. Limit the rotating head to a lightweight target (≤150 g) and keep its center of mass near the axis. Use the slip ring only for low-current eye wires.
- Reuse the existing ServoBus-6 board for two low-current 5 V hand microservos and sensor breakouts. The new `electronics/dxl_neck/` board is only a one-servo logic translator and fused neck branch; it is not the walking-leg power board.

## Current planning budget

See [`WALKING_360_BOM.csv`](WALKING_360_BOM.csv) for quantities, prices, estimates, sources and stock notes. Reconciled estimate: **USD 981.33–1,177.33 before contingency; USD 1,128.53–1,353.93 including 15% contingency**, before shipping/tax. Kit contents may reduce the battery/charger allowance. Availability risk is material because both the reference kit and extra XL-320 were shown backordered/sold out during the research snapshot.

The XL-320 manufacturer page lists 0.39 N·m stall torque at 7.4 V / 1.1 A and advises stable motions at roughly one-fifth of stall torque or less. This is not a validated head payload rating; the actual head mass, bearing friction, wire drag, temperature and current must be tested.

## Build and safety scope

The small robot can demonstrate supervised walking and handling of very light, soft objects. It is not a general household assistant and must not operate near people/pets, use tools, carry hot/sharp/heavy objects, climb stairs, or run unattended. Revalidate the stock gait after each shell, battery, head or arm change because added mass changes balance and joint load.

Follow the staged bench tests, hardwired latching actuator emergency stop, current/polarity checks, tethered gait tests, and mechanical fit gates in [`COMPLETE_BIPED_BUILD.md`](COMPLETE_BIPED_BUILD.md).

## Primary references

- [ROBOTIS MINI e-Manual and official STL/STEP downloads](https://emanual.robotis.com/docs/en/edu/mini/)
- [ROBOTIS XL-320 specifications, wheel mode and communication circuit](https://docs.robotis.com/docs/dxl/model_reference/x_series/xl_series/xl320)
- [ROBOTIS MINI retailer price/stock reference](https://steamcup.us/products/robotis-mini)
- [Adafruit 6-wire slip ring](https://www.adafruit.com/product/775)

Prices were observed on 2026-10-08 and are indicative US-dollar references, not checkout quotes. Recheck exact model, stock, voltage and protocol before purchasing.
