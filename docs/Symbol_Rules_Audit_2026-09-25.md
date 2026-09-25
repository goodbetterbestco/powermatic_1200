# Powermatic schematic symbol review - 2026-09-25

Controls terminal layouts were subsequently revised under the controls exception; see [Control Terminal Layout Review](Control_Terminal_Layout_2026-09-25.md). The results below describe the preceding audit snapshot.

Audited all 15 symbol definitions used in the saved schematic: 19 distinct library units and 34 placed units. The 42 current symbol rules were evaluated for every definition (630 checklist entries). There were 515 passes, 104 not-applicable entries and 11 retained source/numbering qualifications. No electrical pin mapping was changed.

## Corrections

| Item | Correction |
|---|---|
| All 34 placed units | Repositioned Reference and Value above the body and Part Name below it. Removed automatic-field-placement flags from these instances. All 102 visible field positions now follow each unit's own body. |
| M12 panel socket T4171310004-001 | Centered the labels above and below the four-square column; removed the placed right justification. Pin order 1-4 and zero-length center pins retained. |
| HMC-9B30-11-DS unit B | Reduced body height from 20.32 to 10.16 mm; three power poles use y=+2.54, 0, -2.54 mm. |
| HTOR32-6-S unit B | Reduced body height from 10.16 to 7.62 mm; two contact rows use y=+/-1.27 mm. |
| 800S-3SA unit C | Reduced STOP body height from 7.62 to 5.08 mm; its two terminals use y=0. |
| HMC-9B30-11-DS unit A | Reduced body width from 20.32 to 15.24 mm while retaining the coil group and all auxiliaries. |
| 365-TAV2111 | Reduced body width from 20.32 to 15.24 mm. Native KiCad text metrics confirm the opposing labels fit. |
| NDR-240-24 | Increased body width from 10.16 to 15.24 mm to separate opposing input/output names. |

The library changes affect five definitions. The other 40 Controls definitions are unchanged. The schematic's symbol anchors, UUIDs, unit assignments, pin UUIDs, field values and metadata are preserved. It currently contains no wires.

## Contactor terminal inventory

The apparent duplicate auxiliary labels represent the two ends of each real contact:

| Contact | Terminals |
|---|---|
| Normally open auxiliary | 43-44 |
| Normally closed auxiliary | 31-32 |

All four auxiliary pins remain. The saved exact-model AD data sheet specifies one NO and one NC auxiliary. The reviewed pin manifest records 43NO/44NO and 31NC/32NC. The manufacturer's HMC/HTOR instruction drawing also shows separate A1/A2 coil access at both ends. A1.TOP, A1.BOT, A2.TOP and A2.BOT therefore remain four separate connection points with their existing library qualifiers.

Sources: `_parts/datasheets/HMC-9B30-11-DS_Datasheet.pdf`, `HMC-9B30-11-DS_Drawing.pdf`, `HMC_Contactor_Instructions.pdf`, and `reviews/Controls/pin_manifest.json`. Previously reviewed pin inventories and unchanged local source hashes were checked across the audit. [TE's current product page](https://www.te.com/en/product-T4171310004-001.html) confirms the M12 receptacle has four contacts; its existing drawing-backed pin assignment is retained.

## Rules clarified

- SYM-BODY-001: size each unit from its own compact pin stack; do not enlarge it to match another unit.
- SYM-GRID-001 and SYM-GRID-003: derive the odd/even grid separately for each unit.
- SYM-TEXT-004: verify placed fields as well as library defaults; automatic placement must not put Part Name above the body or connector fields at the side.

KiCad shares library property anchors between units. The placed schematic fields are consequently positioned per unit, rather than enlarging the smaller unit to fit shared library field positions. A single feedthrough terminal retains its dedicated two-clamp symbol; it is not treated as a multi-contact plug/socket column.

## Remaining placement findings

1. There are five HMC coil/AUX A units but six power-pole B units. All are unannotated, so the extra B unit is flagged rather than deleting an arbitrary user placement. B-unit positions (mm): (58.42,83.82), (87.63,86.36), (114.3,88.9), (139.7,90.17), (165.1,87.63), (201.93,87.63).
2. The existing motor and E-stop placements extend past the A4 drawing frame, and the lower row occupies the title-block region. This is page arrangement, not library geometry; original placements and page size are preserved.

The 11 source qualifications concern documented local terminal identifiers, field-terminal modeling boundaries and installed assembly identity. They are retained in the rule checklist, not inserted into symbol definitions. This is a symbol/rules review, not a completed circuit/ERC signoff.

## Verification

- All physical pin IDs, names, electrical types, pin lengths and unit memberships preserved.
- No duplicate pin IDs, hidden pins or stacked connection points.
- All bodies centered; compact height, odd/even pin grid, side anchors and minimum legible widths checked.
- All visible placed fields centered on the 1.27 mm grid and clear of their own bodies.
- All 19 unit geometries and all 34 placed instances checked in native KiCad schematic output.
- Native KiCad 9 editor reload passed: saved canonical schematic opened with a clean title; all 34 placed units visually checked.
- Catalog metadata unchanged; no database rebuild needed.

Checklist and machine-readable results: `_parts/reviews/Powermatic_Schematic_2026-09-25/rule-checklist.csv` and `validation.json`.
