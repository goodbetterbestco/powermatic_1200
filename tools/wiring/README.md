# Schematic-owned wiring

Wire records in the saved `.kicad_sch` file are authoritative. The PCB supplies
terminal positions and duct geometry. The generated CSV is a review output.

Start the generated review from Finder with **Generate Wiring Review.app**, or:

```sh
python3 tools/wiring/generate.py --open
```

The launcher reuses one localhost reviewer and does not open a Terminal window.
The generated review is read-only: Find, sorting, flags and copying work, but
cell edits and Overwrite are disabled. Save CSV downloads a report copy.

## First section

The first six records cover the incoming phases only:

| Wire | From | To |
|---|---|---|
| W001 | J2.X / L1 | TB40.BOT |
| W002 | TB40.TOP | FH1.P1.A |
| W003 | J2.Y / L2 | TB41.BOT |
| W004 | TB41.TOP | FH1.P2.A |
| W005 | J2.Z / L3 | TB42.BOT |
| W006 | TB42.TOP | FH1.P3.A |

These records are **pending review**. The three mains rows measure panel tails
through the power gland. They do not replace the overall external cable allowance
in the BOM. Existing cut estimates are retained as minimums during migration.
Automatic cuts use the modeled route plus 200 mm, rounded upward to 50 mm.

The chosen feedthrough convention is TOP/BOT as actual schematic pin and footprint
pad numbers. The transition keeps the PCB placement and pad coordinates unchanged;
native netlist comparison checks that renamed pins keep their original connections.
The three PE blocks are reviewed separately from the feedthrough block symbol.

The legacy 91-row `Wire_schedule.csv` has been preserved. Six rows have been
migrated; 85 remain for section-by-section reconciliation. Generating a partial
schedule cannot overwrite the legacy file. Coverage in the generated report
shows which electrical nets have a complete physical connection plan.

## Add or edit a wire

Use actual KiCad pin numbers in commands. The CSV displays the selected human
labels, such as L1/L2/L3 and TOP/BOT.

```sh
python3 tools/wiring/records.py list
python3 tools/wiring/records.py set W001 --length 500
python3 tools/wiring/records.py set W001 --length auto
python3 tools/wiring/records.py set W001 --review reviewed
python3 tools/wiring/records.py set W002 --from TB40.TOP --to FH1.P1.A
python3 tools/wiring/records.py add W007 --from FH1.P1.B --to SW1.1 \
  --section '02 Fuse outputs and disconnect' --awg 14 \
  --term1 'Ferrule 14 AWG; L=TBD mm' --term2 'Ferrule 14 AWG; L=TBD mm'
python3 tools/wiring/generate.py
```

Save current KiCad edits before changing records through the helper. Reload the
schematic with **File → Revert** after an external record update, before making
more editor changes. The helper refuses to overwrite a file that changed while
it was checking the new record.

Records are hidden `Wire.W001`, `Wire.W002`, etc. properties on each wire's origin
symbol. Each is a JSON object with its origin pin, target symbol UUID and pin,
section, gauge, termination text, connection kind, length policy and review state.
Endpoint UUIDs let reference renumbering follow the same physical symbol. Deleting
and replacing a symbol intentionally requires relinking its wire records.
An explicit origin UUID prevents copied symbols from silently duplicating the
original wire list. Inherited records on other copies are ignored and reported.
`WireName` and `WirePin.<number>` fields control output names without changing the
symbol's electrical pin numbers. No extra parts, pins or graphics are introduced.

## Connection kinds

- `wire`: an assembled/installed conductor.
- `panel_cable_core`: an assembled panel tail of an external cable.
- `factory`, `internal`, `bridge`, `plug_cable`: documented fixed connections,
  excluded from assembly rows.

The generator never assumes a complete wire list from a many-pin net. Separate
terminal-block bridges must be recorded. Only the known feedthrough/PE blocks'
internal pin connections are implicit. Factory straps and plug-in M12 conductors
are not inferred as new assembly wires.

## Routing and validation

The board's horizontal ducts are split into top/bottom halves. Vertical ducts
are not split. Device TOP/BOT ports use the duct immediately above/below their
device. Sidewall and gland endpoints use the closest open duct end. Same-whole-
duct paths use the target half's centerline; different whole ducts use whole
centerlines and the vertical trunk. This version supports one vertical trunk.

Every record must resolve to real schematic pins on the same connected net.
Directly drawn wire paths are also checked for the wrong physical terminal clamp,
even when TOP/BOT are electrically common. Missing PCB pads, deleted symbols,
duplicate records and inconsistent routing endpoints stop generation. Conflicting
unrecorded sections are not silently filled in from legacy data or caption text.

Outputs:

- `reviews/wiring_generated/Wire_schedule_generated.csv`: generated eight-column review.
- `reviews/wiring_generated/review.md`: section, length and coverage review.
- `reviews/wiring_generated/Wire_schedule_generated.source.json`: derived audit/provenance.

The exporter checks saved file hashes so a concurrent save cannot publish a mixed
schematic/PCB snapshot. `--check` validates without writing; `--section` filters a
single recorded section. Estimated wire lengths remain estimates for review.

Unannotated symbols in other unfinished sections receive temporary references only
in the export snapshot. Their drawing and saved names are preserved. Generation
stops if an unfinished symbol shares a recorded wire net; other unfinished sections
are listed in the coverage report without blocking the current section.

## Checks

```sh
python3 -m unittest discover -s tools/wiring -p 'test_*.py'
python3 tools/wiring/generate.py --check
```
