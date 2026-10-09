#!/usr/bin/python3
"""Fill the neck PCB copper zones and persist the filled KiCad board.

KiCad 7's Python zone filler is stable here after loading a saved board and
building connectivity first. Run this after generate_board.py and before DRC
or fabrication export.
"""
from pathlib import Path
import pcbnew

board_path = Path(__file__).resolve().parent / "TARS-Lite-DXL-Neck.kicad_pcb"
board = pcbnew.LoadBoard(str(board_path))
if board is None:
    raise SystemExit(f"Could not load {board_path}")
if len(board.Zones()) == 0:
    raise SystemExit("No copper zones found; refusing to export an unfilled board")

board.BuildConnectivity()
filler = pcbnew.ZONE_FILLER(board)
if not filler.Fill(board.Zones(), False, None):
    raise SystemExit("KiCad zone filling failed")
pcbnew.SaveBoard(str(board_path), board)
print(f"Filled {len(board.Zones())} zone(s) and saved {board_path}")
