// TARS-Lite v0.1 — parametric stationary desktop humanoid
// Units: mm. Render the selected part by setting `part` below.
// Fit-test all servo pockets against the exact purchased units before printing.
part = "assembly"; // assembly, head, face, torso, upper_arm, forearm, gripper, leg, foot
$fn = 48;
servo_w = 23.2; servo_h = 12.6; servo_d = 29.0; clearance = 0.6;
wall = 2.4; screw_d = 3.2;

module rounded_box(size=[40,30,20], r=3) {
  hull() for (x=[r,size[0]-r], y=[r,size[1]-r], z=[r,size[2]-r])
    translate([x,y,z]) sphere(r=r);
}
module servo_pocket() {
  // Open-ended pocket; add the real servo's mounting ears only after measuring.
  cube([servo_w+clearance, servo_h+clearance, servo_d+2], center=true);
}
module head() {
  difference() {
    rounded_box([74,62,56],5);
    translate([wall,wall,wall]) cube([74-2*wall,62-2*wall,56-2*wall]);
    // Face aperture on front (negative Y)
    translate([37,-1,29]) cube([59,wall+2,39],center=true);
    // Rear service opening
    translate([37,62-wall,29]) cube([44,wall+2,32],center=true);
  }
}
module face() {
  difference() {
    cube([58,2.4,38],center=true);
    for (x=[-15,15]) translate([x,0,4]) rotate([90,0,0]) cylinder(d=12,h=8,center=true);
    // Front range sensor window; size must be adapted to the purchased ToF module.
    translate([0,0,-10]) cube([16,8,10],center=true);
    for (x=[-23,23]) translate([x,0,-12]) rotate([90,0,0]) cylinder(d=screw_d,h=8,center=true);
  }
}
module torso() {
  difference() {
    rounded_box([96,62,122],6);
    translate([wall,wall,wall]) cube([96-2*wall,62-2*wall,122-2*wall]);
    // Rear electronics door. Pi/ESP board size must be measured before drilling mounts.
    translate([48,62-wall,66]) cube([72,wall+2,75],center=true);
    // Bottom cable/leg passages
    for (x=[24,72]) translate([x,31,-1]) cylinder(d=15,h=8);
    // Head neck and arm cable passages
    translate([48,31,114]) cylinder(d=20,h=18);
    for (x=[-1,97]) translate([x,31,89]) rotate([0,90,0]) cylinder(d=12,h=12);
  }
}
module upper_arm() {
  difference() {
    rounded_box([35,34,92],5);
    // Side-open pocket for insertion/removal of the servo case.
    translate([17.5,32,46]) cube([servo_w+clearance,servo_d+2,servo_h+clearance],center=true);
    for (z=[14,78]) translate([17.5,-1,z]) rotate([90,0,0]) cylinder(d=screw_d,h=40,center=true);
  }
}
module forearm() {
  difference() {
    rounded_box([31,30,78],5);
    // Side-open pocket; remeasure clearance and horn exit on the actual servo.
    translate([15.5,30,39]) cube([servo_w+clearance,servo_d+2,servo_h+clearance],center=true);
    translate([15.5,15,76]) cylinder(d=14,h=12,center=true);
  }
}
module gripper() {
  // Simple palm plus two passive hinged fingers; a single servo and linkage can close them.
  difference() {
    rounded_box([38,30,24],4);
    translate([19,15,1]) cube([24,18,5]);
    for (x=[8,30]) translate([x,15,12]) rotate([90,0,0]) cylinder(d=3.2,h=36,center=true);
  }
}
module leg() {
  // Fixed support shell only; never treat as a powered or weight-rated leg.
  difference() {
    hull() {
      translate([0,0,0]) cylinder(d=33,h=82);
      translate([4,0,0]) cylinder(d=29,h=82);
    }
    translate([2,0,2]) cylinder(d=22,h=80);
    translate([2,0,41]) rotate([90,0,0]) cylinder(d=screw_d,h=40,center=true);
  }
}
module foot() {
  difference() {
    rounded_box([64,42,12],4);
    for (x=[14,50]) for (y=[8,34]) translate([x,y,-1]) cylinder(d=screw_d,h=16);
    translate([32,21,6]) cube([18,14,14],center=true);
  }
}
module assembly() {
  color("#303842") translate([11,0,172]) head();
  color("#d9dfe4") translate([48,-1,201]) face();
  color("#4c5965") translate([0,0,48]) torso();
  for (side=[-1,1]) {
    mirror([side<0?1:0,0,0]) {
      color("#596675") translate([97,15,110]) rotate([0,0,-90]) upper_arm();
      color("#6a7784") translate([112,15,23]) rotate([0,0,-90]) forearm();
      color("#252a30") translate([125,-1,-12]) gripper();
      color("#424b54") translate([22,31,0]) leg();
      color("#515b65") translate([-10,10,-12]) foot();
    }
  }
}
if (part=="assembly") assembly();
else if (part=="head") head();
else if (part=="face") face();
else if (part=="torso") torso();
else if (part=="upper_arm") upper_arm();
else if (part=="forearm") forearm();
else if (part=="gripper") gripper();
else if (part=="leg") leg();
else if (part=="foot") foot();
