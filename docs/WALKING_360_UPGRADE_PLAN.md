# TARS-Lite: Walking + 360° Neck Upgrade Plan

**Status:** planning proposal only — no revised walking CAD, motion firmware, or walking PCB has been built or validated.  
**Pricing basis:** USD retail references checked 2026-10-08; shipping, tax, and local-price differences excluded.  
**Recommended first complete demo budget:** **about $1,200–$1,600**, with 15% contingency, subject to actuator torque tests and kit availability.

## Executive recommendation

Treat the present TARS-Lite package as the **stationary v0.3 baseline**. Do not try to make its six SG90-class servos, rigid support-leg shells, 5 V servo rail, or PWM breakout walk. Instead, establish bipedal gait on a small purpose-built 16-DOF platform, add a separately tested 360° head module, then adapt the enclosure and lightweight grippers around that proven gait.

A realistic first goal is **slow, supervised walking on a clean, flat floor**, turning, looking around, gesturing, and—only after the gripper is independently tested—moving a very light object. This is not a robot that can do general household or human jobs. Door handles, stairs, lifting, tools, hot/sharp objects, and working near people are expressly out of scope.

## Stages and acceptance gates

### Stage 0 — verify the actuator and safety envelope

1. Set a small-body target and weigh the final assembly on paper before sizing joints. Keep the battery and heavy electronics low in the torso; keep the head and arms light.
2. Bench-test one candidate serial-bus actuator against the intended lever arm. Measure current, temperature, position error, and holding torque over repeated cycles. A stall-torque headline is **not** a continuous-duty rating.
3. Mount the moving hardware in a tethered test stand with a padded catch area. Add a physical, hardwired motor-power emergency stop before trying a gait.
4. If a joint heats, resets, slips, or cannot hold the calculated load with margin, stop and choose a larger actuator or a smaller/lighter body. Do not “solve” an undersized joint by increasing software torque limits.

**Gate:** no free-standing gait until the mass, center of gravity, joint moment arms, actuator temperature/current, foot-contact sensing, and stop procedure have been checked.

### Stage 1 — make the head turn through a full revolution

- Use a **closed-loop position actuator with at least a 0–360° position range**. The ROBOTIS XL430-W250-T listing describes 0–360° position mode and extended multi-turn position mode; the retrieved listing showed $27.50 but was marked sold out. This is a pricing/reference example, not a purchase recommendation until stock is confirmed.
- Support the neck on a bearing/turntable; do not make the servo output shaft carry the whole head as a cantilever.
- Add a 6-wire slip ring ($17.50 retail reference) for low-current head wiring. Keep high-current servo power off the ring. Put the ToF sensor on the torso/front chest for the first version, so only eye/pilot-signal wiring must pass through the rotating joint.
- Limit yaw speed in software, keep a physical clear perimeter, and test loss-of-communications behavior. “360° head” means one complete selectable heading range; it does **not** imply rapid or unrestricted spinning.

**Gate:** complete a full 360° sweep repeatedly without wire winding, brownout, lost position, excessive backlash, or hot slip-ring contacts.

### Stage 2 — prove biped gait using a known small platform

Use the 16-DOF ROBOTIS MINI as a **cost and architecture reference**, or an equivalent currently available platform with documented actuator limits and a working example gait. The retailer listing describes 16 XL-320 smart actuators, an OpenCM9.04C controller, a printable frame, and currently marks the kit backordered at $593.89. Confirm availability and contents before planning around it.

First reproduce the kit's supported standing and walking motions with its intended controller. Then instrument a slow test on a tether/stand. Only after repeatable baseline walking should the project add the heavier TARS torso, new battery, sensor brackets, neck, and hands; every addition changes center of gravity and leg torque.

Do not have two controllers command the same actuator bus at once. Keep the kit controller for baseline validation; when replacing it, implement and bench-test the ESP32-S3 bus interface and gait loop before connecting a full robot.

**Gate:** stand up, stop, walk a few slow steps, and stop again on a level padded surface, without falls, overheating, bus errors, or the physical emergency stop being needed.

### Stage 3 — integrate TARS appearance and light interaction

- **Pi 5 1 GB:** high-level command/logging only for this prototype. Avoid assuming it can run demanding vision/AI workloads.
- **ESP32-S3:** candidate real-time actuator-bus and IMU loop after the selected bus protocol, transceiver, update rate, and watchdog are verified. It is not a certified safety controller.
- **Arduino UNO R4:** face LEDs and button/input events only; keep it out of the balance-control and emergency-stop chain.
- Maintain an independent, hardwired way to disconnect actuator power. The Pi, ESP32, Arduino, and software must not be the only safety stop.
- Start with the head sweep, torso/foot sensor telemetry, point/gesture motions, and a low-force gripper. If object handling is later added, begin with a foam object under 50 g over a padded table; stop on unexpected contact or slip.

**Gate:** repeat demonstrations with the final printed shell and battery fitted; recheck torque/current/temperature and tipping margins after every change in mass or reach.

## Recommended control and hardware architecture

| Subsystem | Planned role | Important constraint |
|---|---|---|
| Raspberry Pi 5 1 GB | Human-issued commands, logs, optional lightweight interface | Not responsible for motor timing or the hard emergency stop |
| ESP32-S3 | Low-level gait/IMU loop and selected serial actuator bus | Requires the right bus transceiver and tested packet/update timing; not a safety-rated controller |
| Arduino UNO R4 | LEDs and local input events | Noncritical interface only; avoid duplicating gait control |
| Smart actuators | Feedback-capable serial bus joints | Select from continuous/duty-cycle and thermal data; distribute power at multiple points as required |
| Battery and DC/DC rails | Separate regulated actuator rail and Pi/logic rail | Size from measured worst-case current; fuse branches; no servo current through MCU or signal PCB |
| Emergency stop | Hardwired actuator-power interruption | Accessible and tested with a spotter before walking |
| Feet/IMU | Foot contact and torso orientation feedback | MPU6050 telemetry alone is not a balance system |

The existing `ServoBus-6` PCB and six PWM servo headers are **not compatible with a daisy-chain serial smart-servo bus**. Do not fabricate that board for walking control. The biped version needs either the reference kit's intended controller/power harness or a new, reviewed serial-bus and power-distribution design after the actuator and current limits are fixed.

## Indicative staged budget

This is a planning estimate, not a purchase quote. The range assumes the previous project's Raspberry Pi 5, ESP32-S3, Arduino, their Pi accessories, and the ToF/IMU/eye parts are bought/reused where applicable; the old micro servos, fixed-leg design, 5 V rail and PWM breakout are not counted as walking hardware.

| Cost item | Low | High | Basis |
|---|---:|---:|---|
| 16-DOF biped reference kit | $593.89 | $593.89 | Retail listing; currently backordered; confirm availability/contents |
| Three-controller + Pi accessories + existing sensors/eyes | $133 | $133 | Reused estimate carried from current BOM: boards, Pi supply/storage/cooler, ToF/IMU, eye/UART items |
| 360° neck motor, 6-wire slip ring, bearing/mount and wiring | $75 | $110 | XL430 price reference $27.50 (listed sold out), Adafruit slip ring $17.50, remaining parts allowance |
| Battery, charger, regulated rails | $80 | $160 | Allowance only; size after measuring actuator peak current; kit contents may change this |
| Hardwired e-stop, fusing and power harness | $35 | $70 | Allowance for prototype-rated components and wiring |
| TARS-style shell, lightweight grippers, fasteners and print material | $100 | $250 | Custom-fit allowance; assumes access to a printer |
| Bus interface and power distribution adaptation | $30 | $70 | Allowance; depends on whether kit controller is retained or ESP32-S3 takes over |
| **Estimated subtotal** | **$1,046.89** | **$1,386.89** | Before contingency/shipping/tax |
| **15% contingency included** | **$1,203.92** | **$1,594.92** | Rounded recommendation: **$1,200–$1,600** |

If the electronics from the previous BOM are already purchased and reusable, they reduce future cash outlay by roughly $133, but do not reduce total project cost. If the 16-DOF kit is unavailable, the custom-actuator route needs a new, torque-sized BOM and may cost materially more. Do not treat the old $223 stationary BOM as a complete biped budget.

## Torque and cost reality check

- FEETECH STS3215 smart servos were listed by a retailer at $24.99 each, 55 g, 7.4 V, with 19.5 kg·cm **stall** torque and position/speed/load/voltage/temperature feedback. This is a useful candidate for bench work or light arms, but the retrieved listing does not give a continuous leg-joint torque rating. Do **not** assume 19.5 kg·cm is safe holding torque for a walking knee/ankle; validate it thermally under the actual leverage or use a higher-rated actuator.
- As a higher-load reference, the ROBOTIS XH430-W350-R listing was $413.89, 3.4 N·m stall torque, and 0.68 N·m estimated rated continuous torque (the vendor says the latter is estimated at 20% of stall). Twelve units would be **$4,966.68 for actuators alone**; the page was marked sold out. This demonstrates why a robust, larger, reliable biped can quickly move into several-thousand-dollar territory. It is not a final actuator selection; joint torque must be calculated from robot mass and geometry.
- A 360° neck is mechanically much easier than biped walking. A small smart servo with absolute position feedback plus a slip ring can handle a lightweight head, but the slip ring must not carry the actuator/battery's high-current rail.

## Scope boundary: “human work”

A small hobby biped can demonstrate coordinated motion; it cannot safely substitute for a person. Initial tasks should be limited to supervised, rehearsed demonstrations: stand, short slow steps, turn, look/point, and perhaps move a very light soft object. No stairs, doors, lifting people, hot/sharp tools, liquids, or unsupervised operation. For practical household utility, a wheeled base with a purpose-built arm is much more achievable and stable; the user's selected priority here is the biped learning/demo path.

## Price and specification references

Prices are US-dollar web listings observed 2026-10-08; sold-out/backordered markers mean they are **references**, not confirmed stock or guaranteed checkout prices.

1. [ROBOTIS MINI, STEAMCUP](https://steamcup.us/products/robotis-mini) — $593.89; 16 XL-320 actuators, OpenCM9.04C controller, printable frame; page marked backordered.
2. [DYNAMIXEL XL430-W250-T, ROBOTIS](https://robotis.us/products/dynamixel-xl430-w250-t) — $27.50 listing; 0–360° and extended multi-turn position modes; 1.4 N·m stall, 0.28 N·m estimated rated continuous; marked sold out.
3. [Miniature 6-wire slip ring, Adafruit](https://www.adafruit.com/product/775) — $17.50; 6 wires, 2 A per circuit, 12 mm diameter, rated up to 300 RPM.
4. [FEETECH STS3215 19.5 kg smart servo, BABSCO](https://shop.babsco.com/feetech-sts3215-19-5kg-smart-servo-c001) — $24.99 listed; 7.4 V and 19.5 kg·cm stall torque; retailer says 55 g.
5. [DYNAMIXEL XH430-W350-R, ROBOTIS](https://robotis.us/products/dynamixel-xh430-w350-r) — $413.89 listing; 3.4 N·m stall, 0.68 N·m estimated continuous; marked sold out.
