# Saved schematic redraw review — 2026-10-06

Reviewed saved schematic SHA-256 `47d27aabec82b7e2a4e306206bafa62d9b7f740b898bb02bca52fed1f798e405` using KiCad 10.0.6 native netlist/ERC, exported artwork, cached/shared pin maps, and local part evidence. No schematic, PCB, or library edits were applied. This is a schematic connectivity review, not a commissioning or PCB validation.

## Findings

1. **K6 has no coil drive.** `Net-(K6-A1_BOT)` contains only K6.A1.TOP, K6.A1.BOT and SP6.1. Its other coil side is 0V. The high-speed supply contactor therefore cannot energize from the control circuit. K5 can energize and short T1/T2/T3 while K6 remains off. Add the intended controlled high-speed feed to K6 A1. ERC does not identify this floating passive coil/suppressor island.
2. **Dangling wire at K5 A1.BOT.** Wire UUID `4ce07e3c-8ffa-4182-b442-7ddc084cbe49` extends from (287.02, 62.23) to the unconnected endpoint (284.48, 62.23) mm. The main A1 connection is intact; this is an extra stub. Remove the stub unless it is intended to carry another connection. This is the sole current ERC warning. The ERC JSON coordinates/length are scaled differently from the schematic coordinates; UUID and source geometry locate it unambiguously.
3. **PE documentation is incomplete.** The saved PE net has only J2.G and PS1.1_BOT. There are no explicit motor-frame, panel/backplate, enclosure/door, or retained metal control-station bonding endpoints. The motor evidence explicitly says it has no factory grounding lug and leaves its frame bond as installation work. Document actual bonding endpoints separately; do not invent a motor winding pin or manufacturer terminal. This finding concerns the drawing; it does not establish whether hardware bonds exist.
4. **Old wire records reference removed terminals.** `python3 tools/wiring/generate.py --check` fails on deleted/replaced destination UUID `782cabbe-a58e-46f3-9f97-d5cf96f2f77e`. J2 still has Wire.W001/W003/W005 records targeting former terminal symbols. These do not affect KiCad electrical connectivity, but the generated schedule cannot presently be regenerated. Reconcile records with the chosen PCB-only routing model before treating that schedule as current.
5. **Minor naming: `OL1_OK` joins OL4.96 to OL6.95.** The electrical chain is correct; the name refers to an old designator. `OL4_OK` would match the present drawing.

The earlier `CCC` / `HS_COIL` mismatch was corrected by the owner's save during this review. The final net contains K4.32, K5 A1.TOP/BOT, SP5.1 and K5.43.

## Traces checked

- Unique combined contactor and overload instances; all 14 contactor and 10 overload pin numbers, functions and coordinates match the current shared symbols.
- Incoming X/Y/Z through the three fuses and disconnect; Q1 feeds PS1 from L1/L2. PS1 1_BOT is PE, 2_BOT is AC N, 3_BOT is AC L; DC output polarity is consistent. The motor evidence records a 208 V supply, within the local NDR-240 datasheet's 90–264 VAC input range.
- K1/K2 reverse the two outer phases and retain the middle phase. Their NC electrical interlocks feed the opposite coils; NO auxiliaries supply holding paths.
- LOW: S3.1.U feeds K6 NC, then K5 NC, then K4 A1. K4 feeds OL4 and T1/T2/T3.
- HIGH: S3.2.U feeds K4 NC and K5 A1. K5 explicitly shorts T1/T2/T3; K6's missing drive is the break in this path.
- S3 settled positions match the recorded bench schedule: position 1 sections 1/4/7, position 2 sections 2/3/5/6/8, OFF all open. Switch transition timing was not established by that evidence.
- OL4 95–96 and OL6 95–96 are in series ahead of the STOP NC contact. Either overload or STOP removes the control feed.
- S1's two NC contacts are in series through the matching J6/J1 four-pin links. K3's two NO contacts are in series to create +24V_EN.
- Suppressors connect across their associated coils; unused relay/overload contacts have explicit no-connect markers.

The high-speed motor outputs are currently L1→T4, L2→T5, L3→T6. The photographed manufacturer plate specifies L1→T6, L2→T4, L3→T5. The current assignment is a cyclic phase permutation, preserving phase sequence; this alone is not evidence of reversed rotation. Matching the printed mapping would make later verification clearer.

## Evidence

- `netlist.xml`, `erc.json`, `verification.json` are from the reviewed saved snapshot.
- `schematic.svg` is a native export with only its SVG viewport expanded for visibility. Much of the original drawing lies outside its A4 page; normal page exports clip it.
- Motor mapping: `_parts/reviews/Controls/evidence/motor_six_lead_map_2026-09-23.md`.
- Switch states: `_parts/reviews/Controls/evidence/drum_365_TAV2111_bench_confirmation_2026-09-23.md`.
- PSU terminal/input data: `_parts/datasheets/NDR-240-24_NDR-240-24.pdf`.

Native ERC result: **0 errors, 1 warning**. The project ignores single-global-label, four-way-junction, simulation-model and footprint-filter checks. Passive connectivity checks do not establish contactor operating logic or hardware safety.
