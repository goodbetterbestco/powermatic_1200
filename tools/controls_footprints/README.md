# Controls footprint review

## Simplified enclosure artwork

The approved fuse-holder standard is now applied to every device footprint used
on the saved project board: 13 unique device types, 56 placed instances. The
latest rollout updates 12 shared library footprints and 55 board instances;
`RM25030-3SR_Front` / `FH1` keeps the approved pilot. The two DIN rails stay on
User.Drawings as the background structure.

- **F.Fab:** complete original imported drawing, with source coordinates and
  graphical records preserved exactly apart from the layer.
- **F.Silkscreen:** body contours and major functional elements, using 0.25 mm
  lines and analytic arcs/circles. Keep terminals, mounting features, actuators,
  clips, protruding blades, leads and connector sections. Omit screw slots,
  ribs, thread detail, hidden edges and repeated parallel molding lines.
- **F.Adhesive:** opaque fill following the physical body and protrusions. Open
  forks, gaps between leads and actual through-openings remain open. This is a
  display layer for panel layout, not an adhesive specification or keepout.
- Keep the existing visible 2.5 mm reference on F.Silkscreen. Hidden metadata
  stays hidden. Pads, terminal IDs, nets, footprint origins, placements and 3D
  model transforms are preserved.

For layout, make **F.Silkscreen active**, show **F.Adhesive**, hide **F.Fab**, and
keep shape opacity at 100%. The device fills cover the rails on User.Drawings.
Selecting User.Drawings brings that layer forward. To inspect the original
CAD, hide the fill and show F.Fab. The existing dashed wall datums on SW1 are
also retained as background annotation on User.Drawings.

The editable recipes are in `silkscreen/project_traces.json`. Body contours are
traced from the saved source drawings, with at most 0.03 mm polygon simplification
and major curves restored as analytic arcs; internal feature traces omit the
fine detail. The PSU case and lamp lens have open seams in the CAD projection;
the fill closes those seams at the measured physical outline. Connector thread
ridges are reduced to a plain collar envelope. These are nominal layout views,
not machining or clearance dimensions.

`silkscreen/project_rollout.py`, run with KiCad's bundled Python, prepares
candidates, checks each original drawing against its library, and verifies exact
preservation of all non-artwork records. `--install` requires unchanged source
and candidate hashes; `--verify` checks the installed result. Existing Q1 and
PS1 drawing-origin offsets in the board are retained when placing their new
artwork. Native save roundoff and arc endpoint reversal are accounted for in
the geometry comparison. `silkscreen/project_validation.json` records those
checks and the per-part results. Temporary source backups and the native review
board live under `/private/tmp/powermatic-artwork-rollout/`.

[Rollout gallery](silkscreen/project_review.html) shows the simplified device
views. The fuse pilot remains documented by `silkscreen/fuse_holder.py` and
`silkscreen/validation.json`.

The earlier generators and reference-label utility below predate this standard
and can restore the older Dwgs.User convention. Do not rerun them over the
reviewed artwork; use the saved recipes and preservation checks when rebuilding.

## Historical reference-label workflow

Before the artwork rollout, Controls footprints showed only the Reference
property in 2.5 × 2.5 mm KiCad text on Dwgs.User. It is centered on the drawing's vertical centerline, between
the topmost drawing line and the midpoint of that centerline. Value and other
text remain hidden. The catalog rules are FP-CTRL-006 through FP-CTRL-008.

`label_references.py`, run with KiCad's bundled Python, searches vertically for
the least overlap using KiCad's rendered text strokes, drawing lines and pads.
The four footprint generators call it automatically. Pass a footprint directory
or PCB file plus `--write` to reapply it after changing reference names. Only text
records change; component geometry, pads, models and placements stay untouched.
The historical geometry reviews below predate this text convention.

17 footprints from 16 DXFs: 16 new footprints and the preserved, approved fuse-holder sample. The reversing-busbar kit produces separate line and load footprints.

Open the **Controls** library in KiCad Footprint Editor from the Powermatic project. This historical review used **Dwgs.User**; current project devices use the layer standard above. The 62 numbered wiring targets use 3 mm pads with 2 mm holes, carrying forward the 14 AWG review convention. These are panel-layout wiring targets; they do not specify PCB fabrication or final wire sizes.

## Geometry and validation

All 55 selected DXF dimension features agree with the printed manufacturer dimensions to within 0.05 mm, consistent with their decimal rounding. This is a nominal drawing comparison, not a manufacturing tolerance. For the Socomec mounting span, the manufacturer STEP value of 131.3 mm is the preferred layout dimension.

KiCad 9.0.7 loaded and exported all 17 files. All 62 pads have unique IDs within their footprint, positive clearance, and the specified pad/drill sizes. All nine footprints with matching existing Controls symbols have exactly the same pin-number sets across their symbol units. The AUX11-F uses its four manufacturer terminal IDs; it has no matching Controls symbol yet. Seven mechanical/accessory footprints have no independent wire terminals and no pads.

Origins are at the center of each projected physical envelope. They are **not** yet aligned to STEP mounting/back-face origins, DIN datums or accessory assembly origins. No STEP models are attached in this review pass. Pin targets were kept at true projected terminal centers; none of these selected views needs fan-out. The generator supports the agreed symmetric fan-out without leaders if coincident terminals are introduced.

## Assembly conventions and remaining geometry detail

- **HTOR32-6-S / HMC-9B30-11-DS:** the overload mounts below the contactor, into its three load terminals (2/T1, 4/T2, 6/T3). The catalog shows this arrangement on PDF page 20. Separate supplier CAD models show 14.3 mm versus 10.9 mm blade/terminal pitch; the exact installed blade arrangement remains to be established. Both models retain their source dimensions.
- **HMX1-SSVRC-DC:** two flexible factory lead wires connect across coil terminals A1/A2; the body clips into the contactor. These leads are included with the suppressor and are separate from the HMX1-BBREV reversing busbars. The catalog installation diagram is on PDF page 21. The 24 mm fork spacing in CAD is a depicted wire position, not a fixed mating pitch.
- **22013003:** use the manufacturer STEP mounting-hole span, **131.3 mm**, as the preferred layout dimension. Existing footprint geometry already uses that model. Retain 131.4 mm from the drawing and 131.351 mm from DXF dimension endpoints as source comparisons, not correction targets.
- **HMX1-MI:** projected terminal arrangement accepted. Two outer screws lie behind nearer plastic in this projection; their pads remain at the actual projected screw centers and the review JSON records the two screw depths.

## Footprints

Dimensions below are projected graphic envelopes in millimeters, excluding stroke width, text and wiring-pad overhang. They are not necessarily the dimensioned body features. Small details and protruding leads are retained.

| Footprint | Width × height | Pads | Source view |
| --- | ---: | ---: | --- |
| [14070532_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/14070532_Front.kicad_mod) | 319.956 × 5.000 | 0 | DXF selected elevation |
| [148E1111_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/148E1111_Front.kicad_mod) | 88.445 × 70.957 | 0 | DXF selected elevation |
| [22013003_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/22013003_Front.kicad_mod) | 78.808 × 142.730 | 6 | STEP visible-edge projection |
| [22943016_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/22943016_Front.kicad_mod) | 78.000 × 188.976 | 0 | DXF selected elevation |
| [CVR-RH-25030_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/CVR-RH-25030_Front.kicad_mod) | 21.182 × 99.092 | 0 | DXF selected elevation |
| [FAZ-D4-2-NA-L_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/FAZ-D4-2-NA-L_Front.kicad_mod) | 35.400 × 105.000 | 4 | DXF selected elevation |
| [HC3096N-52-900-24_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HC3096N-52-900-24_Front.kicad_mod) | 17.903 × 106.792 | 10 | DXF selected elevation |
| [HMC-9B30-11-DS_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMC-9B30-11-DS_Front.kicad_mod) | 45.000 × 75.500 | 14 | DXF selected elevation |
| [HMX1-AUX11-F_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMX1-AUX11-F_Front.kicad_mod) | 25.000 × 48.000 | 4 | STEP visible-edge projection |
| [HMX1-BBREV_Line_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMX1-BBREV_Line_Front.kicad_mod) | 90.700 × 26.500 | 0 | DXF selected elevation |
| [HMX1-BBREV_Load_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMX1-BBREV_Load_Front.kicad_mod) | 90.700 × 19.500 | 0 | DXF selected elevation |
| [HMX1-MI_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMX1-MI_Front.kicad_mod) | 21.200 × 83.000 | 4 | STEP visible-edge projection |
| [HMX1-SSVRC-DC_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HMX1-SSVRC-DC_Front.kicad_mod) | 37.400 × 39.473 | 2 | DXF selected elevation |
| [HTOR32-6-S_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/HTOR32-6-S_Front.kicad_mod) | 45.000 × 74.550 | 10 | DXF selected elevation |
| [KN-10J12_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/KN-10J12_Front.kicad_mod) | 51.125 × 5.000 | 0 | DXF selected elevation |
| [KN-T12GRY-25_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/KN-T12GRY-25_Front.kicad_mod) | 5.000 × 44.200 | 2 | DXF selected elevation |
| [RM25030-3SR_Front](/Users/evanthayer/Projects/_parts/footprints/Controls.pretty/RM25030-3SR_Front.kicad_mod) | 74.491 × 80.400 | 6 | Approved DXF sample |

[Visual gallery](review.html) · [Preview 1](previews/review-1.png) · [Preview 2](previews/review-2.png) · [Preview 3](previews/review-3.png)

## Dimensional evidence

The table compares the actual endpoints of dimensioned features with their published values. [dimension_review.json](dimension_review.json) retains source hashes, DXF handles, dimension endpoints, terminal coordinates, transformations and notes.

| Part | Checked feature | Published mm | CAD mm | Difference mm |
| --- | --- | ---: | ---: | ---: |
| 14070532 | Stock length | 320.000 | 319.956 | -0.044 |
| 14070532 | Shaft width | 5.000 | 5.000 | +0.000 |
| 14070532 | Cross-pin span | 11.700 | 11.667 | -0.033 |
| 148E1111 | Escutcheon diameter | 71.000 | 70.957 | -0.043 |
| 148E1111 | Handle dimension | 88.000 | 87.971 | -0.029 |
| 148E1111 | Depth | 37.000 | 37.015 | +0.015 |
| 22013003 | Body width | 78.000 | 78.000 | +0.000 |
| 22013003 | Pole pitch | 26.000 | 26.000 | +0.000 |
| 22013003 | Mounting span | 131.400 | 131.351 | -0.049 |
| 22013003 | Depth including shaft socket | 75.000 | 74.983 | -0.017 |
| 22943016 | Width | 78.000 | 78.000 | +0.000 |
| 22943016 | Individual cover length | 71.600 | 71.631 | +0.031 |
| 22943016 | Installed pair envelope | 189.000 | 188.976 | -0.024 |
| 22943016 | Depth | 50.100 | 50.107 | +0.007 |
| CVR-RH-25030 | Length | 99.100 | 99.092 | -0.008 |
| CVR-RH-25030 | Width | 21.200 | 21.182 | -0.018 |
| FAZ-D4-2-NA-L | Width | 35.400 | 35.400 | -0.000 |
| FAZ-D4-2-NA-L | Height | 105.000 | 105.000 | +0.000 |
| FAZ-D4-2-NA-L | Pole pitch | 17.700 | 17.700 | +0.000 |
| FAZ-D4-2-NA-L | Screw row pitch | 66.000 | 66.000 | +0.000 |
| HC3096N-52-900-24 | Body width | 17.900 | 17.900 | -0.000 |
| HC3096N-52-900-24 | Height dimension | 106.800 | 106.769 | -0.031 |
| HC3096N-52-900-24 | Depth | 65.100 | 65.050 | -0.050 |
| HMC-9B30-11-DS | Width | 45.000 | 45.000 | -0.000 |
| HMC-9B30-11-DS | Height | 75.500 | 75.500 | +0.000 |
| HMC-9B30-11-DS | Mounting pitch X | 34.000 | 34.000 | -0.000 |
| HMC-9B30-11-DS | Mounting pitch Y | 65.000 | 65.000 | +0.000 |
| HMC-9B30-11-DS | Depth | 103.600 | 103.600 | -0.000 |
| HMX1-AUX11-F | Width | 25.000 | 25.000 | -0.000 |
| HMX1-AUX11-F | Front length | 48.000 | 48.000 | -0.000 |
| HMX1-AUX11-F | Depth | 35.000 | 35.000 | +0.000 |
| HMX1-BBREV | Line bar length | 90.700 | 90.700 | -0.000 |
| HMX1-BBREV | Line bar height | 26.500 | 26.500 | +0.000 |
| HMX1-BBREV | Load bar length | 90.700 | 90.700 | -0.000 |
| HMX1-BBREV | Load bar depth | 22.800 | 22.800 | -0.000 |
| HMX1-MI | Front height | 83.000 | 83.000 | +0.000 |
| HMX1-MI | Body width | 12.000 | 12.000 | +0.000 |
| HMX1-MI | Actuator span | 21.200 | 21.200 | +0.000 |
| HMX1-MI | Depth | 80.500 | 80.500 | +0.000 |
| HMX1-SSVRC-DC | Width | 37.400 | 37.400 | +0.000 |
| HMX1-SSVRC-DC | Body span in terminal-facing view | 15.000 | 15.000 | +0.000 |
| HMX1-SSVRC-DC | Inner body width | 35.000 | 35.000 | +0.000 |
| HMX1-SSVRC-DC | Body span in other view | 22.500 | 22.500 | +0.000 |
| HTOR32-6-S | Width | 45.000 | 45.000 | -0.000 |
| HTOR32-6-S | Body height | 57.900 | 57.900 | +0.000 |
| HTOR32-6-S | Prong extension | 16.700 | 16.650 | -0.050 |
| HTOR32-6-S | Depth | 90.000 | 90.000 | +0.000 |
| KN-10J12 | Length | 51.100 | 51.125 | +0.025 |
| KN-10J12 | Bar width excluding screw heads | 4.400 | 4.350 | -0.050 |
| KN-10J12 | Depth | 15.800 | 15.752 | -0.048 |
| KN-T12GRY-25 | Length | 44.200 | 44.200 | -0.000 |
| KN-T12GRY-25 | Thickness | 5.000 | 5.000 | -0.000 |
| KN-T12GRY-25 | Depth | 42.500 | 42.504 | +0.004 |
| RM25030-3SR | Width dimension | 74.500 | 74.487 | -0.013 |
| RM25030-3SR | Covered height | 99.100 | 99.092 | -0.008 |

## Source notes

- **14070532:** Stock shaft side elevation; length remains untrimmed. No electrical terminal. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/14070532_CAD_Drawing.pdf)
- **148E1111:** Operating face. Outline includes a small protrusion outside the 88 mm dimension. No distortion to force the envelope to 88 mm. Rotation center is not the footprint origin. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/148E1111_CAD_Drawing.pdf)
- **22013003:** Bare screw-facing projection from manufacturer STEP; the DXF front view obscures the face with a handle. 78 mm is body width, not the complete 78.808 mm clip envelope. Bare height 142.730 mm is CAD-derived; 189 mm applies to the cover pair. Use the STEP mounting-hole center span of 131.3 mm for this layout. The published drawing gives 131.4 mm and the DXF dimension endpoints give 131.351 mm; those values remain recorded as source evidence. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/22013003_CAD_Drawing.pdf)
- **22943016:** Both terminal covers shown at manufacturer installed spacing. Empty center remains empty. Overlay registration to the disconnect requires assembly alignment; each footprint is independently centered. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/22943016_CAD_Drawing.pdf)
- **CVR-RH-25030:** Single-pole cover rotated to align with fuse-holder orientation; one footprint is one cover. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/CVR-RH-25030_CAD_Drawing.pdf)
- **FAZ-D4-2-NA-L:** Screw-facing elevation; four terminals, two poles. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/FAZ-D4-2-NA-L_Drawing.pdf)
- **HC3096N-52-900-24:** Terminal numbering uses the 2NO/2NC variant in the manufacturer datasheet. Screw centers fitted to supplier spline geometry; small real top/bottom offsets retained. Envelope 106.792 mm includes detail beyond the height dimension endpoints. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HC3096N-52-900-24_Drawing.pdf)
- **HMC-9B30-11-DS:** All 14 terminals retained, including four separate coil-access screws. Built-in auxiliary terminals are 43/44 NO and 31/32 NC. Pole pitch 10.9 mm in supplied model; overload mating needs assembly verification. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HMC-9B30-11-DS_Drawing.pdf)
- **HMX1-AUX11-F:** Manufacturer STEP supplies the screw-facing view absent from DXF. Actual product photograph identifies left NC 51/52 and right NO 63/64. No matching Controls symbol currently exists; these are manufacturer terminal IDs. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HMX1-AUX11-F_CAD_Drawing.pdf)
- **HMX1-BBREV:** Kit split into line and load pieces. Graphics-only accessory: connections occur at mating contactor terminals, not independent wire terminals. Load-piece height 19.5 mm is CAD-derived. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HMX1-BBREV_CAD_Drawing.pdf)
- **HMX1-MI:** Screw-facing manufacturer STEP projection, not the large flat side in DXF. Four screws at different depths project separately; no fan-out required. Terminal order top to bottom: 111,121,112,122. Outer two screws are hidden by nearer model geometry in the true front projection; their wiring pads retain the measured screw centers and depths. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HMX1-MI_Drawing.pdf)
- **HMX1-SSVRC-DC:** Terminal-facing view includes the supplier lead shape. The two flexible factory lead wires terminate in forks and connect across the contactor coil terminals; the body clips into the contactor mounting space. These are supplied suppressor leads, separate from the HMX1-BBREV reversing busbars. Their 24 mm CAD spacing is a depicted wire position, not a fixed mating pitch. Final installed wire routing can vary. Numbers 1/2 match the catalog symbol, not polarity. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HMX1-SSVRC-DC_Drawing.pdf)
- **HTOR32-6-S:** Front includes three input blades and seven screw terminals. The overload mounts below the contactor, directly into its three load terminals (2/T1, 4/T2, 6/T3). Input pad centers are at the blade tips. Supplier CAD input pitch is 14.3 mm, whereas HMC-9B30-11-DS has 10.9 mm pole pitch; the manufacturer lists compatibility, but the exact installed blade arrangement is not represented by these separate models. No scaling or bending was invented. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/HTOR32-6-S_Drawing.pdf)
- **KN-10J12:** Screw-facing jumper. 4.4 mm drawing dimension describes the bar; head envelope is 5 mm. Graphics-only accessory, without independent wire terminals. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/KN-10J12_CAD_Drawing.pdf)
- **KN-T12GRY-25:** Rotated into installed vertical terminal orientation on a horizontal DIN rail. Two actual wire terminals; jumper is separate. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/KN-T12GRY-25_CAD_Drawing.pdf)
- **RM25030-3SR:** Approved uncovered sample preserved byte-for-byte. 80.400 mm uncovered height is from CAD; published 99.1 mm is the covered height. Six approved 14 AWG review pads retained. [Manufacturer drawing](/Users/evanthayer/Projects/_parts/datasheets/RM25030-3SR_Drawing.pdf)

Terminal identities were checked against the Controls catalog and manufacturer terminal diagrams/photos. Exact photo copies are in `sources/`; their manufacturer URLs are recorded in the JSON. The 2NO/2NC relay map comes from `HC3096N_Datasheet.pdf`, rather than the generic geometry drawing.

## Rebuild

- `generate.py` requires Python with `ezdxf` (used version 1.4.4). It verifies source DXF hashes, reads the reviewed entity selections/projections in `config.json`, and recreates the 16 new footprints. It deliberately leaves the approved RM25030-3SR file untouched.
- `project_step.py 22013003 HMX1-AUX11-F HMX1-MI` requires OCP and recreates the three visible-edge STEP projections in `sources/`. Other curves are tessellated to 0.002 mm; lines and circular arcs remain analytic. Manufacturer model hashes are recorded.
- `validate.py` runs under KiCad 9’s bundled Python with `pcbnew`. It checks the native files, exact symbol/pad ID sets, pad geometry and overlaps, then exports SVGs. Pass a Controls.kicad_sym path as its first argument to override the default catalog location.
- `render_previews.cjs` uses `sharp` to rasterize the native SVGs and produce the three review sheets. Preview colors are darkened for readability; footprint graphics are unchanged.

## October 2 model alignment repair

The desktop STEP replacements changed the HMC contactor and HMX suppressor coordinate frames. `model_alignment/settings.json` records the installed model transforms, attached-accessory offsets, and exact hashes of the preserved replacement files. The front and side review in `model_alignment/review.html` reproduces the user’s nominal Fusion assembly views. Accessory positions use screenshot measurements and source mounting geometry; exact Fusion joint dimensions were unavailable, and this is not an interference-free fit approval. The supplied solids overlap in the nominal assembly.

All 58 footprint instances were audited across 14 types. Q1, FH1 and PS1 now use the existing DIN-datum model variants, with local XY compensation where needed to retain their artwork. The restored 300 mm rail model uses an unscaled 300 mm cut of the retained 350 mm source, shifted to match the existing slot positions. Original 2D artwork, local pad geometry and nets were preserved; only the seven attached-accessory placements changed. Recheck installed links, transforms, scales, source hashes and accessory positions using KiCad’s Python with `model_alignment/verify.py`. The earlier artwork validation is a historical checkpoint and therefore predates these intentional model/placement changes.

During publication, remote `_parts` commit `eee0d7d` supplied the original 300 mm rail export and its left-origin model. The merge retains that remote rail model and library footprint, plus all new rail/duct variants. Native KiCad comparison found identical 218-element rail drawing geometry; the remote reference label is centered and visible in the library, while placed-board fields remain unchanged. CAD comparison confirmed the same 300 × 35 × 7.5 mm bounds; the cut-derived local solid differs by 0.097193 mm³ (0.000762% of volume). `model_alignment/publication_reconciliation.json` records this replacement; `rail_geometry.json` remains the earlier cut-model checkpoint. The installed model report was regenerated after the merge.
