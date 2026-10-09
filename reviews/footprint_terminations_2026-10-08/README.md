# Footprint-owned terminations

The owner requires TERM 1 and TERM 2 to belong to their endpoint parts. The
saved PCB now holds 305 hidden F.Fab `Termination.<terminal>` fields on 67
footprints. Edit these selections in Footprint Properties. They are project
instance data, so preserve them when updating footprints from their libraries.
Reports are derived outputs.

The migration moves all 182 existing symbol termination fields into their
corresponding footprints and removes the symbol copies. It also removes
`term1`/`term2` from the three surviving schematic wire records. The generator
reads TERM 1 from the source footprint and TERM 2 from the destination footprint.
Missing footprint fields stop export instead of using a wire-record fallback.
The record editor no longer accepts termination-copy arguments.

All 33 feedthrough/ground blocks' 66 wire clamps now describe the part capability:
`Ferrule or twin ferrule as required`. One conductor uses a ferrule; two in one
clamp use a twin ferrule. The owner clarified that blocks and unused jumpers
are available graphics until needed during routing. Part fields therefore carry
no wire-gauge or barrel-length assignment, and unallocated clamps are not
reported as missing termination choices. Actual conductor gauges remain in wire
records/sizing declarations. Ferrule size, length and single/twin form are chosen
when routing assigns conductors. Every block records `Wire.TerminationPolicy`;
grounding-block PE rail feet retain their conductive-contact classification.
`ferrule_policy.json` records the initial family requirement and
`block_capabilities.json` records the owner's allocation clarification and
geometry-preservation check. Other parts' existing barrel-length and
ring-dimension TBDs are retained.

Gland route markers are classified as cable pass-throughs without electrical
terminations. Mechanical interlock markers and grounding-terminal rail contacts
are also classified explicitly. Legacy enclosure, door and backplate stud
descriptions live on the enclosure footprint; rail lug descriptions live on the
two rail footprints. Those legacy bond selections remain pending reconciliation
with the newer bonding plan and do not establish additional wire connections.

At the owner's request M1, J2, S1 and J6 now have metadata-only footprints.
Their terminal inventory is stored in `Wire.TerminalPins`, with one termination
field per terminal. They have no pads, artwork or models, are marked board-only,
allow missing courtyards, and are excluded from BOM and position exports. Their
hidden fields on F.Fab do not change the panel drawing. Their schematic symbols
and electrical connections are retained.

H1 and H2 still have older symbol UUIDs in the board paths. Before associating
their termination fields, the migration verified unique references, matching
MPNs, complete matching terminal inventories and identical native net names.
It preserves the existing paths, placements and models. Both receive the
existing blue 18 AWG indicator ferrule selection.

Validation performed:

- Native KiCad PCB loading: 97 footprints, 305 hidden termination fields.
- Four metadata-only owners: zero pads, graphic items or models and the intended
  board-only/BOM/position exclusion attributes.
- Structured comparison: every original footprint's geometry, placement, pads,
  nets, models, UUIDs and non-termination fields unchanged. All other PCB objects
  unchanged. Schematic changes restricted to removal of termination copies.
- Native schematic netlist comparison: all 186 pin-to-net assignments identical.
- Migration repeated on its result: byte-for-byte idempotent.
- 33 wiring tests passed, including conflicting owner selections, migration,
  external owners, footprint edits flowing into schedule output and missing
  fields rejecting stale wire-record fallbacks.
- Source hashes checked before installing both saved files after the owner's
  saved/editing-paused confirmation. Whitespace check passed.

`validation.json` records hashes and preservation checks. `provenance.json`
records the origin of every migrated selection. These are evidence, not runtime
data sources. Run `python3 tools/wiring/terminations.py` to review the saved PCB.

The rest of the physical wire-record migration remains unchanged. Complete
schedule generation still fails on deleted schematic endpoint UUIDs. No wire
allocation, routing, cut-length redesign, DRC severity changes or library edits
were included in this task.
