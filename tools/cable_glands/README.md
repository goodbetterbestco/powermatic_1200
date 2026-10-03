# Powermatic bottom cable glands

Three Bimed cable glands from the current project BOM are added to Controls and
the non-LCSC catalog, represented by separate schematic connectors and placed
in the enclosure layout. J2 remains the external power plug and M1 the motor.
J5 links the panel nets to the existing S2/S3 speed and direction pendant.

| Ref | Gland | Cable MPN | Cores | Bottom-wall center position |
|---|---|---|---:|---|
| J3 | BNSPDX-23-W | 7081K33 | 4 | 80 mm from left exterior edge |
| J4 | BSPDX-23-W | 7081K7 | 6 | 100 mm from right exterior edge |
| J5 | BSPBX-22-W | 6452T44 | 7 | 50 mm from right exterior edge |

All three gland axes are **75 mm forward of the rear exterior edge**, as
requested, and point out of the bottom wall. Motor/control pitch is 50 mm;
the measured maximum transverse CAD envelopes leave about 16.98 mm between
them. Current backplate artwork/components stop above the gland wire entries.

The source STEP and dimensioned drawing for each part are downloaded from
AutomationDirect, retained unchanged in _parts, and linked in geometry.json:

- https://ftp.automationdirect.com/support/drawings/3d/step/BNSPDX-23-W.STEP
- https://ftp.automationdirect.com/support/drawings/3d/step/BSPDX-23-W.STEP
- https://ftp.automationdirect.com/support/drawings/3d/step/BSPBX-22-W.STEP
- https://cdn.automationdirect.com/static/drawings/BNSPDX-23-W.pdf
- https://cdn.automationdirect.com/static/drawings/BSPDX-23-W.pdf
- https://cdn.automationdirect.com/static/drawings/BSPBX-22-W.pdf

The derived BottomWall models rotate the source 180 degrees about X, seat the
washer rear face at the exterior bottom wall and move only the locknut along
the thread to contact the 1.8796 mm wall's inside face. They preserve all five
source solids, with black polyamide appearance. The axis height is baked into
STEP at Z=48.6604 mm above the footprint datum; offsets/rotations are zero and
scale is one. This variant is specific to the current Hammond EN4SD20208GY /
EP2020 datum and must be recalibrated for another enclosure/backplate datum.

F.Fab is an OCP hidden-line front projection with curved edges sampled to 0.08
mm deflection. The user-finished power gland uses a stepped F.Silkscreen outline
and body seam lines, plus a matching filled F.Adhes silhouette. Motor and
controls glands now use the same treatment, with their own nut, washer, neck
and CAD-derived rounded cap contours. Silk detail lines clear the logical core
pads by 0.15 mm. The F.Adhes fills are layout artwork. `upgrade_artwork.py`
applies this finish after asset generation, preserving all F.Fab, pads and
models. J4/J5 board artwork is synchronized without moving their placements.
The power silhouette is now an exact mirror of its original left half about
X=0, with 22 unique vertices on both layers; its overlapping crossline is
consolidated into one symmetric line. See `power_symmetry_review.json`,
`artwork_review.json` and `footprint-artwork.png` for the saved reviews.
Pads are **logical cable-core wiring targets**, not gland contacts or a hole
pattern. No gland holes are cut into the enclosure CAD or backplate. The source
CAD/drawing is the dimension reference for eventual enclosure hole work.

J3 retains the J2 X/Y/Z/G conductor identities. J4 retains M1 T1-T6
identities. The user-finished J3 is the schematic artwork guide: J4/J5 now
use a 50 mil coordinate grid, 100 mil core pitch, a narrow 100 mil divided
body, zero-length pins, outside pin names, hidden pin numbers and close
reference/value/part-name fields. Net-label wires end at the core centers.
`style_gland_symbols.py` stages this update while preserving pin UUIDs and
net labels; `symbol_artwork_review.json` records unchanged membership of
all 149 saved nets and unchanged native ERC findings. J5 is a seven-core passive interface: 1 +24V_CTRL,
2 +24V_RUN, 3 FWD_CMD, 4 REV_CMD, 5 STOP_CHAIN, 6 LOW_CMD, 7 HIGH_CMD.
These are project wire-core assignments, not manufacturer contact numbering or
wire colors. Internal S2/S3 pendant connections remain internal. Seven control
conductors are required by the saved circuit. Five auto-generated control net
names are replaced by the descriptive command names in schematic and PCB.

Verification preserves every original schematic pin's net membership and every
original PCB record apart from those five net-name strings. ERC remains 76
pre-existing unconnected-pin findings. DRC remains 297 pre-existing violations;
17 added, connected core wiring targets increase unconnected items from 73 to
90. Native STEP axis measurement confirms all
three at 75.0000001 mm from the exported enclosure rear surface.

The authoritative CSV/database rebuild yields 429 LCSC and 64 non-LCSC entries;
CSV/SQLite parity, unique keys and PRAGMA integrity_check pass. Original purchase
BOM gland quantities and packaging remain intact; the controls cable SPN is
updated to 6452T44 per the user correction.

Scripts build into a staging directory and refuse duplicate part/reference
installation. build_assets.py and verify_native.py require OCP; place_board.py
uses KiCad's bundled Python. Intermediate native exports/backups were kept in
/private/tmp/powermatic-glands. Validation reports and the final previews are
saved alongside these scripts. No commits or pushes are made by this workflow.
