# Left-wall footprints

SW1 now uses [BACO 222102_LeftWall](../baco/README.md), with an outer-wall/shaft-axis origin and direct panel mounting. The Socomec SW1 details and scripts below are retained as the previous design; do not reinstall them over the BACO. H1 and J1 remain as described here.

Left-wall variants in the standard `${PARTS_LIB}/footprints/Controls.pretty` library for SW1, H1 and J1. Their
operating/mating faces point left in the backplate layout, and their original
manufacturer STEP models receive the same rigid rotation. All model scales are
1:1. The footprints and their referenced models are stored in `_parts`.

| Reference | Footprint | Projected envelope, mm | Wiring targets |
| --- | --- | --- | --- |
| SW1 | 22013003_LeftWall | Body 63.971 × 142.730; see assembly dimensions below | 1/3/5 above and 2/4/6 below; each coincident set uses a 120° fan-out |
| H1 | XB4BVB1_LeftWall | 53.751 × 46.200 | X1/X2 at the actual projected rear screw centers |
| J1 | T4171310004-001_LeftWall | 22.400 × 19.900 | Four rear wire-tail stub centers, with each overlapping pair spread left/right |

The footprint origin is at the horizontal center of the projected model
envelope and at the operating/connector axis vertically. Z=0 is the rearmost
envelope in this new orientation. It is not a wall-seating or mounting datum.
SW1 retains its original body origin when the assembly is added; the whole
assembly is intentionally not re-centered. Final height above the backplate
must be applied during placement. `geometry.json` records source axes, transforms,
actual terminal coordinates and displaced wiring targets.

`layout_basis.json` records the confirmed installation: left wall, disconnect
shaft center 120 mm below the enclosure top, H1 above the handle, J1 center about
80 mm above the bottom (428 mm from the top of the 508 mm enclosure). Existing
working PCB locations are preserved; they are not final enclosure placements.

Socomec instruction `534924I`, arrangement C, lists the selected 148E1111 handle
for front operation. Rotating the whole switch to face the left enclosure wall
uses that arrangement, rather than the switch's separate left-side drive. The
body needs its own panel/bracket mounting; the handle and shaft do not support
it. SW1 now includes the handle, cut shaft and a provisional wall-mounted
bracket in one footprint and one STEP file in the standard Controls model folder.

## SW1 assembly

`assembly/build.py` combines the original 22013003 and 148E1111 STEP geometry,
with a shortened 14070532 shaft that retains its factory cross pin. No model is
scaled. The wall reference is two lines on Dwgs.User; it is not a wall solid in
the STEP. The assembly model is at
`${PARTS_LIB}/3dmodels/Controls/22013003_LeftWall_Assembly.step`.

The handle's seating flange touches the outside wall. Wall thickness is
**1.8796 mm**, measured between parallel faces of the manufacturer's
N412201608C STEP. Socomec 534924I, page 2 arrangement C, gives a minimum
**25 mm** between the front coupling end and inside wall. The nominal
75 mm mounting-base-to-coupling dimension therefore puts the switch rear
mounting plane **100 mm** inside the wall. The corresponding S0/S00 shaft
formula gives **57 mm** (`L = X + 32`). This is a layout cut length; confirm
engagement against the actual assembled hardware before cutting stock.

The bracket is a **provisional 3 mm steel hat-section envelope**, 220 mm high,
80 mm deep, with a 100 mm reach from the inner wall to the switch mounting
plane. Two rear holes follow the switch STEP's 131.3 mm vertical separation
and 26 mm depth offset. Four 6.5 mm wall holes are provisional. Sharp corners
represent the envelope only: bend radii, allowances, reliefs, fastener access,
wall stiffness and wiring clearance still require fabrication review.

The supplied switch STEP does not contain the front-operation coupling. Its
nominal depth is reserved in the assembly spacing, but a made-up coupling
solid is not added. Terminal covers and mounting screws are also absent.
The handle, shaft and body use manufacturer geometry; only the bracket is
a project-designed placeholder. `assembly/dimensions.json` records datums,
source hashes and component bounds.

Socomec also offers a factory steel door/panel support kit, **22993609**.
Its EU declaration COD 24 132772 lists it with 22013003, but the SIRCO M
catalogue specifies **S00 handles only** for the mounting kits. Our 148E1111
is an **S0** handle. The factory kit is therefore a candidate requiring exact
assembly compatibility confirmation, not a substitute already adopted here.
No dimensioned manufacturer drawing of the steel support was found. The
533750G and 534935D instruction sheets cover the different 22993309 and
22993409 kits; they are not drawings for the fabricated bracket in this model.

References for the factory-kit research:
- https://emea.socomec.com/en/reference/22993609
- https://emea.socomec.com/en/p/sirco-m-mounting-kit
- https://apac.socomec.com/sites/default/files/2025-02/SIRCO-M-%26-SIRCO-M-IN-ENCLOSURE_UE-DECLARATION_DECLARATION-OF-CONFORMITY_2025-02_COD-24-132772--SIRCO-M_EN.pdf
- https://emea.socomec.com/sites/default/files/2022-01/SIRCO-M-AND-SIRCO-MV---UNIVERSAL-LOAD-BREAK-SWITCHES-FROM-16-TO-160-A_CATALOGUE---PAGES_2021-08_DCG0024502EN_EN.pdf (page 10)

Your manually adjusted library fields and six pads are preserved. SW1's PCB
fields, nets, pads and placement are also preserved; its drawing and model
are the only updated PCB objects.

Sources: `_parts/datasheets/Socomec_534924.pdf`,
`22013003_CAD_Drawing.pdf`, `XB4BVB1_XB4BVB1.pdf`, and
`T4171310004-001_Drawing.pdf`, plus the corresponding original STEP models.
The Socomec STEP's bare body is 63.971 mm deep, consistent with the drawing's
64 mm body dimension. The 75 mm drawing dimension includes the shaft coupling.
Cover geometry must still be included when checking the final assembly space;
the front coupling's nominal depth is reserved as described above.

Geometry stays on Dwgs.User. The established 3 mm pads / 2 mm holes are panel
wiring targets, not panel drilling instructions. Coincident terminal fan-out
follows FP-CTRL-002 through FP-CTRL-005 without leaders. J1's flexible wire length
is absent from its STEP; its targets identify the modeled wire departure ends.

The original `generate.py` / `validate.py` / `install.py` are the baseline
three-view workflow and overwrite manually adjusted text positions. Do not
rerun them for this assembly update. Instead run `assembly/build.py` with OCP,
`assembly/validate_native.py` with KiCad 9's Python, then
`assembly/install_board.py` with Python. Assembly rebuilding uses the saved
body geometry in `assembly/body.kicad_mod`, while retaining the current
library properties/pads. The original baseline installation changes the three schematic footprint
properties and the corresponding PCB footprints. It preserves pad numbers,
UUIDs, nets, fields and placement, and checks other top-level records unchanged.
Temporary review boards/renders live in `/tmp/powermatic-left-wall`.

Validation: native load, SVG, STEP and render; original pin-set equality and
pad clearance; native STEP terminal-center comparisons. The latter compare true
terminal centers, before the documented fan-out offsets. These checks validate
the footprint views, not a finished enclosure arrangement or drilling template.
