# Double-D draw-stud punch — Rev A

Dimensioned prototype for the TE T4171310004-001 connector cutout, using the owner's complete existing 7/16-20 draw stud and flat-faced bearing. CAD completion does not establish tool load capacity.

## Package contents

- `Double_D_punch_dimensioned_drawings.pdf`: six sheets covering assembly, all three custom parts, fabrication, and the first coupon record.
- `DD01_Cutter.step`, `DD02_Cup_die.step`, `DD03_Indexed_guide.step`: individual machining models in millimeters.
- `Double_D_punch_assembly.step`: assembly at first tooth contact with 1.8796 mm sheet. Bearing and stud are reference envelopes; their unmeasured details are deliberately omitted.
- `Double_D_punch_exploded.step`: three custom parts, without stock reference hardware.
- Seven DXFs: controlling functional XY profiles in millimeters; PDF Z stations define their axial extent.
- `Design_parameters.json` and `CAD_verification.json`: selected geometry and completed numerical checks.

## Design choices

Three custom one-piece parts replace the original round cutter and cup: a threaded cutter, cup die, and indexed guide sleeve. The sleeve clocks the cutter to the cup without modifying the stud or bearing. The cup has AF30 wrench flats; the cutter has AF24 flats for handling/removal. The stud rotates inside the stationary keyed cutter. Reusing the complete bearing avoids reverse engineering its internal construction.

The required finished hole is 15.4–15.5 mm major diameter and 13.6–13.7 mm across flats. The initial cutter is 15.45 × 13.65 mm, with a 2 mm balanced shear grind. The initial die is a true 0.19 mm outward normal offset of that profile, including the arc-to-flat transitions. These are prototype tooling choices; a coupon must establish the actual resulting hole.

The cutter thread is in its enlarged rear body. The STEP contains a tap-core representation and lead cones, not a helical thread. The drawing's **7/16-20 UNF-2B** callout controls machining. The through keyway interrupts a portion of the thread circumference. The full axial thread window is 17 mm; effective strength is not inferred from axial overlap alone.

Whole-millimeter dimensions are used where convenient. The connector profile, fits, thread interfaces, and clearance are intentionally not rounded to centimeter increments; the earlier enclosure-layout rounding preference does not apply to cutting-tool tolerances.

## Measured hardware and physical checks

The owner-confirmed dimensions from bearing face P are: first full stud thread 12.70 mm, last full thread 76.20 mm, tip 82.55 mm. Bearing OD is 25.40 mm; thickness is approximately 10.16 mm; face P is flat. Original cutter thread-crest reach is approximately 17.145 mm and is not treated as original cutter overall height.

The new guide provides D16 clearance over the first 14 mm from P. **Verify that the actual stud shoulder clears this space before manufacturing the guide.** Its unmeasured diameter and transition are not established by the first-full-thread measurement. The complete existing bearing remains in place.

Use S7 cutter at 54–56 HRC, A2 cup die at 58–60 HRC, and S7 guide at 52–54 HRC. Use controlled alloy-specific hardening and tempering; finish critical profiles and matched fits afterward. These are proposed prototype specifications, not a reproduction of the original manufacturer's tool design.

The small guide has a nominal 0.50 mm minimum radial wall. The cutting nose is also thin around the guide socket. No clamp or set screw may bear on the stem. Tooth bending, guide-key contact, thread stripping, stud proof load, heat treatment, wear and fatigue require engineering or physical validation before a working load can be assigned.

The flat-edge reference is 31.07 kN (3.49 US tons), calculated as perimeter × 1.8796 mm × assumed mild-steel shear strength 344.7 MPa. It is neither a maximum force nor a tightening-torque rating. No shear-grind reduction is credited to driver capacity. The owner's 3-ton arbor press falls below this unreduced reference.

Before enclosure use, verify dry assembly, guide clearance and clocking, and make a coupon in the actual enclosure material. Inspect the entire hole profile, burr, slug release, connector fit, cutting edges, key and threads. Adjust the initial tooling only if the resulting hole requires it. The six-sheet drawing includes a coupon record. No impact-driving qualification is supplied.

## Verification completed

All three custom STEP exports were reimported as single valid solids and matched source-model volume. Both assembly STEP exports were reimported and checked. No cutter/cup or cutter/guide interference occurred at eight sampled positions from first tooth contact through 5 mm tooth entry. Full axial thread overlap is 17 mm throughout this modeled stroke; the guide has 2 mm clearance to the cutter's bore step at the end. The seven DXFs have millimeter units. See `CAD_verification.json` for results. These geometric checks do not establish strength or punched-hole performance.

## Sources

- [TE T4171310004-001 product and drawing](https://www.te.com/en/product-T4171310004-001.html), customer drawing B2; local source: `/Users/evanthayer/Projects/_parts/datasheets/T4171310004-001_Drawing.pdf`.
- Owner hardware measurements and cutter photograph recorded in this conversation; source measurements retained one directory above in `Measured_hardware_dimensions.json`.
- [Mate Technical Solutions Guide, LIT00682 Rev E](https://www.mate.com/wp-content/uploads/2021/03/LIT00682_TechSolutionsGuide_RevE_LR.pdf): clearance and force methodology.
- [Carpenter S7 technical data](https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/S7.pdf) and [Hudson A2 technical data](https://hudsontoolsteel.com/technical-data/steelA2): material and heat-treatment basis.
- [TEMCo double-D punch with indexed mandrel](https://temcoindustrial.com/double-d-punch-die-set-0-769-inch-x-0-642-inch-knockout-hole-w-case/): alignment architecture reference only; its hole dimensions do not match this connector.

23 October 2026. The PDF and functional DXFs govern the prototype dimensions; STEP thread geometry is simplified as stated above.
