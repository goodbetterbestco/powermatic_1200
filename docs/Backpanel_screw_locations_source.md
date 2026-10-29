# Backpanel and enclosure cutout drawing

Current enclosure sheet: [Enclosure_knockout_layout.pdf](Enclosure_knockout_layout.pdf), Rev I, 2026-10-29; one portrait 11 x 17 inch sheet. It replaces the former Rev E enclosure page with three exterior views and A-E hole details. Details are 1:1 when printed on portrait tabloid at 96%; pilot sizes, punch part numbers and the E filing area are included. The right-face entry locations follow the owner's fabrication measurements; finished hole types are unchanged. Rev I specifies two McMaster 9357K15 gasketed plugs with hex retaining nuts for the unused A pair. See [enclosure drawing sources](Enclosure_knockout_layout_source.md).

[Backpanel_screw_locations.pdf](Backpanel_screw_locations.pdf) retains the original landscape Rev E backpanel page and now includes the portrait Rev I enclosure sheet as page 2. The approved standalone [backpanel first sheet](Backpanel_screw_locations_page1.pdf) remains unchanged. All dimensions are mm; use written dimensions, not scaled measurements.

The historical Rev E datum, location and profile records below remain as the source cross-reference. Legacy profiles C1-C5 correspond to the current A-E respectively.

## Installation record — 2026-10-27

The user reports that backplate layout and installation of the DIN rails and wire duct are complete. All 20 mounting holes were drilled and tapped 10-24. The specified 10-24 fasteners were used and worked well.

Drilling the steel was challenging, and the self-drilling screws did not work. The successful process used a solid-carbide bit to drill pilot holes, followed by drilling and tapping all 20 holes to 10-24.

This records the reported installation method and completion of this phase. Final installed coordinates were not remeasured here; the drawing and coordinate schedules below retain their design values.

## Common datum and design intent

Both sheets use the enclosure LEFT and BOTTOM exterior faces as the common X/Y origin. Enclosure wall depth D is measured from the REAR exterior face. The backplate retains its physical position; the dashed enclosure outline on sheet 1 identifies the measurement datum. Coordinates must not be measured from the backplate edge.

The proposed installation rounds shared centerlines as groups. It does not modify the native PCB, original part models, panel envelope or factory mounting features. Cutout sizes and fixed hardware hole patterns retain functional dimensions.

| Constraint | Corrected common coordinate |
|---|---|
| Top duct D1 and indicators H1/H2 | Y = 690 mm |
| Middle DIN rail R2 and disconnect SW1 | Y = 420 mm |
| Bottom DIN rail R3 and M12 socket J1 | Y = 190 mm |
| Vertical duct V1 and motor entry J4 | X = 450 mm |
| All rails and horizontal ducts | Left X = 30 mm; right X = 430 mm |
| Horizontal duct right ends and V1 left edge | X = 430 mm |
| Bottom duct D4 and V1 bottom edge | Y = 50 mm |
| SW1/J1 wall-depth centerline | D = 100 mm |
| Indicator symmetry about SW1/J1 depth axis | H1 D = 75 mm; H2 D = 125 mm; spacing = 50 mm |

Indicator depth locations intentionally use 5 mm increments. Exact 50 mm spacing and symmetry about a centerline on the 10 mm grid cannot both be preserved with two indicator depths also on that grid.

## Saved source

- Native board: `kicad/powermatic_1200/powermatic_1200.kicad_pcb`; SHA-256 `c731a221f87b926be2c003654d6b80d86224b43d60473315bae08dab0162202a`.
- Native mechanical centerlines checked: R2/SW1 PCB Y=67; R3/J1 Y=297; D1/H1/H2 Y=-203; V1/J4 PCB X=431 mm.
- Source enclosure left face X=-23, bottom face PCB Y=485. Physical backplate left X=0.241 and bottom PCB Y=461.759 mm, so its left and bottom edges are 23.241 mm from the enclosure datum. This exact offset is retained internally rather than independently rounded between sheets.
- Panel overall is shown as rounded REF dimensions, 460 x 720 mm; actual saved CAD envelope is 461.518 x 715.518 mm. The physical enclosure is 508 x 762 x 203.2 mm and is retained.
- Placed model axes give source indicator depths 76.6/126.6 mm, symmetric about SW1/J1 depth 101.6 mm; proposed depths are 75/125 about 100 mm.
- Native board and BOM were not edited. Existing BOM local edits were preserved.

## Sheet 1 screw schedule

Three 400 mm DIN rails, four 400 mm horizontal ducts D1-D4 and one 650 mm vertical duct V1 require 20 screws: 9 rail, 8 horizontal-duct and 3 vertical-duct screws. Duct tags D1-D4 distinguish the ducts from indicator reference designators H1/H2.

| ID | X from enclosure left (mm) | Y from enclosure bottom (mm) |
|---|---:|---:|
| R1-1 | 40 | 590 |
| R1-2 | 220 | 590 |
| R1-3 | 420 | 590 |
| R2-1 | 40 | 420 |
| R2-2 | 220 | 420 |
| R2-3 | 420 | 420 |
| R3-1 | 40 | 190 |
| R3-2 | 220 | 190 |
| R3-3 | 420 | 190 |
| D1-1 | 80 | 690 |
| D1-2 | 380 | 690 |
| D2-1 | 80 | 510 |
| D2-2 | 380 | 510 |
| D3-1 | 80 | 290 |
| D3-2 | 380 | 290 |
| D4-1 | 80 | 70 |
| D4-2 | 380 | 70 |
| V1-1 | 450 | 650 |
| V1-2 | 450 | 380 |
| V1-3 | 450 | 100 |

Rail holes are at 10, 190 and 390 mm from their common left end; all were checked against saved slot straight sections after translating the rail envelopes. Horizontal duct holes have 50 mm end insets. Vertical duct holes are Y=650, 380 and 100 mm. Check physical duct perforations and select fastener/drill sizes before drilling.

## Sheet 2 cutout schedule

A is X from enclosure left for TOP/BOTTOM; Y above enclosure bottom for LEFT. D is from rear exterior. Seven device locations produce nine openings including two SW1 mounting holes.

| ID | Face | A (mm) | D (mm) | Profile |
|---|---|---:|---:|---|
| J3 | TOP | 390 | 80 | C1 |
| J4 | TOP | 450 | 80 | C1 |
| J2 | BOTTOM | 90 | 80 | C2 |
| H1 | LEFT | 690 | 75 | C3 |
| H2 | LEFT | 690 | 125 | C3 |
| SW1 | LEFT | 420 | 100 | C4 |
| J1 | LEFT | 190 | 100 | C5 |

C1: diameter 22.2 mm (7/8 inch) for selected 1/2-inch LFNC fittings. C2: diameter 28.2 mm (1-7/64 inch) for BNSPDX-23-W mains gland. C3: diameter 22.5 mm pilots. C4: diameter 10 mm shaft plus two diameter 4.3 mm mounting holes, 15 mm either side along depth (30 mm spacing). C5: diameter 15.4 +0.1/0 mm with 13.6 +0.1/0 mm across flats, flats parallel to enclosure height. Functional sizes and patterns are not rounded to the location grid.

## References

- Current WIRING_STANDARD.md and BOM_quantity_review_2026-10-19.md: J3/J4 gland artwork is superseded by 1/2-inch LFNC fittings; the distinct mains gland remains selected.
- Local manufacturer drawings in `/Users/evanthayer/Projects/_parts/datasheets/`: EP3020_Drawing.pdf, EN4SD30208GY_Drawing.pdf, T4171310004-001_Drawing.pdf, XB4BVB1_XB4BVB1.pdf and XB4BVB4_XB4BVB4.pdf.
- [BACO catalog 803, printed page 200](https://bacocontrols.com/wp-content/uploads/Baco-Controls-Catalog-803.pdf#page=202): disconnect panel drilling pattern.
- [McMaster LFNC fittings](https://www.mcmaster.com/products/ul-type-b-conduit/): selected 1/2-inch fittings.
