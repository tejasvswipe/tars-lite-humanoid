#!/usr/bin/python3
"""Generate the editable KiCad DYNAMIXEL neck interface PCB (KiCad 7 API).
Logic-only 3.3V UART translator plus fused power branch for ONE XL-320 neck servo.
This does not carry the biped's 16-joint power bus.
"""
from pathlib import Path
import pcbnew

ROOT = Path(__file__).resolve().parent
OUT = ROOT
MM = pcbnew.FromMM
V = pcbnew.VECTOR2I
board = pcbnew.BOARD()
board.SetTitleBlock(pcbnew.TITLE_BLOCK())
board.GetTitleBlock().SetTitle("TARS-Lite DXL Neck Interface — 1x XL-320")
board.GetTitleBlock().SetRevision("1.0")
board.GetTitleBlock().SetComment(0, "Separate data bus; fused single-servo power branch")

NETS = {}
for name in ["GND", "+5V_LOGIC", "ESP_TX", "ESP_RX", "DXL_DIR", "DXL_DIR_N", "TX_STAGE", "DXL_DATA", "VBAT_2S", "V_SERVO"]:
    n = pcbnew.NETINFO_ITEM(board, name)
    board.Add(n)
    NETS[name] = n

def fp(lib, name, ref, val, x, y, rot=0):
    path = Path("/usr/share/kicad/footprints") / (lib + ".pretty")
    obj = pcbnew.FootprintLoad(str(path), name)
    if not obj:
        raise RuntimeError(f"Footprint not found: {path}/{name}")
    obj.SetReference(ref); obj.SetValue(val)
    obj.SetPosition(V(MM(x), MM(y)))
    obj.SetOrientationDegrees(rot)
    board.Add(obj)
    return obj

def pads(obj):
    return {p.GetNumber(): p for p in obj.Pads()}

def net(obj, nums, name):
    for num in nums:
        pads(obj)[str(num)].SetNet(NETS[name])

def xy(pad):
    p = pad.GetPosition()
    return (pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))

def track(a, b, name, width=0.45, layer=pcbnew.F_Cu):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(V(MM(a[0]), MM(a[1]))); t.SetEnd(V(MM(b[0]), MM(b[1])))
    t.SetWidth(MM(width)); t.SetLayer(layer); t.SetNet(NETS[name])
    board.Add(t)

def route(points, name, width=0.45, layer=pcbnew.F_Cu):
    for a, b in zip(points, points[1:]):
        if abs(a[0]-b[0])+abs(a[1]-b[1]) > 0.001:
            track(a,b,name,width,layer)

def pin(obj, n): return xy(pads(obj)[str(n)])

# Footprints (all real KiCad standard-library parts; through-hole logic parts are hand-solderable).
J1 = fp("Connector_PinHeader_2.54mm", "PinHeader_1x05_P2.54mm_Vertical", "J1", "ESP32: 5V/GND/TX/RX/DIR", 8, 9)
U1 = fp("Package_DIP", "DIP-14_W7.62mm_Socket", "U1", "74HCT125N", 29, 9)
U2 = fp("Package_DIP", "DIP-14_W7.62mm_Socket", "U2", "74HCT14N", 49, 9)
J2 = fp("Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical", "J2", "XL-320: GND/VDD/DATA", 76, 9)
J3 = fp("TerminalBlock", "TerminalBlock_bornier-2_P5.08mm", "J3", "2S AUX POWER IN", 75, 43)
R1 = fp("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", "R1", "220R", 48, 31)
R2 = fp("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", "R2", "10k", 25, 40)
R3 = fp("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", "R3", "20k", 25, 47)
R4 = fp("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal", "R4", "10k", 13, 30)
C1 = fp("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "C1", "100nF", 40, 40)
C2 = fp("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "C2", "100nF", 60, 47)
F1 = fp("Fuse", "Fuse_1812_4532Metric", "F1", "PTC 2A HOLD", 64, 42)

# Connector, IC, resistor, fuse and decoupling nets.
net(J1,[1],"+5V_LOGIC"); net(J1,[2],"GND"); net(J1,[3],"ESP_TX"); net(J1,[4],"ESP_RX"); net(J1,[5],"DXL_DIR")
net(U1,[1],"DXL_DIR_N"); net(U1,[2],"ESP_TX"); net(U1,[3],"TX_STAGE"); net(U1,[14],"+5V_LOGIC"); net(U1,[7],"GND")
net(U1,[4,10,13],"+5V_LOGIC") # disable unused buffer channels
net(U1,[5,9,12],"GND")       # unused data inputs are not left floating
net(U2,[1],"DXL_DIR"); net(U2,[2],"DXL_DIR_N"); net(U2,[14],"+5V_LOGIC"); net(U2,[7],"GND")
net(U2,[3,5,9,11,13],"GND")  # unused inverter inputs tied low
net(J2,[1],"GND"); net(J2,[2],"V_SERVO"); net(J2,[3],"DXL_DATA")
net(J3,[1],"VBAT_2S"); net(J3,[2],"GND")
net(R1,[1],"TX_STAGE"); net(R1,[2],"DXL_DATA")
net(R2,[1],"DXL_DATA"); net(R2,[2],"ESP_RX")
net(R3,[1],"ESP_RX"); net(R3,[2],"GND")
net(R4,[1],"DXL_DIR"); net(R4,[2],"GND")
net(C1,[1],"+5V_LOGIC"); net(C1,[2],"GND")
net(C2,[1],"+5V_LOGIC"); net(C2,[2],"GND")
net(F1,[1],"VBAT_2S"); net(F1,[2],"V_SERVO")

# 5V logic rail, separate from 2S servo rail.
route([pin(J1,1),(12,9),(12,4),(37,4),(37,9),pin(U1,14)], "+5V_LOGIC", 0.55)
route([(37,4),(60,4),(60,7),(56.62,7),pin(U2,14)], "+5V_LOGIC", 0.55)
# Tie unused active-low buffer enables high; extend the 5V spine to decouplers.
route([pin(U1,4),(34.5,16.62),(34.5,4),(37,4)], "+5V_LOGIC", 0.45)
route([pin(U1,13),(39,11.54),(39,4)], "+5V_LOGIC", 0.45)
route([pin(U1,10),(39,19.16),(39,11.54)], "+5V_LOGIC", 0.45)
route([pin(C1,1),(39,40),(39,19.16)], "+5V_LOGIC", 0.45)
route([pin(C2,1),(pin(C2,1)[0],40),(84,40),(84,7),(56.62,7),pin(U2,14)], "+5V_LOGIC", 0.45, pcbnew.B_Cu)
# ESP32 UART TX to buffer input.
route([pin(J1,3),(13,14.08),(24,14.08),pin(U1,2)], "ESP_TX", 0.35)
# DXL direction is active-high at the ESP32; 74HCT14 inverts it to active-low /OE.
route([pin(J1,5),(8,50),(42.5,50),(42.5,8),(49,8),pin(U2,1)], "DXL_DIR", 0.35)
# Safe default direction: 10k pulldown; resistor end connects to the same DIR node.
route([pin(J1,5),(11,18),(11,30),pin(R4,1)], "DXL_DIR", 0.35)
# Direction inverter output to buffer /OE on the opposite copper layer.
route([pin(U2,2),(45,pin(U2,2)[1]),(45,5),(29,5),pin(U1,1)], "DXL_DIR_N", 0.4, pcbnew.B_Cu)
# Buffer output → series resistor → DXL bus DATA. Keep this run on B.Cu so it
# does not cross the +5V tie trace for U1's unused /OE pins.
route([pin(U1,3),(26,14.08),(26,32),(48,32),pin(R1,1)], "TX_STAGE", 0.35, pcbnew.B_Cu)
route([pin(R1,2),(61,31),(73,31),(73,14.08),pin(J2,3)], "DXL_DATA", 0.6)
# 10k/20k receive divider reduces the 5V DXL line to about 3.3V at ESP32 RX.
route([pin(J2,3),(79,14.08),(79,34),(pin(R2,1)[0],34),pin(R2,1)], "DXL_DATA", 0.35, pcbnew.B_Cu)
route([pin(R2,2),(pin(R2,2)[0],43),(5.5,43),(5.5,16.62),pin(J1,4)], "ESP_RX", 0.35, pcbnew.B_Cu)
route([pin(R2,2),(pin(R2,2)[0],43),(22,43),(22,47),pin(R3,1)], "ESP_RX", 0.35)
# Fused, single-servo 2S branch. The fuse is not for the 16-joint leg bus.
route([pin(J3,1),(75,51),(54,51),(54,42),pin(F1,1)], "VBAT_2S", 2.0)
route([pin(F1,2),(68,38),(82,38),(82,pin(J2,2)[1]),pin(J2,2)], "V_SERVO", 2.0)

# B.Cu ground plane joins logic ground and servo return at the connector; all GND THT pads attach.
zone = pcbnew.ZONE(board)
zone.SetLayer(pcbnew.B_Cu); zone.SetNet(NETS["GND"])
zone.SetLocalClearance(MM(0.25)); zone.SetThermalReliefGap(MM(0.30)); zone.SetThermalReliefSpokeWidth(MM(0.30))
zone.Outline().NewOutline()
for x,y in [(2,2),(83,2),(83,53),(2,53)]: zone.Outline().Append(MM(x),MM(y))
board.Add(zone)

# Board outline and mounting holes.
outline = pcbnew.PCB_SHAPE(board); outline.SetShape(pcbnew.SHAPE_T_RECT)
outline.SetStart(V(MM(0),MM(0))); outline.SetEnd(V(MM(85),MM(55))); outline.SetLayer(pcbnew.Edge_Cuts); outline.SetWidth(MM(0.05)); board.Add(outline)
for x,y in [(4,4),(81,4),(4,51),(81,51)]:
    h = pcbnew.PCB_SHAPE(board); h.SetShape(pcbnew.SHAPE_T_CIRCLE); h.SetCenter(V(MM(x),MM(y))); h.SetEnd(V(MM(x+1.6),MM(y))); h.SetLayer(pcbnew.Edge_Cuts); h.SetWidth(MM(0.05)); board.Add(h)

def text(txt,x,y,size=1.0):
    t=pcbnew.PCB_TEXT(board); t.SetText(txt); t.SetPosition(V(MM(x),MM(y))); t.SetLayer(pcbnew.F_SilkS); t.SetTextSize(V(MM(size),MM(size))); t.SetTextThickness(MM(0.15)); board.Add(t)
text("TARS-LITE DXL NECK",3,2.5,1.2)
text("J1: +5 G TX RX DIR",3,22,0.9)
text("J2: GND 7V DATA",68,4,0.8)
text("FUSED 1 SERVO ONLY",51,51,0.8)

board_path = OUT / "TARS-Lite-DXL-Neck.kicad_pcb"
pcbnew.SaveBoard(str(board_path), board)
print(board_path)
print(f"Footprints: {len(board.GetFootprints())}, tracks: {len(board.GetTracks())}, zones: {len(board.Zones())}")
