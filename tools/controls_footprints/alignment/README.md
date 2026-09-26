# Controls footprint and model alignment

Reviewed 2026-09-25 against the saved Powermatic 1200 schematic. Eight additional
part types have `Controls:<MPN>_Front` footprints with matching symbol pin IDs and
original manufacturer STEP models. The previous three additions remain linked.

| Part | Pads | Elevation width × height, mm | Source comparison |
|---|---:|---|---|
| HMC-9B30-11-DS | 14 | 45 × 75.5 | Drawing dimensions match; all four coil screws are separate pads. |
| HTOR32-6-S | 10 | 45 × 74.55 | 57.9 body plus 16.65 modeled blade extension; drawing rounds extension to 16.7. |
| HMX1-SSVRC-DC | 2 | 37.4 × 39.473 | Supplier lead pose retained; fork centers are 24 mm apart. |
| HMX1-MI | 4 | 21.200 × 83 | Existing approved model projection; outer two terminals lie behind the front plastic. |
| KN-T12GRY-25 | 2 | 5 × 44.2 | Drawing dimensions match; mounted vertically across horizontal DIN rail. |
| FAZ-D4-2-NA-L | 4 | 35.4 × 105 | Drawing dimensions, 17.7 pole pitch and 66 screw-row pitch match. |
| 22013003 | 6 | 78.808 × 142.730 | Manufacturer model envelope retained, including 131.3 mounting pitch as requested. |
| RM25030-3SR | 6 | 74.491 × 80.400 | Approved uncovered DWG outline retained. STEP envelope is 74.751 wide; outer screw centers differ by 0.130 mm. Pads now follow STEP centers. |

Published-dimension references and the original DWG/DXF checks are in
`../config.json` under `parts`, with source drawings in `_parts/datasheets`.
The fuse holder discrepancy is a difference between manufacturer files; neither
file has been scaled to conceal it. No fuse or cover model is added.

## Coordinate convention

Front faces +Z in KiCad's 3D viewer. The footprint origin is centered on the
projected model envelope; Z=0 is the rearmost modeled geometry. This matches the
rear-origin convention used for the earlier additions. It is **not a DIN bearing
plane**. Mounting a part on a rail will still require its rail engagement offset.

`config.json` records each original model's axes, translation, rotation, terminal
XYZ coordinates, corresponding pad XY coordinates, and any pad movement.
`geometry_review.json` records source model and final footprint hashes. Models
are attached at scale 1,1,1 using rigid rotations and translations. The eight
manufacturer STEP files are unchanged.

The overload's simplified supplier CAD omits the adjustment dial shown on the
left in AD's product photo. The modeled right-hand feature is the reset control.
Its existing drawing and original STEP have the same handedness; no reflected
copy is required or installed.

Graphics remain on Dwgs.User. The established 3 mm pads / 2 mm holes are panel
wiring targets, not manufacturing drill specifications. Existing exact pin IDs
are retained. No pad overlap or fan-out is needed on these eight footprints.

## Verification

- Native KiCad 9 footprint load, SVG plotting, 3D render and STEP export for all
  eight parts.
- Exact symbol/pad set equality: 48 distinct physical terminal targets in total,
  including both units of multi-unit symbols.
- All 48 pad centers match terminal features in native KiCad STEP exports within
  0.000006 mm. Three overload inputs use blade-tip face centroids; other targets
  use circular screw/fork edges. Results are in `model_alignment.json`.
- Front orientation was compared visually with the reviewed drawings and native
  renders. The breaker model was turned to match the drawing's asymmetric ends.
- Both database rebuilds passed: 427 LCSC and 46 non-LCSC records, exact CSV/SQLite equality and integrity checks. Native export of an isolated test schematic passed for all 11 linked Controls part types, including both units of multi-unit parts. See `catalog_validation.json`.
- Catalog CSV, Controls library, schematic embedded definitions and placed
  symbol instances receive matching footprint links. Those symbols are enabled
  for board transfer. Required Package metadata is filled for newly linked parts. Symbol graphics, pin definitions, wiring and placements
  are preserved.

`previews/aligned-1.png` and `aligned-2.png` compare drawings and native renders.
The green substrate in those renders is a temporary test board, not a proposed
panel. `validate.py` creates these review boards only under `/tmp`.

Regeneration: run the existing DXF batch if needed, then `alignment/generate.py`
to apply the final links/transforms. Run `validate.py` with KiCad's Python and
`verify_model_alignment.py` with OCP. Earlier approved footprints are snapshotted
in `sources/` so transforms are repeatable. Source snapshots are input evidence,
not alternative catalog footprints.

## Assembly limits and scope

HTOR's supplied blade spacing remains 14.3 mm versus HMC's 10.9 mm terminal pitch.
The vendor lists compatibility, but their separate models do not establish the
installed blade arrangement. Likewise, the suppressor's flexible leads are shown
in the vendor's CAD pose. These are individual-part layouts, not verified
contactor/overload/suppressor assemblies.

External motor, E-stop, drum switch, button station and plug models remain
outside this pass. End covers, end stops and marker tags remain excluded by
request. Parts absent from the saved schematic, including HC3096N-52-900-24,
were not inserted. The working PCB is not populated or altered.
