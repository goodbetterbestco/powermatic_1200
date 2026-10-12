# M1 illustrative motor footprint

`Controls:PWRM1200-MOTOR_Top_150mm` is the owner-requested machine-layout
representation, based on
`depositphotos_650674342-stock-photo-electric-motor-top-view-illustration.jpg`.
The stock illustration supplies appearance only. The motor's actual package,
mounting pattern and junction-box geometry have not been measured from it.

The shaft tip at source X=140 and rear cover at X=1460 define the 150 mm
horizontal dimension. The image-derived height, including the lower foot,
is 106.477273 mm. The motor axis is the footprint's Y=0 datum; the complete
150 mm horizontal extent is centered on X=0. Graphic stroke widths are
additional to these centerline dimensions.

The saved board places M1 at (290, 630) mm, below the enclosure, clear of the
existing S2 and S3 drawings. The shaft points left. Only M1's footprint block
changes; existing tracks and all other footprint blocks are byte-preserved.

| Pad | Local X, Y (mm) | Net |
| --- | --- | --- |
| T1 | -10, -24 | M1_T1 |
| T2 | 0, -24 | M1_T2 |
| T3 | 10, -24 | M1_T3 |
| T4 | -10, -14 | M1_T4 |
| T5 | 0, -14 | M1_T5 |
| T6 | 10, -14 | M1_T6 |

These are six logical wire-routing targets in an illustrative connection
area, not a physical six-screw arrangement. Pads follow the existing Controls
3 mm copper / 2 mm drill representation, with copper/mask on both board faces
and no paste. Detailed graphics are on F.Fab, essential contours on
F.Silkscreen, and the opaque silhouette on F.Adhesive. Only the reference
field is visible. There is no model or courtyard, consistent with the
panel-elevation exception FP-CTRL-011.

The owner requested exactly six terminals. The existing M1.PE symbol pin,
termination, connector and bonding-plan metadata are retained, without adding
a seventh pad. This is a documented exception to FP-CTRL-002's one-pad-per-pin
rule: native schematic parity consequently reports the missing PE pad. The
six new targets are deliberately unrouted. No DRC exclusions are added.

The shared symbol default, non-LCSC catalog footprint association and saved
schematic instance/cache agree with the new footprint. The symbol's pin
geometry, electrical types and project connectivity are unchanged. The
managed databases are rebuilt from their CSV sources.

`manifest.json` records source identity, scale and target positions.
`validation.json` records native loading, netlist parity, bounded edits,
database checks and DRC comparison. `motor-detail.png` is a native KiCad
export of the saved footprint. The open PCB/schematic editor must reload the
saved files to show these external changes.
