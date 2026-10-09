#!/usr/bin/env python3
"""Minimal Raspberry Pi OS Lite serial monitor/logger for TARS-Lite ESP32 telemetry."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
import serial

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--port',default='/dev/ttyACM0',help='ESP32 USB CDC port')
    ap.add_argument('--baud',type=int,default=115200)
    ap.add_argument('--log',default='tarslite-telemetry.log')
    args=ap.parse_args()
    try:
        ser=serial.Serial(args.port,args.baud,timeout=2)
    except serial.SerialException as e:
        print(f'Cannot open {args.port}: {e}',file=sys.stderr); return 2
    path=Path(args.log)
    print(f'Recording ESP32 text telemetry from {args.port} to {path}; Ctrl-C to stop.')
    try:
        with path.open('a',encoding='utf-8') as out:
            while True:
                raw=ser.readline().decode('utf-8','replace').strip()
                if not raw: continue
                stamped=f'{datetime.now(timezone.utc).isoformat()} {raw}'
                print(stamped,flush=True)
                out.write(stamped+'\n'); out.flush()
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    return 0
if __name__=='__main__': raise SystemExit(main())
