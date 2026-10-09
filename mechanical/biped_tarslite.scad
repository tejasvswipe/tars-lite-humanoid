// TARS-Lite Biped Add-on Pack v1.0 — parametric concept geometry
// Lower-body gait platform: use the official ROBOTIS MINI/Darwin-Mini frame files.
// These add-ons are not fit-validated. Print coupons and measure the purchased hardware.
$fn = 48;
part = "assembly";
// Tunable interface dimensions (mm)
platform_slot_pitch = 30;
head_w = 96; head_d = 72; head_h = 70;
torso_w = 104; torso_d = 68; torso_h = 112;
wall = 2.4;
servo_w = 25; servo_l = 37; servo_h = 28; // XL-320 body envelope + clearance
bearing_od = 22.2; bearing_id = 8.4; bearing_h = 7.3; // common 608 bearing envelope

module rounded_box(x,y,z,r) {
  hull() for (xx=[r,x-r], yy=[r,y-r], zz=[r,z-r])
    translate([xx,yy,zz]) sphere(r=r,$fn=16);
}
module slot2d(len=8,w=3) { hull() { translate([-len/2,0]) circle(d=w); translate([len/2,0]) circle(d=w); } }
module screw_slot(x,y,len=9,w=3.2) { translate([x,y,0]) linear_extrude(height=8) slot2d(len,w); }
module head_shell() {
  difference() {
    rounded_box(head_w,head_d,head_h,7);
    translate([wall,wall,wall]) rounded_box(head_w-2*wall,head_d-2*wall,head_h-2*wall,5);
    // Open lower service access
    translate([-1,-1,-1]) cube([head_w+2,head_d+2,wall+2]);
    // Twin eye apertures through the front (-Y face)
    for (x=[head_w*0.32,head_w*0.68]) translate([x,-1,head_h*0.58]) rotate([-90,0,0]) cylinder(d=15,h=wall+2);
    // Rear cable notch, kept clear of the rotating interface
    translate([head_w*0.38,head_d-wall-1,head_h*0.18]) cube([head_w*0.24,wall+2,10]);
  }
}
module faceplate() {
  difference() {
    linear_extrude(height=2.6) offset(r=5) square([head_w-10,head_h-10]);
    for (x=[(head_w-10)*0.30,(head_w-10)*0.70]) translate([x+5,0,1]) cylinder(d=15,h=4);
    for (x=[8,head_w-18]) for (z=[8,head_h-18]) translate([x,z,1]) cylinder(d=3.2,h=4);
  }
}
module neck_base() {
  // Top plate holds a common 608 bearing; the XL-320 case is clamped below it.
  difference() {
    union() {
      translate([0,0,0]) cube([72,66,6]);
      // Bearing retaining ring, 8.5-mm through bore and 22.2-mm bearing seat
      translate([36,33,6]) difference() { cylinder(d=30,h=4); cylinder(d=bearing_od+0.1,h=5); }
      // Servo side rails form a removable cradle below the deck
      for (x=[13,59]) translate([x-2,15,-servo_h]) cube([4,36,servo_h]);
    }
    translate([36,33,-1]) cylinder(d=bearing_id,h=12);
    translate([36,33,6.5]) cylinder(d=bearing_od,h=bearing_h+0.5);
    // Adjustable 6-mm-grid style mounting slots; adjust pitch after measuring host frame
    for (x=[36-platform_slot_pitch/2,36+platform_slot_pitch/2], y=[33-platform_slot_pitch/2,33+platform_slot_pitch/2])
      translate([x,y,-1]) cylinder(d=3.4,h=9);
    // Clamp holes on both cradle rails; do not drill through the actuator case
    for (x=[11,61], y=[21,45]) translate([x,y,-servo_h/2]) rotate([0,90,0]) cylinder(d=3.2,h=10,center=true);
    // Encoder-board mounting slots near the bearing axis; set 1–3 mm magnet gap
    for (x=[22,50]) translate([x,33,1]) cylinder(d=2.4,h=8);
  }
}
module neck_rotor() {
  // Inner-race shaft plus adjustable horn-slot plate. Confirm horn geometry before use.
  difference() {
    union() {
      cylinder(d=30,h=4);
      translate([0,0,4]) cylinder(d=7.8,h=9);
      translate([0,0,13]) cylinder(d=48,h=4);
      for (a=[0:90:270]) rotate([0,0,a]) translate([22,0,13]) cylinder(d=6,h=4);
    }
    translate([0,0,-1]) cylinder(d=3.2,h=20);
    // Four radial slots for a measured XL-320 horn adapter; dimensions are tunable.
    for (a=[0:90:270]) rotate([0,0,a]) translate([9,0,13]) rotate([0,0,90]) linear_extrude(height=4) slot2d(9,3.2);
    for (a=[0:90:270]) rotate([0,0,a]) translate([22,0,12]) cylinder(d=3.2,h=6);
  }
}
module torso_shell() {
  difference() {
    rounded_box(torso_w,torso_d,torso_h,6);
    translate([wall,wall,wall]) rounded_box(torso_w-2*wall,torso_d-2*wall,torso_h-2*wall,4);
    // Rear electronics access, removable panel supplied separately
    translate([-1,torso_d-wall-0.1,8]) cube([torso_w+2,wall+2,torso_h-16]);
    // Arm cable/shoulder relief cutouts on both sides
    for (x=[-1,torso_w-12]) translate([x,8,torso_h*0.58]) cube([13,torso_d-16,24]);
    // Mount slots for the specific platform's 6-mm-grid adapter (measure first)
    for (x=[12,torso_w-12],z=[16,torso_h-16]) translate([x,torso_d/2,z]) rotate([90,0,0]) cylinder(d=3.4,h=torso_d+2,center=true);
  }
}
module torso_back() {
  difference() {
    cube([torso_w-2*wall,2.4,torso_h-16]);
    for (x=[10,torso_w-2*wall-10],z=[10,torso_h-26]) translate([x,1,z]) rotate([90,0,0]) cylinder(d=3.2,h=5,center=true);
  }
}
module forearm_shell() {
  difference() {
    rounded_box(30,28,72,4);
    translate([wall,wall,wall]) rounded_box(30-2*wall,28-2*wall,72-2*wall,2);
    translate([15,-1,12]) rotate([-90,0,0]) cylinder(d=3.2,h=30);
    translate([15,-1,60]) rotate([-90,0,0]) cylinder(d=3.2,h=30);
    translate([10,7,63]) cube([10,15,12]);
  }
}
module gripper_palm() {
  difference() {
    union() {
      rounded_box(38,28,16,3);
      // Fixed finger
      translate([3,-7,0]) cube([9,35,12]);
      // SG90 cradle for a single closing finger
      translate([17,18,0]) cube([21,10,20]);
    }
    translate([19,19,2]) cube([18,8,18]);
    translate([20,-1,8]) rotate([-90,0,0]) cylinder(d=3,h=30);
    for (x=[5,33]) translate([x,14,-1]) cylinder(d=3.2,h=20);
    // Servo lead exit
    translate([22,24,8]) cube([17,6,12]);
  }
}
module gripper_finger() {
  difference() {
    union() { translate([0,0,0]) cube([8,34,10]); translate([0,27,0]) cube([8,10,10]); }
    translate([4,5,-1]) cylinder(d=3.2,h=12);
    translate([4,31,-1]) cylinder(d=2.0,h=12);
  }
}
module electronics_tray() {
  difference() {
    cube([80,50,3]);
    for (x=[5,75],y=[5,45]) translate([x,y,-1]) cylinder(d=3.2,h=6);
    // Vent slots
    for (x=[20:10:60]) translate([x,18,-1]) cube([3,14,6]);
  }
}
module assembly_preview() {
  translate([2,0,0]) torso_shell();
  translate([(torso_w-head_w)/2, -2, torso_h]) neck_base();
  translate([(torso_w-head_w)/2+36,31,torso_h+23]) neck_rotor();
  translate([(torso_w-head_w)/2+36-head_w/2,-4,torso_h+44]) head_shell();
  translate([torso_w+8,0,0]) forearm_shell();
  translate([torso_w+48,0,0]) gripper_palm();
}
if (part=="head_shell") head_shell();
else if (part=="faceplate") faceplate();
else if (part=="neck_base") neck_base();
else if (part=="neck_rotor") neck_rotor();
else if (part=="torso_shell") torso_shell();
else if (part=="torso_back") torso_back();
else if (part=="forearm_shell") forearm_shell();
else if (part=="gripper_palm") gripper_palm();
else if (part=="gripper_finger") gripper_finger();
else if (part=="electronics_tray") electronics_tray();
else assembly_preview();
