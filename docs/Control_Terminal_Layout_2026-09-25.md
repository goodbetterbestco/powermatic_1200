# Controls terminal grouping review — 2026-09-25

Reviewed all 15 symbol definitions currently used by the Powermatic schematic against the controls exceptions SYM-CTRL-001/002/003. Revised 10 definitions, covering 12 units. The schematic retains 34 placed units.

This review supersedes the earlier same-day IC-style contact layouts in `Symbol_Rules_Audit_2026-09-25.md`. Physical terminal IDs, electrical types, pin lengths, unit assignments, catalog metadata, reference designators, instance identity, and pin UUIDs are preserved. There are no wires in the saved schematic.

## Changes

| Symbol / unit | Final arrangement |
| --- | --- |
| HMC-9B30-11-DS A | Left-only: A1_TOP, A1_BOT, A2_TOP, A2_BOT; AUX_NO_1/2 on 43/44; AUX_NC_1/2 on 31/32. Coil access points remain distinct physical terminals. |
| 800S-3SA A | Left-only: FWD_NC_1/2 on L1/R2, then FWD_NO_1/2 on L2/R1. |
| 800S-3SA B | Left-only: REV_NC_1/2 on L3/R4, then REV_NO_1/2 on L4/R3. |
| 800S-3SA C | Left-only: STOP_NC_1/2 on L5/R5. |
| 365-TAV2111 | Each U/L contact pair adjacent. LOW sections 1, 4, 7 at left; HIGH sections 2, 3, 5, 6, 8 at right. Names LOW1_U/LOW1_L, HI2_U/HI2_L, etc. Sides identify speed groups, not electrical input/output direction. All 16 screws remain represented. |
| XB4BVB1 | Left-only: LAMP_1/2 on X1/X2. No unsupported polarity labels added to this 24 VAC/DC lamp. |
| HTOR32-6-S B | Left-only: TRIP_NC_1/2 on 95/96; TRIP_NO_1/2 on 97/98. |
| HMX1-MI | Left-only: NC_A_1/2 on 111/122; NC_B_1/2 on 121/112. Manufacturer's crossed terminal numbering retained. |
| HMX1-SSVRC-DC | Left-only: SUP_1/2 on existing lead IDs 1/2. No polarity inferred. |
| PWRM1200-ESTOP-ASSEMBLY | Left-only: 1/3, then 2/4. Existing distinct names NC1/BRN, NC1/BLK, NC2/WHI, NC2/BLU retained. |
| PWRM1200-MOTOR | All six leads at left, grouped T1/T2/T3 and T4/T5/T6. No electrical outputs or grounding terminal invented. |
| NDR-240-24 | Retains input/output layout. Duplicated output access points now named +V_1/+V_2 and -V_1/-V_2; terminal IDs and internal common relationships unchanged. |

Two terminals of one contact are not internally common when that contact is open. Endpoint suffixes distinguish the ends of one contact; they do not create another contact. The A1 access points are internally common with each other, as are the A2 access points.

## Reviewed and retained

| Symbol / unit | Reason |
| --- | --- |
| HMC-9B30-11-DS B | Three main poles retain L1/L2/L3 on left and T1/T2/T3 on right. |
| HTOR32-6-S A | Three motor-current paths retain line/load layout. |
| 22013003 | Three-pole motor disconnect retains line/load layout. |
| FAZ-D4-2-NA-L | Two-pole circuit breaker retains line/load layout. |
| RM25030-3SR | Three fuse paths retain opposed endpoints. |
| T4171310004-001 | M12 connector retains its four stacked 2.54 mm squares and centered zero-length pins. |
| KN-T12GRY-25 | Dedicated one-section feedthrough symbol retains opposed wire connections. |

## Geometry and preservation

- Each contact pair has 2.54 mm pin spacing. Functional groups have a 5.08 mm gap.
- Bodies remain centered and sized from each unit's compact pin stack; right groups, when present, begin at the top.
- KiCad's stroke-font text widths were used to choose the narrowest fitting body width on the existing horizontal grid.
- Reference and Value remain centered above each placed unit; Part Name remains centered below.
- The pendant FWD unit and motor instance moved up 5.08 mm to clear the next symbol's labels. All other instance anchors are unchanged.
- All 35 other Controls library definitions are unchanged.
- 50 terminal display names changed. No terminal IDs, types, lengths, units, or connectivity changed.
- Existing photo-based numbering and assembly-identity qualifications remain; no new physical evidence is claimed.
- The prior six HMC B units versus five A units discrepancy remains. No placed unit was deleted.
- Existing A4 page-frame overflow remains outside this symbol-layout change.

## Evidence and validation

- HMC contactor cut sheet, drawing, and HMC/HTOR instruction manual: duplicate A1/A2 access and 1NO + 1NC auxiliary inventory.
- `IronHorse_HMC_HTOR.pdf`, page 20: HMX1-MI 111–122 and 121–112 contact pairs.
- Same catalog and HTOR32-6-S sources: 95–96 NC and 97–98 NO.
- XB4BVB1 datasheet, page 1: X1–X2, 24 VAC/DC.
- HMX1-SSVRC-DC cut sheet/drawing: two-lead coil suppressor.
- Existing pendant photos and terminal mapping, drum switch photos and bench confirmation, E-stop corrected pin map, and motor connection plate: preserved physical mappings.
- Automated checks passed for pin identity, intended names, unit allocation, electrical types, visible pins, unique connection points, geometry, metadata, schematic cache agreement, instance UUIDs, and field placement.
- Native KiCad schematic SVG export passed; rendered geometry and all affected placed units were visually checked.
- Native KiCad 9 editor reload passed: canonical schematic opened with a clean title; all 34 placed units visible and checked.

The catalog CSV and database mappings did not change; a database rebuild is not needed for these library geometry and pin-name changes.
