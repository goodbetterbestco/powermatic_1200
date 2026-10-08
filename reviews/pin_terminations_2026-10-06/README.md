# Pin termination draft — applied 2026-10-06

The owner selected one combined description field per pin. The active schematic
now has 184 `Termination.<actual pin number>` fields across all 25 physical
schematic symbols. Power flags/power symbols are excluded. Fields are hidden on
the drawing and editable in Symbol Properties or the Symbol Fields Table.

Descriptions were populated from the existing schematic wire records and legacy
`Wire_schedule.csv`, with its old device/pin names mapped to current IDs. Current
`Wire.Sizes` AWG values override obsolete legacy gauges. The current motor-end
Wago plan takes precedence over the legacy motor-PE ring entry. The source
schematic, PCB and project were captured in `before/`; source hashes were checked
before the atomic write. The prior editing pause remained in effect and no
desktop UI or screen-sharing tools were used.

Individual recorded terminations are retained, including twin ferrules. Where
no pin-specific description exists, the draft uses the existing ferrule profile
for that same part type. This inheritance is identified in the provenance file.
Recorded ferrule lengths, remote-terminal selections and ring dimensions were
not invented or researched; existing TBDs remain for the requested review.
Supplied suppressor forks, factory pigtails, retained jumpers, mating interfaces,
direct-mounted connections and unused pins are described as separate categories.

`terminations.md` is the complete per-pin review and description inventory;
`terminations.json` is derived from the installed custom fields.
`powermatic_1200.termination-provenance.json` records the initial mapping and its
source descriptions. Review edits belong in the schematic fields, then refresh
with `python3 tools/wiring/terminations.py --report reviews/pin_terminations_2026-10-06/terminations.md`.
The populate/stage command preserves an already-existing Termination field rather
than overwriting a user's reviewed selection.

All 27 wiring tests pass. Native KiCad export preserves every one of the 184
termination fields and every original net membership. Removing only these fields
from the candidate gives the exact original parsed schematic: no existing sizing
fields, symbols, cached libraries, pins, wire geometry or labels changed. Candidate
and installed ERC each report zero errors and zero warnings under existing settings.
The PCB, project settings, shared library and BOM were not changed.

The summary counts pin fields, not hardware purchasing quantities. PCB-only
terminal blocks, glands and enclosure studs do not have schematic symbols;
they were not assigned footprint fields or new schematic symbols in this task.
The legacy ring entries target those mechanical endpoints, except the obsolete
motor-PE entry superseded by the current splice plan. No new loose-wire ring or
fork part number is selected by this population. Terminal allocation and the
actual physical conductor count remain separate work.

Reload the schematic with File → Revert before editing, so the native editor reads
the externally added fields. The installed file was validated through native CLI
exports/ERC; no desktop reload was performed.
