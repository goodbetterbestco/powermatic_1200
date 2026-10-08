# Switch artwork and panel user-layer review

Installed in the saved PCB, shared S2/S3 footprints and governing Controls
rules on 2026-10-08. This remains a visual panel-placement/wiring artifact.

Q1 was the owner's requested benchmark. Its full F.Fab projection includes
1,578 graphic primitives; the working silkscreen has 151. The reviewed Q1
recipe retains both poles, four plain terminals, toggle assemblies, indicators
and mounting feet, while omitting molding ribs and screw slots. Q1's physical
artwork was not changed; its hidden sheet metadata was relocated to F.Fab.

| Footprint | Detailed F.Fab graphics, preserved | F.Silkscreen graphics before | F.Silkscreen graphics after |
| --- | ---: | ---: | ---: |
| Q1 | 1,578 | 151 | 151 |
| S2 | 4,861 | 0 | 98 |
| S3 | 5,339 | 349 | 604 |

S2 silkscreen now shows its true casing profile, three bezels/button faces,
mounting features, ten terminal plates and plain measured screw-head rims.
S3 now shows the case, shaft, contact body, electrodes/terminal plates,
brackets, visible jumpers and plain measured screw rims. Both follow Q1's
approved 0.25 mm elevation-outline style. Screw slots, threads, engraved
legends/numbers and fine tessellation remain in the full F.Fab source view.
The drawing proxy cylinders affect only projected artwork; no model is edited.
Connected linework is simplified with a 0.075 mm maximum chord deviation.

The Reference is the only visible property/user text. S2's reference moved
from Dwgs.User to F.SilkS. S3's reference moved within the upper case gap,
at local X=10.5, Y=-31.75 mm, to avoid its newly drawn mechanical detail.
Silkscreen is clipped to the circular logical wire-target copper using the
actual 0.25 mm stroke width. Minimum rendered-edge gaps are 2.428988 mm for
S2 and nominally 0.15 mm for S3 (rounding error below 0.000001 mm).

All 38 hidden Sheetfile/Sheetname fields formerly on Dwgs.User were moved
to F.Fab. All four locked dashed backplate mounting-clearance circles formerly
on Cmts.User were moved to Dwgs.User without altering geometry or locking.
Cmts.User has zero objects and its native SVG export contains no geometry.
Dwgs.User now contains only enclosure, backplate, wire-duct and DIN-rail
information. The two existing dashed enclosure-wall section lines inside
SW1's footprint remain there because they describe the enclosure wall.

The owner-requested policy is recorded in `_parts/kicad_rules.csv`:
FP-CTRL-007 now places device references on F.Silkscreen; FP-CTRL-009 reserves
the user layers; FP-CTRL-010 records the Controls elevation detail exception.
Generic PCB land-pattern rules are not weakened by these panel-layout rules.
Both switch builders reproduce the reviewed silkscreens exactly. The common
reference-label helper also follows the new layer policy.

Validation preserves every original F.Fab graphic verbatim, all pad records,
nets, positions, attributes, footprint/pad UUIDs, models/transforms, tracks,
vias, zones, Edge.Cuts and other board records. Schematic, project settings,
symbol library, catalog CSV/SQLite and both colored STEP models remain
byte-identical. Native before/after layer exports and the expanded full-layout
view were inspected. The native export page was expanded for `whole-layout`
so the machine-mounted switches and external fittings outside the backplate
are visible; its geometry is unchanged from the original export.

Final native ERC: zero errors and the same ten existing library warnings.
Native DRC again exited 134 without a report, so DRC remains unverified.
The direct stroke-clearance and preservation checks passed; these are not
fabrication, fitment or physical installation signoff.

Evidence: `before/`, `after/`, `artwork-source.json`, `validation.json`,
`installed.json`, `final-erc.json`, `kicad_rules.csv` and the adjacent native
SVG/PNG files. The same switch-specific evidence is retained in the shared
parts library's `reviews/Controls/SwitchArtwork_2026-10-08/` directory.
