# Enclosure hole layout - sources and verification

Drawing: [Enclosure_knockout_layout.pdf](Enclosure_knockout_layout.pdf), Rev I, 2026-10-29. One portrait 11 x 17 inch sheet. It contains enclosure views, edge-referenced center locations, 1:1 A-E profile details, pilot sizes and punch identification. All callout leaders are 45 degrees.

## Right-face entry revision - 2026-10-29

The owner added two alternate motor/control entry holes to the right wall and moved the power entry from the bottom to the right wall. The actual right-face A centers are 75 and 135 mm below the top, each 125 mm from the face's left/front edge when viewed from outside. The 75 mm location is the motor alternative; 135 mm is the controls alternative. The power center is recorded as 70 mm above the bottom (owner-approved rounding of the measured 2.75 inches / 69.85 mm), centered across the 203.2 mm body depth at 101.6 mm from either front or rear. The former bottom B hole was moved, not retained as another opening. This gives 11 holes at 9 device/pattern locations.

The four power-entry terminals were moved in the saved layout to the lower right in order 4E/4F/4G/G4, retaining their references. Contactors and the existing motor/control banks remain in place. The active cable-route model continues to use the top motor/control entries; the right pair is an alternate mounting option.

Rev I replaces the previously selected wing-nut seals with two McMaster 9357K15 gasketed fiberglass plugs to close the unused A pair. QUA 2, PACK 1, ORDER 2, COST $10.83, LINE $21.66. Each plug fits a 7/8-inch unthreaded knockout, accepts panels up to 1/4 inch thick, and includes the gasket and hex retaining nut. The approximately 0.074-inch / 1.9 mm 14-gauge enclosure wall is within that capacity. McMaster lists NEMA 6P, IP66 and IP68 ratings. No wing nut, separate gasket or additional fastener is required. Hole locations, profiles and print scaling are unchanged from Rev H.

Source: [McMaster 9357K15 product page](https://www.mcmaster.com/9357K15/), specifications, rear product image and $10.83 each price checked 2026-10-29.

## Coordinate convention

Top and bottom use distance from the physical enclosure LEFT body edge, matching the front-view left edge. Depth is measured from the REAR exterior body face. The top view looks down (rear at top). The outside left-wall view has rear at left and front/door at right. The outside right-wall view has front/door at left and rear at right; its 125 mm dimension therefore runs from the front edge. Heights are measured from the enclosure BOTTOM body edge. These are enclosure datums, not backplate datums.

Top and left-wall centers retain the prior fabrication plan. Right-wall centers use the owner-reported measurements above, with the power height recorded as 70 mm by owner direction. Nominal enclosure extents are 508 x 762 x 203.2 mm. The location views remain reduced; transfer their written dimensions. All finished-hole details and pilot circles are geometrically enlarged by 1/0.96 in the PDF so they print 1:1 when the entire portrait 11 x 17 inch page is printed at exactly 96%. The check bar is 75 PDF points and therefore prints 72 points (1 inch) at 96%. Printing this revision at 100% makes the details 4.1667% oversize.

## Locations and profile cross-reference

| Face | From left or bottom (mm) | From rear (mm) | Current type | Previous profile | Source device |
| --- | ---: | ---: | --- | --- | --- |
| Top | 390 from left | 80 | A | C1 | J3 |
| Top | 450 from left | 80 | A | C1 | J4 |
| Right | 70 from bottom | 101.6 from rear / depth center | B | C2 | J2 |
| Right | 75 below top | 125 from front (78.2 from rear) | A | Added alternate | Motor |
| Right | 135 below top | 125 from front (78.2 from rear) | A | Added alternate | Controls |
| Left | 690 from bottom | 75 | C | C3 | H1 |
| Left | 690 from bottom | 125 | C | C3 | H2 |
| Left | 420 from bottom | 100 | D | C4 | SW1 |
| Left | 190 from bottom | 100 | E | C5 | J1 |

## Hole details

- A: four round holes, diameter 22.2 mm (7/8 inch), for the selected 1/2-trade LFNC fittings. This retains the existing drawing callout; 7/8 inch is exactly 22.225 mm. The old gland models remain routing proxies.
- B: one round hole, diameter 28.2 mm (1-7/64 inch), for the selected BNSPDX-23-W mains gland. This retains the existing drawing callout; 1-7/64 inch is exactly 28.178125 mm.
- C: two round indicator holes, diameter 22.5 mm.
- D: one three-hole pattern: center diameter 10 mm shaft hole and two diameter 4.3 mm mounting holes, each 15 mm from the center along enclosure depth. Actual mounting-hole centers are at 85 and 115 mm from the rear at 420 mm height.
- E: one double-D opening, major diameter 15.4 +0.1/0 mm and 13.6 +0.1/0 mm across flats. Flats are parallel to enclosure height. Rev G shows a drilled 1/2-inch (12.7 mm) starter, then filing to the finished double-D boundary. The hatched region is exactly the final opening minus the drilled circle. This is the finished-hole profile, not the prototype cutter or die profile.

Nine device/pattern locations produce 11 physical holes. Types A/B/C/E account for eight holes; D accounts for three. Only two A holes carry fittings at a time; the other pair is sealed. No device references, coordinate tables, rail/duct information or wire data appear on the drawing.

## Pilot holes and punch identification - Rev G

| Type | Pilot or starter | McMaster punch assembly | Basis |
| --- | --- | --- | --- |
| A | 1/2 inch (12.7 mm) | 34685A265 | Catalog: 7/16 inch stud, 7/8 inch finished hole; rated through 1/8 inch steel. |
| B | 7/8 inch (22.225 mm) | 34685A186 | Catalog: 3/4 inch stud, 1-7/64 inch finished hole; rated through 1/8 inch steel. |
| C | 1/2 inch (12.7 mm) | 34685A218 | Catalog: 7/16 inch stud, 22.5 mm finished hole; rated through 1/8 inch steel. |
| D | 1/8 inch (3.175 mm) at all three centers | N/A - drill | Shop pilot selection for subsequent 10 mm and 4.3 mm drilling; no knockout punch is specified. |
| E | Drill 1/2 inch (12.7 mm), then file | N/A - drill and file | The round starter is entirely inside the finished double-D, including the minimum 13.6 mm across-flats boundary. |

McMaster directs the user to drill a hole larger than the draw stud. The sheet selects 1/2 inch for the two 7/16-inch studs, and 7/8 inch for the 3/4-inch stud. These are drawing-selected clearance sizes, not a claim of a McMaster-published minimum. Greenlee's driver setup guidance independently uses these 1/2-inch and 7/8-inch pilot sizes for small and 3/4-inch draw-stud configurations. B's starter may be opened with the A punch after first drilling its 1/2-inch pilot.

The PN labels identify full punch/die/stud assemblies, not replacement dies or studs. In particular, 34685A17 in the custom-tool reference folder is a replacement die and is not a complete punch assembly.

D and E are explicitly marked N/A rather than assigned an unsuitable punch. The catalog's small 1/2-inch actual-hole punch 34685A27 is listed for only 1/16-inch steel, below the enclosure's approximately 0.074-inch sheet thickness, so it is not specified for E. The existing custom double-D prototype package is unchanged; its 13.3 mm guide-clearance pilot applies to that prototype process, not the drill-and-file method drawn here.

## Source evidence

- Previous enclosure drawing: page 2 of `Backpanel_screw_locations.pdf`, Rev E, 2026-10-23. Its pre-revision SHA-256 was `71d4ef8ea9047537395d408a49b43b995ff3810969b80bfde51f1e5efb378522`. The top and left-wall center locations and all functional hole types derive from that sheet; Rev H adds the two owner-measured right-wall alternatives and relocates B.
- Saved native PCB SHA-256: `04f916bcc7674bb8db68ffcfc75c5fe25b5ecf4fd1e167e0c03079a843f9d11f`. The saved-board placement was re-read with native KiCad. J2 is now at X=485, Y=415, rotated 90 degrees, with the gland axis centered in enclosure depth. As previously documented, the fabrication drawing uses rounded/common datum targets rather than copying every native proxy origin.
- [TE T4171310004-001 customer drawing B2](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=T417131000X00L&DocType=Customer+Drawing&PartCntxt=T4171310004-001): E diameter/across-flats limits. Local copy: `_parts/datasheets/T4171310004-001_Drawing.pdf`.
- [BACO catalog 803, printed page 200](https://bacocontrols.com/wp-content/uploads/Baco-Controls-Catalog-803.pdf#page=202): D shaft/mounting-hole pattern, diameter 10 and diameter 4.3 with 15 mm each side.
- Shared local Schneider datasheets `XB4BVB1_XB4BVB1.pdf` and `XB4BVB4_XB4BVB4.pdf`: 22.5 mm recommended indicator hole.
- Shared local Hammond `EN4SD30208GY_Drawing.pdf` and Bimed `BNSPDX-23-W_Drawing.pdf`: enclosure body and gland identity.
- `Double_D_punch/Rev_A/Design_parameters.json`: independently agrees with the E finished-hole limits. Its tooling qualification status is unchanged.

Additional live sources checked 2026-10-29:

- [McMaster 7/8-inch punch catalog](https://www.mcmaster.com/products/hole-punches/hole-diameter~7-8-1/): 34685A265 and its 7/16-inch stud.
- [McMaster draw-stud/punch catalog](https://www.mcmaster.com/products/draw-studs/): 34685A186, 34685A218, steel capacities, and stud dimensions. The PDF PN labels link directly to the three catalog parts.
- [Greenlee LS60L operation manual](https://greenlee-cdn.ebizcdn.com/media/52047673REV03.pdf), setup page 9: 1/2-inch pilot for the small-stud configuration and 7/8-inch pilot for the 3/4-inch draw stud.

## Verification

The sheet is portrait 792 x 1224 points with 11 face-view hole profiles and nine A/A/A/A/B/C/C/D/E location tags. Written right-wall locations are 75/135 from the top, 125 from the front, and power 70 from the bottom / 101.6 from the front. All callout leaders remain 45 degrees. All seven detail profiles, all pilot circles and the scale bar retain the 1/0.96 compensation and print 1:1 at 96%. The hatched E filing region and punch assignments are unchanged.

The combined drawing retains its original first page and uses the same Rev I enclosure page as the standalone PDF. The approved standalone backpanel sheet and the user's saved schematic edits are preserved. Rev I changes only the seal specification and revision text. The preceding right-face revision's native placement and route checks retain every unrelated contactor/terminal position and every unrelated track. All 126 wire endpoint identities, gauges and terminations are retained; only eight cut lengths change in that preceding revision.
