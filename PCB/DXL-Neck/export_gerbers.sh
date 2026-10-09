#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p gerber
/usr/bin/python3 fill_zones.py
kicad-cli pcb export gerbers --output gerber/ --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts TARS-Lite-DXL-Neck.kicad_pcb
kicad-cli pcb export drill --output gerber/ --excellon-separate-th --generate-map TARS-Lite-DXL-Neck.kicad_pcb
 (cd gerber && rm -f TARS-Lite-DXL-Neck-Gerbers.zip && zip -q -j TARS-Lite-DXL-Neck-Gerbers.zip TARS-Lite-DXL-Neck-F_Cu.gtl TARS-Lite-DXL-Neck-B_Cu.gbl TARS-Lite-DXL-Neck-F_Mask.gts TARS-Lite-DXL-Neck-B_Mask.gbs TARS-Lite-DXL-Neck-F_Silkscreen.gto TARS-Lite-DXL-Neck-B_Silkscreen.gbo TARS-Lite-DXL-Neck-Edge_Cuts.gm1 TARS-Lite-DXL-Neck-PTH.drl TARS-Lite-DXL-Neck-NPTH.drl TARS-Lite-DXL-Neck-PTH-drl_map.pdf TARS-Lite-DXL-Neck-NPTH-drl_map.pdf TARS-Lite-DXL-Neck-job.gbrjob)
echo "Gerber package: $(pwd)/gerber/TARS-Lite-DXL-Neck-Gerbers.zip"
