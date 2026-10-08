#!/usr/bin/env python3
"""Generate TARS-Lite ServoBus-6 single-sided prototype Gerbers (mm).
Passive interface only; inspect/DRC independently before fabrication.
"""
from pathlib import Path
import zipfile
OUT=Path(__file__).parent/'gerber'; OUT.mkdir(exist_ok=True)
# Board 100 x 55 mm. Pads tuples: x,y,copper_diameter,drill_diameter,net,ref.
pads=[]; routes=[]; npth=[]
# 2-pin external regulated servo-power terminal, 5.08 mm pitch.
pads += [(5,10,3.0,1.3,'+5V','J_PWR'),(10.08,10,3.0,1.3,'GND','J_PWR')]
# Two I2C ports: MCU and one sensor bus port (use short Y lead for second sensor).
# Both ports: 3V3, GND, SDA, SCL; 2.54 mm pitch.
for ref,y in [('J_CPU',10),('J_I2C',20)]:
    for i,(net,x) in enumerate(zip(['3V3','GND','SDA','SCL'],[20,22.54,25.08,27.62])):
        pads.append((x,y,1.8,0.9,net,ref))
# Six individual PWM input pads align with servo signal pads.
for i in range(6):
    x=44+i*8
    pads.append((x,10,1.8,0.9,f'PWM{i+1}',f'JPWM{i+1}'))
# Six 3-pin servo output headers: GND / +5V / Signal.
for i in range(6):
    x=44+i*8
    for y,net in [(31,'GND'),(38,'+5V'),(45,f'PWM{i+1}')]:
        pads.append((x,y,1.8,0.9,net,f'J{i+1}'))
# Mounting holes: NPTH, 3.2 mm.
npth=[(4,4,3.2),(96,4,3.2),(4,51,3.2),(96,51,3.2)]
# Power bus routing. Connect input at x=5 to the +5 rail and GND x=10 to GND rail.
routes += [((5,10),(5,38),2.0,'+5V'),((5,38),(88,38),2.0,'+5V')]
routes += [((10.08,10),(10.08,31),2.0,'GND'),((10.08,31),(88,31),2.0,'GND')]
# I2C ports parallel bus. Branch input ports to the MCU header; 3V3/GND shared.
# Route the four aligned pin columns directly between ports; power ground then taps the ground column.
for x,net in zip([20,22.54,25.08,27.62],['3V3','GND','SDA','SCL']):
    routes.append(((x,10),(x,20),0.65,net))
# MCU ground into servo ground bus; separate from the 3.3V logic pin.
routes += [((22.54,10),(22.54,31),1.0,'GND')]
# Power feed to servo output pads and six PWM signal paths.
for i in range(6):
    x=44+i*8
    routes += [((x,10),(x,45),0.65,f'PWM{i+1}')]
    routes += [((x,31),(x,31),0.01,'GND'),((x,38),(x,38),0.01,'+5V')]
# Through hole pad diameters: 3.0 mm (terminal), 1.8 mm (headers).

def xy(x,y): return f"X{round(x*1_000_000):010d}Y{round(y*1_000_000):010d}"
def head(): return '%FSLAX46Y46*%\n%MOMM*%\n%LPD*%\n'
def apertures():
    return '%ADD10C,3.000*%\n%ADD11C,1.800*%\n%ADD12C,2.000*%\n%ADD13C,1.000*%\n%ADD14C,0.650*%\n%ADD15C,0.010*%\n'
def copper(bottom=False):
    s=head()+apertures()
    # Establish the finite set of pad apertures once.
    for dcode,dia in [(20,3.0),(21,1.8)]: s+=f'%ADD{dcode}C,{dia:.3f}*%\n'
    for x,y,d,dr,net,ref in pads:
        s+=f'D{20 if d>=2.5 else 21}*\n'+xy(x,y)+'D03*\n'
    for (a,b,w,net) in routes:
        # PWM paths cross shared +5V/GND buses; route them on the opposite copper layer.
        if (net.startswith('PWM')) != bottom: continue
        d={2.0:12,1.0:13,0.65:14,0.01:15}[w]
        s+=f'D{d}*\n'+xy(*a)+'D02*\n'+xy(*b)+'D01*\n'
    return s+'M02*\n'
def mask():
    s=head()+'%ADD20C,3.200*%\n%ADD21C,2.000*%\n%ADD22C,3.400*%\n'
    for x,y,d,dr,net,ref in pads:
        s+=f'D{20 if d>=2.5 else 21}*\n'+xy(x,y)+'D03*\n'
    for x,y,d in npth: s+='D22*\n'+xy(x,y)+'D03*\n'
    return s+'M02*\n'
def outline():
    pts=[(0,0),(100,0),(100,55),(0,55),(0,0)]
    s=head()+'%ADD10C,0.100*%\nD10*\n'+xy(*pts[0])+'D02*\n'
    for p in pts[1:]: s+=xy(*p)+'D01*\n'
    return s+'M02*\n'
def drill(plated=True):
    selected=[p for p in pads if p[3] > 0] if plated else []
    holes=selected if plated else [(x,y,0,d,'NPTH','H') for x,y,d in npth]
    # Only two drill diameters per plated set: terminals 1.3 and connectors 0.9.
    s='M48\n; TARS-Lite ServoBus-6; units mm\nMETRIC,TZ\n'
    if plated: s+='T01C1.300\nT02C0.900\n'
    else: s+='T03C3.200\n'
    s+='%\n'
    for p in holes:
        x,y=p[0],p[1]
        if plated: tool='T01' if p[3]>=1.2 else 'T02'
        else: tool='T03'
        s+=tool+'\n'+xy(x,y)+'\n'
    return s+'M30\n'
files={'TARS-Lite-ServoBus-6.GTL':copper(False),'TARS-Lite-ServoBus-6.GBL':copper(True),'TARS-Lite-ServoBus-6.GTS':mask(),'TARS-Lite-ServoBus-6.GBS':mask(),'TARS-Lite-ServoBus-6.GTO':head()+'%ADD10C,0.150*%\nD10*\nG04 Connector legends intentionally omitted; use BOARD_SPEC.md pin map*\nM02*\n','TARS-Lite-ServoBus-6.GKO':outline()}
for name,text in files.items(): (OUT/name).write_text(text)
(OUT/'TARS-Lite-ServoBus-6-PTH.DRL').write_text(drill(True))
(OUT/'TARS-Lite-ServoBus-6-NPTH.DRL').write_text(drill(False))
(OUT/'README.txt').write_text('TARS-Lite ServoBus-6 prototype files. Units mm; GTL top copper; GBL bottom copper; GTS/GBS top/bottom solder mask; GTO blank silkscreen; GKO outline; PTH.DRL and NPTH.DRL separated. Board 100 x 55 mm, 2-layer 1 oz assumed. Power rails on top, PWM routes on bottom to avoid shorts at bus crossings. Includes two 4-pin I2C headers (MCU and sensor bus), six PWM input pads and six servo output headers. The I2C sensor port is one shared bus: daisy-chain or use a short Y harness for ToF + IMU. No power regulation, fuse, reverse protection, or active driver. Prototype only; inspect in a Gerber viewer and verify manufacturer DRC/current limits before order.\n')
with zipfile.ZipFile(OUT/'TARS-Lite-ServoBus-6-Gerbers.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in files:z.write(OUT/name,name)
    for name in ['TARS-Lite-ServoBus-6-PTH.DRL','TARS-Lite-ServoBus-6-NPTH.DRL']:z.write(OUT/name,name)
print('Generated fabrication pack:',OUT/'TARS-Lite-ServoBus-6-Gerbers.zip')
