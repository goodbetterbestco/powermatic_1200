# Furnas 50MA3KLE S2 integration

Status: installed in the shared parts library and the saved Powermatic project.
KiCad was saved and editing paused at the owner's confirmation on 2026-10-08.
The original saved schematic, board and project settings are in `before/`.

Source: `/Users/evanthayer/Desktop/Furnas_50MA3KLE.step`, exported at 13:13 PDT.
The complete source imports as 35 valid solids, with dimensions 52 x 116 x
44.7 mm. Source bounds are X=-96..-44, Y=-58..58, Z=-89.4..-44.7 mm.
Buttons already face +Z. Keep the colored STEP byte-identical and apply model
offset X=70, Y=0, Z=89.4 mm, rotation 0,0,0 and scale 1,1,1. This centers the
station and makes the rear mounting plane Z=0.

`model-preview.png` is a native KiCad 10 render. `native-model-preview.json`
records a native STEP export with all 35 valid solids, dimensions unchanged,
and its base at KiCad's Z=1.595 mm top component plane. The preview board has
no board outline because it is solely an isolated component rendering fixture.

The staged symbol is `Controls:50MA3KLE`, derived from S2's existing geometry
and terminal inventory. Value and MPN become `50MA3KLE`, Manufacturer becomes
`Furnas`, and Footprint becomes `Controls:50MA3KLE_Top`. The obsolete AB
datasheet link is cleared. The old Allen-Bradley library symbol/catalog row
remain available. The new catalog supplier identifier matches the existing
owner BOM: `FURNAS_50MA3KLE`.

The owner confirmed T contacts are NC and B contacts are NO for FWD/REV;
STOP is NC between 5T and 6T, with no 5B or 6B terminals. S2 now uses these physical IDs throughout its symbol, footprint, board pads,
Wire.Sizes and Termination fields. The Old ID column records the completed
migration from the earlier asymmetric L/R convention:

| Function | Old ID | Current physical ID | Saved net |
| --- | --- | --- | --- |
| FWD NC 2 | L1 | 2T | No external connection |
| FWD NC 1 | R2 | 1T | OVERLOAD_OK through installed jumper |
| FWD NO 2 | L2 | 2B | SPEED_SET |
| FWD NO 1 | R1 | 1B | FWD_CMD |
| REV NC 2 | L3 | 4T | No external connection |
| REV NC 1 | R4 | 3T | OVERLOAD_OK through installed jumper |
| REV NO 2 | L4 | 4B | SPEED_SET through required 2B-4B link |
| REV NO 1 | R3 | 3B | REV_CMD |
| STOP NC 2 | L5 | 6T | STOP_RELEASED |
| STOP NC 1 | R5 | 5T | OVERLOAD_OK |

The owner's existing 1T-3T and 3T-5T jumpers can remain with this wiring:
2T and 4T are unused, and the common links do not bypass STOP. A third
2B-4B jumper is required for the saved circuit's common NO feed; its physical
installation is not confirmed. The schematic explicitly joins the NC common
rail to STOP input, with junctions only at 3T and 5T. Other crossings remain
unjoined. This merges only the former isolated NC common bus into OVERLOAD_OK.
The five external conductor nets and their termination fields are unchanged.
4B now explicitly identifies the required 2B-4B jumper rather than claiming
that the historical common link is already installed.
1T/3T Wire.Sizes entries now record the installed NC jumper net accurately.

Installed placement: S2 X=600, Y=120 mm, angle 0, above S3. All 89 original board
footprints and every original top-level board record remain unchanged. All pads are logical panel wiring targets, not a PCB
drilling pattern; this remains a visual-placement artifact.

Baseline native ERC: zero errors and ten existing library-mismatch warnings.
Final native ERC: zero errors and the same ten pre-existing library-mismatch
warnings. Catalog CSV/SQLite parity and integrity passed; source STEP stays
byte-identical. Native pad-to-model alignment preserves all 35 valid solids,
with maximum screw-rim error below 0.000001 mm. Detailed checks are retained
in the adjacent JSON files and native SVG/PNG exports.

Native DRC exited 134 without producing a report, matching the prior project's
checker limitation; DRC is unverified. Live Symbol Editor visual inspection
(SYM-VIS-001) remains pending; the exported S2 view has been inspected. These
checks certify neither fabrication nor physical installation/mechanical fit.
Controls styling now shows S2 on F.Silkscreen, with the physical terminal mapping
in this review table and geometry.json.

Physical numbering and standard review were completed after KiCad was closed.
The library body is centered at (0,0), 15.24 x 38.1 mm, with 2.54 mm pins
at X=-10.16 mm. Its fourteen-row compact stack uses the required 1.27 mm
vertical half-grid. Reference, Value and Part Name fields use the 1.27 mm grid.
The placed symbol center moved from X=67.31 to X=68.58 mm to preserve every
absolute pin/wire connection point. Pin names use the physical endpoint suffix
(FWD_NC_1 at 1T, FWD_NC_2 at 2T, etc.). The model and PCB placement are unchanged.

All 172 connected endpoints retain valid sizing assignments; all 27 wiring
tests pass. Native PCB loading verifies all ten pad nets, functions and types.
Final ERC remains zero errors and ten baseline warnings. The before/after
files, native netlists, current symbol export, full symbol checklist and
preservation checks are in `pin_numbering/`. Legacy L/R wire-schedule names
are translated deliberately by the import tool.

The required live Symbol Editor check remains pending: computer control could
not launch the closed KiCad app, and its launch API is unavailable. Open
Controls:50MA3KLE in KiCad's Symbol Editor for SYM-VIS-001. The native exported
view was inspected independently and is not recorded as satisfying that rule.

Artwork/layer policy was subsequently reviewed against Q1. Current S2/S3
silkscreens and reserved user layers are documented in
`../artwork_layers_2026-10-08/README.md`. Detailed F.Fab and source STEP
remain unchanged.
