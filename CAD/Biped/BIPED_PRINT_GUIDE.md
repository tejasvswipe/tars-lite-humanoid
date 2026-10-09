# Biped Add-on Print Guide — v1.0

This package supplies TARS-style **add-on shells, a rotating-head support, and simple hand grippers**. For the two-legged gait base, use the manufacturer-provided ROBOTIS MINI/Darwin-Mini frame and stock motion package; those vendor models are intentionally not redistributed here. Download them from the [official e-Manual](https://emanual.robotis.com/docs/en/edu/mini/) (STL and STEP links in its Download section).

## Editable source and parts

`biped_tarslite.scad` is the design source. Its default dimensions are a fit-study starting point, **not verified against your particular kit**. Before the full print, measure the frame, XL-320 horn, 608 bearing, and SG90-style microservo; tune the OpenSCAD parameters and print small fit coupons.

| `part` value / STL | Qty | Use | Fit status |
|---|---:|---|---|
| `torso_shell` | 1 | Lightweight box-shaped TARS cover around the biped torso | Interface slots adjustable; measure kit |
| `torso_back` | 1 | Removable rear service cover for electronics access | Screw pattern provisional |
| `electronics_tray` | 1 | Rear/spinal-side controller shelf | Check clearances, airflow and cable bend radii |
| `neck_base` | 1 | XL-320 cradle, 608-bearing seat and encoder-board mounting points | Servo clamp / host slots require fit coupon |
| `neck_rotor` | 1 | Bearing inner-race shaft and adjustable horn-slot plate | XL-320 horn pattern is intentionally adjustable, not certified |
| `head_shell` | 1 | Lightweight head enclosure with two eye openings | Aim for ≤150 g rotating mass, including face and brackets |
| `faceplate` | 1 | Removable two-eye face plate | Eye LEDs and resistors are separate electrical parts |
| `forearm_shell` | 2 | Lightweight covers over kit arms / wiring | Do not block stock joint travel |
| `gripper_palm` | 2 | Microservo palm with one fixed finger | For very light objects only; validate pinch force |
| `gripper_finger` | 2 | Movable finger; hinge and horn linkage are hardware-specific | Add measured linkage / M3 hinge hardware |

## Print and assembly starting points

- Print a small fit coupon before full parts; use 0.2 mm layers, 3–4 walls and 20–30% infill as initial settings, not a strength guarantee.
- Use PETG or another suitable material for moving brackets; PLA is acceptable for non-load-bearing shells. Printed parts are not safety-rated.
- The neck uses a common 608 bearing (nominal 8 × 22 × 7 mm) to carry head weight; the servo horn should transmit rotation, **not act as the head's structural bearing**.
- `faceplate.stl` prints flat in the XY plane; rotate it 90° at assembly to align it to the head shell's vertical front face, then verify both eye apertures before drilling/final fastening.
- Keep the rotating head mass at or below 150 g as a design target, with its center of mass close to the yaw axis. ROBOTIS lists XL-320 stall torque 0.39 N·m and advises stable motions at or below roughly one-fifth of stall torque; this is only a preliminary screening criterion, not a validated load rating.
- The AS5600 angle sensor is mounted to the stationary neck base; its diametric magnet is attached to the rotor. Set a 1–3 mm sensor/magnet air gap and check alignment through one complete revolution.
- The six-wire slip ring carries only low-current eye LED wires. Never route the leg/neck actuator supply through it.
- Do not drill or modify XL-320 actuator cases. Use a measured horn adapter and strain-relieved bracket.
- Install arm/gripper covers only after stock biped poses have been tested. Keep the feet clear of any new shell or cable.
- First walking trials must use the platform's proven stock gait and a spotter/tether over a padded, unobstructed floor; no operation on stairs, tables, near people, pets or fragile objects.
