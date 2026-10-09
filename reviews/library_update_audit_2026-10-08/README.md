# Schematic library-update audit — 2026-10-08

The saved schematic has ten library-symbol-mismatch warnings and no ERC errors.
All ten instance caches were compared with the current Controls definitions selected
by their non-LCSC catalog records. The pin sets, names, electrical types, full pin
definitions (including coordinates, lengths and text styles), body geometry and
root electrical/placement attributes agree.

| References | Part | Pins per symbol | Electrical/drawing differences |
|---|---|---:|---|
| SP1, SP2, SP4, SP5, SP6 | HMX1-SSVRC-DC | 2 | None |
| FH1 | RM25030-3SR | 6 | None |
| SW1 | 222102 | 6 | None |
| K3 | HC3096N-52-900-24 | 10 | None |
| Q1 | FAZ-D4-2-NA-L | 4 | None |
| PS1 | NDR-240-24 | 7 | None |

The cached copies contain database-added Part ID, Supplier, Supplier PN, inventory
and footprint-filter properties not present in the underlying Controls templates.
K3 also has catalog Package=DIN-RAIL, while its underlying template Package is empty.
These differences do not alter the connection interface. This identifies the source
of the underlying-definition differences, but does not claim every metadata detail
of KiCad's runtime database-generated symbol has been reproduced.

## Update settings

Update only these ten selected instances. Uncheck all Update/Reset Fields selections
and disable Remove fields if not in library, Reset fields if empty in library,
Update/reset field text, visibilities, sizes/styles and positions. Leave Reset alternate
pin to default off. Preserve Wire.*, Termination.*, Mounting, exact MPN, footprint
and the drafted reference/value/Part Name positions.

Run ERC and compare the native netlist after the actual editor update. A temporary
metadata-only cache comparison copy preserved all net memberships, pin functions
and electrical types, but still produced ten warnings. It is not a native editor
update and is not a candidate to install; clearance of the warnings remains to be
verified after the actual library update.

No schematic, PCB or shared-library source files were modified by this audit.
The PCB DRC CLI aborted with exit 134 before producing a report. The owner's
exported PCB-editor DRC report is needed to classify the approximately 300 findings.

This is an electrical-equivalence and structured drawing comparison. No fresh
visual or live Symbol Editor review was performed in this audit; SYM-VIS-001
remains outside this check and no full library-review completion is claimed.

[KiCad update-symbol documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#updating-and-exchanging-symbols)
