# Powermatic control signal names

The shared [signal naming standard](../../_parts/SIGNAL_NAMING_STANDARD.md)
governs this project. Use `[FUNCTION]_[DETAIL]_[ROLE]` in uppercase, with the
detail omitted when unnecessary. The active functions are `CONTROL`,
`DIRECTION`, and `SPEED`. Control signals use `CMD`, `ENABLE`, `FB`, `COIL`,
or `LINK` as their role; power rails and motor power conductors retain their
electrical names.

The saved schematic owns net names and connectivity. PCB pad nets, embedded
`Wire.Sizes` declarations, physical wire records and generated outputs must
use that same native name. A leading `/` in KiCad exports denotes sheet scope
and is not part of the functional naming convention. Reusable symbol pin names
and physical terminal numbers remain manufacturer/contact functions.

## Operator connections

| Signal | S2/S3 terminal | Energized meaning |
|---|---|---|
| `CONTROL_OVERLOAD_ENABLE` | S2.5T; retained links to 1T and 3T | Feed has passed the upstream control enable and both overload NC contacts. |
| `CONTROL_RUN_ENABLE` | S2.6T; S3.1B with retained link to 2B | The overload-qualified feed has also passed STOP's NC contact. |
| `DIRECTION_ENABLE` | S2.2B with required link to 4B | Either speed contactor K4 or K6 has closed its auxiliary NO contact, supplying the direction start/holding circuits. |
| `DIRECTION_FWD_CMD` | S2.1B | Forward command path is energized by the button or K1's holding contact. |
| `DIRECTION_REV_CMD` | S2.3B | Reverse command path is energized by the button or K2's holding contact. |
| `SPEED_LOW_CMD` | S3.1T with retained link to 3T | LOW selector command path is energized. |
| `SPEED_HIGH_CMD` | S3.2T | HIGH selector command path is energized. |

S2 retains five external conductors and S3 retains three. This naming update
does not change any connection or establish installation of an unconfirmed link.
The S2 2B-to-4B link remains required and physically unconfirmed.

An energized command net does not prove a button remains pressed or a motor is
moving. `CONTROL_RUN_ENABLE` is a positive permission path, not an active-high
STOP request. Loss of a cumulative enable may result from any upstream open
contact or missing feed; it does not uniquely diagnose the last device.

## Other named control nets

| Signal | Function |
|---|---|
| `CONTROL_ESTOP_ENABLE` | Feed through the E-stop contact chain to K3's coil. |
| `CONTROL_ESTOP_DISABLED_FB` | K3 NC31-32 supplies the red H2 lamp when the E-stop enable relay is released and 24 V power is present. This also indicates an unplugged/broken E-stop loop or a failure to energize K3; it does not uniquely identify the physical button position. |
| `CONTROL_LOW_OVERLOAD_ENABLE` | Intermediate feed after OL4's NC contact and before OL6's NC contact. |
| `DIRECTION_FWD_COIL` | K1 coil feed after the reverse contactor's NC interlock. |
| `DIRECTION_REV_COIL` | K2 coil feed after the forward contactor's NC interlock. |
| `SPEED_LOW_COIL` | K4 coil feed after the high-speed interlocks. |
| `SPEED_HIGH_SHORTING_COIL` | K5 shorting-contactor coil feed after K4's NC interlock. |
| `SPEED_HIGH_COIL` | K6 coil feed after K5's NO sequencing contact. |
| `SPEED_LOW_K6_NC_LINK` | Intermediate low-speed command path between K6's and K5's NC interlock contacts. |
| `CONTROL_ESTOP_CONTACT_LINK` | Intermediate connection between the two E-stop NC contacts. |
| `CONTROL_K3_CONTACT_LINK` | Intermediate connection between K3's series NO contacts. |

`FB` is reserved for an actual feedback contact or sensor. No feedback signal
introduced here indicates shaft motion. A contactor auxiliary contact confirms its defined
contact state, not measured shaft speed or direction. `+24V`, `+24V_EN`, `0V`,
`PE`, phase-stage names and motor terminal names remain power-net identifiers.

## Verification of the naming update

The 2026-10-08 update preserves all net terminal memberships, symbol pin functions
and electrical types. PCB changes are name substitutions only. One schematic
coil label rotates at its original connection point to avoid overlapping a
neighboring symbol. Wires, UUIDs, terminal numbers, component positions and models
are unchanged.
Validate the final native netlist and embedded sizing declarations together.
Review exported operator/control artwork for label readability.

| Shared rule | Result | Evidence |
|---|---|---|
| `SCH-NAME-001` | Pass | All 17 explicitly named control nets use the shared roles. No remaining old-name usages were found in either repository's current searchable files. |
| `SCH-NAME-002` | Pass | Operator/cumulative meanings are recorded above; the native exports were inspected, and the long K5 coil label was rotated without moving its connection point. |
| `SCH-NAME-003` | Pass | Before/after native netlists retain all 64 net groups with identical terminal memberships, pin functions and electrical types. PCB sources retain every non-name byte; schematic sources differ only in names and one label rotation. |

Native PCB loading confirms 90 footprints and 279 pads. The sizing validator
classifies all 172 connected terminals, including eight external S2/S3 wires.
All 27 existing wiring tests pass. Final ERC has zero errors and the same ten
library-symbol-mismatch warnings as the baseline; its violation records are
identical. These checks validate the rename, not fabrication or electrical release.
