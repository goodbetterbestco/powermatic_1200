# Wire-size policy — Powermatic 1200

Control signal names are governed by [SIGNAL_NAMING.md](SIGNAL_NAMING.md) and
its linked shared standard. Use the schematic's native net names consistently
in sizing declarations, physical wire records, PCB pad nets and generated outputs.

Preferred gauge set: **12 AWG, 14 AWG, 16 AWG, 18 AWG and 22 AWG**. Use AWG consistently; the previously stated “12GA” means 12 AWG in this project. These are preferred conductor classes, not a requirement to replace factory leads or purchased bonding assemblies with those sizes.

This document is the project policy. Actual conductor gauge and cable/part identity belong in the individual wiring records. Termination selections belong to the endpoint footprints' `Termination.<pin>` fields. A preferred gauge does not by itself establish ampacity, fault protection or terminal suitability.

## Preferred applications

| Gauge | Project application | Current evidence / qualification |
|---|---|---|
| 12 AWG | Incoming mains cable phase and PE cores; discrete motor-conduit PE conductor | Selected McMaster 7081K33 is 12/4 SOOW. Owner specifies one 12 AWG PE conductor alongside T1–T6 in the motor conduit. KN-G12SP-10 includes 12 AWG in its wire range; conductor preparation and termination selection still apply. Existing incoming-phase schematic records specify 12 AWG, although their old terminal endpoints require reconciliation. |
| 14 AWG | Six motor-conduit conductors T1–T6; discrete panel motor-power and PSU AC-input wiring; default custom panel PE wiring where sizing permits | Owner specifies six motor conductors. Current BOM stocks 14 AWG black machine wire and 14 AWG green/yellow machine wire. Per-circuit protection and actual terminal specifications still govern. |
| 16 AWG | Individual external control wires in conduit: five for S2 and three for S3 | Owner confirms individual wires and selects 16 AWG for both runs. Match circuit protection, wire product and terminations to the installed conductors. |
| 18 AWG | New discrete 24 V control wiring inside the enclosure/operator stations, including coil/interlock/indicator circuits | Legacy control wiring uses 18 AWG. Match protection to the actual wires and factory leads in each branch before construction. |
| 22 AWG | Small factory connector pigtails, specifically J1's T4171310004-001 M12 leads | The manufacturer drawing specifies 0.34 mm² / 22 AWG. This is a factory-lead class; use 18 AWG as the normal new discrete control-wire choice. Do not infer that all other connector/cable variants have the same leads. |

The preferred classes do not automatically imply a loose-wire spool for every size. The incoming 12 AWG conductors and 22 AWG M12 leads are supplied by the selected cable/device; the motor-conduit 12 AWG PE is a separate discrete wire. Purchase discrete wire only where the physical wire list actually requires it.

## KiCad route widths and netclasses

For panel wire drawings, track width represents the nominal bare conductor
diameter. The presets below use NBS Handbook 100, table 1's nominal diameters
in mils, converted to millimetres and rounded to 0.001 mm. They exclude
insulation and are drawing widths; actual stranded-conductor dimensions remain
part-specific.

| Width profile | Nominal diameter / track width (mm) | Use |
|---|---:|---|
| `AWG_10` | 2.588 | Planned prefabricated bonding assemblies |
| `AWG_12` | 2.052 | Incoming cable cores and motor-conduit PE |
| `AWG_14` | 1.628 | Panel power, motor conductors and normal panel PE |
| `AWG_16` | 1.290 | Individual external S2/S3 control-conduit wires |
| `AWG_18` | 1.024 | Internal panel control wiring |
| `AWG_22` | 0.643 | J1's supplied factory pigtails |

KiCad 10 combines functional netclasses with an AWG width profile. The AWG
classes set only track width; functional groups identify the circuit. Existing
clearance, via and other parameters inherit from `Default`. The saved project
contains exact-name assignment patterns, visible in **Board Setup → Net
Classes**. The Net Inspector groups nets by netclass.

| Functional group | Default width profile | Assigned circuit |
|---|---|---|
| `INCOMING_MAINS` | `AWG_12` | `L1_IN`, `L2_IN`, `L3_IN` |
| `PANEL_POWER` | `AWG_14` | Fused/switched/direction power, PSU AC input and `HS_SHORT` |
| `MOTOR_POWER` | `AWG_14` | `M1_T1`–`M1_T6`; direct-mounted overload interfaces are separately marked internal |
| `CONTROL` | `AWG_18`, or `AWG_22` for the factory-only E-stop contact link | 24 V supply/return and `CONTROL_*` signals |
| `DIRECTION` | `AWG_18` | `DIRECTION_*` signals |
| `SPEED` | `AWG_18` | `SPEED_*` signals; retained S3 straps are separately marked internal |
| `PE` | `AWG_14` | Panel PE default; choose `AWG_12` or `AWG_10` for the specified individual conductors |
| `DEVICE_INTERNAL` | No assumed AWG | Direct-mounted overload interfaces and retained S3 straps; retain the existing `Default` drawing width |

A netclass width is a routing default, not a per-conductor gauge declaration.
The saved declarations contain 13 mixed-gauge nets: incoming phases, PE,
24 V/E-stop circuits and external control signals. Select the actual conductor's
width preset when routing those individual wires. In particular, external
S2/S3 wires use the 1.290 mm preset even though their panel-side net default is
1.024 mm. Use the 0.643 mm preset for J1's supplied leads on mixed E-stop nets.
The existing `Wire.Sizes`, `Wire.AWG.<pin>` and termination fields continue to
own actual conductor specifications; the schedule does not infer AWG from
track width.

PCB Editor is configured for **90 degree rounded** routing with free-angle
mode disabled. New routes use horizontal/vertical straight sections joined by
fillet arcs. The project disables automatic width pickup from an existing
track, so an old 0.2 mm trace cannot silently override the netclass width.
Select **Use netclass width** for the normal default, or an AWG preset for an
individual mixed-gauge wire. These settings preserve existing routed geometry.

The corner setting is a KiCad user preference and applies across projects on
this Mac. KiCad's corner-mode shortcuts can still change it during routing.
Rounded tracks use real arcs; KiCad does not support dragging arcs and treats
them as immovable in shove mode.

Sources: [NBS Handbook 100, Copper Wire Tables, table 1](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook100.pdf),
[KiCad 10 netclasses and interactive routing](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html).
The saved assignment inventory is in
[`reviews/routing_standards_2026-10-08/assignments.json`](reviews/routing_standards_2026-10-08/assignments.json).

## Discrete wire colors

Carry forward the existing BOM's color convention by application: black for
power wiring, blue for 24 VDC control wiring and green/yellow for PE. Apply that
same convention to the new 12 AWG motor PE and 16 AWG control-conduit wires.

| AWG | Color | Application |
|---|---|---|
| 12 | Green/Yellow | Motor-conduit PE |
| 14 | Black | Panel power, PSU AC input and motor-conduit T1–T6 |
| 14 | Green/Yellow | Discrete panel PE, including PSU PE |
| 16 | Blue | S2/S3 control-conduit wires |
| 18 | Blue | Internal 24 VDC control wires |

These colors are stored with the sizing entries in the schematic's custom
`Wire.Sizes` fields. Incoming cable cores retain their supplied colors; no new
loose-wire stock color is inferred for them. J1's supplied 22 AWG pigtails retain
pin 1 Brown, pin 2 White, pin 3 Blue and pin 4 Black. Jumpers and other retained
or supplied connections remain separate from this discrete wire inventory.

## External conduit runs — owner specification, 2026-10-06

| Run | Conductors | Destination / function |
|---|---|---|
| Motor conduit | Six 14 AWG plus one 12 AWG | One 14 AWG conductor for each of T1–T6; one 12 AWG PE conductor |
| Controls conduit, S2 | Five individual 16 AWG | S2 forward/reverse/stop button station |
| Controls conduit, S3 | Three individual 16 AWG | S3 OFF/LOW/HIGH drum switch |

The controls run contains eight individual 16 AWG control conductors in total. The owner confirms individual wires in conduit and selects 16 AWG for S2/S3. NFPA 79 (2024), §12.6.2 specifies at least 16 AWG for ordinary lighting/control conductors on the machine and in raceways, or 18 AWG where part of a jacketed multiconductor cable assembly. The 18 AWG enclosure/operator-station provision in §12.6.3 does not establish an 18 AWG minimum for the external conduit run. Retain 18 AWG as the internal panel control-wire default.

The motor conduit replaces the previous McMaster 7081K6 16/7 motor-cable plan. The S2/S3 conduit specification supersedes the previous single McMaster 6452T44 18/7 controls-cable plan. Those cable SKUs and their cable glands remain legacy BOM selections pending procurement reconciliation; do not treat them as conduit fittings or assume the old seven-core controls cable covers the eight specified conductors. Conduit type/size, wire product, fittings, installed lengths and exact terminations remain to be selected.

## Button-station terminations — owner specification, 2026-10-06

S2 is the vintage Furnas 50MA3KLE button station. Its physical terminal IDs are
1T/2T and 1B/2B for FWD, 3T/4T and 3B/4B for REV, and 5T/6T for STOP.
T contacts are normally closed; B contacts are normally open. There are no
5B/6B terminals. All
terminals have #8-32 screws and accept a maximum terminal width or ring OD of
9 mm. The five new 16 AWG wire ends use ring terminals sized for #8 studs, with
an OD no greater than 9 mm. This selection is stored in S2's corresponding
footprint `Termination.<pin>` fields.

S3's three new 16 AWG wire ends (1B, 1T and 2T) use the same existing
16 AWG #8-32 ring-terminal selection, assigned by the owner on 2026-10-06.
This selection is stored in S3's corresponding footprint `Termination.<pin>` fields.

## Component-specific exceptions

### K1/K2 reversing busbars — owner selection, 2026-10-09

Use one HMX1-BBREV kit on K1/K2, represented by two PCB-only footprints:
BB1 `HMX1-BBREV_TOP` is the upper/line-side piece; BB2 `HMX1-BBREV_BOT` is the
lower/load-side piece. Each has six contact pads and three native KiCad
`jumper_pad_groups`. TOP joins 1–1, 3–3 and 5–5; BOT joins 2–6, 4–4 and 6–2.
The existing local BOM item remains one kit. TOP owns purchase quantity 1 and
BOT quantity 0; both share `Wire.KitID=HMX1-BBREV_K1_K2` and retain the actual
manufacturer MPN `HMX1-BBREV`. The exact TOP/BOT names are footprint IDs and
`PartID` values, not separately orderable manufacturer part numbers.

Both footprints bind host roles A/B to the K1/K2 footprint UUIDs and record each
mated pad. Extraction checks host identity, exact overlap and net agreement,
then recognizes the native jumper groups without adding loose-wire rows.
Incoming and outgoing loose wires keep their K1/K2 terminal preparation
selections. Unspecified overlapping terminals remain extraction errors. The
front elevations preserve manufacturer geometry and logical routing targets;
installed 3D depth and physical assembly fit have not been verified.

No suitable catalogued IronHorse kit was found for K4/K5. Keep its existing
wiring plan, including the K5 1–3–5 shorting bridge. HMX1-BBREV's reversing
connections do not match that pair. Source: [IronHorse accessory catalog](https://cdn.automationdirect.com/static/specs/ironhorsehmcandhtor.pdf).


H2 is the red Schneider XB4BVB4 E-stop/control-disabled indicator below SW1.
Connect raw `+24V` to K3.31, K3.32 to H2.X1 on
`CONTROL_ESTOP_DISABLED_FB`, and H2.X2 to `0V`. The two new K3 terminal
connections and both H2 terminals use blue 18 AWG panel-control wiring with
ferrule terminations. The existing E-stop connector/conduit wiring is unchanged.
Physical routes and cut lengths remain pending, as for the other panel wires.

### Terminal preparation selections — owner decisions, 2026-10-09

Ferrule `L` means the metal barrel/contact length, not overall ferrule length or
wire stripping length. Strip wire according to the selected ferrule's instructions.

| Component / terminals | Selected preparation |
|---|---|
| Q1 pins 1/3 (`L1_SW`/`L2_SW`) and 2/4 (`L1_PSU`/`L2_PSU`) | Bare stranded copper, 14 AWG; strip per device instructions. Eaton does not recommend ferrules or crimp terminals for FAZ-NA. |
| PS1 `3_BOT` L (`L1_PSU`), `2_BOT` N (`L2_PSU`), `1_BOT` PE | Bare stranded copper, 14 AWG; 5 mm stripping per the NDR installation manual. These are the three AC-input/PE terminals, not three phase inputs. |
| PS1 `1_TOP`/`2_TOP` (−V, `0V`) and `3_TOP`/`4_TOP` (+V, `+24V`) | Bare stranded copper, 18 AWG; 5 mm stripping per the NDR installation manual. |
| H1/H2 X1 and X2 | Single ferrule, 18 AWG, standard 6 mm metal barrel; owner-selected length. |
| KN-T12GRY-25 feedthrough clamps | Single or twin ferrule for the assigned conductor(s); 10 mm metal barrel. |
| KN-G12SP-10 ground clamps | Single ferrule only, one conductor per clamp; 10 mm metal barrel. |
| FH1 `P1.A`/`P1.B`, `P2.A`/`P2.B`, `P3.A`/`P3.B` | Ring terminal, 14 AWG; #10-32 screw; ring tongue OD ≤9 mm to clear the terminal recess. |
| SW1 pins 1-6 | Bare stranded copper, 14 AWG; 12 mm stripping per the disconnect instructions checked by the owner. |

These selections are stored on the saved footprint instances. All seven PS1
terminals use bare stranded copper. Mean Well's NDR manual gives common wire
preparation instructions for input and output; it does not explicitly approve
or prohibit ferrules. The lamp choice records the owner's decision; it does not
claim a completed physical fit check.

FH1 uses the RM25030-3SR screw-terminal version. The AD drawing shows a nominal
12.6 mm terminal-recess width; the selected 9 mm maximum ring OD keeps clearance
within that width. AD/Z+F V70RK004012 is a sourcing candidate: 16–14 AWG,
5 mm hole, 8.6 mm ring tongue width, 23 mm overall length. The catalog dimensions
support lateral fit; screw seating, barrel/wire exit and cover clearance still
require a physical assembly check. This selection replaces all six previous
FH1 ferrule fields. Sources: [FH1 drawing](https://cdn.automationdirect.com/static/drawings/RM25030-3SR.pdf),
[AD ring-terminal dimensions](https://cdn.automationdirect.com/static/specs/dinwiring.pdf),
[Class R block terminal specification](https://cdn.automationdirect.com/static/specs/efusemodblocksr.pdf).

AutomationDirect's Z+F catalog lists standard single/twin barrel lengths of
8, 10 and 12 mm in the applicable wire sizes. The gray 18 AWG versions are
0.75 mm² per conductor; the red versions are 1.0 mm² per conductor. Keep those
capacities distinct when selecting a ferrule for the actual wire. This catalog
availability does not assign a length to the remaining unverified terminals.
The owner-selected 6 mm lamp ferrules require a separate source.

Sources: [FAZ-NA specifications](https://cdn.automationdirect.com/static/specs/eatonfazna.pdf),
[NDR installation manual](https://www.meanwell.com/Upload/PDF/NDR%20DIN%20rail.pdf),
[AD Z+F ferrule catalog](https://cdn.automationdirect.com/static/specs/dinwiring.pdf).

| Actual size | Component / use | Treatment |
|---|---|---|
| 10 AWG | Proposed Hammond GRDKIT01 prefabricated bonding jumpers | Record the supplied assembly and its installed terminations separately. The enclosure–door jumper retains ring lugs at both ends. For each motor-end jumper, remove the Wago-end lug if present and terminate the correctly stripped 10 AWG conductor in a suitable Wago; retain the far-end ring lug for the motor body or machine-frame bond. Two kits supply four 12-inch assemblies, one spare for the three planned bonds, subject to usable length after modification and stud fit. These are not loose-wire stock and cannot terminate in KN-G12SP-10 clamps. |
| Manufacturer-defined | Suppressor leads, retained switch straps and other fixed device wiring | Keep the actual supplied conductor specification. Do not assign an unverified stock gauge or create an extra assembly wire for a factory/internal connection. |

KN-G12SP-10 accepts 26–12 AWG. Use separate suitable clamps for the incoming cable PE, the 12 AWG motor-conduit PE and PSU PE wire. Its two wire clamps and conductive rail foot are electrically common. Prepare each conductor according to the terminal manufacturer's instructions. The 10 AWG bonding-jumper ends use compatible studs or a wire-splicing connector rated for that conductor; they do not enter these KN-G12SP-10 clamps.

The routed PE continuation `TB43_1` to `TB51_2` uses 12 AWG to match the incoming
mains PE core. The PSU PE branch `TB50_1` to `TB52_2` uses 14 AWG to match the
existing PS1 PE feed. These actual-wire assignments are stored in the four
endpoint footprints' `Wire.AWG.<pin>` fields; they do not set a gauge for the
whole PE net or for unused terminal-block clamps. Both ends use single ferrules
with a 10 mm metal barrel (`F12_10mm` or `F14_10mm`).

All feedthrough-terminal and grounding-block wire clamps use ferrules with a
10 mm metal barrel. Feedthrough clamps use a single ferrule for one conductor
or a twin ferrule for two conductors, sized for the actual conductors. Ground
clamps accept one conductor only and use a single ferrule; no twin ferrules.
These owner requirements are stored in each block footprint's
`Wire.TerminationPolicy`. Individual `Termination.<terminal>` fields describe
the part's termination capability and selected barrel length. They do not assign
a conductor gauge or wire count to an available routing resource. Blocks and unused
jumpers are allocated only when needed during physical routing; available clamps
do not constitute missing wiring data. Select ferrule gauge and permitted
single/twin form for the actual assigned conductors during routing. The grounding block's
PE rail contact is a retained conductive foot, not a ferruled wire clamp.

## Bonding plan and conductor classification

- Three prefab bonds: enclosure stud to door stud; motor-end Wago PE splice to motor body; that same splice to machine frame. The owner specifies cutting off the Wago-end jumper connector if present and inserting the correctly stripped conductor into the Wago. Keep the remaining ring lug at the bonded metal part.
- One cable-core PE connection: mains cable PE to the panel PE terminals, supplied within the incoming cable.
- One discrete external PE connection: the 12 AWG motor-conduit conductor between a suitable panel PE termination and the motor-end PE junction.
- One discrete panel PE wire: PSU PE to a panel PE terminal, using the 14 AWG default subject to actual termination/protection requirements.
- Owner's planned mechanical bonds: three conductive fasteners per rail to the backplate; four conductive fasteners from backplate to enclosure. All holes are to be drilled and tapped. Contact preparation, suitable thread engagement and installed bonding verification remain necessary. These connections are recorded as mechanical bonds, not purchased wire lengths.

Use **PE** for protective-earth conductor naming. Document the actual installation and bonding verification separately from this planned topology.

## Motor-end Wago connections

The owner selects WAGO 221-412 for standard two-conductor wire splices, including
the six 14 AWG motor-conduit conductors to the corresponding T1–T6 motor leads.
Each power splice connects only its corresponding conduit conductor and motor
lead, one conductor per port. The 221-412 accepts up to 12 AWG and specifies
11 mm stripping. Prepare these ends as bare copper; retain the actual supplied
motor-lead gauge and check it against the connector's conductor range.

For the motor-box PE junction involving the 10 AWG grounding straps, the owner
selects the three-port WAGO 221-613, rated for conductors up to 10 AWG. It
replaces the initial two-port 221-612 proposal for this junction. WAGO specifies
12–14 mm stripping; the project uses 13 mm bare ends on all three conductors.

The PE splice needs at least three suitable ports, one conductor per port:

1. Motor-conduit PE conductor: 12 AWG.
2. Modified jumper to motor body: 10 AWG if GRDKIT01 is selected.
3. Modified jumper to machine frame: 10 AWG if GRDKIT01 is selected.

The selected PE junction accommodates one 12 AWG conduit PE conductor and two
10 AWG jumper conductors, one per port. The M1 metadata footprint stores the
connector models, seven motor-conduit end preparations and the three-port PE
connection plan. Compact schedule term codes will be `B14_11mm` for the six
power-conductor ends, `B12_13mm` for the PE feed and `B10_13mm` for each modified
strap end. Six 221-412 connectors and one 221-613 are required for this topology.
These are required component counts; purchasing pack quantities remain separate.

The insulated Wago forms a wire-to-wire PE junction; placing it inside a metal motor junction box does not itself bond that box. Account for the box-to-motor-body bond through a verified conductive attachment or an explicit separate bonding connection. Motor-body and frame bonding attachment hardware/locations remain to be defined and verified.

## Wire schedule presentation

The generated CSV and editor use eight positional columns:
`From, Pin, To, Pin, AWG, Length, Term 1, Term 2`. The two `Pin` titles have
separate column positions; they are not dictionary keys. Length is in millimetres.

Pin labels include the reference, followed by an underscore and the terminal
identifier, for example `PS1_PE`, `FH1_P2A`, `TB40_TOP`, `K1_A1_TOP`.
Hidden PCB footprint fields `Wire.PinLabel.<electrical pin number>` supply
aliases for PS1 and FH1. PS1 output aliases are `V1_NEG`, `V2_NEG`, `V1_POS`,
`V2_POS`. Other compound identifiers replace delimiters with underscores.
Electrical pad numbers, schematic connectivity and routing remain unchanged.
Terminal-block device names display as `Terminal 40`, for example, for `TB40`.

Compact termination codes have no underscore between type and wire gauge:

- `F18_10mm`: single ferrule for 18 AWG, 10 mm metal barrel.
- `F2x18_10mm`: twin ferrule for two 18 AWG conductors, 10 mm metal barrel.
- `R18_1032_9mm`: ring for 18 AWG, #10-32 screw, maximum ring tongue width 9 mm.
- `B18_5mm`: bare stranded 18 AWG copper, 5 mm strip length. Omit the final
  segment when no numeric stripping length is assigned.
- `F14_TBDmm` or `FTBD_10mm`: retain unresolved length or conductor gauge visibly.
- `supplier`: a termination already installed by the device/cable supplier.
- Blank: a non-electrical routing marker that receives no termination.

These are generated presentation labels. The saved footprint `Termination.*`
fields retain the full specification, including maximum ring-width limits,
single-conductor restrictions and factory-connection descriptions. A terminal
block's compact ferrule gauge comes from the actual routed wire; its source
capability does not assign a gauge. Refresh regenerates the compact labels.

## Where information belongs

1. **Policy:** this document owns preferred gauge classes, application defaults and explicit exceptions. Root README and tools/wiring/README link here; avoid duplicating a second policy table in the BOM or generator.
2. **KiCad data:** custom schematic `Wire.Sizes` fields record per-terminal conductor sizing and `Wire.SizePlan` retains proposed bonding assemblies. M1.PE records 12 AWG motor-conduit PE. Saved PCB trace paths own physical wire endpoints and route geometry; the old schematic `Wire.Wxxx` fields are no longer the schedule source. One combined `Termination.<pin>` field on each placed footprint owns the termination selection at that terminal. TERM 1 and TERM 2 are read from the source and destination footprints. M1, J2, S1 and J6 use metadata-only footprints without physical geometry, excluded from BOM and position exports. Bonding-strap attachment hardware belongs in the BOM; mechanical bonding points do not carry wire-schedule termination fields. Reports and wire records do not own duplicate termination selections. These fields do not define routes or wire allocation; Completed routed paths generate wire rows; missing gauge assignments and unrouted connections are reported.
3. **Procurement:** `Powermatic_BOM_revP.csv` owns exact cable/device/spool/ferrule/lug/kit selections and purchase quantities. Include AWG and conductor count in cable descriptions and AWG in termination descriptions; retain the exact supplier part number. A preferred gauge without a required wire is not an automatic BOM purchase.
4. **Live schedules:** `Wire_schedule.csv` is the single live physical-wire schedule. Finder launch or browser Refresh extracts completed saved PCB trace paths into it. CSV edits remain local and never update KiCad. No traces are currently saved, so the fresh schedule contains zero routed wires. `Powermatic_BOM_revP.csv` retains SOURCE tags and stable keys so refresh updates KiCad-linked data while preserving Local purchasing rows and fields; KICAD QTY is separate from purchasing QUA. No historical CSV variants are generated.
5. **Part specifications:** `_parts` datasheets and catalog entries own supplied cable/lead sizes, terminal wire ranges and manufacturer-specific termination requirements. Keep project-wide stock policy here rather than embedding it in reusable symbols.

## Current reconciliation items

- J1's factory leads are 22 AWG. Any 18 AWG extension must be routed as a separate conductor with an explicit joining method; it cannot silently change the factory-lead gauge. The live schedule now reports only completed saved trace paths.
- Old schematic incoming-phase wire records target deleted terminal symbols. They are not read by the trace exporter. Route actual physical paths in the PCB and save before refreshing the schedule; missing routing is reported as incomplete. J2 uses a four-pad mains-gland footprint proxy matching X/Y/Z/G. Its existing incoming traces define the panel tail, not the unrecorded external supply cord; footprint `Wire.LengthScope` records this limit. Gland-only boundaries remain explicit drawn sections, with no inferred electrical termination.
- BOM cable descriptions currently emphasize outside diameter but omit AWG/core count. Its motor/controls cable and gland selections require reconciliation with the new conduit plan. Current loose-wire entries cover 14 AWG black and green/yellow and 18 AWG blue; ferrule entries cover 14 and 18 AWG. Add the required 12 AWG motor PE wire, 16 AWG control-conduit wire, conduit fittings and terminations against the eventual wire list. Choose ferrules/lugs for the actual conductor and device terminal; color alone is not a size specification.
- The saved schematic shows no dedicated DC branch overcurrent device after PS1. NDR-240-24 is a 10 A supply with constant-current overload limiting at 105–130% rated output. Reconfirm protection for the 18 AWG control conductors and especially the 22 AWG factory leads; nominal coil current and a 24 V label are not sufficient evidence of fault protection. This policy records intended classes, not final approval of every wire size.
- Exact wire insulation/type, temperature/voltage rating, routing derating and terminal preparation must be verified against the actual product and circuit. The existing BOM's “machine wire” entries alone do not establish all those specifications.

## Sources reviewed 2026-10-06

- Current saved schematic, current `Powermatic_BOM_revP.csv`, and legacy `Wire_schedule.csv`.
- Owner's 2026-10-06 motor/controls conduit conductor counts and gauges.
- [NFPA 79, 2024 edition](https://previewnorm.com/nfpa/NFPA%2079-2024%20PDF.pdf), §§12.6.2–12.6.4 (printed page 79-43); external raceway versus enclosure control-wire provisions.
- [McMaster incoming cable 7081K33, 12/4](https://www.mcmaster.com/products/wire/cable-awg~12-4/).
- Superseded selection: [McMaster motor cable 7081K6, 16/7](https://www.mcmaster.com/products/electrical-cable/cable-awg~16-7/).
- Superseded selection: [McMaster controls cable 6452T44, 18/7](https://www.mcmaster.com/products/wire/cable-awg~18-7/).
- `_parts/datasheets/T4171310004-001_Drawing.pdf`, factory lead specification 0.34 mm² / 22 AWG.
- [Hammond GRDKIT wire assemblies](https://www.hammfg.com/electrical/products/accessories/grdkit).
- [KN-G12SP-10 manufacturer cut sheet](https://cdn.automationdirect.com/static/specs/cutsheet/KN-G12SP-10_cutsheet.pdf).
- [Mean Well NDR-240 specification](https://www.meanwell.com/Upload/PDF/NDR-240/NDR-240-SPEC.PDF).
- [Wago 221-613, three-conductor 10 AWG connector](https://www.wago.com/us/wire-splicing-connectors/compact-splicing-connector/p/221-613).
- [Wago 221-412/413/415 conductor specifications](https://www.wago.com/us/products/electrical-interconnect/splicing-connectors-221).

## Panel-layout alignment grid

This industrial-controls PCB view is an alignment and wiring workspace. Optimize
it for ease of placement and routing on a 1 mm grid. Prefer integer X/Y footprint
origins and wire-target centers; use the outer face of the mounting panel as the
datum for wall-mounted devices. Preserve terminal identity and connectivity when
adapting a footprint's routing representation.

The backplate view is 462 x 462 mm, from (0, 0) to (462, 462). The 508 x 508 mm
enclosure is centered around it with a 23 mm border: its outer corner datums are
(-23, -23), (485, -23), (485, 485), and (-23, 485). Side-wall device origins use
X=-23; bottom-wall gland origins use Y=485. These layout choices do not change
the enclosure's manufacturer dimensions. See the [placement grid review](reviews/placement_grid_2026-10-09/README.md).

## Integer-grid DIN routing views

The placed integer-origin DIN equipment uses shared `Controls:<base>_Grid1mm` variants. The routing-view mounting faces are integer X coordinates and wire-target pads use ceiling-rounded integer X/Y positions. Original footprints, F.Fab and STEP remain nominal hardware references. The drawing-grid view does not change the hardware conductor or termination specification. See the [layout and complete coordinate audit](reviews/din_grid_repack/README.md).
