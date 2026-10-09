# Print and fit guide

The meshes are ASCII STL files exported from `tarslite.scad`; the editable parametric source remains the design authority. The modeled parts are concept-scale, not fit-validated against purchased hardware. Dimensions and pockets must be checked with actual servos, sensor boards, screws, and controller before printing the full set.

| STL | Print quantity | Use / notes |
|---|---:|---|
| `head.stl` | 1 | Head shell; fit face plate and provide service access for sensor wiring |
| `face.stl` | 1 | Face plate with two eye openings and a provisional ToF window; measure module before use |
| `torso.stl` | 1 | Main body shell; rear electronics access, cable passages |
| `upper_arm.stl` | 2 | Mirror left/right in assembly; revise servo pockets after measurement |
| `forearm.stl` | 2 | Mirror left/right; check articulation range and horn clearance |
| `gripper.stl` | 2 | Simple palm body; separate/linkage fingers still require hinge pins and a suitable linkage |
| `leg.stl` | 2 | Rigid support shells only; not actuated or weight-rated |
| `foot.stl` | 2 | Mirror left/right; stable stance on a level surface |

## Slicer starting points

- Print a small fit coupon first; use 0.2 mm layers, 3-4 walls, 20-30% infill as initial non-certified defaults.
- PLA is adequate for visual fit prototypes; PETG is preferable for parts subject to repeated handling. No material is structural-rated here.
- Orient parts to avoid weak layer direction at joints; add supports only where your slicer shows unsupported overhangs.
- Use metal M3 screws/nuts at articulated joints; do not thread fasteners directly into printed plastic.
- Allow clearance for wire routing, servo horns, and the actual ToF/IMU carrier boards. The model does not include detailed sensor board clips or a validated Pi/ESP32 mounting pattern.
- After printing, check for cracks, delamination, loose joints and pinch points before powering servos. Keep legs fixed and robot supervised.