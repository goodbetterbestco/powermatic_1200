# DIN layout and pin-coordinate audit

The final layout uses 12 shared `_Grid1mm` variants on 71 eligible DIN footprint instances.
All 205 pin pads in those instances and both mounting faces are on exact integer coordinates.
The two rows are packed as assemblies on Y=130 mm and Y=308 mm; their grid-body envelopes
fit the existing 400 mm rails without overlap between independent assemblies.

The original nominal footprints, STEP models and F.Fab detail are retained as hardware
references. The grid variants implement the owner-requested routing representation.
Pin coordinates use upward ceiling rounding. Halfway mounting walls use the outward
integer. Fuse inserts/covers retain mating offsets, and non-DIN components were unchanged.

The final saved PCB contains 96 footprints and 277 numbered pin pads. 86 footprint origins have integer X and Y; ten remain fractional: six fuse/cover mating datums and four wall connectors.
The coordinate workbook includes every pin pad and every footprint origin. The 36
padless footprints are listed on the Origins worksheet; no pin coordinates were invented.

## Grid classification

Coordinates are absolute KiCad board millimetres: X increases right, Y increases down.
The saved grid origin is (0,462) mm. Both axes must match exactly; no numerical tolerance
is applied. Metric candidates are 5, 2.5, 2, 1, 0.5, 0.25, 0.2, 0.125, 0.1, 0.0625,
0.05, 0.025 and 0.01 mm. Inch candidates are 100, 50, 25, 10, 5 and 1 mil.
`None of tested grids` means no match in this finite set; a finer or shifted lattice
may still describe the point. Local footprint coordinates and local grid matches are
also included, so nominal terminal geometry can be distinguished from placement offsets.

## Files

- [Final layout and validation](grid1mm/README.md)
- [Final exported layout](grid1mm/layout.png)
- [Sortable coordinate workbook](../../outputs/01a11f24-8bcc-77e0-af58-1f3d5466a457/pin_coordinates.xlsx)
- [Complete coordinate JSON](coordinates.json)
- [Original source recovery snapshot](before_board.zip)
- [Before-grid PCB and schematic snapshot](grid1mm/before_grid.zip)

## Final grid counts

| Classification | Pins |
|---|---:|
| Metric | 205 |
| None of tested grids | 72 |

## Remaining fractional footprint origins

| Reference | Part | X (mm) | Y (mm) | Reason |
|---|---|---:|---:|---|
| F1 | FRN-R-10 | 84.484112 | 130.000000 | Assembly mating datum |
| F2 | FRN-R-10 | 109.484112 | 130.000000 | Assembly mating datum |
| F3 | FRN-R-10 | 134.484112 | 130.000000 | Assembly mating datum |
| J1 | T4171310004-001 | -25.000000 | 307.500000 | Outside DIN repacking scope |
| J2 | 3PH-4W-PLUG | 57.000000 | 485.241000 | Outside DIN repacking scope |
| J4 | BSPDX-23-W | 385.000000 | 485.241000 | Outside DIN repacking scope |
| J5 | BSPBX-22-W | 435.000000 | 485.241000 | Outside DIN repacking scope |
| REF** | CVR-RH-25030 | 84.500000 | 130.000000 | Assembly mating datum |
| REF** | CVR-RH-25030 | 109.500000 | 130.000000 | Assembly mating datum |
| REF** | CVR-RH-25030 | 134.500000 | 130.000000 | Assembly mating datum |

Source SHA-256: `fbe823d4e8d51115c49e3e389eada75a6284db6dfc230625cb2b023f1e0f2385`.
