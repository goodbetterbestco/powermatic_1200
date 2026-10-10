# KiCad-owned wiring

Saved PCB traces own physical conductor paths. The saved schematic owns logical
connectivity and per-terminal gauge declarations. Placed footprints own
termination selections and can override physical gauge with `Wire.AWG.<pin>`.
The live CSV is an extracted, locally editable schedule.

Use the current names in the [project signal table](../../SIGNAL_NAMING.md).
Net renames must flow through schematic labels, PCB pad/track nets and embedded
`Wire.Sizes` data before extraction. Old `Wire.Wxxx` records are not read by the
trace exporter.

Stale `Wire.Sizes` net stamps are reported and their gauge declarations ignored,
so an edited or flipped symbol does not hide unrelated routed wires. Resolve
the stale declaration to restore its sizing evidence. Nets on the actual routed
endpoints must still agree. Different nets reaching the opposite internally
common clamps of one block are reported as electrical conflicts; all explicitly
drawn wires remain visible, and the extraction review is marked incomplete.

Preferred conductor sizes and component-specific exceptions are defined in the
project [wire-size policy](../../WIRING_STANDARD.md). Actual AWG remains
per-conductor data and terminations belong to the endpoint footprints. The
generator must not substitute a default for a
factory lead or cable-core specification.

## Connection sizes before physical routing

KiCad graphical wires do not have a native AWG property. The custom symbol field
`Wire.Sizes` can hold sizing declarations for every connected terminal while
physical terminal allocation remains pending. Each declaration binds an actual
symbol UUID/pin and native net name to its application and AWG. Different parts
of the same electrical net can have different sizes: 18 AWG panel wiring,
16 AWG external S2/S3 wires and 22 AWG J1 factory pigtails.

The `color` value records black power wire, blue DC control wire and green/yellow
PE wire for discrete conductors. J1 retains its four supplied lead colors.
Incoming cable-core colors are retained as supplied, rather than inferred from
the discrete-wire color convention.

Fixed switch links, suppressor leads, mating connector interfaces and direct-mount
overload connections are classified separately, without guessing a supplied wire
size or adding a loose wire. Internally common coil/PSU terminals do not imply
extra jumpers. `Wire.SizePlan` records planned mechanical PE/bond conductors
without inventing a motor symbol pin.

`sizes.py` prepares a candidate copy and validates declarations against a native
netlist. It never writes the active schematic. Applying a validated candidate
requires saved editors, an editing pause and a source-hash check.

The 2026-10-06 population is installed in the active schematic: all 172 connected
terminals are classified, with 128 numeric AWG assignments and 44 fixed/interface
classifications. M1.PE is 12 AWG, in addition to the six 14 AWG motor conductors.
See the [generated sizing review](../../reviews/wire_sizes_2026-10-06/sizing.md).
Validate the saved sizing fields or refresh their derived review with:

```sh
python3 tools/wiring/sizes.py
python3 tools/wiring/sizes.py --report reviews/wire_sizes_2026-10-06/sizing.md
```

```sh
python3 tools/wiring/sizes.py --stage /private/tmp/powermatic-sizes/powermatic_1200.kicad_sch \
  --report /private/tmp/powermatic-sizes/sizing.md
python3 tools/wiring/sizes.py --schematic /private/tmp/powermatic-sizes/powermatic_1200.kicad_sch
```

Connection-size declarations are not a physical wire schedule. Actual saved
trace paths identify conductors; endpoint metadata supplies their gauges and
terminations. Resolve per-wire sizing conflicts before using a cut list. No
net-wide or copper-width gauge default is inferred.

## Pin termination descriptions

Each physical part footprint has one combined custom field per terminal, named
`Termination.<pin>`: for example `Termination.A1.BOT` or `Termination.P1.A`.
Fields are hidden on F.Fab and editable in Footprint Properties. These are custom
footprint fields keyed by actual pad number, not graphics or a separate summary.
The schedule reads TERM 1 from the source footprint and TERM 2 from the destination
footprint. Missing fields stop export. Wire records do not own termination copies.

The footprint migration moves existing symbol selections into placed footprints
and includes PCB-only terminal blocks. M1, S1 and J6 have metadata-only
footprints: no pads, artwork or models, and excluded from BOM/position exports.
J2 now uses the mains gland model/artwork as its physical routing proxy, with
four pads matching plug terminals X, Y, Z and G. It owns its plug termination
fields and inherits the plug's schematic sizing declarations. The four existing
incoming routes are preserved. `Wire.LengthScope` declares that their cut
estimates cover the panel tail only, excluding the external supply cord.
Enclosure, door and backplate stud descriptions live on the enclosure footprint;
rail lug descriptions live on each rail footprint. Legacy bond descriptions
remain drafts for later topology reconciliation. Feedthrough and ground wire
clamps describe the ferrule/twin-ferrule capability without attaching a wire
gauge to the part. Blocks and unused jumpers are available routing resources
until allocated. Supplied contacts, retained jumpers, cable pass-throughs and
direct-mounted connections are separate from loose-wire crimps. Counts are
terminal fields, not purchasing quantities.

A route terminating at an otherwise uncontinued gland pad is exported as an
explicit drawn section, with the gland's N/A termination and an incomplete
external-length warning. When both paired gland sides are routed, the exporter
joins them into one continuous wire rather than adding a termination at the gland.

Refresh the review from saved fields with:

```sh
python3 tools/wiring/terminations.py --report /private/tmp/footprint_terminations.json
```

`terminations.py --stage-dir <separate directory>` prepares both schematic and
PCB candidates. Existing footprint selections are preserved; conflicting symbol
and footprint choices stop migration. Importing the old CSV is a one-time
migration fallback, not a runtime schedule source. Applying candidates requires
saved editors, an editing pause and source-hash checks. Staging never overwrites
the active files. Preserve these project fields when updating footprints from a
library; actual conductor gauges and selections belong to the placed instances.

Terminal blocks and glands are PCB-only. The saved PCB traces now define the
physical wire graph. Complete pad-to-pad paths become wire rows; unused graphics
and unrouted nets do not. Old W001/W003/W005 schematic records are not used and
their stale UUIDs do not block trace extraction. See the
[trace rules](../schedules/README.md#wiring-ownership) for branches, layers,
glands, gauge selection and cut-length allowances.

Open **Open Wire Schedule Review.app** or **Generate Wiring Review.app**. Both
extract fresh traces into the single existing `Wire_schedule.csv`; Refresh does
the same in the browser. CSV edits remain local. No CSV history is retained.

```sh
python3 tools/wiring/generate.py --open
```

## Route a wire

In PCB Editor, draw a continuous trace between actual terminal pads and save the
PCB. Refresh the wiring browser to add the row. Deleting that saved path removes
the row on Refresh. A path through an intermediate terminal becomes two wires;
branch at a terminal rather than at an unmarked point in space. Set
`Wire.AWG.<pin>` in Footprint Properties when existing endpoint sizing does not
identify the actual conductor. The existing manual-record helpers below are
legacy tools and do not drive the current trace export.

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
  --section '02 Fuse outputs and disconnect' --awg 14
python3 tools/wiring/generate.py
```

Save current KiCad edits before changing records through the helper. Reload the
schematic with **File → Revert** after an external record update, before making
more editor changes. The helper refuses to overwrite a file that changed while
it was checking the new record.

Records are hidden `Wire.W001`, `Wire.W002`, etc. properties on each wire's origin
symbol. Each is a JSON object with its origin pin, target symbol UUID and pin,
section, gauge, connection kind, length policy and review state. Termination text
is read from the endpoint footprints' `Termination.<pin>` fields.
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

Current trace endpoints must resolve to real footprint terminals and agree
with the saved schematic's electrical nets. The manual-record validation below
applies only to the legacy helpers.

Every legacy record must resolve to real schematic pins on the same connected net.
Directly drawn wire paths are also checked for the wrong physical terminal clamp,
even when TOP/BOT are electrically common. Missing PCB pads, deleted symbols,
duplicate records and inconsistent routing endpoints stop generation. Conflicting
unrecorded sections are not silently filled in from legacy data or caption text.

Output: root `Wire_schedule.csv`, the single live eight-column schedule.
No extra generated CSV or archived CSV is created. Coverage/provenance are
returned to the caller for status reporting rather than kept as schedule copies.

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
# Supplied busbar contacts

The HMX1-BBREV_TOP and HMX1-BBREV_BOT footprints each use three native KiCad
`jumper_pad_groups`, for six isolated bridges in total. `Wire.SuppliedAssembly=busbar` marks its contacts as supplier hardware.
`Wire.MatingPads` contains a schema-1 map from each accessory pad to a host role
and terminal number; `Wire.Host.A` and `Wire.Host.B` bind those roles to the
placed host footprint UUIDs. Host roles are independent of reference renaming.

Extraction validates every overlap, host identity, schematic net, and native
jumper group before collapsing a supplier contact onto its host terminal.
Unexplained overlaps still fail. Native busbar bridges count toward electrical
coverage and are omitted from loose-wire rows and ferrule conductor counts.
External wires retain the host terminal's name and preparation selection.


The TOP/BOT pieces share `Wire.KitID`; `Wire.PurchaseQuantity` assigns the one
kit to TOP (1) and no additional purchase to BOT (0). Their `PartID` values
identify the pieces while both retain manufacturer MPN `HMX1-BBREV`.
