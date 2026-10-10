# Integer panel placement and 462 mm backplate

Owner-authorized layout update, 2026-10-09. This PCB is an industrial-controls
alignment and routing view. Whole-millimetre datums take priority for ease of use.
The policy is recorded in the project's WIRING_STANDARD.md.

The backplate outline is 462 x 462 mm, from (0,0) to (462,462). Its existing
notches and mounting holes retain their local shapes, radii and distances from
the nearest edges. Upper corner groups move upward by 0.482 mm; right corner
groups move right by 0.482 mm. Long spans grow accordingly. The native outline
remains closed.

The enclosure remains 508 x 508 mm. Controls:EN4SD20208GY_Open_Front_Grid1mm
centers it on the 462 mm backplate with a 23 mm border. It retains the original
backplate lower-left footprint origin, placed at PCB (0,462). Enclosure corner
datums are (-23,-23), (485,-23), (485,485), (-23,485). The original library
footprint remains available as the nominal 461.518 mm backplate reference.

The new variant translates enclosure graphics by (+0.241,-0.241) mm and the
model by (+0.241,+0.241,0) mm, accounting for KiCad's opposite model/PCB Y axes.
The source STEP is unchanged and unscaled. Native CAD inspection found nine
solids, including the 508 mm housing, hardware and brackets; the backplate view
comes from the KiCad board. The mapped housing bounds agree with the 2D datums.

Wall-device positions:

| Reference | X mm | Y mm |
|---|---:|---:|
| H1 | -23 | 52 |
| SW1 | -23 | 130 |
| H2 | -23 | 207 |
| J1 | -23 | 308 |
| J2 | 57 | 485 |
| J4 | 385 | 485 |
| J5 | 435 | 485 |

All seven origins and all 46 placed wiring targets are now integer global X/Y.
The pad offsets, numbers, nets, dimensions and UUIDs from the previous datum
update are retained. H1/H2 retain their matching 60.05 mm model Z offsets.
The remaining 88 footprints, including fuse-insert/cover mating assemblies,
retain their saved origins and geometry. There are 96 footprints, 277 pads and
zero track segments before and after. Schematic and project settings are retained.

Native footprint/board load, board serialization/reload, whole-mm origin/pad
checks, backplate outline continuity and hole-radius checks pass. The focused
native SVG/PNG shows the frame and the seven wall devices; its extra viewport
outline is review-only. Appearance was inspected from that export.

Applicable checklist: FP-CTRL-001 preserves the hardware model geometry while
adapting the authorized routing view; FP-CTRL-009 retains layer ownership;
FP-CTRL-011 retains the enclosure/device physical projections without adding
courtyards. No electrical symbol body changes or live Symbol Editor review are
claimed. This is not a PCB fabrication footprint/layout review.

`manifest.json` records exact placement and model bounds, `prepare.py` records
the transforms, and `before.zip` restores the pre-update project files.

Final saved-project ERC reports zero violations. The DRC CLI aborts with exit 134 before writing a report, as in prior checks; no DRC pass is claimed. Final native checks and source-preservation results are recorded in validation.json.
