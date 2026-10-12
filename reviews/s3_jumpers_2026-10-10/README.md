# S3 retained jumper connectivity

The owner saved the revised `Controls:365-TAV2111_Top` drawing and exited
KiCad before this change. The saved library and placed S3 already contained
the revised drawing. Every pre-existing source byte is preserved except for
one native jumper-group block in each of the four affected files.

Six native electrical groups represent three long and four short straps:

| Electrical group | Physical straps |
| --- | --- |
| 1B, 2B | Long 1B–2B |
| 1T, 3T | Short 1T–3T |
| 3B, 4B, 5B | Long 3B–4B and short 3B–5B |
| 4T, 6T | Short 4T–6T |
| 5T, 7T | Short 5T–7T |
| 7B, 8B | Long 7B–8B |

`jumper_pin_groups` is set on the shared `365-TAV2111` symbol and its project
schematic cache. `jumper_pad_groups` is set on the shared footprint and placed
S3. Duplicate-number jumper behavior remains disabled; all sixteen existing
terminal IDs are preserved. The external terminals remain 1B, 1T and 2T;
6B and 8T remain unwired.

The drawing, model links, pads, net assignments, metadata, reference, position,
rotation and all PCB routes are unchanged. No copper tracks are introduced
for the seven straps. Native jumper groups count toward electrical coverage,
while the existing schedule extractor reads physical wires from tracks.

Native before/after schematic netlists are identical. PCB DRC retains the same
149 existing violations and nine existing parity findings; unconnected items
drop from 90 to 83, removing the seven internal strap requirements. Final ERC
is recorded separately in `validation.json`.

`verify_schedule.py` makes native routing fixtures using the actual saved S3
footprint, its real sixteen pad IDs and nets, and three external 16 AWG wire
routes. Before/after wire rows are identical: three external rows, zero added
strap rows. After grouping, all connected fixture nets are covered.

The full-project schedule generator fails identically before and after this
change with `BB2.A2: missing or invalid host terminal`. The existing placed
BB2 has empty `Wire.Host.A` and `Wire.Host.B` fields. These unrelated bindings
are left untouched, and the live `Wire_schedule.csv` is not overwritten.

Native exported footprint artwork was inspected. No symbol pin geometry or
text changed; live Symbol Editor inspection was not performed. This record
does not claim the pending SYM-VIS-001 live-editor check or a clean overall PCB.
Catalog/database associations did not change, so no database rebuild is needed.

Changes remain local and uncommitted.
