# PCB migration — 2026-10-06

The saved PCB was migrated in place after the owner confirmed both KiCad editors were saved and editing paused. All **87 original footprint UUIDs, positions, rotations and layers** are retained. No footprint was added, removed, moved or replaced. Component graphics, STEP models, board graphics and groups are preserved. The schematic, project settings and project footprint-library table are byte-identical to the checkpoint.

All **19 schematic-based footprints** now carry their current symbol links and exact native-export pad nets. References OL1/OL2 become OL4/OL6; suppressors SP3/SP4/SP5 become SP4/SP5/SP6 without changing which contactor each physical suppressor accompanies. PS1's seven pads were renamed in place to the current symbol terminal IDs. The shared PSU footprint received the same naming correction.

All **68 PCB-only footprints** have the native Not in schematic flag. The 29 gray feedthroughs retain TOP/BOT native jumper pairs, with all 58 pad-net assignments cleared at the owner's request for routing later. The three PE blocks remain assigned PE with a common 1/2/PE jumper group. MI1/MI2 retain their geometry and positions; obsolete schematic links and unused contact-net metadata are removed.

The glands are PCB-only native jumpers: mains J3 has four pairs/eight pads; motor J4 has six pairs/twelve pads; controls J5 has eight pairs/sixteen pads. Existing conductor functions were reconciled to current net names. Controls pair 8 remains unassigned. The virtual pads represent continuous cable conductors, not electrical gland terminals or a manufacturing land pattern. Their paired IDs are .IN/.OUT. Mechanical gland outlines, mounting datums and STEP models remain unchanged.

Native KiCad 10.0.6 validation:

- ERC: **0 errors, 0 warnings**.
- Schematic parity: **99 findings before → 0 after**.
- Layout DRC: **293 findings before and after**, with identical type/severity counts and identical non-silkscreen findings by item UUID. Silkscreen overlap reporting selects different pairs among the unchanged overlapping artwork.
- Unconnected items: **157 before → 93 after**. The board is intentionally awaiting routing and terminal allocation; this reduction is not completed routing.
- Native load checks confirm 87 retained footprints, 19 schematic links, 68 PCB-only footprints, 29 unassigned gray blocks, and gland counts 8/12/16 pads.
- Native serialization retains all jumper groups. An isolated gland fixture has zero violations and zero open connections; removing only its 18 jumper groups creates exactly 18 open connections.
- Native full-board and gland-fixture SVG exports were rendered and visually inspected without desktop capture. The board-area preview clips hardware outside the backplate; the separate gland fixture shows all conductor ports.

Six shared footprints were updated: the three glands, PSU pad IDs, and PCB-only defaults for HMX1-MI and KN-G12SP-10. All other library assets are unchanged by this migration. Existing legacy layout findings remain; this is a synchronized visual-placement artifact, not a fabrication or commissioning signoff. Old schematic Wire.Wxxx records still reference removed terminal symbols; wire-schedule reconciliation is separate from this PCB migration.

## Editor reload and future updates

Reopen the PCB or use File → Revert so the editor reads the migrated file before further editing. Normal future Update PCB from Schematic runs should use UUID matching, with reference-based relinking off. Intentional PCB-only parts now have deletion protection. Retain the conservative replacement/deletion settings when preserving this established placement. Existing terminal pads are ready for net assignment during routing.

## Recovery and evidence

`before/` contains the exact saved project checkpoint. `library-before/` contains all six original shared files. `validation.json` contains source hashes, reference/net mappings and native results. Native reports, netlist, previews and the staging/verification scripts are preserved alongside it. Copies of the shared-footprint evidence are in `_parts/reviews/Controls/PCBMigration_2026-10-06/`.
