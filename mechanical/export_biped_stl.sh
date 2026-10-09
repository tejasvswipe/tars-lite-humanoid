#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p biped_stl
for p in head_shell faceplate neck_base neck_rotor torso_shell torso_back forearm_shell gripper_palm gripper_finger electronics_tray; do
  openscad -o "biped_stl/${p}.stl" -D "part=\"${p}\"" biped_tarslite.scad
 done
printf 'Exported %s STL parts to %s\n' "$(find biped_stl -name '*.stl' | wc -l)" "$(pwd)/biped_stl"
