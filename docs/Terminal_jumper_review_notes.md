# Terminal jumper guide - review notes

Review B, 2026-10-28. Companion to `Terminal_jumper_installation_guide.pdf`.

## Basis

- Saved board: `kicad/powermatic_1200/powermatic_1200.kicad_pcb`.
- Board SHA-256: `b738d5c0a8aec3e600c9eabf21a384ae3e65b1bcc55b7f4382337b39da2ae1b6`.
- Schematic SHA-256: `ec05a769f229676cdc260f3afbc86aff7428d5f3d3a0f636fb506abe6cc74894`.
- Extracted direct JMP-to-JMP tracks from the saved board; each numbered bank is one connected component of gray feedthrough blocks. All members are consecutive in their rail and share the same pad net.
- Circuit names also exist in the current exported schematic netlist. The terminal-block placements are board-level layout items; this is not a claim that terminal symbols were checked in the schematic.
- The supplied installation photo confirms the broad module arrangement. Individual terminal labels are not readable, so the as-built terminal identities still need review.

## Current jumper list

| Guide ID | Rail | Terminal order, left to right | Net | Poles |
| --- | --- | --- | --- | --- |
| 01 | Upper | 1A + 1B | M1_T1 | 2 |
| 02 | Upper | 1C + 1D | M1_T2 | 2 |
| 03 | Upper | 1E + 1F | M1_T3 | 2 |
| 04 | Upper | 1K + 1L + 1M | DIRECTION_ENABLE | 3 |
| 05 | Upper | 1N + 1P | DIRECTION_FWD_CMD | 2 |
| 06 | Upper | 1Q + 1R | DIRECTION_REV_CMD | 2 |
| 07 | Upper | 1S + 1T | CONTROL_RUN_ENABLE | 2 |
| 08 | Middle | 2A + 2B + 2C + 2D + 2E + 2F | 0V | 6 |
| 09 | Middle | 3A + 3B + 3C | CONTROL_RUN_ENABLE | 3 |
| 10 | Middle | 3D + 3E + 3F | HIGH_SEQUENCE_ENABLE | 3 |
| 11 | Middle | 3G + 3H | HIGH_SEQUENCE_TRIGGER | 2 |
| 12 | Middle | 3J + 3K | LOW_SEQUENCE_ENABLE | 2 |
| 13 | Lower | 4B + 4C + 4D | +24V | 3 |
| 14 | Lower | 5A + 5B | L1_SW | 2 |
| 15 | Lower | 5C + 5D | L2_SW | 2 |
| 16 | Lower | 5E + 5F | L1_DIR | 2 |
| 17 | Lower | 5G + 5H | L2_DIR | 2 |
| 18 | Lower | 5J + 5K | L3_DIR | 2 |

## Review findings

- Current saved board: **18 independent bar sections, 44 contact poles, 26 gray-block adjacent links**. Cut tally: thirteen 2-pole, four 3-pole, one 6-pole section.
- `WIRING_STANDARD.md` now includes the current 18-bank / 44-pole / 26-link allocation, including 2F in the 0V bank and all four middle-right sequence-control banks.
- One pack of five KN-10J12 ten-pole bars still covers the plan. The new allocation uses all five stock bars and leaves six poles, rather than one full spare bar. BOM quantities were not changed.
- 4E, 4F and 4G are three separate incoming phase terminals: no jumper between them. 4A and all other gray blocks without a teal bridge remain unjumpered.
- 5C and 5D are adjacent members of the same L2_SW bank.
- The two drawn PE JMP links (G1/G2 and G5/G6) represent rail-foot continuity, not KN-10J12 bars. No bar is specified for any of the six PE blocks. Inter-rail bonding wires remain part of the separate wire schedule.

## Stock-bar allocation

| Stock | Separate sections (guide ID / poles) | Used poles |
| --- | --- | --- |
| A | 08 / 6P, 01 / 2P, 02 / 2P | 10 |
| B | 04 / 3P, 09 / 3P, 03 / 2P, 05 / 2P | 10 |
| C | 10 / 3P, 13 / 3P, 06 / 2P, 07 / 2P | 10 |
| D | 11 / 2P, 12 / 2P, 14 / 2P, 15 / 2P, 16 / 2P | 10 |
| E | 17 / 2P, 18 / 2P | 4 |

## Manufacturer references

- [AutomationDirect Konnect-It accessories: KN-10J12 compatibility and jumper-screw torque](https://cdn.automationdirect.com/static/specs/konnectacc.pdf). 10 poles per bar, 5 bars per pack; screw-down KN-T12-compatible jumper; 0.4-0.6 N m / 3.5-5.3 lb-in.
- [AutomationDirect Konnect-It overview: separators, end covers, and top covers](https://cdn.automationdirect.com/static/specs/konnectoverview.pdf).
- [KN-G12SP-10 grounding terminal](https://www.automationdirect.com/pn/KN-G12SP-10); shared local OEM cut sheet confirms the electrical connection to 35 mm DIN rail through the clamping foot.

## Review status

Review B uses the approved module/letter labels, with I/O skipped and G1-G6 for grounds. All 63 saved board terminal references, documentation and wire-schedule endpoints were updated together. Footprint placement, pad numbers, nets, tracks, wire lengths and BOM purchasing fields were preserved. The saved schematic contains no terminal-block reference instances to rename. See Terminal_numbering.md for the legacy cross-reference. This guide does not verify rail-bond continuity or authorize energization.

## Verification - 2026-10-28

- Native KiCad reload comparison: all 63 terminal references follow the approved map; all 159 footprint positions/orientations, pad UUIDs/numbers/nets, and 1,265 routed track objects are unchanged.
- Refresh generated 126 wires with complete saved-net route coverage. Every wire has the same pair of endpoints after renaming, with the same endpoint termination, gauge and cut length. From/To orientation and row order follow the new reference sorting.
- Loose-stock length totals are byte-identical to the previous saved totals. BOM purchasing data and the saved schematic are unchanged.
- The separate bom_review regression suite passed all 69 tests, including conduit allowances under the new terminal references.
- Schematic ERC: 0 errors and the same pre-existing Controls:PWRM1200-MOTOR library-copy mismatch warning for M1 as before renumbering.
- The jumper guide is one portrait 11 x 17 inch page. Both rendered drawings were visually reviewed, and all 63 current terminal labels are present.
