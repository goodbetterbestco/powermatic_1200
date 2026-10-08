# 50MA3KLE physical terminal numbering and symbol-standard review

The owner closed KiCad and authorized replacing the legacy L/R IDs with the
physical station numbering: odd positions 1,3,5 on the owner's left-side
reference, even positions 2,4,6 on the right; T is top and B is bottom.
The named STEP screws govern each physical pad coordinate.

| Contact | Physical terminals | At rest | Pressed |
| --- | --- | --- | --- |
| FWD NC | 1T, 2T | Closed | Open |
| FWD NO | 1B, 2B | Open | Closed |
| REV NC | 3T, 4T | Closed | Open |
| REV NO | 3B, 4B | Open | Closed |
| STOP NC | 5T, 6T | Closed | Open |

There are no 5B or 6B terminals. All ten symbol pins are passive and visible.
Names distinguish each contact end using its physical position number, e.g.
FWD_NC_1 at 1T and FWD_NC_2 at 2T. Each pair remains adjacent on one side of
the symbol, 2.54 mm apart, with 5.08 mm between successive pairs.

The centered body is 15.24 x 38.1 mm. The fourteen-row even stack uses the
required half-grid Y positions; connection X=-10.16 mm is on the 2.54 mm
grid. Reference at Y=22.86, Value at Y=20.32 and the two-line Part Name at
Y=-21.59 all follow the 1.27 mm field grid. Native exports rejected a narrower
body and a closer reference placement because they overlapped text. The
current native exported image is `S2-symbol.png`.

The placed symbol center moved 1.27 mm right so all ten absolute wire
connection points remain unchanged. S2's UUID and pin UUIDs are preserved.
Its schematic cache, shared symbol, footprint pads, PCB pad IDs/functions,
Wire.Sizes entries and Termination field keys now agree. Only the two
generated unconnected-net names changed beyond the pin-ID migration.

The schematic's five external 16 AWG conductors remain at 5T, 6T, 2B, 1B and
3B. Installed jumpers 1T-3T and 3T-5T remain documented; 2T/4T are unwired.
The required 2B-4B jumper remains explicitly unconfirmed as a physical
installation. No component model, pad coordinate or board placement changed.

Validation: all 172 connected endpoints have valid sizing assignments; all
27 wiring tests pass. Native PCB loading verifies 90 footprints and exact
agreement of all ten S2 pad nets, functions and types with the native netlist.
Final ERC has zero errors and the same ten pre-existing library warnings.
Unrelated symbol definitions, circuit connections and board records are
preserved. The catalog CSV/database and original colored STEP are unchanged.

The governing checklist is the current `_parts/kicad_rules.csv`. All 45
symbol rules are accounted for in the adjacent checklist. Two limitations
are explicit: manufacturer datasheet evidence is unavailable, so the owner
STEP and confirmed physical contact states/IDs are the governing source;
SYM-VIS-001 remains pending because computer control could not launch the
closed KiCad application and its launch API was unavailable. The inspected
native export is not marked as a live Symbol Editor check. Open
Controls:50MA3KLE in KiCad's Symbol Editor to complete that rule.

Native DRC remains unverified following the prior exit-134 failure. This is
a panel-layout wiring footprint; no manufacturing or installation signoff
is implied. `before/`, `installed.json`, native netlists and `validation.json`
retain the saved checkpoint and migration evidence.
