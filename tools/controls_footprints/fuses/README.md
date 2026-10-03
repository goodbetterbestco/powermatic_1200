# FRN-R-10 fuses in FH1

FRN-R-10 is an Eaton Bussmann fuse supplied by Allfuses. Its existing catalog row
and off-board electrical symbol now reference the new physical assembly footprint
`Controls:FRN-R-10_RM25030-3SR_Front`. The authoritative family drawing in
`_parts/datasheets/FRN-R-10_FRN-R_1019_Archive.pdf` specifies a nominal 2 inch
length and 0.56 inch diameter for the 0–30 A frame: **50.8 × 14.224 mm**.
Manufacturer family source: [Bussmann data sheet 1019](https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/fuses/data-sheets/bus-ele-ds-1019-frn-r-1-10-60a.pdf).
Supplier: [Allfuses FRN-R-10](https://www.allfuses.com/frn-r-10).

The generated neutral STEP has its axis along Y and its center at XYZ=0.
`FRN-R-10_RM25030-3SR.step` bakes the centerline height into the geometry, with
zero footprint model offsets/rotations and unity scale. The installed holder is
`RM25030-3SR_DIN35x7p5.step`; paired inner clip-cylinder surfaces have common
Z=30.414015 mm, at local pole centers X=-24.0284945, 0.484112, 24.996719 mm.
The clip cylinder pairs have opposing lateral centers: their midpoint defines
the pole center, rather than either individual spring surface axis.
`clip_axes.json` retains measured face radii, axes and extents.

The user selected **25 mm fuse pitch**, rounding the CAD's 24.512607 mm pitch
up to the closest 1 mm. The middle pole remains centered; the outside fuses
are consequently about 0.487393 mm outward from their clip midpoints.

| Reference | X (mm) | Y (mm) | Rotation |
|---|---:|---:|---:|
| F1 | 104.910003 | 137 | 0° |
| F2 | 129.910003 | 137 | 0° |
| F3 | 154.910003 | 137 | 0° |

F.Fab is an analytic top projection of the modeled body and two end caps.
F.Silkscreen is the simplified full envelope with two cap-boundary lines.
The caps are represented as 12.7 mm long and the central body as 13.6 mm in
diameter. These subdivisions and colors are illustrative; the rejection groove,
labels and internals are omitted. Overall length/diameter are drawing-backed.
The holder CAD depicts unloaded spring clips, so contact-region overlap in this
simplified assembly does not establish physical fit.

The PCB objects have no pads and are board-only, excluded from placement/BOM
exports. FH1 continues to own all electrical connections; the existing purchase
BOM already lists three FRN-R-10 fuses. All existing PCB records, identities,
placements and nets are preserved. The schematic was not edited.

Validation: native KiCad footprint/board load, unique PCB UUIDs, F.Fab/silkscreen
SVG export and visual inspection, valid generated STEP topology/envelope, native
assembly STEP axis measurement, CSV/database equality, unique keys and SQLite
integrity checks. DRC is identical before/after: 297 existing violations and 73
unconnected items. Native export adds the board surface at Z=1.595 mm, giving
fuse centerline Z=32.009015 mm in the exported assembly.

`generate.py` requires cadquery-ocp and takes `--output <asset-root>`.
`place.py` runs with KiCad's bundled Python and refuses duplicate F1–F3 refs.
`verify_step.py <native-export.step>` verifies the actual exported fuse axes.
`placement.json`, `step_validation.json`, `geometry.json`, and previews retain
review evidence. The STEP CLI export includes the board body; KiCad 9.0.7's
`--no-board-body` failed to produce this assembly.
