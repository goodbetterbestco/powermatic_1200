# Live schedule extraction

`kicad_schedules.json` connects the shared `bom_review` Finder launcher and Refresh
server to this project's `extract.py`. Each mode has exactly one live CSV:
`Powermatic_BOM_revP.csv` and `Wire_schedule.csv`. Successful extraction overwrites
that file. Failure preserves it. No CSV versions or backup files are retained.
Make any desired copies elsewhere yourself.

The browser/editor, source-tag preservation, generic BOM row merge and refresh
transaction live in `/Users/evanthayer/Projects/bom_review`. This adapter reads
the saved schematic and PCB and applies Powermatic's component/wire rules.

## BOM ownership

- SOURCE=KiCad: linked to a stable SOURCE KEY and refreshed from modeled parts.
- SOURCE=Local: purchasing-only data remains in this CSV and survives refresh.
- KICAD QTY: modeled piece count, independent of purchasing QUA and packaging.

Initial tagging only adds these columns; it preserves every existing nine-column
cell. Matches use unique saved MPN/supplier identifiers, whole identifier tokens
in vendor-prefixed SKUs or unique part names. Ambiguous rows stay Local.

Refresh updates a linked part's name where KiCad provides one and its modeled
count. Local purchasing quantity, price, packaging, supplier and supplier SKU
are retained. Explicit `BOM.PACK`, `BOM.UNIT`, or `BOM.COST` KiCad fields can
supply those purchasing fields when present. Newly specified native parts are
added with purchasing quantity left for the user. Deleted linked parts are
removed; Local entries are kept.

This is a panel BOM. Existing purchasing rows can link to mechanical Controls
models even when those models are excluded from a conventional PCB BOM. Their
modeled quantities include available graphics and are informational until
physical allocation. Such excluded models do not create new purchasing rows.
Metadata-only footprints are not counted again; schematic units and placed
footprints representing the same component are counted once. Assemblies without
an actual part identifier are not automatically added as new purchasing SKUs.

## Wiring ownership

The saved PCB traces are the physical wire source. A continuous pad-to-pad
path produces one wire row. Connected segments, bends, arcs and via layer changes
remain within that wire. A terminal met along the path splits it into separate
wires. Branches away from a terminal/splice footprint are rejected as ambiguous;
unfinished paths are omitted and reported. Cable-gland IN/OUT routing markers
continue the same wire, using their saved jumper groups, rather than becoming
extra wire ends. Unused block graphics produce no wires.

Endpoint nets are checked against the saved schematic. Board-only unassigned
clamps acquire the circuit from their actual traced connections for export;
different nets on internally common clamps are rejected. The exporter does not
write back to KiCad or assign pad nets in the source file.

AWG comes from footprint `Wire.AWG.<pin>` overrides, schematic `Wire.Sizes`, or an
existing gauge-bearing termination selection. Missing/conflicting sizes stay
blank with a warning; copper trace width is not interpreted as a wire gauge.
Terminations come from footprints. Generic block fields resolve to single or
twin ferrules based on the number of completed routed wires sharing that clamp.

LENGTH is a cut estimate: native route length plus 100 mm, rounded upward to
10 mm. Native arcs use curved length.
Vias are drawing-layer transitions and add no physical via/PCB-thickness length.

Stale sizing metadata produces warnings and cannot supply an outdated gauge.
Conflicting nets on internally common block clamps are reported without hiding
the recorded routes. These wires have `net-conflict` review state in the
extraction report, and the overall routing review remains incomplete.

Old schematic `Wire.Wxxx` records are no longer a route source and do not block
trace export. There are currently no saved traces, so fresh wiring extraction
produces the eight-column header with zero routed wires and reports incomplete
electrical coverage. Only a saved completed trace path adds a wire; drawing in
an unsaved editor does not change extraction.

## Data direction

Saved KiCad data flows into the schedules. CSV-owned purchasing entries/fields
stay local. Browser Overwrite saves only the current CSV, including source tags.
There is no path from a browser edit back into the schematic, PCB or libraries.

Tests cover source changes, package quantity preservation, Local row retention,
removed linked parts, duplicate/missing keys, ambiguous matching, CSV tag round
trips, refresh failures and concurrent saves.
