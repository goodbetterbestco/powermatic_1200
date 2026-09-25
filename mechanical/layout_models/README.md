# Rail and duct layout models

User-supplied Fusion STEP exports received 2026-09-25. The originals are saved here unchanged; source paths and SHA-256 hashes are in `sources.json`.

Current layout scope is the panel enclosure. The user has deferred modeling the external L15-20 plug, drum switch and button station; their models are not prerequisites for this layout.

| Model | Measured envelope | Solids |
|---|---|---:|
| DN-R35S1.step | 261 mm long × 35 mm wide × 7.5 mm high | 1 |
| DN-R35S1_350mm.step | 350 mm long × 35 mm wide × 7.5 mm high; working rail model | 1 |
| T1-1530G1-1.step | 1000 mm long × 40 mm wide × 80 mm high, including cover | 2 |

All three files imported into Open CASCADE and passed its BRep validity check. Dimensions are from the actual imported solids, not a scan of STEP control points. The duct's advertised nominal size is 1.5 × 3 inches; use the 40 × 80 mm CAD envelope for layout.

## Proposed working lengths

- DIN rail: **350 mm** for the first component-placement pass; use `DN-R35S1_350mm.step`. The earlier 261 mm export is retained as a source reference.
- Horizontal duct: **350 mm** as an initial model variant.
- Vertical duct: derive its length after component rows and horizontal ducts are placed.

These are proposed CAD layout dimensions, not a fabrication cut list. The user has chosen to let the component layout determine enclosure size. There is no fixed rail count or backplate size yet.

The five 45 mm contactors occupy 225 mm before interlocks. Allowing two nominal 12 mm interlock bodies gives about 249 mm, before end stops and group spacing. The supplied 261 mm rail offers little allowance; 350 mm offers about 101 mm beyond that initial estimate. Actual interlock engagement and assembled placement remain to be checked.

Keep the 1000 mm duct as a stock/master model. Make individual length variants from the native Fusion design so the profile, slots and cover remain unchanged. Do not scale the complete model to change length.

The duct length along a particular run will follow the arrangement of intersections, terminations and clearances; it need not equal the adjacent rail length in the final layout.

`step_measurements.json` records the supplied models and selected vendor component envelopes in their native coordinate systems. Vendor axis order is not a standardized width/height/depth orientation.
