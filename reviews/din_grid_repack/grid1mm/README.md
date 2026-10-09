# Grid-aligned DIN layout

Installed 12 shared `_Grid1mm` elevation variants on 71 placed footprint instances.
All 205 pin pads in those instances lie on exact integer X/Y coordinates.
Their left and right mounting faces are also integer X. The 77 DIN-associated
instances were restacked as assemblies on the existing 130 mm and 308 mm rail
centre lines, keeping both 400 mm rails. Fuse inserts/covers keep their mating
offsets; their noninteger origins exclude them from the grid-variant operation.

The original footprints and STEP model parameters are preserved. F.Fab remains
the nominal hardware reference; the visible grid view and wire-target markers
are a routing representation. This review verifies 2D grid-envelope packing,
not a change in the manufactured hardware dimensions.

Native checks retain all 96 footprint instances, 277 pin pads, 18 track segments
and the four completed routed endpoint pairs. Schematic footprint overrides
were updated in 16 placed symbols; all 63 nets and 186 pin/net memberships are unchanged.

The exported [layout](layout.png) was visually inspected. Per-instance positions,
route adjustments and identity checks are in [packing.json](packing.json).
The [variant manifest](variants.json) records source hashes and pin rounding.
The preceding saved PCB and schematic are recoverable from [before_grid.zip](before_grid.zip).
