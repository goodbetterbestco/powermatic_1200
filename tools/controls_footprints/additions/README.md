# Three Controls footprint additions

Reviewed 2026-09-25. These are panel-layout elevation footprints under FP-CTRL-001 through FP-CTRL-005. Manufacturer STEP geometry is projected at 1:1 scale onto Dwgs.User; attached models are unchanged and face +Z. The 3 mm pads / 2 mm holes are wiring targets using the existing 14 AWG review convention, not PCB lands, panel drilling instructions, or a final wire-size selection.

| Part | Footprint | Electrical pads | Dimension check, mm |
|---|---|---:|---|
| NDR-240-24 | Controls:NDR-240-24_Front | 7 | Case 63 × 125.2; CAD depth 113.25 vs published 113.5, within stated ±1 tolerance. Full front projection 63 × 128.712 includes DIN clip. |
| XB4BVB1 | Controls:XB4BVB1_Front | 2 | CAD 29.9 × 46.2 × 53.751 vs published 30 × 46.5 × 54. Small source differences retained; no rescaling. |
| T4171310004-001 | Controls:T4171310004-001_Front | 4 | 18 across flats; 20 body length, 10.2 front length, 13.5 rear diameter match drawing. Full model depth 22.4 includes contact stubs. |

## Sources and pin mapping

- Mean Well: `_parts/datasheets/NDR-240-24_NDR-240-24.pdf`, mechanical specification and terminal tables, page 4; `_parts/3dmodels/Controls/NDR-240.stp`. Bottom TB1.1 = FG, TB1.2 = N/DC−, TB1.3 = L/DC+. Top TB2.1 and TB2.2 = −V; TB2.3 and TB2.4 = +V. Screw centers taken from circular edges in the model. The family model includes the complete case and DIN clip.
- Schneider: `_parts/datasheets/XB4BVB1_XB4BVB1.pdf`, dimension drawing page 3 and panel cutout page 4; `_parts/3dmodels/Controls/XB4BVB1.stp`. Supplier's newer model differs slightly from the older rounded drawing. X1 is upper and X2 lower with the model in this orientation. Both screws are on the rear: their wiring targets are projected through the front lens view. The actual lens remains in the manufacturer model.
- [Schneider ZBVB1 light block](https://www.se.com/us/en/product/ZBVB1/): official rear photograph and drawing retained in `sources/ZBVB1_Rear.jpg` and `sources/ZBVB1_Drawing.pdf`. Photograph source: `https://download.schneider-electric.com/files?p_Doc_Ref=ZBVB1_Rear&p_File_Type=rendition_369_jpg&default_image=DefaultProductImage.png`.
- [TE customer drawing T417131000X00L, revision B2](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=T417131000X00L&DocType=Customer%20Drawing&DocLang=English&DocFormat=pdf&PartCntxt=T4171310004-001), archived as `_parts/datasheets/T4171310004-001_Drawing.pdf` and `sources/T417131000X00L_B2.pdf`; `_parts/3dmodels/Controls/T4171310004-001.stp`. Viewed into the female mating face, key upward: 1 upper left, 2 upper right, 3 lower right, 4 lower left. TE colors: 1 BRN, 2 WHI, 3 BLU, 4 BLK. The central modeled bore is not a fifth terminal. No electrical shell pad is inferred. Flexible 200 mm wire tails are absent from the supplied model; pads locate mating contacts, not the free wire ends. The drawing specifies a 15.4 diameter / 13.6 across-flats panel opening; no cutout is added to Edge.Cuts.

## Origins and models

`config.json` records model coordinates, physical terminal centers, viewing basis and rigid transforms. `geometry_review.json` adds hashes and generated pad coordinates.

- PSU: origin at center of full elevation projection, rear-most modeled DIN clip at Z=0. This is **not the DIN bearing plane**; placement onto an actual rail requires its mounting offset.
- Lamp: origin on lens/mounting axis, rear model envelope at Z=0.
- M12: origin on connector axis, rear contact-stub envelope at Z=0; key at 12 o'clock.

KiCad stores the PSU rotation as `(90, -90, 0)` degrees. Its native rotation signs differ from the standard active matrix used for the projection. All models have scale `(1,1,1)` and resolve through `${PARTS_LIB}`.

## Validation and regeneration

`generate.py` creates the three review copies from cached manufacturer projections. `project_step.py` regenerates a projection with OCP: model filename, normal vector CSV, right vector CSV, output stem. Non-circular curves are chorded to 0.005 mm; lines, arcs and circles remain native primitives.

`validate.py`, run with KiCad 9's bundled Python, checks exact symbol/pad identities, distinct pad locations, size/drill, Dwgs.User graphics and model paths. It creates temporary review boards under `/tmp/powermatic-three-controls`, native SVGs and 3D renders, and native STEP exports. The STEP exports include a temporary board body because this KiCad build fails to export these assemblies with `--no-board-body`; that substrate is not an enclosure design.

`verify_model_alignment.py`, run with OCP, compares all 13 pad centers with circular edges in KiCad's exported STEP. Maximum discrepancy is less than 0.000005 mm. Native render views and 2D plots were visually reviewed. `native_validation.json` and `model_alignment.json` contain results.

Installed library: `_parts/footprints/Controls.pretty`. The source symbols, catalog and three saved schematic instances carry the matching footprint references and are included in board export. No schematic wiring, placement or PCB layout was changed.

## Exclusions

KN-ECT6GRY-25 end covers, KN-EB7-10 end stops, and KN-L5X-BLNK-220 tags are explicitly skipped. External motor/control assemblies remain deferred. The earlier 17 review footprints are outside this three-part installation; this report does not certify or install that earlier batch.
