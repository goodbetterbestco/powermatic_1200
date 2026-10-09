# Powermatic 1200 Controls Retrofit

Rev P is the current contactor-based design for the Powermatic 1200. Retain the existing motor, OFF/LOW/HIGH drum switch and fixed FWD/REV/STOP button station. Operator controls use 24 VDC; motor-power switching is located in the panel enclosure.

## Active files

- [Rev P BOM](Powermatic_BOM_revP.csv) — current component list, grouped by unique part number.
- [Wire-size policy](WIRING_STANDARD.md) — conductor gauges, motor/controls conduit plan, component exceptions and documentation responsibilities.
- [KiCad project](kicad/powermatic_1200/powermatic_1200.kicad_pro)
- [Schematic](kicad/powermatic_1200/powermatic_1200.kicad_sch) — work in progress.
- [Open work](TODO.md)

The contactor references are KF (forward), KR (reverse), KL (low speed), KH (high-speed supply) and KS (high-speed shorting). The current design also includes the selected disconnect, fuses, supply-input breaker, motor overloads, coil suppression, coil-enable relay, white indicator and M12 E-stop connection. The BOM records selected parts; schematic completion and commissioning remain open.

## Review the BOM

Use the local [BOM review editor](https://github.com/goodbetterbestco/bom_review)
to edit the CSV in a browser:

Double-click **Open BOM Review.app** in Finder. It opens the first CSV whose
filename contains `bom` (case-insensitive, alphabetically sorted) beside the
launcher. The launcher can be copied into another project folder to review its
BOM. Repeated launches reuse the same reviewer server. It runs in the background;
the launcher opens a Terminal window only when none exists and leaves existing
Terminal sessions alone. Closing Terminal does not stop the reviewer.

Or launch from a terminal:

```sh
python3 ~/Projects/bom_review/review.py ~/Projects/_hardware/powermatic_1200/Powermatic_BOM_revP.csv
```

The editor uses TYPE, NAME, QUA, PACK, UNIT, COST, LINE, SUPPLIER and SPN.
LINE calculates QUA × COST; the header total includes all parts. Blank and summary
rows are omitted. Other cells remain editable text. **Overwrite** saves directly
to the original project CSV. **Save CSV** downloads a separate copy. Relaunch the
Finder app after updating the reviewer to use its latest server features.

## Generate a wiring review

The [wire-size policy](WIRING_STANDARD.md) defines conductor classes and exceptions.
`Open BOM Review.app` and `Open Wire Schedule Review.app` use the shared
`bom_review` editor. On launch they extract fresh saved KiCad data into the
existing BOM or wiring CSV. The browser's Refresh button repeats extraction.
Overwrite saves browser edits only to that live CSV; it never writes to KiCad.
There is one CSV per schedule and no automatically retained CSV history.

The BOM's SOURCE column distinguishes KiCad-linked rows from Local purchasing
items. SOURCE KEY, hidden in the grid, identifies linked parts across refreshes.
KICAD QTY is the modeled count; purchasing QUA and packaging remain CSV data.
Refresh retains all Local rows and the purchasing fields on linked rows. Initial
tagging preserves all existing BOM values. See [schedule extraction](tools/schedules/README.md).

Both wire-review Finder apps use the same live `Wire_schedule.csv`. Complete
saved PCB trace paths become physical wire rows; bends/arcs/vias do not create
extra wires. Refresh updates routes and footprint termination data and reports
unrouted or ambiguous connections. There are currently no saved traces, so a
fresh schedule contains zero routed wires. Old `Wire.Wxxx` fields are not used.

See [KiCad-owned wiring](tools/wiring/README.md) for the record editor, routing
rules and generated coverage report. To generate without opening a browser:

```sh
python3 tools/wiring/generate.py
```

## Shared parts library

Control-net names follow the shared `_parts` naming convention. See the
[project signal table](SIGNAL_NAMING.md) for operator connections, enable paths,
coil feeds and intermediate links.

Reusable assets are kept in the separate `_parts` repository:

- `symbols/Controls.kicad_sym` — control symbols.
- `datasheets/` — product documents and drawings, including the May 1968 Bulletin 365 catalog.
- `3dmodels/Controls/` — 21 vendor STEP files and three user rail/duct STEP files, in their original orientations.
- `reviews/Controls_Panel_Models_2026-09-25/` — source mapping and verified file hashes.

Controls layout footprints have not been created. Model orientation, mounting datums and terminal positions still require review before footprint use. External L15-20 plug, drum-switch and button-station modeling is deferred. The fuse model is excluded; its holder and cover models are available.

Component placement will determine the enclosure size. The 350 mm DIN rail is the current working model; duct cut lengths and rail count remain to be determined.

## Archived working material

The mechanical collection, generated reports, previous BOM snapshot and earlier project notes are preserved in [archive commit 8ceac95](https://github.com/goodbetterbestco/powermatic_1200/tree/8ceac956c50b004d06b5bfea7e3169a44bf2d5c7). They were removed from the active tree after the archive was pushed and the shared-library asset copies were verified. Older Rev M design files remain in earlier Git history.
