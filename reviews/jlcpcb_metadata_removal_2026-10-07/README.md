# JLCPCB metadata removal — 2026-10-07

Removed the seven `JLCPCB` properties (Class, Assembly, Part, MPN, Match, Checked UTC, Source) from the project PCB and schematic after the owner confirmed both editors were saved and editing paused.

- PCB: 133 properties removed across 19 footprints.
- Schematic: 112 properties removed across 10 placed symbol instances and 6 cached library symbols.
- Parsing and comparing the complete S-expression trees confirmed that every other element remained unchanged, including placement, geometry, nets, UUIDs, model transforms and other metadata.
- Both staged and final files passed native KiCad parsing: PCB position export and schematic netlist export.

`before/` preserves the exact saved files immediately before this edit. `validation.json` records hashes and field counts. Shared parts libraries and database configuration were outside the requested project edit; library updates or new database-symbol placements can reintroduce these fields.
