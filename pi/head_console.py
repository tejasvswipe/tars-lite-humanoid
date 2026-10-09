#!/usr/bin/env python3
"""Small interactive Pi console for TARS-Lite biped add-on commands."""
import argparse
import sys
import time

try:
    import serial
except ImportError:
    print("Install dependency: python3 -m pip install pyserial", file=sys.stderr)
    raise SystemExit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", default="/dev/ttyACM0")
    ap.add_argument("--baud", type=int, default=115200)
    args = ap.parse_args()
    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.2, write_timeout=1)
    except serial.SerialException as exc:
        raise SystemExit(f"Cannot open {args.port}: {exc}")
    time.sleep(2.0)  # ESP32 USB CDC reset window
    print("Commands: arm | head 0..359 | left 0..180 | right 0..180 | stop | disarm | quit")
    try:
        while True:
            line = input("tars> ").strip().lower()
            if line in ("quit", "exit"):
                ser.write(b"DISARM\n")
                break
            if line == "arm": out = "ARM"
            elif line == "stop": out = "STOP"
            elif line == "disarm": out = "DISARM"
            elif line.startswith("head "):
                try: angle = int(line.split()[1])
                except (IndexError, ValueError): print("Use: head 0..359"); continue
                if not 0 <= angle < 360: print("Angle must be 0..359 degrees"); continue
                out = f"HEAD {angle}"
            elif line.startswith("left ") or line.startswith("right "):
                pieces = line.split()
                try: angle = int(pieces[1])
                except (IndexError, ValueError): print("Use: left/right 0..180"); continue
                if not 0 <= angle <= 180: print("Gripper command must be 0..180 degrees"); continue
                side = "L" if pieces[0] == "left" else "R"
                out = f"GRIP {side} {angle}"
            else:
                print("Unknown command"); continue
            ser.write((out + "\n").encode("ascii"))
            time.sleep(0.1)
            while ser.in_waiting:
                msg = ser.readline().decode("utf-8", errors="replace").strip()
                if msg: print(msg)
    except (KeyboardInterrupt, EOFError):
        ser.write(b"DISARM\n")
        print("\nDisarmed.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
