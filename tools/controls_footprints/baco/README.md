# BACO 222102 left-wall view

SW1 uses `Controls:222102_LeftWall`, a side-wall footprint in the standard Controls library for
the BACO 222102 / manufacturer reference 0172001. The complete handle and
switch body are included in one footprint and one STEP assembly. The handle
points left, outside the enclosure; the body extends right, inside.

The untouched manufacturer model is
`_parts/3dmodels/Controls/222102.step`. The original STEP/IGES ZIP and source
records are also retained in `_parts/reviews`. Its source is BACO's exact-part
[0172001 CAD archive](https://assets.legrand.com/webf/baco/0172001.zip).

## Datums and orientation

The footprint origin is the operating-shaft center on the **outside wall face**.
The inside wall face is X=+1.8796 mm, matching the measured enclosure steel.
Both wall faces are dashed reference lines on `Dwgs.User`; the component STEP
does not include an enclosure wall solid.

The manufacturer assembly has no panel gap. The wall-spaced model
`${PARTS_LIB}/3dmodels/Controls/222102_LeftWall_1p8796mm.step` moves only the
yellow handle base, red knob and captive handle screw outward by 1.8796 mm.
All shapes retain their scale, product names and colors. The switch internals,
shaft and mounting hardware retain their original geometry. This is an
assembly-spacing adjustment for layout, not a new switch or shaft design.

The source switch seating plane is Z=49.95 mm. After opening the panel gap,
the handle seating plane is Z=51.8296 mm. Source +Z points toward the handle,
source +Y is up, and source +X points toward the viewer in the side view.
The footprint projection is X=51.8296-source_Z, Y=-source_Y. KiCad's model
settings are offset (51.8296, 0, 33), rotation (0, 90, 0), scale (1, 1, 1).

The model's rear-most envelope is Z=0 relative to the footprint; its shaft
is Z=33 mm. This avoids embedding the component in the layout plane. The
final shaft depth above the backplate is still a placement choice. SW1's
existing staging-board XY position is preserved, not interpreted as a final
wall position. The intended shaft height remains 120 mm below the enclosure top.

## Geometry and wiring targets

Visible edges are projected from the adjusted STEP onto `Dwgs.User`, without
mirroring or scaling. The complete side envelope is **89.9896 × 75.15 mm**.
The handle extends 32.95 mm outside the wall; the switch extends 55.16 mm
past the inside wall. The catalog gives 33, 55 and 75.4 mm respectively;
the model geometry is retained, with these small differences recorded in
`geometry.json`. The handle face is 66 mm in both sources.

Six pads match the symbol terminals: line 1/3/5 above, load 2/4/6 below.
The three front-access screw centers in each bank overlap in this view.
Their wiring targets form an equilateral triangle, radius 6 mm, centered on
the true projected screw position. There are no leaders. The 3 mm pads and
2 mm holes represent the agreed 14 AWG wiring targets, not mounting or PCB
drilling instructions. Pads retain the original SW1 nets and UUIDs.

The reference is the only visible footprint text: 2.5 × 2.5 mm, horizontally
centered on the drawing, in its upper half. Native text-envelope checks found
no graphic overlap at the selected position.

## Rebuild and verification

Run in this order:

1. `build.py` with Python and cadquery-ocp/OCP 8: creates the adjusted model,
   projected footprint and geometry record. It preserves the original STEP.
2. `validate_native.py` with KiCad 9's Python: places the reference label,
   checks six pads and model association, and exports a scratch-board SVG,
   STEP and two native 3D renders to `/tmp/baco-leftwall`.
3. `verify_geometry.py` with OCP: compares all 80 model-solid bounding boxes
   from KiCad's STEP export against an independent rigid transformation.
   The scratch board is excluded and its common model-height offset removed.
4. `install.py` with Python: updates only SW1's schematic footprint field
   and PCB footprint geometry/metadata, checking other top-level objects are
   byte-identical. Backups go to `/tmp/baco-leftwall/before-install`.

The native SVG and both 3D renders were visually inspected. All 80 solids
survive the assembly adjustment and native export. The original source hash
is unchanged; `alignment_validation.json` records numerical alignment error.
This validates the component view and linkage. Final enclosure placement,
clearances and drilling are separate layout work.

The shared catalog and Controls symbol both use `Controls:222102_LeftWall`.
The footprint and adjusted assembly model are stored in `_parts`, using
`${PARTS_LIB}` paths. The wall thickness remains explicit in the model filename
and footprint description.
