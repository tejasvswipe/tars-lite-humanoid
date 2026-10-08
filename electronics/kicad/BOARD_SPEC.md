# ServoBus-6 sensor and servo distribution PCB

**Board:** TARS-Lite ServoBus-6  
**Revision:** 0.2  
**Units:** mm  
**Construction:** 2 copper layers, 1.6 mm FR-4, 1 oz copper assumed, plated through holes, 100 × 55 mm outline.

## Purpose
Passive interface board only. It does not generate/regulate 5 V and has no active motor driver. It distributes externally regulated servo power, six PWM signals, and a shared 3.3 V I2C bus for the VL53L0X-class ToF and MPU6050-class IMU modules.

## Connector map

- `J_PWR` 2-pin terminal: pin 1 = +5 V SERVO, pin 2 = GND.
- `J_CPU` 4-pin header: 3V3, GND, SDA, SCL (ESP32 I2C connection).
- `J_I2C` 4-pin header: 3V3, GND, SDA, SCL (sensor bus). Use a short Y lead/daisy chain to connect both sensors; check module pullups and addresses.
- `JPWM1..6`: individual through-hole PWM input pads aligned by channel with output.
- `J1..J6`, 3-pin servo headers: GND, +5 V, PWM. Confirm connector pin order before plugging in; common color convention is brown/black, red, orange/yellow/white.

## Routing and electrical limitations

- Power rails are routed on top copper; PWM paths are on bottom copper to cross bus rails without electrical shorts.
- Use 3.3 V-compatible servo PWM input, common ground, a regulated external 5 V servo supply, and an inline fuse.
- The six servo supply current may exceed safe limits for a small PCB, connectors, or 1 oz copper under simultaneous stalls. Check actual load, wire gauge and connector ratings; use external higher-current distribution if needed.
- The board provides no reverse-polarity protection, transient/ESD protection, fuse, voltage regulation, or active driver.
- Use 3.3 V-compatible sensor modules. Confirm I2C addresses; modules may carry pull-up resistors in parallel.

## Manufacturing pack
`../gerber/` contains GTL/GBL copper, GTS/GBS solder mask, GTO legend (blank), GKO outline, and separate PTH/NPTH drills. Inspect in a Gerber viewer and run the manufacturer's DRC before ordering. Design generator creates fabrication artwork, but this board has not been manufactured, assembled, or independently electrically validated.