# Wiring and routing standard — Powermatic 1200

> Repository cleanup, 2026-10-19: references below to project scripts, generated review folders and extraction commands are historical. Those tools were removed; Project Review now edits the saved root CSVs. Technical wiring policy and installation assumptions remain here.

Control signal names are governed by [the control signal naming reference](#control-signal-naming-reference) and
its linked shared standard. Use the schematic's native net names consistently
in sizing declarations, physical wire records, PCB pad nets and generated outputs.

Preferred gauge set: **12 AWG, 14 AWG, 16 AWG, 18 AWG and 22 AWG**. Use AWG consistently; the previously stated “12GA” means 12 AWG in this project. These are preferred conductor classes, not a requirement to replace factory leads or purchased bonding assemblies with those sizes.

This document is the project policy. Actual conductor gauge and cable/part identity belong in the individual wiring records. Termination selections belong to the endpoint footprints' `Termination.<pin>` fields. A preferred gauge does not by itself establish ampacity, fault protection or terminal suitability.

## Current document set - 2026-11-09

The retained document set has eight files. [Panel drawings](Panel_drawings.pdf)
combines the module layout, terminal jumper and marker guides, approved backpanel
sheet, and Rev I enclosure-hole sheet. [Wire installation guide](Wire_installation_guide.pdf)
combines the device-label and connector-preparation sheets with the 131-row checklist.
Its preparation sheets are PDF pages 2-5; checklist pages are 6-8. Panel drawing
page 6 must be printed at 96% for its 1:1 details. Other location views use written
dimensions; the module-layout view is schematic.

The 4 November K1/K2 wire-jumper plan supersedes the BB1/BB2 busbar artwork on
the earlier module-layout sheet and the older busbar-retention wording below.
The [129-row native schedule](Wire_schedule.csv), [wire totals](Wire_length_totals.csv),
[connector inventory](Wire_connector_bins.csv), [installation order](Wire_installation_groups.json),
and [termination-code mapping](Wire_termination_types.json) are retained unchanged.
All three supporting inventory/order/mapping files are required by Project Review Refresh.
Refresh does not rebuild the printable guide. The two supplemental pendant rows
must be added when rebuilding it, using the retained record below.

Backplate rail/duct installation was reported complete on 27 October: all 20
holes were drilled and tapped 10-24, using the specified fasteners. Solid-carbide
pilot drilling followed by drilling and tapping succeeded; self-drilling screws
did not. This is the reported installation record, not a remeasurement.

The sections below retain dated design history. Current installation sequence,
terminal numbering, signal naming, and preparation source notes are consolidated
in the reference sections at the end of this document.

## Conductor construction and purchased links

All specified discrete power, control and PE wires shall use **stranded copper**,
including loose same-device and same-assembly jumper wires. Specify stranded
copper in the BOM wire descriptions and when selecting wire stock. Flexible
supply-cable cores, factory pigtails and prefabricated bonding leads also use
stranded copper; retain their supplied gauge and assembly identity. The selected
GRDKIT01 bonding leads are 10 AWG factory assemblies, separate from loose-wire
stock. Solid wire is not the default or an interchangeable procurement substitute.

**Bare** termination means correctly stripped stranded copper without a ferrule;
it does not mean solid wire. Ferrules and ring terminals remain separate wire-end
hardware selected for the actual conductor and terminal.

**Twin/dual ferrules are not used in this project** (owner decision, 2026-10-14).
Each ferrule terminates one conductor. Every feedthrough or PE wire clamp holds
one conductor with one single ferrule. Branch through separate verified internally
common clamps or an OEM-jumpered terminal bank; do not join two wires in a ferrule.
This does not alter documented bare-wire device connections, stacked individual
ring lugs at an approved stud, or rigid supplier hardware.

Rigid OEM terminal-bank jumper bars/clips and supplier busbars remain separate
purchased hardware, with their own part numbers and quantities. They are not
stranded-wire stock, loose-wire schedule entries or ferrule requirements. Retain
the HMX1-BBREV reversing busbar kit for K1/K2 as its own BOM item.

### OEM terminal-bank jumper coverage — saved board, 2026-10-28

Terminal references follow the owner-approved [module/letter numbering](#terminal-numbering-reference).
The number identifies one physical terminal strip; letters run left to right,
skipping I and O. Grounding blocks use G1-G6 separately. Module numbering does
not imply electrical commonality. The [11 x 17 jumper guide](Panel_drawings.pdf#page=3)
shows each independent jumper section and its installation checklist.

The BOM includes **one pack of five KN-10J12 ten-pole screw-down jumper bars**
for the placed KN-T12GRY-25 feedthrough blocks. AutomationDirect lists these
OEM bars for KN-T12/KN-D12 blocks, rated 24 A / 750 V; KN-10JM12 is a different
push-in accessory and is not the selected part. Jumper-screw tightening torque
is **0.4-0.6 N m (3.5-5.3 lb-in)**.

The current saved board has **18 independent jumpered feedthrough banks**:
thirteen two-pole, four three-pole, and one six-pole bank, requiring
**44 contact poles and 26 adjacent links**. The six-pole 0V section includes
2A through 2F. Four middle-right sequence-control banks are included. This
supersedes the 2026-10-15 summary of 14 banks / 33 poles / 19 links.

Cut the ten-pole stock into independent bank-length sections. The allocation
uses all five bars, leaving six poles. Guide section IDs below identify the
teal tags on the jumper guide; they are separate from terminal module numbers.

| Stock bar | Separate guide sections and pole counts | Poles used |
| --- | --- | --- |
| A | 08 (6), 01 (2), 02 (2) | 10 |
| B | 04 (3), 09 (3), 03 (2), 05 (2) | 10 |
| C | 10 (3), 13 (3), 06 (2), 07 (2) | 10 |
| D | 11 (2), 12 (2), 14 (2), 15 (2), 16 (2) | 10 |
| E | 17 (2), 18 (2); six poles remain | 4 |

Every section bridges only its own circuit. Use the OEM separators and top
covers already listed in the BOM to separate exposed cut ends and cover the
uninsulated bars. Cut between poles, deburr, and remove all metal chips before
fitting. Verify each bank's continuity and its isolation from adjacent different
circuits before wiring.

The former incoming phase blocks 4E/4F/4G are removed. E-stop
block 4A and the nine single motor/command blocks on the upper rail also require
no inter-block jumper. All 10 standalone gray blocks are shown without a teal
bridge in the guide.

The KN-G12SP-10 PE blocks connect through their conductive feet to the DIN
rail; KN-10J12 is not specified for any PE block. Two PE JMP strokes depict
the lower G5/G6 bank and upper G1/G2 bank. A separate 12 AWG wire joins
G1.2 to G5.2. The rail-2 block G3 adds a second 12 AWG wire from G2.2
to G3.1. These wire jumpers bond all three rails. The JMP strokes are not
KN-10J12 clips. Use the numbered wire clamps for the bonding wires; the PE pad
represents the conductive foot and is not an additional wire terminal.

Sources: [KN-10J12 OEM listing](https://www.automationdirect.com/adc/shopping/catalog/wire_-a-_cable_termination/terminal_blocks/jumpers/kn-10j12),
[jumper selection and torque](https://cdn.automationdirect.com/static/specs/konnectacc.pdf),
and [Konnect-It accessory guidance](https://cdn.automationdirect.com/static/specs/konnectoverview.pdf).

## FH1 at lower-right power entry — 2026-10-30

Owner photo IMG_4273.JPG and installation reports establish the order
`5K → G4 → existing end stop → FH1`. FH1 retains its 180-degree orientation;
its three fuses and three covers move with it. Its right edge is approximately
15 mm from the metal backplate edge. The DIN rails and wire ducts have not moved.
The saved layout uses the measured edge clearance to anchor FH1; its enlarged
2D module envelopes are routing proxies, not a physical clearance certification.
All existing end-stop positions are retained.

4E/4F/4G are removed. Incoming cable phases go directly to FH1's A terminals;
B remains the fused side feeding SW1. Phase identities are retained:

| Wire endpoints | Current cut (mm) |
| --- | ---: |
| J2.X (L1) to FH1.P3.A | 290 |
| J2.Y (L2) to FH1.P2.A | 260 |
| J2.Z (L3) to FH1.P1.A | 230 |
| FH1.P3.B to SW1.1 | 880 |
| FH1.P2.B to SW1.3 | 880 |
| FH1.P1.B to SW1.5 | 870 |
| G4.2 to J2.G (unchanged) | 330 |
| G4.1 to G5.1 (unchanged) | 380 |

The three cable phase cores are 12 AWG with the existing #10-32 ring terminations
at FH1. The fused wires to SW1 remain 14 AWG. Cable-tail cuts exclude the external
supply cord. G4 and both of its PE wires remain unchanged. All 18 rigid jumper
sections, 44 poles and 26 links remain unchanged. The schedule now contains
123 complete records, with no unrouted nets. Loose-stock totals are 113 wires /
87.690 m. There is no discrete black 12 AWG wire requirement; black 14 AWG stock
is 116.5 ft, rounded upward to one decimal place.

Ten end stops remain installed. One additional stop is desired at FH1's right
end but is not installed or represented as available stock. The existing stop
between G4 and FH1 must remain identifiable in the installation drawings.

The terminal requirement is 54 gray blocks plus six PE blocks; two markers per
block require 120 markers. Removing the three standalone phase blocks removes
three end covers and six 12 AWG ferrules. End covers therefore change 31 to 28,
and the 12 AWG single-ferrule requirement changes 15 to 9. Purchasing packs for
these parts do not change. Separator and jumper-cover quantities are unchanged.
The additional desired end stop is recorded as outstanding, not as installed.

The mains gland J2 remains on the right wall, centered across enclosure depth,
70 mm above the enclosure bottom. The top motor/control entries retain their
routes; the two right-wall alternatives and two McMaster 9357K15 plugs retain
the previously documented hole plan. FH1 relocation does not change hole locations.

## Panel routing policy

This is an enclosure wiring layout, not a PCB manufacturing file. Tracks depict
individual wires. Route geometry, connection identity, wire size and endpoint
preparation are separate requirements. This section owns the current routing
policy; helper READMEs and dated review proposals must defer to it.

The owner supplied the twelve rules below on 2026-10-12. The subsequent
low-current clarification replaces the original 18-AWG eligibility shortcut.
On 2026-10-13 the owner adopted at least two local connections (including all-local
circuits), a TB fallback, and the duct serving the most connections as the working
duct. Recording the policy does not change the PCB or implement a routing checker.

### Terms and connection counting

- **Circuit:** the electrically common net being allocated, rather than an entire
  series control sequence containing several different nets.
- **Connection:** a required external/discrete-wire attachment node on that net.
  Count after recognizing verified internal connections, supplier contacts and
  retained links. A verified internally common group can have several available
  physical clamps; retain those clamp choices in the wire plan. Raw pad count
  is not the connection count.
- **PTP:** one continuous physical wire between its actual terminations, with no
  intermediate feedthrough terminal. It can contain several drawing segments,
  cross ducts and pass through a gland.
- **FT:** an individual feedthrough terminal component.
- **TB:** the jumpered distribution bank for one circuit, containing one or more
  terminal components. Size it for the actual wire ends and permitted clamp
  capacities. A single component uses its internal common connection; a bank
  with several components needs explicit bridges between them. Existing `TB#`
  footprint references are retained; this terminology does not rename them.
- **Chase:** the right-hand vertical duct used to transfer between horizontal ducts.
- **Local/remote:** the destination's relation to the particular horizontal duct
  being considered, not its wire gauge, net name or membership of an assembly.

Gland IN/OUT markers represent a continuous conductor and are not two extra
connections. An external endpoint represented through a gland is counted once,
not again for every routing marker. Unused clamps and unallocated block graphics
do not add connections. A shared net alone does not establish an installed jumper.

### Owner routing and placement rules

1. A **local connection** is a terminal on the closest rail above or below the
   duct. Other connections are **remote connections**.
2. A wire in a duct targeting a local connection travels along the duct until
   directly opposite the terminal, then leaves the duct and proceeds directly
   to that terminal. For a horizontal duct this aligns the exit with the terminal's X.
3. A wire targeting a remote connection travels right to the chase, turns up or
   down, and reaches the target duct. It enters that duct and follows rule 2 for
   its final approach. Entering another duct changes the local/remote relation
   for that approach; it does not change the wire's continuous layer assignment.
4. A circuit with **two connections** uses PTP wiring with no intermediate FT,
   except for the mandatory motor/command enclosure-entry landings below.
   Crossing a duct or rail does not by itself require a terminal block.
5. A **three-connection low-current control circuit**, with at least two connections
   local to its working duct (including all three local), may use two PTP wires
   when the junction device provides separate verified internally common clamps,
   one conductor per clamp. The chain `A–B–C` uses separate B clamps and a single
   ferrule at each ferrule-prepared wire end. If B has only one suitable clamp,
   use the TB fallback.
6. A **four-connection low-current control circuit**, with at least two connections
   local to its working duct (including all four local), may use a PTP chain where
   each junction device provides separate verified internally common clamps.
   Four independent endpoints require **three** PTP wires: `A–B–C–D` uses separate
   clamps at B and C, with one conductor and one single ferrule per prepared end.
   If either junction lacks suitable separate clamps, use the TB fallback. Two wires
   can suffice only when an existing verified internal connection already joins
   a pair; after collapsing that connection there are three independent nodes.
7. A circuit with **five or more connections** uses a jumpered TB, including
   low-current control circuits.
8. A **power or PE circuit with three or more connections** uses a jumpered TB.
   Low-current control eligibility is determined for the whole circuit by its
   function and loads, as described below, rather than by the smallest AWG
   number among its wires. A three- or four-connection control circuit uses a TB
   whenever the local-count or actual termination requirements for PTP cannot
   be met. Unclassified circuits require classification first.
9. Place a TB ideally at the closest available rail position to the geographic
   center of the circuit's parts. This is a strong placement preference. The
   bank must still fit its allocated rail space with its necessary accessories.
10. Left-wall parts belong to the duct or rail directly across from them and
    follow the same routing rules.
11. Place related parts next to the other parts in their circuits. Circuits should
    generally flow left to right along a rail. Shared parts participate in several
    circuits; this is a placement preference rather than a unique coordinate solution.
12. Bottom-wall entries belong to the lowest duct and route directly into it.
    Top-wall entries belong to the uppermost duct and adjacent right-hand chase.
    They remain pass-through markers, not wire junctions or gauge-change points.

**Same-device jumper exception (owner direction, 2026-10-14):** a loose wire
between terminals on the same physical device may take a short, accessible
path at that device without entering a duct. Keep its assigned terminal IDs,
wire size and termination types, one continuous layer, rounded corners and
drawing clearance. It remains a discrete physical wire in the schedule; this
exception does not make it a factory link or an invisible internal jumper.
Wires that enter a duct still follow the local/remote and lane rules above.
The applied example is `K5.43 → K5.A1.TOP`.

**Same-assembly extension (owner direction, 2026-10-14):** discrete wires
between parts in one documented assembly may also take short, accessible
paths at that assembly without entering a duct, provided the change adds no
wire crossings. Documented membership, rather than proximity or sharing a
circuit, defines the assembly. Current examples are the K1/K2 reversing
assembly, the complete K4/K5/K6 speed assembly with OL4/OL6, and the paired
Q1/PS1 control-power module. Keep actual terminal assignments, wire sizes,
termination metadata and one continuous layer per wire. Supplier busbars,
direct-mounted interfaces and supplied leads still take precedence over
adding loose wires.

Verified busbars, direct-mounted overload contacts, supplied suppressor leads,
native internal jumper groups and documented retained/device-specific links are
recognized before allocating new loose wiring. The component-specific exceptions
below still apply, including the K1/K2 reversing jumpers and the K5 shorting bridge.
Do not add redundant wires or TBs to recreate an existing fixed connection.

All loose-wire junctions must land on actual device clamps, FT/TB clamps or an
explicit splice footprint. Off-pad T-junctions in a duct are not permitted.
Internally common pads must have compatible assigned nets and documented jumper
groups. Different-net graphical crossings are not electrical junctions.

### Low-current control eligibility

The original "18 AWG or higher" proposal meant numerically higher AWG values
(thinner wires), but the owner's purpose was to identify low-current wiring.
The revised strategy uses the **whole circuit's function and connected loads**.
Wire gauge and terminal suitability remain independently specified.

| Circuit class in the current design | Treatment |
|---|---|
| 24 VDC command, permission, interlock, feedback, coil and indicator circuits: `CONTROL_*`, `DIRECTION_*`, `SPEED_*` | Eligible for the small-circuit PTP exception when the locality and actual termination requirements are met. |
| The S2/S3 external control conductors, although specified as 16 AWG | Remain low-current control circuits. Their raceway wire size does not force a TB by itself. Preserve the 16 AWG specification. |
| J1's 22 AWG factory control pigtails | Remain control wiring; preserve their supplied gauge and termination requirements. |
| `+24V`, `+24V_EN`, `0V` serving the existing control loads | Control supply/return circuits; assess aggregate loads. The five-or-more-connection rule still requires a TB. New motor, heater or other substantial DC loads require reclassification. |
| Incoming/fused/switched/direction mains, PSU AC input, motor power and `PE` | Power/bonding class, outside the low-current PTP branching exception. The two-connection PTP rule still applies to newly allocated two-ended wires. |
| Unknown function or load | Review classification; do not infer it from gauge or a net-name prefix alone. |

This refinement supersedes the earlier tentative answer that any conductor
thicker than 18 AWG would force a TB. It does not make a partial exception for
one thin branch of an otherwise power circuit. For context, AD's HMC coil table
lists 6 W at 24 VDC for the HMC-9B family, approximately 0.25 A per coil; the
existing operator signals switch control loads, not the motor-power conductors.
[HMC coil characteristics](https://cdn.automationdirect.com/static/specs/ironhorsehmcandhtor.pdf#page=13).

Junction eligibility requires verified internally common separate clamps and
the actual conductor size, preparation and barrel length for each clamp.
Use one single ferrule per prepared conductor; preserve each wire's assigned
gauge rather than resizing it to fit a junction. The former twin-ferrule branching
exception is retired. [AD ferrule specifications](https://cdn.automationdirect.com/static/specs/dinwiring.pdf).

The existing endpoint preparation selections remain in force. In particular,
PE clamps and H1/H2 have single-conductor selections; PS1 and Q1 have bare-wire
selections. They are not automatically eligible branch junctions. Existing
internally common separate clamps can distribute connections without a fabricated
output-to-output jumper. Ferrule totals above illustrate ferrule-compatible
separate-clamp chains; actual wire-end preparations come from the selected endpoints.

### Working duct and allocation decision

For each circuit, use the horizontal duct serving the **most connections** as its
working duct. Count local connections using rule 1, after collapsing verified
internal/fixed connections. Include left-wall devices at the level across from
them and wall entries at their corresponding uppermost/lowest duct interface for their external
endpoints. Record the counts and the working duct before applying rules 5 and 6.
Do not count every endpoint as local merely because its wire eventually enters
its target duct. A tie leaves several eligible working ducts; record the chosen
one and its routing/terminal-access basis rather than silently choosing a source.

| Independent connections | Allocation |
|---|---|
| Two | PTP, without an intermediate FT. |
| Three or four, low-current control, at least two local to the working duct, verified separate internally common junction clamps | PTP is permitted, including all-local circuits. Use two wires for three independent nodes, three wires for four; one conductor per prepared clamp. |
| Three or four, low-current control, failing locality or termination requirements | Jumpered TB fallback. If suitability is unverified, retain the PTP proposal as unconfirmed; plan a TB fallback rather than assuming approval. |
| Three or more, power or PE | Jumpered TB. |
| Five or more, any class | Jumpered TB. |
| Unknown class | Resolve function/load before selecting the applicable row. |

Verified fixed connections take precedence. PTP is permitted rather than mandatory
for eligible three/four-node controls; choose the concrete clamps and individual
wires before claiming completion. A TB bank is sized by actual wire-end capacity,
not by the circuit's raw pad count.

### Terminal access and placement choices

The working-duct, at-least-two-local and TB-fallback decisions are adopted.
The following implementation choices still require an explicit recorded basis:

- **Terminal approach side:** a nearest-rail terminal may face the opposite duct.
  Identify an accessible direct approach under rule 2 while preserving TOP/BOT
  terminal identity. Do not treat geographic eligibility as proof of clamp access.
- **Centroid and ties:** for an enclosure plan, the recommended center uses the
  in-panel parts and actual entry interfaces, not arbitrary drawing positions
  of external motor/operator illustrations. Record the chosen rail/duct and
  how ties or occupied rail positions are resolved.

Retain unfinished stubs until their actual terminations are allocated. Apply the
TB fallback when the PTP requirements cannot be met; do not infer a completed
physical wire list from a many-pin net.

### Layer assignments

Each physical wire uses **one continuous copper drawing layer from terminal to
terminal**. Do not insert inline vias or change layers within a wire. A genuine
intermediate terminal divides the path into separate physical wires, each with
its own complete layer assignment. A gland is a pass-through marker, not an
intermediate electrical termination.

Reuse each available layer for as many compatible whole wires as possible before
adding another. Check the entire wire against other wires and reserved hardware
on that layer, using the saved **0.2 mm minimum edge clearance**. Crossings and
loose-wire junctions on one layer must land at actual matching terminal pads.
When the available layers cannot accommodate the whole paths, enable additional
copper drawing layers in KiCad's stack. Keep duct positions provisional until
more of the circuit is populated.

This owner direction supersedes the earlier mandatory In1.Cu assembly,
In2.Cu same-duct and B.Cu remote assignments. The local/remote definitions,
right-chase geometry, terminal approach rules and PTP/TB strategy still apply;
a layer alone no longer identifies the wire's route category. F.Cu can carry
whole wires as well as explicitly grouped JMP hardware.

The completed drawing now contains 45 power wires, 47 control wires (42 added
in the control pass and five earlier examples) and one frame-PE wire. Each of
these 93 physical paths stays on one drawing layer. At the provisional paths,
the first onion pass uses nineteen drawing layers, with twenty enabled because
KiCad requires an even layer count. A nineteen-wire conflict clique proves
that nineteen layers are necessary for these fixed paths; compatible whole
wires share those layers. No vias
remain. Six formerly sharp corners in the K4/K6 phase feeds now use 5 mm arcs.
The seven motor conductors retain one layer through J4 to M1.

J2/J3/J4 use all-layer logical connection targets so a wire can enter a gland
on its assigned layer. These targets are pass-through markers, not electrical
terminations. J3's eighth pair carries the separate S3 RUN conductor; pairs 9–11 serve
the added timer/selector connections. Five S2 and six S3 control wires remain
16 AWG from their actual
panel clamp to their station clamp; a gauge change would require a real
intermediate termination. New discrete internal control wires remain 18 AWG.

J1 is vertically aligned with the lower DIN rail at Y = 297 mm. Its four factory
pigtails remain 22 AWG and are limited to the owner's approximately 200 mm
supplied length. Their drawn routes are 64 mm (pin 1 to 4B.BOT), 41 mm (pin 2
to 4A.TOP), 55 mm (pin 3 to 4A.BOT) and 138 mm (pin 4 to K3.A1+). The
leads connect directly to nearby lower-row clamps, outside the ducts, to retain
length for end preparation. 4A is the owner-approved single feedthrough that
joins the two factory loop pigtails; it is a specific factory-interface exception
to the usual two-node PTP rule. Do not add the stock-wire 100 mm cut allowance
to a fixed factory lead or assume it can be extended without a real junction.

The placed K1/K2/K4/K5/K6 coil TOP/BOT pairs are internally common. Use the
facing duplicate clamp to keep local wires in the working duct and avoid a
second conductor at a device clamp. Suppressors remain supplied connections at
A1.TOP/A2.TOP. Owner confirmation on 2026-11-02 supersedes the former assumption that S2's 1T-3T-5T straps were installed. All three original pendant jumpers (2T-4B, 2B-4T and 3B-1B) have been removed. Add 1T-3T, 3T-5T and 2B-4B later: all three are 16 AWG blue station wires with bin RA ring terminals at both ends. The first two are explicit supplemental checklist rows; 2B-4B remains a native routed row.

The owner also confirms removal of S3 straps 1T-3T, 5T-7T, 1B-2B, 3B-4B, 3B-5B and 6T-4T. Only 7B-8B remains. This matches the current timed speed-change schematic. No replacement S3 jumpers are pending.

Block-to-block JMP bridges use a bold drawing stroke of **90% of the smaller
endpoint JMP pad's outer diameter**: 3.6 mm for the 4 mm gray-block pads and
2.7 mm for the 3 mm PE-block pads. All 28 existing bridges remain on F.Cu,
with their original endpoints and bank grouping. Their stroke is a visibility
convention, not a field-wire AWG or a new wire-procurement row.

Changing a wire's layer does not change its endpoints, path, width or net.
Historical layer and via trials remain dated snapshots, not current policy.

### Draft horizontal duct lanes — 2026-10-13

The owner authorized these horizontal lane rules on 2026-10-13 for the three
existing routing examples and three additional wires. Use the saved netclasses'
inherited **0.2 mm minimum edge clearance** for now. Round lane positions outward
to the 1 mm grid. The original six-wire trial is now part of the completed routing set, while
lane coordinates remain provisional. The local/remote, working-duct and
continuous-layer rules still apply.

The subsequent owner direction is to populate more circuits before fixing final
lane positions. Current lane coordinates remain provisional. Incoming cable
phase cores land directly at lower-right FH1 P3.A/P2.A/P1.A for L1/L2/L3.
The retired 4E/4F/4G blocks are absent. Incoming PE lands at G4.2; the separate
12 AWG G4.1-to-G5.1 bond remains. J2 cable-tail lengths exclude the external
supply cord. FH1's fused B terminals feed SW1 as before.

The downstream routes continue through FH1 and SW1 to the existing phase banks,
Q1/PS1 and K1/K2 through their supplied busbars. The motor-power routes continue
through the direction banks to K4/K6 and their direct-mounted overloads. OL4 and
K5 join the T1–T3 banks; OL6 feeds T4–T6 directly to J4 through the chase. K5's
1–3–5 shorting bridge and the main-PE-to-J4 feed are also routed. Motor phases
remain 14 AWG and motor PE is 12 AWG. The control pass now completes the
E-stop, indicators, interlocks, overload chain, coil feeds/returns and eleven
operator-station conductors; their duct positions remain provisional.
The previous inline layer transitions have been removed from completed power
wires; the continuous-layer rule above now governs the drawing.

1. Split each horizontal duct at its centreline into a **top half** and a
   **bottom half**. For a 40 mm duct these are two 20 mm lane sections. They are
   halves of one duct segment, not separate duct segments or KiCad layers.
2. For a **local destination**, use the half on the destination terminal's side
   of the duct: top for a terminal above it, bottom for one below it. Run along
   that half until opposite the terminal, then approach the terminal directly.
3. For a **remote destination**, use the half closest to the device whose wire
   is entering the source duct. Run right to the chase. After transferring to
   the target duct, choose its half using the local-destination rule.
   Left-wall devices use their corresponding duct/rail relation; bottom-wall
   entries use the nearest outer duct half: bottom for bottom-wall entries,
   top for top-wall entries.
4. Pack each half starting at its **inside border**, the duct centreline.
   Place the first wire as close to that border as its drawn width and the
   required drawing gap allow, keeping the full stroke within its half.
5. Add each subsequent parallel wire tightly outside the occupied wires,
   towards that half's outer duct wall. Use the smallest permitted drawing gap
   between wire edges. For widths `w1` and `w2` and edge gap `g`, parallel
   centreline separation must be at least `(w1 + w2) / 2 + g`. Respect the 1 mm
   routing grid by rounding the offset outward, never inward below that gap.
6. Parallel runs may share an XY lane on different drawing layers, as approved
   by the owner on 2026-10-13. Apply the width-plus-gap separation to runs on
   the same layer. Each physical wire still stays on one continuous layer;
   top/bottom lane selection does not determine its layer.

The current packing gap is 0.2 mm. It is a **drawing clearance**, not a PCB
manufacturing clearance or an established electrical separation requirement.
Current AWG track widths represent nominal bare conductor diameters, so compact
drawn lanes do not establish physical duct fill or spacing between insulated
wires. Physical packing must use the actual wire outside diameters and any
applicable circuit-separation requirements.

For lane ordering, use the owner's onion / woodgrain strategy: peel the
outermost terminal spans first, alternating the two outer sides, then place
successive inner spans inside them. Reduce wire crossings before reducing
wire length: a crossing reduction wins even when it adds length. Order the
horizontal duct halves and right-hand chase together. Retain rounded corners,
terminal approaches and the 1 mm route grid.

The first pass fixes device placement, bank assignments, widths and physical
wire topology. Its discrete lane moves and adjacent lane exchanges converged
to a local optimum: 853 to 288 proper XY crossings and 37.113 to 36.696 m of
drawn wire. Parallel overlaps and shared-clamp joins are excluded from the
crossing metric. This is a first pass, not proof of a global optimum or a
finished cut-length schedule. Bank reassignment proposals are reviewed
separately and are not applied by the lane pass. See the
onion routing review (historical reference).

The subsequent 2B return swap is applied: H2.X2 uses 2B.TOP and routes
locally in D2; H1.X2 uses 2B.BOT and reaches D1 through D3 and the right
chase. Both remain single 18 AWG wires. Bank placement, hardware bridges and
all other wire paths were preserved in that pass. It reduced the drawing to
273 proper XY crossings and 36.002 m of drawn wire, saving approximately 694 mm.
See the 2B swap verification (historical reference).

The 2026-10-14 shortening pass is applied, including the short K5 same-device
jumper. Seven physical wire paths change; placement, terminal assignments,
wire sizes and all other routes stay fixed. It saves approximately 210 mm and
reduces proper XY crossings from 273 to 267, with no wire pair gaining a
crossing. That pass ended at 35.792 m of drawn wire, before cut allowances.
All 93 physical wires remain on continuous individual layers, using the same
nineteen drawing layers with twenty enabled. See the
applied shortening verification (historical reference).

The same-assembly direct-routing pass shortens four further wires: K1.32 to
K2.A1.BOT, K4.32 to K5.A1.BOT, and the two Q1 outputs to PS1's L/N inputs.
It saves approximately 445 mm, bringing the drawn total for that pass to 35.347 m,
and reduces proper XY crossings from 267 to 265. No wire pair gains a
crossing. Each wire remains on one continuous layer. The L2 PSU feed moves as a whole
from B.Cu to existing In2.Cu to separate the overlapping runs; no additional
layer is needed. All other routes, placement, terminal assignments, gauges
and hardware bridges are preserved. See the
assembly-routing verification (historical reference).

The coordinated approach pass is applied for the five remaining assembly
wires: K2.32 to K1.A1.BOT, OL4.96 to OL6.95, K6.32 to K5.31, K5.32 to
K4.A1.BOT, and K5.44 to K6.A1.BOT. Nine surrounding approach/exit paths
change with them, while placement, terminal assignments, wire sizes and all
other routes stay fixed. Short parallel XY overlaps use separate continuous
layers. 2C.TOP to K1.A2.BOT moves as a whole from In6.Cu to In8.Cu;
1K.TOP to K1.43 moves as a whole from In8.Cu to In16.Cu. No additional
layer or inline via is needed. The complete pass saves approximately 546 mm
and reduces proper XY crossings from 265 to 232, with no wire pair gaining
a crossing. The current drawn total is 34.801 m before cut allowances.
Native checks of the installed PCB verify all 93 physical wires and continuity
against the saved schematic. See the
coordinated routing verification (historical reference).

### Drawing and schedule rules

Use horizontal/vertical segments with rounded 90-degree bends and the appropriate
per-wire AWG width. Width requirements apply to classified stubs too. Leave an
unclassified wire's gauge unresolved rather than guessing from its existing width.
Prefer integral placement origins and wiring-target coordinates while retaining
the physical footprint outlines and STEP geometry.

Saved completed terminal-to-terminal routes own the physical wire schedule.
An intermediate actual termination splits a path into separate wires; a gland
does not. Supplier/internal/retained connections are recognized separately.
Unfinished stubs are reported as incomplete and omitted from completed-wire rows.
AWG comes from sizing/termination metadata, not from measuring a track width.
Stock-wire cut estimates use native path length plus 100 mm, rounded upward to
10 mm. For the 2026-10-14 length estimate, allocate this existing 100 mm as
20 mm of termination allowance and 30 mm of service slack at each end.
Termination allowance is a cut-length budget, not the specified stripping length.
The current totals by AWG/color are in `Wire_length_totals.csv`: 88 loose wires,
73.33 m including allowances. They exclude J1 E-stop factory leads, J2 mains
cable tails and the GRDKIT01 factory bonding strap. Discrete panel feeders
from the incoming blocks remain included. External conduit wire paths are
illustrative, so their lengths remain estimates until checked on the machine.
Fixed factory pigtails retain their supplied length; verify the drawn path
and end-preparation allowance fit that length instead of adding this cut allowance.
Do not add inline vias: assign one layer to the complete physical wire. Old via-based trials are superseded. Native wire lengths still sum the track segments and arcs on the continuous layer.

These geographic/PTP/TB decisions are documentation policy. The existing exporter
checks saved paths, nets, gauges, terminations and known fixed links; this document
update does not add automatic enforcement of all the new routing/placement rules.

## Preferred applications

| Gauge | Project application | Current evidence / qualification |
|---|---|---|
| 12 AWG | Incoming mains cable phase and PE cores; discrete PE feed from G4 to the main PE bank; discrete motor-conduit PE conductor | Selected McMaster 7081K33 is 12/4 SOOW. Owner specifies one 12 AWG PE conductor alongside T1–T6 in the motor conduit. KN-G12SP-10 includes 12 AWG in its wire range; conductor preparation and termination selection still apply. Incoming cable phase cores land directly at FH1; no loose black 12 AWG panel feeds remain. |
| 14 AWG | Six motor-conduit conductors T1–T6; discrete panel motor-power and PSU AC-input wiring; default custom panel PE wiring where sizing permits | Owner specifies six motor conductors. Current BOM stocks 14 AWG black machine wire and 14 AWG green/yellow machine wire. Per-circuit protection and actual terminal specifications still govern. |
| 16 AWG | Individual external control wires in conduit: five for S2 and six for S3 | Owner confirms individual wires and selects 16 AWG for both runs. Match circuit protection, wire product and terminations to the installed conductors. |
| 18 AWG | New discrete 24 V control wiring inside the enclosure/operator stations, including coil/interlock/indicator circuits | Legacy control wiring uses 18 AWG. Match protection to the actual wires and factory leads in each branch before construction. |
| 22 AWG | Small factory connector pigtails, specifically J1's T4171310004-001 M12 leads | The manufacturer drawing specifies 0.34 mm² / 22 AWG. This is a factory-lead class; use 18 AWG as the normal new discrete control-wire choice. Do not infer that all other connector/cable variants have the same leads. |

The preferred classes do not automatically imply a loose-wire spool for every size. The incoming 12 AWG phase conductors and 22 AWG M12 leads are supplied by the selected cable/device. Motor-conduit PE and the G4-to-G5 PE bond are separate 12 AWG green/yellow wires. Direct cable-to-FH1 termination eliminates the former three loose black 12 AWG phase feeds. Purchase discrete wire only where the physical wire list actually requires it.

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
`reviews/routing_standards_2026-10-08/assignments.json` (historical reference).

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

The schedule's `Color` is conductor insulation color, separate from ferrule or
ring-terminal collar color. Refresh resolves native `Wire.Sizes` declarations
by endpoint, net and AWG, retaining incoming and factory lead colors.
The owner identified WXP-4A-1204-25 cores as GRN, RED, BLK and WHI on
2026-10-30. J2's saved footprint assigns G/PE Green, X/L1 Black, Y/L2 Red
and Z/L3 White. The two supplied 10 AWG GRDKIT01 bonds are Green/Yellow,
as specified in the [Hammond manufacturer drawing](https://www.hammfg.com/files/parts/pdf/GRDKIT01.pdf?v=1697661958).

### Loose-wire purchase selection — 2026-10-14

All selected wire is stranded copper MTW, rated 600 V. McMaster's metric PE
wire uses tin-plated copper; it remains stranded. Selection covers the current
cut estimates, including termination allowance and service slack, with no
E-stop leads, mains cable or prefabricated bonding straps added to loose stock.

| AWG | Color | McMaster SKU | Purchased stock lengths |
|---|---|---|---|
| 12 | Black | 9874T611 | 1 x 25 ft |
| 12 | Green/Yellow | 6513T631 | 2 x 10 ft |
| 14 | Black | 9874T511 | 1 x 100 ft |
| 14 | Green/Yellow | 6513T531 | 2 x 10 ft |
| 16 | Blue | 9874T421 | 1 x 100 ft, owner-approved 2026-10-15 |
| 18 | Blue | 9874T321 | 1 x 50 ft |

Each selected stock length can supply its allocated complete cuts. The owner
selected one 100 ft roll for 16 AWG blue; that purchase remains unchanged after
the revised external-run estimates below. The selected 9874-series stranded MTW family has
25 ft increments; the 6513-series green/yellow option has 10 ft stock lengths.
In the BOM's wire rows, ORDER counts purchased lengths, PACK is feet per length,
UNIT is FT, and COST is per purchased length. NAME is only a display name.
QUA holds the required cut feet, including the existing termination/service
allowance, rounded upward to 0.001 ft. Accessory QUA values count required
pieces, including 48 terminal markers at one per feedthrough/PE block. Duct
QUA counts three 1 m stock lengths, which supply the five cut sections.

Sources: [McMaster stranded MTW wire](https://www.mcmaster.com/products/wire/cable-designation~mtw/),
[14 AWG PE wire](https://www.mcmaster.com/6513T5-6513T531/),
[12 AWG PE wire](https://www.mcmaster.com/6513T6-6513T631/).

## External conduit runs — owner specification, 2026-10-06

| Run | Conductors | Destination / function |
|---|---|---|
| Motor conduit | Six 14 AWG plus one 12 AWG | One 14 AWG conductor for each of T1–T6; one 12 AWG PE conductor |
| Controls conduit, S2 | Five individual 16 AWG | S2 forward/reverse/stop button station |
| Controls conduit, S3 | Six individual 16 AWG | S3 OFF/LOW/HIGH drum switch |

The enclosure-to-S3 controls run contains eleven individual 16 AWG control conductors, plus its separate PE. Five control conductors continue through S3 to S2; six terminate on S3. The owner confirms individual wires in conduit and selects 16 AWG for S2/S3. NFPA 79 (2024), §12.6.2 specifies at least 16 AWG for ordinary lighting/control conductors on the machine and in raceways, or 18 AWG where part of a jacketed multiconductor cable assembly. The 18 AWG enclosure/operator-station provision in §12.6.3 does not establish an 18 AWG minimum for the external conduit run. Retain 18 AWG as the internal panel control-wire default.

The motor conduit replaces the previous McMaster 7081K6 16/7 motor-cable plan. The S2/S3 conduit specification supersedes the previous single McMaster 6452T44 18/7 controls-cable plan. The motor/control cable glands are superseded by the LFNC-B fittings below. Existing gland artwork/models at J3/J4 are drawing proxies, excluded from BOM auto-add; they are not the selected fittings' CAD models.

### Motor and command entry strips — owner direction, 2026-10-15

Every conductor in J4's motor conduit and J3's command conduit must land on an
entry terminal block before continuing inside the enclosure. This interface rule
also applies to two-connection circuits. Each clamp accepts one conductor; the
gland remains a continuous pass-through, not a termination. Use the TOP/1 clamps
for the external leads and separate common clamps for the panel-side wires.

The initial entry-strip revision reused 43 gray feedthroughs and five PE blocks.
The two-timer integration adds fourteen gray feedthroughs, for 57 gray blocks
and five PE blocks in the current drawing. Entry banks occupy the upper rail;
phase distribution remains on the lower rail. The fuse and reversing assemblies
retain their internal geometry after the approved upper-rail move.

| External conductor | Entry clamp | Panel-side destination(s) |
|---|---|---|
| M1 T1 | 1A.TOP | 1A.BOT to OL4.2; common 1B.BOT to K5.2 |
| M1 T2 | 1C.TOP | 1C.BOT to OL4.4; common 1D.BOT to K5.4 |
| M1 T3 | 1E.TOP | 1E.BOT to OL4.6; common 1F.BOT to K5.6 |
| M1 T4 / T5 / T6 | 1G / 1H / 1J.TOP | Matching BOT to OL6.2 / .4 / .6 |
| M1 PE | G1.1 | G1.2 to lower main PE bank G5.2 |
| S2 forward / reverse | 1N / 1Q.TOP | Common bank clamps to K1/K2 auxiliary contacts |
| S2 direction enable | 1M.TOP | Common 1K/1L BOT clamps to K4.44 / K6.44 |
| S2 run / S3 run | 1S / 1T.TOP | 1S.BOT to middle run bank 3A–3C; 1T.BOT to K6.43 |
| S2 overload enable | 1W.TOP | 1W.BOT to OL6.96 |
| S3 high / low speed | 1U / 1V.TOP | Matching BOT to K5.43 / K6.31 |
| S3 timed-low supply (1B) | 1X.TOP | 1X.BOT to TD2.18 |
| S3 high enable (3B) | 1Y.TOP | 1Y.BOT to bank 3D–3F |
| S3 high trigger (3T) | 1Z.TOP | 1Z.BOT to bank 3G–3H |
| Command PE to S3 splice GS1 | G2.1 | Bonded upper PE rail to G1 and its lower-bank bond |

The original terminal references are retained even where the six reclaimed
blocks change net. Rebuild only matching bank JMP links. All filled Controls silhouettes belong on B.Adhesive and stay opaque.
B.Adhesive uses the same RGB (72, 72, 72) as the former F.Adhesive backgrounds;
retain the Fab/Silkscreen detail and source model geometry. Each physical wire remains on one continuous drawing
layer; the entry revision uses 24 copper drawing layers. Exterior wire estimates
continue to use the installed-run assumptions below, not the illustrative path.

### External routing separation — owner direction, 2026-10-15

Motor conductors use J4 exclusively and follow their own conduit path to the
motor junction box. Control and command PE conductors use J3 exclusively. Route
all panel-to-pendant conductors into the drum-switch enclosure through its rear
entry, then out its second rear knockout and into the pendant through its bottom
entry. The five command wires continue through S3 without extra terminations;
the PE continues through the specified S3 bonding/splice arrangement. Wires that
terminate on S3 stop there. Do not route control wires through the motor drawing,
or motor wires through either control-station drawing. Keep the two external
bundles spatially separate; their illustrative XY lengths do not replace the
owner's installed conduit-run assumptions.

H1 and H2 mount at one height across the left-wall depth, 50 mm center to center,
symmetrically about that wall's depth centerline. Their 2D side projections
coincide, so separate their logical wire targets and reference labels. Retain
the true wall-plane datum and use placement offsets to position the existing
shared models; do not duplicate the part models. SW1 aligns with the middle
DIN rail. The motor drawing and its local frame bond stay clear of the enclosure.

### Top-entry conduit plan — owner direction, 2026-10-14

J4 is at (431, -277), J3 at (367, -277), both rotated 180 degrees:
64 mm center spacing on the 1 mm grid. J4 is the motor entry; J3 is the
controls entry immediately to its left. Their pass-through pin pairs and nets
remain unchanged. Panel wires approach these entries through the upper duct
and right-hand chase, retaining one continuous layer per wire.

Use **1/2-inch trade LFNC-B** for all three runs. This is the ordinary NEC
356.20 minimum; 3/8-inch use has specific exceptions and is not the basis of
this plan. Selected McMaster wire outside diameters are 0.14 inch for
14 AWG black, 0.17 inch for 12 AWG PE, 0.12 inch for 16 AWG blue, and
0.15 inch for 14 AWG PE. With these diameters and the same conduit fill area,
the motor bundle uses about 36.6% and the control trunk, including its
14 AWG PE, about 34.4%. Both remain below the 40% fill limit. AWG alone does
not specify insulation diameter. The controls' metal housings require separate
PE conductors because LFNC provides no bonding path.

| Run | Conductors | Entry and exit | Estimated conduit |
|---|---|---|---|
| Panel to motor junction box | Six 14 AWG power wires plus one 12 AWG PE | Straight upward from J4, loop downward, straight into top of motor junction box | 2 ft |
| Panel to drum switch S3 | Eleven 16 AWG controls plus one 14 AWG green/yellow PE | J3 90-degree fitting points rearward; straight fitting into first rear S3 knockout | 3 ft |
| S3 to pendant S2 | Five continuing 16 AWG controls plus one 14 AWG green/yellow PE | Second rear S3 knockout uses a downward 90-degree fitting; loop into bottom of S2 through straight fitting | 1 ft |

#### Installed wire-length estimates — owner direction, 2026-10-15

Use the saved routed length from the panel terminal to the gland's IN target,
then replace the illustrative gland/outer drawing with the run lengths above.
The motor run adds 2 ft plus 6 inches inside the motor box. A wire ending in S3
adds 3 ft plus 6 inches inside the switch box. These six-inch box allowances
replace the normal termination/service allowance at that external end; retain
20 mm termination and 30 mm service slack at the panel end.

The five continuous panel-to-S2 control leads include both conduit sections
(3 ft + 1 ft), 6 inches for passage inside S3, and the normal 20 mm termination
plus 30 mm service slack at each actual wire end. They do not acquire a new
termination at S3. The GS1-to-GL2 PE wire uses 1 ft plus those normal allowances
at both ends. Local station jumpers/pigtails keep their drawn lengths and normal
end allowances. Round every complete cut upward to 10 mm. Factory leads, mains
cable and prefabricated bonding straps remain separate from loose stock.

This section records the installed-run basis. The old project-side
`tools/wiring/external_lengths.json` and automatic Refresh software were removed
during repository cleanup. Automatic wire generation was restored on 2026-10-27
in `~/Projects/bom_review/adapters/powermatic_1200/`; software and configuration
remain outside this hardware repository. Open Project Review, select
`docs/Wire_schedule.csv` in Documents, and use Refresh to regenerate that file
and `docs/Wire_length_totals.csv` together. Generation applies these assumptions
to the current saved panel-to-gland paths rather than substituting the
illustrative exterior tracks. `Wire_length_totals.csv` aggregates estimated route length,
termination allowance, service slack and rounding. Purchase PACK/ORDER stay fixed.

The measured 0.868-inch S3 knockouts correspond to the nominal 7/8-inch hole
for 1/2-inch fittings; leave their larger concentric knockout rings intact.
S2's cast 3/4-inch **female** NPT entry needs a 3/4-inch **male** to 1/2-inch
**female** NPT reducer, accepting the connector's 1/2-inch male NPT thread.

| Item | Supplier / SKU | Project need / purchase |
|---|---|---|
| 1/2-inch gray LFNC-B conduit | 7581K42 | 6 ft estimated; one 10 ft stock length |
| 1/2-inch straight LFNC-B connector, male NPT | 9106K422 | 4 individual fittings |
| 1/2-inch 90-degree LFNC-B connector, male NPT | 9106K522 | 2 individual fittings |
| Steel 3/4-inch male x 1/2-inch female NPT reducer | 44605K262 | 1, at pendant |
| Wiegmann field grounding kit, aluminum lug with mounting hardware | AD WGNDKT | 2 individual kits, one per metal control housing |
| Bonding kit, two 10 AWG stranded straps with factory ring lugs and accessory hardware per pack | AD GRDKIT01 | 1 pack required: two straps for the separate motor and frame J-box branches; door jumper supplied with enclosure. Prior two-pack order provides two spares. |

GBB supplies rail/duct mounting and bonding fasteners; these are excluded from
purchases. GRDKIT01 includes #10-32 screws, nuts and washers, and each WGNDKT
kit includes its own lug mounting hardware. The separate 92597A401 grounding
screw pack is cancelled. Current prices checked on 2026-10-14 are $36 per
two-strap GRDKIT01 pack and $3.25 per WGNDKT kit. GL1/GL2 use the selected
WGNDKT kits with one 14 AWG stranded PE conductor per lug.

The conduit's minimum **centerline bend radius is 4 inches (101.6 mm)**;
a 180-degree loop therefore has at least an 8-inch centerline diameter.
The small rounded corners in the PCB wire drawing are not conduit bend radii.
Keep the actual loops outside the enclosure clear of moving machine parts;
cut lengths are installed measurements, not the illustrative PCB drawing's
external route lengths. Use listed fittings compatible with LFNC-B and stay
within the permitted accumulated bends between pull points.

Use a second WAGO 221-613 from the existing purchased pack at S3: separate
ports for incoming PE, outgoing PE to S2, and a short 14 AWG pigtail to S3's
lug. S2 receives one PE conductor in its own lug. Do not place two conductors
under either single-wire lug. Grounding mounts are dedicated; prepare the
contact surface and provide secure thread engagement according to the
hardware instructions. Their final mounting sites require physical inspection
of the cast housings. The schematic/PCB now represents the branch as GS1
(three-port PE splice), GL1 (S3 housing lug), and GL2 (S2 housing lug):
G2.1 to GS1, GS1 to GL1, and GS1 to GL2, all 14 AWG stranded copper.
J3 includes an additional PE pass-through pair for the control-conduit bond.
GS1's single logical PE node represents three independently clamped ports.
The generic point footprints are drawing targets, not machining/CAD models
of the purchased WAGO and lugs; the casting attachment sites are field-fitted.
GS1/GL1/GL2 are excluded from automatic BOM addition: the local 221-613 and
WGNDKT purchase rows already count their hardware, including the motor PE
splice represented at M1. Do not add a second set of procurement rows for
these generic logical markers.

Sources: [McMaster LFNC-B conduit and fittings](https://www.mcmaster.com/products/ul-type-b-conduit),
[McMaster NPT reducer](https://www.mcmaster.com/products/face-bushings/),
[AD WGNDKT grounding kit](https://www.automationdirect.com/adc/shopping/catalog/enclosures_-a-_racks/enclosure_parts_-a-_accessories/grounding_-a-_isolation/wgndkt),
[AD GRDKIT01 bonding kit](https://www.automationdirect.com/adc/shopping/catalog/enclosures_-a-_racks/enclosure_parts_-a-_accessories/grounding_-a-_isolation/grdkit01),
[Electri-Flex conduit fill](https://www.electriflex.com/engineering-data/conduit-fill-chart/),
[Priority Wire MTW diameters](https://www.prioritywire.com/specs/TEW%20Machine%20Tool%20Wire%20(MTW)%20105C.PDF),
and [NEMA installation and bonding guidance](https://www.electriflex.com/wp-content/uploads/2024/02/NEMA-RV-3-2021-WATERMARKED_2024-02-27.pdf).

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

### K1/K2 reversing jumpers — owner selection, 2026-11-04

Remove both HMX1-BBREV pieces and install the six black 14 AWG jumpers in
checklist rows 1–6. The line side connects R–R, S–S and T–T. The load side
connects K1 U to K2 W, K1 V to K2 V, and K1 W to K2 U. This arrangement
preserves the phase connections of the two factory bars.

The six double wire clamps are K2 R and K1 S, T, U, V and W. Fit two
identical, individually crimped FE ferrules side by side at each shared clamp.
FE is Phoenix Contact 3202533, 14 AWG, 10 mm metal contact, strip 13 mm.
All twelve jumper ends and the six field-wire ends at these clamps use FE.
The corresponding field-wire rows are 7, 8, 13, 16, 19 and 91.
Fit one pair and check independent retention before preparing the set.
The HMC-9B power-clamp torque is 2.25 N·m (20 lb·in).
[IronHorse connections table](https://cdn.automationdirect.com/static/specs/ironhorsehmcandhtor.pdf#page=12)
and [FE ferrule specifications](https://www.phoenixcontact.com/en-us/products/ferrule-ai-25-10-bu-3202533).

No suitable catalogued IronHorse kit was found for K4/K5. Keep its existing
wiring plan, including the K5 1–3–5 shorting bridge. HMX1-BBREV's reversing
connections do not match that pair. Source: [IronHorse accessory catalog](https://cdn.automationdirect.com/static/specs/ironhorsehmcandhtor.pdf).


H2 is the red Schneider XB4BVB4 E-stop/control-disabled indicator below SW1.
Connect raw `+24V` to K3.31, K3.32 to H2.X1 on
`CONTROL_ESTOP_DISABLED_FB`, and H2.X2 to `0V`. The K3 connections and both H2 terminals use blue 18 AWG panel-control wiring.
K3 uses its existing bare stranded-copper terminal preparation; H2 uses the
selected 6 mm single ferrules. The existing E-stop connector/conduit wiring is unchanged.
Physical routes and cut lengths remain pending, as for the other panel wires.

### Terminal preparation selections — owner decisions, 2026-10-09

Ferrule `L` means the metal barrel/contact length, not overall ferrule length or
wire stripping length. Strip wire according to the selected ferrule's instructions.

| Component / terminals | Selected preparation |
|---|---|
| Q1 pins 1/3 (`L1_SW`/`L2_SW`) and 2/4 (`L1_PSU`/`L2_PSU`) | Bare stranded copper, 14 AWG; strip 12 mm per the [Eaton FAZ-NA lift-terminal instructions](https://www.eaton.com/content/dam/eaton/technicaldocumentation/il/circuit-breakers/miniature-circuit-breakers-mcb/eaton-mcb-faz-na-rt-du-il0191333zu.pdf). Eaton does not recommend ferrules or crimp terminals for FAZ-NA. |
| PS1 `3_BOT` L (`L1_PSU`), `2_BOT` N (`L2_PSU`), `1_BOT` PE | Bare stranded copper, 14 AWG; 5 mm stripping per the NDR installation manual. These are the three AC-input/PE terminals, not three phase inputs. |
| PS1 `1_TOP`/`2_TOP` (−V, `0V`) and `3_TOP`/`4_TOP` (+V, `+24V`) | Bare stranded copper, 18 AWG; 5 mm stripping per the NDR installation manual. |
| H1/H2 X1 and X2 | Single ferrule, 18 AWG, standard 6 mm metal barrel; owner-selected length. |
| KN-T12GRY-25 feedthrough clamps | One conductor and one single ferrule per clamp; 10 mm metal barrel. Use the internal common connection/OEM jumper bar for branches. |
| KN-G12SP-10 ground clamps | Single ferrule only, one conductor per clamp; 10 mm metal barrel. |
| FH1 `P1.A`, `P2.A`, `P3.A` (incoming) | Panduit PMV6-5R-L yellow ring on 12 AWG; M5 ring hole on #10-32 device screw; actual ring width 9.5 mm; strip 8 mm (manufacturer range 7.9–8.7 mm). Identified from the supplied bag on 2026-10-30; supersedes the former 9 mm width limit. |
| FH1 `P1.B`, `P2.B`, `P3.B` (fused) | Ring terminal for 14 AWG panel wire; #10-32 screw; ring tongue OD ≤9 mm to clear the terminal recess. |
| SW1 pins 1-6 | Bare stranded copper, 14 AWG; 12 mm stripping per the disconnect instructions checked by the owner. |

These selections are stored on the saved footprint instances. All seven PS1
terminals use bare stranded copper. Mean Well's NDR manual gives common wire
preparation instructions for input and output; it does not explicitly approve
or prohibit ferrules. The lamp choice records the owner's decision; it does not
claim a completed physical fit check.

FH1 uses the RM25030-3SR screw-terminal version. The AD drawing shows a nominal
12.6 mm terminal-recess width. The supplied incoming rings are Panduit
PMV6-5R-L, identified from IMG_4274.JPG: yellow, M5 hole, 9.5 mm wide. Use an
8 mm stripper setting, within the 7.9–8.7 mm range of manufacturer drawing
A41187 rev10A. This replaces the former
incoming-ring 9 mm width selection limit and the inferred PV10-10R-L identity.
The three fused-side 14 AWG ends retain their selected blue #10 rings. Sources:
[FH1 drawing](https://cdn.automationdirect.com/static/drawings/RM25030-3SR.pdf),
[Panduit ring drawing](https://cdn.shopify.com/s/files/1/0843/1616/0235/files/Panduit-PMV6-5R-L-Ring-Terminal-Part-Drawings.pdf).

AutomationDirect's Z+F catalog lists standard single-ferrule barrel lengths of
8, 10 and 12 mm in the applicable wire sizes. The gray 18 AWG versions are
0.75 mm² per conductor; the red versions are 1.0 mm² per conductor. Keep those
capacities distinct when selecting a ferrule for the actual wire. Ferrule catalog
lengths do not establish bare-device strip lengths; the practical bare settings
are recorded below. The supplied 6 mm lamp ferrules are American Electrical
1161010-S, identified from the owner's bag.

Sources: [FAZ-NA specifications](https://cdn.automationdirect.com/static/specs/eatonfazna.pdf),
[NDR installation manual](https://www.meanwell.com/Upload/PDF/NDR%20DIN%20rail.pdf),
[AD Z+F ferrule catalog](https://cdn.automationdirect.com/static/specs/dinwiring.pdf).

| Actual size | Component / use | Treatment |
|---|---|---|
| 10 AWG | Hammond GRDKIT01 motor/frame bonding jumpers | Two independent factory whips run from the motor-box WAGO 221-613: one to motor-bell stud J7 and one to machine-frame lug J5. Retain each metal-part ring; remove each splice-end ring and strip 13 mm for its own WAGO port. Do not chain J5 through J7. One two-assembly kit covers both bonds, subject to usable length and stud fit. The door uses its enclosure-supplied pre-terminated jumper and dedicated body/door lugs, with the supplied hardware; no GRDKIT01 assembly is allocated to the door. These factory assemblies are not loose-wire stock and their 10 AWG ends cannot enter KN-G12SP-10 clamps. |
| Manufacturer-defined | Suppressor leads, retained switch straps and other fixed device wiring | Keep the actual supplied conductor specification. Do not assign an unverified stock gauge or create an extra assembly wire for a factory/internal connection. |

KN-G12SP-10 accepts 26–12 AWG. Use separate suitable clamps for the incoming cable PE, the 12 AWG motor-conduit PE and PSU PE wire. Its two wire clamps and conductive rail foot are electrically common. Prepare each conductor according to the terminal manufacturer's instructions. The 10 AWG bonding-jumper ends use compatible studs or a wire-splicing connector rated for that conductor; they do not enter these KN-G12SP-10 clamps.

The current incoming PE continuation is `G4.1` to `G5.1`, using 12 AWG
single ferrules with a 10 mm metal barrel. The PSU PE branch is `G6.2` to
`PS1.1_BOT`, using 14 AWG with a single ferrule at the PE block and the declared
bare-wire termination at PS1. These are individual wire assignments; they do
not set one gauge for the whole PE net or for unused block clamps. New landing
blocks declare their 12 AWG wire ends in `Wire.Sizes` and `Termination.<pad>`.

All feedthrough-terminal and grounding-block wire clamps use ferrules with a
10 mm metal barrel. Feedthrough and ground clamps each accept one conductor
with one single ferrule, sized for that conductor. Use separate common clamps
and OEM bank jumpers to distribute branches.
These owner requirements are stored in each block footprint's
`Wire.TerminationPolicy`. Individual `Termination.<terminal>` fields describe
the part's termination capability and selected barrel length. They do not assign
a conductor gauge or wire count to an available routing resource. Blocks and unused
jumpers are allocated only when needed during physical routing; available clamps
do not constitute missing wiring data. Select the single ferrule's gauge for
the actual assigned conductor during routing. The grounding block's
PE rail contact is a retained conductive foot, not a ferruled wire clamp.

## Bonding plan and conductor classification

- Three prefab bonds: the enclosure-supplied pre-terminated jumper joins the dedicated enclosure-body and door lugs using supplied hardware; two separate GRDKIT01 whips join the motor-box WAGO PE splice to the motor body and machine frame. Each motor/frame whip retains its metal-part ring, with only its splice-end ring removed and that conductor stripped 13 mm. The motor and frame bonds are parallel branches at the J-box, with no series chain.
- One cable-core PE connection: mains cable PE to incoming grounding block G4, supplied within the incoming cable.
- One discrete incoming PE continuation: G4.1 to main PE block G5.1, using 12 AWG green/yellow panel wire.
- One discrete external PE connection: the 12 AWG motor-conduit conductor between a suitable panel PE termination and the motor-end PE junction.
- One discrete panel PE wire: PSU PE to a panel PE terminal, using the 14 AWG default subject to actual termination/protection requirements.
- Rail and enclosure bonding revision, 2026-10-20: use the terminal-foot and wire-jumper paths below for rail PE continuity. Rail/duct mounting screws provide mechanical attachment; the bonding plan does not rely on those screws as the rail PE path. The owner confirms that the backplate mounts directly on four enclosure grounding lugs/studs. Retain those four mounting/bonding interfaces with the supplied bonding hardware and prepared conductive contact surfaces. Verify the installed backplate-to-enclosure bond. GBB supplies mounting and bonding fasteners. One McMaster 9388K35 ring for the owner-selected 5/16-inch lower-right enclosure grounding lug is purchased separately in the BOM. The enclosure-supplied door jumper and its body/door lugs and hardware require no separate purchase. The earlier requirement to drill and tap every mounting hole is superseded by this plan; self-drilling mounting screws may be used within their specified material and thickness limits.

### Rail and enclosure bonding connections — 2026-10-20

Rail 1 is the upper rail, rail 2 the middle rail and rail 3 the lower rail.
The physical PCB layout contains G3 at X=391, Y=67 mm on rail 2. Its right
end bracket moves from X=395 to X=401 mm; the other rail devices stay in place.
The new block leaves room for the existing end cover after 3K.
G3 is a PCB-only physical terminal, following the existing incoming-terminal
convention. Its wire clamps and conductive rail foot are internally common.

| Connection | Conductor / hardware | Saved-design status |
|---|---|---|
| Incoming cable PE to G4.2 on rail 3 | Supplied 12 AWG cable core | Existing route; retain. |
| G4.1 to G5.1 on rail 3 | 12 AWG green/yellow, single 10 mm ferrule at each end | Existing route; retain. |
| Rail 3 G5.2 to rail 1 G1.2 | 12 AWG green/yellow, single 10 mm ferrule at each end | Existing route; retain. |
| Rail 1 G2.2 to rail 2 G3.1 | 12 AWG green/yellow, single 10 mm ferrule at each end | Continuous PCB route; included in the regenerated schedule. |
| Rail 3 G6.1 (top clamp) to existing lower-right enclosure grounding lug J8.PE | 12 AWG green/yellow; 10 mm ferrule at G6.1 and owner-selected McMaster 9388K35 ring at the 5/16-inch lug | Continuous F.Cu route; 630 mm cut estimate. J8 is concentric with the existing User.Drawings fixture. |
| Backplate to enclosure | Four owner-confirmed mounting studs, supplied nuts/bonding hardware and conductive interfaces | Mechanical bond; verify continuity after assembly. A painted mounting interface alone is not proof of bonding. |
| Dedicated enclosure-body ground lug to dedicated door lug | Enclosure-supplied pre-terminated jumper and hardware, confirmed by owner | Retain factory ring ends; no separate GRDKIT01 purchase for this branch. Do not rely on hinges. |
| Rail 1 G1.1 to motor-box PE splice M1.PE | Continuous 12 AWG green/yellow through motor conduit/J4 | Existing feed; retain. M1.PE represents the WAGO 221-613 inside the J-box. |
| Motor-box WAGO M1.PE to motor-bell stud J7.PE | Separate GRDKIT01 10 AWG whip; bare 13 mm end at WAGO, factory ring at motor stud | Existing route; 200 mm cut estimate. |
| Motor-box WAGO M1.PE to machine-frame lug J5.PE | Separate GRDKIT01 10 AWG whip; bare 13 mm end at WAGO, factory ring at frame lug | Direct parallel branch; 170 mm cut estimate. No J5-to-J7 wire. |

Use one conductor per numbered clamp. G3.2 remains spare. KN-G12SP-10
accepts 26–12 AWG; do not insert the GRDKIT01 10 AWG strap ends into it.
The owner identifies the selected lower-right grounding lug as 5/16 inch.
J8 is an electrical routing endpoint centered at X=449.2876, Y=449.2876 mm,
concentric with the existing grounding fixture in `EN4SD30208GY_Open_Front`
on User.Drawings. Its duplicate circular graphics and generic value label
are removed; the existing fixture supplies the drawing. No new physical lug,
mounting hole or enclosure artwork is added. This fixture is distinct from
the lower-right backplate mounting hole at (449.5286,430.4786) mm.
Use the supplied hardware and the manufacturer's contact preparation and
torque requirements. Verify the backplate-to-body bond and continuity from
incoming PE to all three rails, backplate, enclosure, door, motor and frame
after assembly; exercise the door while checking its jumper. The insulated
J-box WAGO does not itself bond the metal J-box: verify its conductive bond
to the motor body or provide an explicit suitable bonding connection.

The revised requirement is six PE blocks, 63 terminal marker positions and
15 loose 12 AWG single ferrules (12 existing, two for G2–G3, one for
G6.1–J8.PE). Existing purchase packs cover the PE block, markers and ferrules.
The rail-1-to-rail-2 jumper is routed continuously on In22.Cu, with a
252.708 mm centerline and a 360 mm cut estimate under the existing schedule
allowance and rounding rule. The resulting saved 12 AWG green/yellow loose-wire
requirement, including the 630 mm G6.1-to-J8.PE cut, is now 11.9 ft, rounded
upward to one decimal place; the 50 ft purchase is unchanged. Both new jumpers
are included in the regenerated wire schedule and length totals. The schedule
has 126 wires and the loose-stock totals cover 116 wires / 92.210 m. Verify
the routed cut estimates against the assembled duct and terminal approaches
before cutting.

The two motor/frame whips require two GRDKIT01 assemblies. With two assemblies
per pack, the BOM requirement is QUA 2, PACK 2, ORDER 1 at $36.00 per pack.
The owner previously ordered two packs; that order history remains valid and
provides two spare assemblies after the two required whips are allocated.
The revised BOM expresses the build/purchase requirement, not a refund or a
revision to the actual supplier order. The supplied door jumper is included
with the enclosure and does not consume either required GRDKIT01 assembly.

#### Lower-right stud ring terminal

Select **McMaster-Carr 9388K35**, a nylon-insulated tin-plated copper crimp
ring for **16–12 AWG** stranded wire and a **5/16-inch** stud. It accepts the
selected 12 AWG stranded copper PE conductor. Nominal ring width is
0.61 inch / 15.494 mm and thickness is 0.05 inch / 1.27 mm. It has a brass
internal sleeve, closed barrel and single-crimp construction, and is rated
600 V AC, UL Listed and CSA Certified. Use compatible insulated-terminal
crimp tooling and the supplier's preparation instructions.

The BOM adds **MCMC 9388K35**, QUA 1, PACK 10, ORDER 1, UNIT PACK, at
$5.75 per pack checked 2026-10-20. One terminal is required; nine remain spare.
This is an additional purchase requirement, not a confirmed receipt. Other
purchase quantities and receipt flags are retained. The BOM purchase total
is $2,173.03 before additional shipping/tax, including the revised single
GRDKIT01 pack requirement.

J8 owns the full `Termination.PE` selection and compact
`Wire.TerminationCode.PE = R12_516_15.494mm`. This code identifies 12 AWG,
a 5/16-inch stud and the selected ring's nominal width. It does not
impose the fuse-holder's unrelated 9 mm ring-width limit on the enclosure stud.

Sources: [KN-G12SP grounding-terminal specifications](https://cdn.automationdirect.com/static/specs/konnectgnd.pdf),
[Hammond Eclipse assembly and bonding details](https://www.hammfg.com/files/parts/bulletins/BUL10136.pdf).
Ring selection and pack pricing: [McMaster-Carr 9388K35](https://www.mcmaster.com/9388K35/).

Use **PE** for protective-earth conductor naming. Document the actual installation and bonding verification separately from this planned topology.

## Motor-end Wago connections

The owner selects WAGO 221-612 for standard two-conductor wire splices, including
the six 14 AWG motor-conduit conductors to the corresponding T1–T6 motor leads.
Each power splice connects only its corresponding conduit conductor and motor
lead, one conductor per port. The 221-612 accepts 20–10 AWG and specifies
12–14 mm stripping; use 13 mm. Prepare these ends as bare copper; retain the actual supplied
motor-lead gauge and check it against the connector's conductor range.

For the motor-box PE junction involving the 10 AWG grounding straps, the owner
selects the three-port WAGO 221-613, rated for conductors up to 10 AWG. It
provides the three independent ports needed for this junction. WAGO specifies
12–14 mm stripping; the project uses 13 mm bare ends on all three conductors.

The PE splice needs at least three suitable ports, one conductor per port:

1. Motor-conduit PE conductor: 12 AWG.
2. Modified jumper to motor body: selected GRDKIT01 10 AWG supplied lead.
3. Modified jumper to machine frame: selected GRDKIT01 10 AWG supplied lead.

The selected PE junction accommodates one 12 AWG conduit PE conductor and two
10 AWG jumper conductors, one per port. The M1 metadata footprint stores the
connector models, seven motor-conduit end preparations and the three-port PE
connection plan. Compact schedule term codes will be `B14_13mm` for the six
power-conductor ends, `B12_13mm` for the PE feed and `B10_13mm` for each modified
strap end. Six 221-612 connectors and one 221-613 are required for this topology.
These are required component counts; purchasing pack quantities remain separate.

Owner selection, 2026-10-19: use 221-612 for the six motor power splices. The
AutomationDirect 50-piece pack costs $30.50, leaving 44 spares, versus a
100-piece 221-412 pack at $34.00. The BOM retains two 221-613 connectors in
total, including the separate S3 housing PE splice.

The insulated Wago forms a wire-to-wire PE junction; placing it inside a metal motor junction box does not itself bond that box. Account for the box-to-motor-body bond through a verified conductive attachment or an explicit separate bonding connection. The saved routing uses J7 for the motor-bell stud and J5 for the machine-frame lug; verify the installed attachment hardware and conductive contact at each.

## Wire schedule presentation

The 2026-11-02 operator workplan starts with [device labeling and connector-bin
preparation](Wire_installation_guide.pdf#page=2), then the [installation checklist](Wire_installation_guide.pdf#page=6).
The checklist has one 12-point font, up to 42 rows per sheet, checkboxes, plain columns,
and no wire illustrations, color coding, legends or footnotes. The connector inventory remains editable in Wire_connector_bins.csv. The separate
presentation CSVs and generation manifests were removed in the document cleanup;
the checklist source hashes and supplemental rows are retained below. Rebuild
and revalidate the printable guide after changes to the native wiring; Refresh
regenerates the source CSV, not the printable checklist.

The 2026-11-03 ordering revision puts all 12 grounding wires at the bottom:
checklist rows 120–131. Non-grounding wires retain their relative order.
[Installation groups](#installation-sequence) retain the bench versus
off-backplane prerequisites and the order applied by Refresh.

The 2026-11-03 [connector inventory revision](#preparation-source-notes)
updates the connector type catalog, wire schedules and preparation PDF.
Ferrules use FA–FK, rings RA–RJ, spade/fork and blade types SA–SG, and
WAGO/wire-nut types WA–WB. The original preparation page 3 (now PDF page 4) maps labels onto the retained terminal case;
the original page 4 (now PDF page 5) contains the
[bin label placement chart](Wire_installation_guide.pdf#page=5). It maps 30 sidewall codes
and their exact three-line description labels onto the four-row, eight-column
McMaster 5158T52 organizer, with two spare bins. Old A–F map to FA–FF, G–J to RA–RD, and K/L to WA/WB;
FG–FK are five additional 8 mm
American Electrical ferrules from kit 1617050. The retained McMaster kit and
3M 12-8-NB / SS-33-14-NB additions bring the inventory to 30 distinct types.
Blade mating width is recorded in `Tab mm`, separately from screw/stud size.
The live wire CSV, installation checklist, device-label references and manifest
now use these codes. `na` identifies a connector already applied to the wire
by the OEM. Six ends qualify: J5_PE, J7_PE and J1 pins 1–4. `8mm bare` (for
example) gives the saved strip length for a conductor with no added connector.
The four J2 plug clamps still show `bare` because no strip length is recorded. The approved
mapping is saved in [Wire_termination_types.json](Wire_termination_types.json)
and applied by Project Review on Refresh. Detailed preparation codes and strip
settings remain in the native footprint fields and preparation evidence.
Inventory availability does not change the selected parts or strip settings.

Operator terminal-block and grounding-block endpoints use `_top` / `_bottom`.
Ground pin 1 is top and pin 2 is bottom; F4 IN is top and OUT is bottom, checked
against saved board geometry. Device references and missing terminal markings
must be applied before wiring. Manufacturer terminal identifiers are retained
where available. The label preparation table identifies the PSU output positions.
HMC coil endpoints in the printed checklist use `A1_top`, `A2_top`,
`A1_bottom` or `A2_bottom` for the physical clamp. The owner confirms the
installed suppressors occupy both top clamps on K1, K2, K4, K5 and K6.
All five contactors use the two bottom clamps for their field coil wires.
The K4 and K5 A2 returns in rows 35 and 39 start at `2A_top` and `2E_top`.
They pass through the right-hand chase to the lower duct and enter
`K4_A2_bottom` and `K5_A2_bottom`. The K4 approach skirts OL4.
PE1-PE3 identify separate ports of each three-port
splice: GS1 in the controls housing and the M1 motor PE splice. FH1 remains physically rotated 180 degrees in the native layout. Operator labels
now assign P1/P2/P3 left to right and A above/B below. The manifest maps each
native terminal to its printed name.
Bin assignments include the two WAGO splice models. Blank connector cells require no
loose connector: existing bare-wire, plug-clamp and factory-end preparations
remain unchanged. Wire colors use BLK, BLU, BRN, GRN, RED, WHT and GRN/YEL for
the striped conductor. The temporary native extraction on 2026-11-02 matched
all 123 rows of the saved live CSV. These presentation changes do not edit the
native schematic, PCB, termination fields, BOM quantities or live CSV.


The generated CSV and editor use eight positional columns:
`From, Pin, To, Pin, AWG, Color, Term 1, Term 2`. The two `Pin` titles have
separate column positions; they are not dictionary keys.

The installation order is defined in [Wire_installation_groups.json](Wire_installation_groups.json)
and summarized in [Wire_installation_groups.md](#installation-sequence).
The saved plan assigns all 129 native wires exactly once to 23 numbered groups
of at most ten wires. Bench non-grounding wiring comes first, followed by deferred
non-grounding wiring and all grounding wires. The printable checklist adds the
two supplemental pendant jumpers; its row ranges are recorded below.
Group membership and within-group order use endpoint pairs rather than stale
CSV row numbers. The bom_review extractor applies the plan after native wire
extraction and length calculation, so Refresh preserves the installation order.
Missing, obsolete or duplicate pairs and groups over ten wires stop extraction
before publication. The printed checklist retains this order across three portrait 11x17 sheets without group headings. Ordering changes no native source data,
connectivity, wire length, gauge, preparation or quantity.

The native-extraction CSV pin labels include the reference, followed by an underscore and the terminal
identifier, for example `PS1_PE`, `FH1_P2A`, `5A_TOP`, `K1_A1_TOP`.
Hidden PCB footprint fields `Wire.PinLabel.<electrical pin number>` supply
aliases for PS1 and FH1. PS1 output aliases are `V1_NEG`, `V2_NEG`, `V1_POS`,
`V2_POS`. Other compound identifiers replace delimiters with underscores.
Electrical pad numbers and schematic connectivity remain unchanged. Routing follows the current saved-board revision.
Terminal-block device names display as `Terminal 5A` for `5A`, and `Ground G1` for `G1`. See [the terminal numbering reference](#terminal-numbering-reference) for all 60 active labels and their legacy cross-reference.

Compact termination codes have no underscore between type and wire gauge:

- `F18_10mm`: single ferrule for 18 AWG, 10 mm metal barrel.
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

### Connection-diagram preparation research — 2026-10-30

The [connection diagram](Wire_installation_guide.pdf#page=6) and native `Termination.*`
fields now identify all 127 crimp-end preparations from supplied bags and
manufacturer data. See the complete [part/preparation table](#preparation-source-notes)
and [endpoint evidence](#preparation-source-notes).

Owner photographs IMG_4274.JPG and IMG_4275.JPG identify American Electrical
11101075-S (gray, 0.75 mm², 10 mm barrel/strip), 11101010-S (red, 1 mm²,
10 mm barrel/strip), 1161010-S (red, 1 mm², 6 mm barrel/strip), Phoenix
3202533 (blue, 14 AWG, 10 mm barrel, strip 13 mm), Weidmüller 1476290000
(gray, 12 AWG, 10 mm barrel, strip 12 mm), and McMaster 7950K24
(black, 16 AWG, 10 mm barrel, strip 12 mm). The black part's preparation
uses Weidmüller H1,5/16 DS SW data, identified from the supplier's UL file
E499744 and complete listed geometry; the operator ID remains McMaster 7950K24.

Panduit PMV6-5R-L incoming FH1 rings are yellow, M5 hole, 9.5 mm wide,
strip 8 mm within the manufacturer's 7.9–8.7 mm range. Blue 3M 12-8-P (#8)
and 12-10-P (#10) rings are 8.4 mm wide; yellow 3M 123-56-NB (5/16 inch) rings
are 15.5 mm wide. All three 3M types use 9.5 mm stripping per their 3/8 inch
instructions. The CSV has actual ring widths. No conditional crimp flags remain.

The 23 gray 12 AWG/black 16 AWG ferrule ends now use 12 mm stripping, replacing
the earlier 10 mm assumption. All connections, gauges, cut lengths and row
order are unchanged. Q1 shows 12 mm stripping. The four J2 ends say only
`plug`, per the owner; the mains cable is not factory terminated.

The owner requested practical whole-millimetre starting settings for the remaining
73 bare ends and accepts trimming an overlong end. Use **10 mm** on HMC power
terminals 1–6, HTOR power outputs 2/4/6, and GL1/GL2 grounding lugs (27 ends).
Use **8 mm** on HMC coils/auxiliaries, HTOR 95/96, KA1 and K3 (46 ends).
These are project starting settings supported by comparable manufacturer terminal
data, not exact-model published requirements. Sources and reasoning are in
[the preparation source notes](#preparation-source-notes). Seat the first wire fully;
the clamp grips copper and insulation reaches the entrance. Trim excess bare
copper before tightening. Existing documented strip settings are retained,
including TD1/TD2 at 7 mm, independently confirmed by owner photo IMG_4281.JPG.
All field-prepared ends now have numeric settings in native `Termination.*`
fields and the refreshed schedule; no amber preparation flags remain.

## Historical routed termination inventory — 2026-10-14

This snapshot predates the 2026-10-20 bonding revisions above. The current
126-wire schedule uses independent J-box-to-motor and J-box-to-frame bonds;
the earlier frame-bond routing description below is historical.

The single-ferrule 93-wire drawing has 186 wire ends: 70 single ferrules,
16 loose ring lugs, 95 bare preparations and five
supplied terminations. Counts are pieces/preparations rather than purchasing
pack quantities. Frame and motor lug ends supplied by GRDKIT01 are not new
loose-ring requirements. The existing frame bond is now drawn at the kit's
10 AWG width on its original continuous layer and centerline. M1.PE is the
common WAGO 221-613 splice; one conductor enters each physical port, so its
12 AWG conduit PE and 10 AWG bonding leads retain their distinct sizes.
K3.32/A2 use the same bare stranded-copper preparation as its other wired
terminals. All used terminal-block fields have their existing 10 mm ferrule
policies and actual routed gauges. K4 and K6 now have separate single-ferrule
landings in the existing 0V bank; K6 uses its verified internally common lower
A2 clamp. K4 retains `2A.TOP → K4.A2.TOP`; K6 uses
`2E.BOT → K6.A2.BOT`, through D3 on the existing In9.Cu layer. No terminal
block is added. Placement, all wire gauges, the other 92 routes, the 28 OEM
bank-link strokes and the schematic are preserved. All 93 wires are continuous;
the proper XY crossing total remains 232. The K6 route grows by approximately
70 mm to reach the separate accessible clamps. Native verification matches all
178 saved schematic pad-net assignments and reports zero unrouted connections.

The BOM contains no twin-ferrule rows. The 18 AWG / 10 mm single-ferrule demand
is now 23 pieces, still covered by its existing 100-piece pack. The remaining
six single-ferrule and three ring-terminal SKUs require nine packs total,
at $114.10 using the recorded BOM prices. Factory lug ends remain excluded.

See the single-ferrule conversion and current inventory (historical reference).
The earlier connector inventory (historical reference)
and repair verification (historical reference)
remain historical snapshots. The live schedule now exports all 93 physical wires.
Mechanical-interlock markers are explicitly excluded as wire terminals; the
28 terminal-bank hardware bridges and 16 verified direct-mounted/supplied
contacts participate in connectivity without becoming cut wires. Drawn enclosure
coverage is complete. Metadata-only S1/J6 interfaces remain outside that drawn
scope, and J2's external mains-cord length is excluded from its panel-tail
estimate. See the metadata and export verification (historical reference).

## Where information belongs

1. **Policy:** this document owns preferred gauge classes, application defaults and explicit exceptions. The root README and the external bom_review adapter documentation reference it; avoid duplicating a second policy table in the BOM or generator.
2. **KiCad data:** custom schematic `Wire.Sizes` fields record per-terminal conductor sizing and `Wire.SizePlan` retains proposed bonding assemblies. M1.PE is the common WAGO 221-613 connector interface, with separate 12 AWG conduit and 10 AWG supplied-bond ports; each physical wire obtains its gauge from its other endpoint. Saved PCB trace paths own physical wire endpoints and route geometry; the old schematic `Wire.Wxxx` fields are no longer the schedule source. One combined `Termination.<pin>` field on each placed footprint owns the termination selection at that terminal. TERM 1 and TERM 2 are read from the source and destination footprints. M1 uses the illustrative `Controls:PWRM1200-MOTOR_Top_150mm` machine-layout footprint with T1–T6 and PE routing targets and no model. Glands provide explicit pass-through routing markers; S1 and J6 retain metadata-only representations. Bonding-strap attachment hardware belongs in the BOM; mechanical bonding points do not carry wire-schedule termination fields. Reports and wire records do not own duplicate termination selections. These fields do not define routes or wire allocation; completed routed paths generate wire rows, and missing gauge assignments and unrouted connections are reported.
3. **Procurement:** `BOM_other.csv` owns exact cable/device/spool/ferrule/lug/kit selections and purchase quantities. Include AWG and conductor count in cable descriptions and AWG in termination descriptions; retain the exact supplier part number. A preferred gauge without a required wire is not an automatic BOM purchase. The BOM is manually reviewed; wire Refresh does not change purchasing fields.
4. **Live schedules:** `docs/Wire_schedule.csv` is the single live physical-wire schedule. The external bom_review adapter extracts completed saved PCB trace paths on wire-mode Finder launch or on Refresh while this schedule is selected in Documents. `docs/Wire_length_totals.csv` is regenerated with it, using the installed-run assumptions above. CSV edits remain local and never update KiCad. Incomplete routing is reported. Retained busbars and explicitly declared installed station links do not generate cut-wire rows. QUA is project need, PACK is pieces/feet per purchased length or package, and ORDER is purchase quantity. No historical CSV variants are generated.
5. **Part specifications:** `_parts` datasheets and catalog entries own supplied cable/lead sizes, terminal wire ranges and manufacturer-specific termination requirements. Keep project-wide stock policy here rather than embedding it in reusable symbols.

## Current reconciliation items

- J1's factory leads are 22 AWG. Any 18 AWG extension must be routed as a separate conductor with an explicit joining method; it cannot silently change the factory-lead gauge. The live schedule now reports only completed saved trace paths.
- Old schematic incoming-phase wire records target deleted terminal symbols. They are not read by the trace exporter. Route actual physical paths in the PCB and save before refreshing the schedule; missing routing is reported as incomplete. J2 uses a four-pad mains-gland footprint proxy matching X/Y/Z/G. Its existing incoming traces define the panel tail, not the unrecorded external supply cord; footprint `Wire.LengthScope` records this limit. Gland-only boundaries remain explicit drawn sections, with no inferred electrical termination.
- Motor/control cable glands and the 3/4-inch conduit placeholders have been replaced in the purchase BOM by the 1/2-inch LFNC-B plan above. All six loose-wire gauge/color groups now have stranded McMaster SKUs and stock lengths covering the current estimates. Choose ferrules/lugs for the actual conductor and device terminal; color alone is not a size specification.
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
- [Wago 221-612 conductor specifications](https://www.wago.com/us/wire-splicing-connectors/compact-splicing-connector/p/221-612).

## Panel-layout alignment grid

This industrial-controls PCB view is an alignment and wiring workspace. Optimize
it for ease of placement and routing on a 1 mm grid. Prefer integer X/Y footprint
origins and wire-target centers; use the outer face of the mounting panel as the
datum for wall-mounted devices. Preserve terminal identity and connectivity when
adapting a footprint's routing representation.

The current backplate routing view is 462 x 716 mm for Hammond EP3020,
inside the 508 x 762 mm EN4SD30208GY enclosure. The enclosure footprint
retains its saved PCB origin at (0, 462) mm and its zero-degree orientation.
In PCB file coordinates (+Y down), the nominal backplate spans X=0..462
and Y=-254..462; the enclosure spans X=-23..485 and Y=-277..485. The taller
layout grows upward from the existing lower-left datum. The official formed
backplate geometry is retained in its catalog footprint and STEP; the flat
board body is a routing proxy. Existing component positions and wire routes
were preserved. See the enclosure replacement review (historical reference).

## Integer-grid DIN routing views

The integer-origin DIN routing views use canonical `Controls:<base>` footprint
names. The formerly used `_Grid1mm` content was promoted to those base names;
the suffix is not a current footprint-selection rule. Keep approved integer
mounting datums and wiring targets while retaining nominal physical F.Fab/STEP
geometry. The drawing-grid view does not change conductor or termination
specifications. The coordinate audit (historical reference) records
the earlier alignment work; current routing policy is defined above.

### Terminal-label audit - 2026-11-02

Wire_terminal_label_audit.csv distinguishes project labels from saved device
identifiers. Device references are project labels. FH1 pole/end names and the
PS1 output suffixes are project labels, not asserted manufacturer markings.
PE1-PE3 are assigned physical ports on each PE splice. GL1/GL2 and J5/J7/J8
PE labels are project bonding-point labels. Other device-terminal identifiers
were retained from the saved design and have not all been verified against
physical manufacturer markings. The prerequisite sheet is a labeling plan,
not evidence that those markings have already been verified or installed.
The wire checklist has exactly two Connector columns and no bin/strip columns.

### Manufacturer terminal-marking corrections - 2026-11-02

The operator checklist now retains the complete HMC power inscriptions R/1/L1,
S/3/L2, T/5/L3, U/2/T1, V/4/T2 and W/6/T3; built-in auxiliary markings
31NC/32NC and 43NO/44NO; HMX1-AUX11-F markings 51NC/52NC and 63NO/64NO;
HTOR outputs 2T1/4T2/6T3 and NC/NO suffixes; and timer A3(+)/B1(+).
The exact HC3096N.52 manufacturer circuit diagram confirms K3's contact numbers.
PS1 uses -V/+V without invented output numbers, and its earth symbol; the first
-V and first +V screws remain the scheduled physical connection locations.

Wire_terminal_label_evidence.json records the document/photo basis and unresolved
hardware. In particular, the catalog AUX11-F contact sketch conflicts with the
one-NO/one-NC part description; the exact-part factory photo confirms 51NC/52NC
and 63NO/64NO and governs the checklist. Device labels do not replace existing
manufacturer terminal markings. Project terminal labels are applied only where
markings are absent. Manufacturer verification is not complete for installed
SW1, S2, S3, M1 lead tags and the exact J2 plug; these are not approved as verified
manufacturer names merely because the old source schedule contains them.

### Installed terminal markings - owner confirmation, 2026-11-02

SW1 rear view: top left-right 5/L3, 3/L2, 1/L1; bottom left-right 6/T3,
4/T2, 2T1. The operator checklist now uses these exact inscriptions.
S2 has no terminal markings; apply the existing project 1T/1B-style terminal
labels before wiring. These are intentionally project labels, not manufacturer
markings. Motor leads are physically tagged T1-T6, confirmed by the owner.

S3 actual markings, viewed from above with handle facing up: left top-down
1,3,5,7; right top-down 2,4,6,8. The saved S3 footprint instead contains sixteen
generic positions 1B/1T through 8B/8T. Its six scheduled endpoints cannot be
translated by position alone. Rows 116-121 remain unresolved pending an actual
contact/jumper mapping or LOW/HIGH continuity results. Do not apply the generic
S3 names over its printed numbers. J2 exact plug markings also remain pending.

Owner clarification superseding the preceding S3 mismatch finding: each of the
eight numbered S3 sections has a top screw and bottom terminal, so there are
sixteen physical terminals. Source 1T/1B-style identifiers correspond to the
numbered section plus top/bottom position. Apply the missing individual terminal
labels 1T/1B through 8T/8B; preserve the manufacturer's section numbers. S3 rows
116-121 are resolved by this clarification. Only the exact J2 plug markings
remain unconfirmed.

Final J2 owner clarification, 2026-11-02: no terminal labels are present; the
conductors are green, red, white and black. Operator endpoint names are J2_GRN,
J2_RED, J2_WHT and J2_BLK, replacing source aliases G,Y,Z,X respectively using
the existing saved Color fields. Apply matching color labels to the unmarked
ends. These are project conductor identifiers, not asserted manufacturer
markings. No phase, polarity, route or connection is changed. The terminal-name
audit has no remaining unresolved devices; installation and electrical checks
remain separate from this naming audit. Earlier pending-J2 statements are
superseded by this owner confirmation.

## Installation sequence

Start with [device labels and connector bins](Wire_installation_guide.pdf#page=2), then use the [installation checklist](Wire_installation_guide.pdf#page=6).

Non-grounding backplane wires occupy checklist rows 1–82; non-grounding off-backplane connections occupy rows 83–119. All 12 grounding wires are at the bottom, rows 120–131.

Rows 1–82 and 120–123 have both endpoints on the backplane and can be completed on the bench. Rows 83–119 and 124–131 require the backplane to be installed and the off-backplane devices mounted. Defer the whole external connection, including its backplane end; do not leave attached external wire tails on the bench assembly.

Rows 1–6 replace the two K1/K2 busbars. The paired wire landings use matching individual FE ferrules as specified in the [wiring standard](WIRING_STANDARD.md).

| Priority | Stage | Installation group | Wires | Checklist rows |
|---:|---|---|---:|---|
| 01 | bench | Bench - K1/K2 reversing jumpers | 6 | 001–006 |
| 02 | bench | Bench - Disconnect and PSU AC | 6 | 007–012 |
| 03 | bench | Bench - Contactor power distribution | 9 | 013–021 |
| 04 | bench | Bench - Motor power outputs | 9 | 022–030 |
| 05 | bench | Bench - Star links and motor leads | 2 | 031–032 |
| 06 | bench | Bench - DC return - source and coils | 7 | 033–039 |
| 07 | bench | Bench - DC return - timers and lamps | 2 | 040–041 |
| 08 | bench | Bench - Fused DC and safety chain | 7 | 042–048 |
| 09 | bench | Bench - Coil interlock links | 8 | 049–056 |
| 10 | bench | Bench - Direction control bank | 9 | 057–065 |
| 11 | bench | Bench - Speed control bank | 9 | 066–074 |
| 12 | bench | Bench - Timers and auxiliary contacts | 8 | 075–082 |
| 13 | installation | Deferred - Incoming supply and fuses | 6 | 083–088 |
| 14 | installation | Deferred - Disconnect and PSU AC | 3 | 089–091 |
| 15 | installation | Deferred - Star links and motor leads | 6 | 092–097 |
| 16 | installation | Deferred - DC return - timers and lamps | 2 | 098–099 |
| 17 | installation | Deferred - E-stop connector | 4 | 100–103 |
| 18 | installation | Deferred - Button station | 8 | 104–111 |
| 19 | installation | Deferred - Speed selector | 6 | 112–117 |
| 20 | installation | Deferred - Indicator feeds | 2 | 118–119 |
| 21 | bench | Bench - PE - panel backbone | 4 | 120–123 |
| 22 | installation | Deferred - PE - panel backbone | 2 | 124–125 |
| 23 | installation | Deferred - PE - housings and motor | 6 | 126–131 |

FH1 remains part of bench wiring because it is mounted on the lower DIN rail. Off-backplane devices: GL1, GL2, GS1, H1, H2, J1, J2, J5, J7, J8, M1, S2, S3, SW1. Their device labeling can wait until installation.

The printed checklist retains the requested simple columns, with no added stage columns or group headings. Row numbers are checklist positions, not physical wire labels.

The two pendant jumpers `S2_1T–S2_3T` and `S2_3T–S2_5T` are checklist rows 104 and 105, each 16AWG BLU with connector RA at both ends. The existing `S2_2B–S2_4B` jumper is row 111. All three remain pending installation. The added rows and the owner-confirmed removal state are saved in the [supplemental pendant-jumper record](#supplemental-pendant-jumper-record). These two new rows supplement 129 native extracted wires because the native model previously treated these links as retained.

Native ordering is saved by endpoint pair in [Wire_installation_groups.json](Wire_installation_groups.json), which the native extractor applies on Refresh.

### Supplemental pendant-jumper record

The following record preserves the removed supplemental JSON source, including the owner-reported removals and the still-pending additions. The native 129-row extraction does not include its two added wires.

```json
{
  "date": "2026-11-02",
  "purpose": "Supplement native field-wire extraction with two pendant jumpers formerly assumed retained. Native schematic connectivity is unchanged.",
  "insert_before_endpoint": "S2_2B",
  "stage": "installation",
  "wire_rows": [
    [
      "Button Station",
      "S2_1T",
      "Button Station",
      "S2_3T",
      "16",
      "Blue",
      "RA",
      "RA"
    ],
    [
      "Button Station",
      "S2_3T",
      "Button Station",
      "S2_5T",
      "16",
      "Blue",
      "RA",
      "RA"
    ]
  ],
  "preparation_reference": "S2_2B|R16_832_8.4mm",
  "basis": "Use the same 16 AWG blue wire and bin RA #8 ring terminals as the existing scheduled S2 2B-4B jumper. Strip 9.5 mm.",
  "owner_reported_complete": {
    "S2_removed": [
      "2T-4B",
      "2B-4T",
      "3B-1B"
    ],
    "S3_removed": [
      "1T-3T",
      "5T-7T",
      "1B-2B",
      "3B-4B",
      "3B-5B",
      "6T-4T"
    ],
    "S3_retained": [
      "7B-8B"
    ]
  },
  "pending_S2_additions": [
    "1T-3T",
    "3T-5T",
    "2B-4B"
  ],
  "native_metadata_note": "S2 native Wire.Sizes still describes 1T-3T and 3T-5T as installed retained links. Owner confirmation supersedes that physical-state assumption; these checklist additions must not be omitted on regeneration."
}
```

### Printable-checklist snapshot

Native schedule SHA-256: `3fdc736ad7c13dac390511b3e5e3bbfcc5ce17f8d3339e2b9bfced8176a89d55`.

Saved PCB SHA-256: `324ee3c385f0d15c04567307d334cd713a0c3957c40cb34137f0235f574841c5`.

The retained PDF has 131 wires: 129 native plus two supplemental, with 262 endpoint preparations. These hashes identify the source used for the checklist, not electrical or mechanical qualification.

## Terminal numbering reference

Approved 2026-10-28. This is the current installed-label scheme for all 60 active terminal blocks.

The module number identifies one physically separate terminal strip. Module numbers run top to bottom, then left to right. Letters run left to right within each strip and restart at A. Uppercase I and O are skipped. Ground blocks use G1-G6 in the same physical reading order and do not consume letters.

| Module | Location | Labels | Gray blocks |
| --- | --- | --- | --- |
| 1 | Upper rail, right of K1/K2 | 1A-1Z, skipping I/O | 24 |
| 2 | Middle rail, left of K6 | 2A-2F | 6 |
| 3 | Middle rail, right of TD1/TD2 | 3A-3K, skipping I | 10 |
| 4 | Lower left | 4A-4D | 4 |
| 5 | Lower rail, right of PS1 | 5A-5K, skipping I | 10 |

Grounds: upper G1/G2, middle G3, lower-right G5/G6 and relocated G4. The lower-right order ends with 5K, G4, the existing end stop, then FH1.

Installation revision, 2026-10-30: FH1 moves to the lower-right rail in its original orientation. 4E/4F/4G (formerly TB79/TB80/TB81) are retired; do not reuse or renumber those IDs. G4 remains after 5K. The existing end stop is between G4 and FH1; another at FH1's right end is desired but not installed because stock is exhausted. Rails and ducts are unchanged. Owner photo IMG_4273.JPG confirms the arrangement; FH1's right edge is approximately 15 mm from the backplate edge.

The module number identifies physical location, not electrical commonality. Jumper sections remain independently defined in the jumper guide.

Printed-marker migration: retain the original seven printed pairs and their left-to-right order. Discard both copies of 4E (pair 6, position 10), 4F and 4G (pair 7, positions 1 and 2). G4 remains pair 7, position 3. There are 120 active markers, two for each of 60 terminal blocks. See the placement guide for separators and cuts.

Wire-schedule endpoint labels use the new reference followed by the existing clamp identifier, such as `1A_TOP`, `2F_BOT`, or `G1_2`. Pad numbers and electrical connections are unchanged.

### Current labels and legacy cross-reference

Legacy TB labels are retained in this table only for migration. Current design references, guides, and wire schedules use the new labels.

Rows follow saved physical order: upper to lower rail, then left to right.
Checked against the saved PCB on 2026-10-30, including FH1 relocation and the retired phase terminals.

| Rail | Module | Current label | Previous label | Circuit |
| --- | --- | --- | --- | --- |
| Upper | 1 | 1A | TB60 | M1_T1 |
| Upper | 1 | 1B | TB61 | M1_T1 |
| Upper | 1 | 1C | TB63 | M1_T2 |
| Upper | 1 | 1D | TB64 | M1_T2 |
| Upper | 1 | 1E | TB66 | M1_T3 |
| Upper | 1 | 1F | TB67 | M1_T3 |
| Upper | 1 | 1G | TB31 | M1_T4 |
| Upper | 1 | 1H | TB69 | M1_T5 |
| Upper | 1 | 1J | TB72 | M1_T6 |
| Upper | Ground | G1 | TB51 | PE |
| Upper | Ground | G2 | TB52 | PE |
| Upper | 1 | 1K | TB20 | DIRECTION_ENABLE |
| Upper | 1 | 1L | TB21 | DIRECTION_ENABLE |
| Upper | 1 | 1M | TB22 | DIRECTION_ENABLE |
| Upper | 1 | 1N | TB73 | DIRECTION_FWD_CMD |
| Upper | 1 | 1P | TB74 | DIRECTION_FWD_CMD |
| Upper | 1 | 1Q | TB75 | DIRECTION_REV_CMD |
| Upper | 1 | 1R | TB76 | DIRECTION_REV_CMD |
| Upper | 1 | 1S | TB77 | CONTROL_RUN_ENABLE |
| Upper | 1 | 1T | TB78 | CONTROL_RUN_ENABLE |
| Upper | 1 | 1U | TB62 | SPEED_HIGH_CMD |
| Upper | 1 | 1V | TB65 | SPEED_LOW_CMD |
| Upper | 1 | 1W | TB68 | CONTROL_OVERLOAD_ENABLE |
| Upper | 1 | 1X | TB84 | SPEED_LOW_TIMED_ENABLE |
| Upper | 1 | 1Y | TB85 | HIGH_SEQUENCE_ENABLE |
| Upper | 1 | 1Z | TB86 | HIGH_SEQUENCE_TRIGGER |
| Middle | 2 | 2A | TB10 | 0V |
| Middle | 2 | 2B | TB11 | 0V |
| Middle | 2 | 2C | TB12 | 0V |
| Middle | 2 | 2D | TB13 | 0V |
| Middle | 2 | 2E | TB14 | 0V |
| Middle | 2 | 2F | TB87 | 0V |
| Middle | 3 | 3A | TB88 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3B | TB89 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3C | TB90 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3D | TB91 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3E | TB92 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3F | TB93 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3G | TB94 | HIGH_SEQUENCE_TRIGGER |
| Middle | 3 | 3H | TB95 | HIGH_SEQUENCE_TRIGGER |
| Middle | 3 | 3J | TB96 | LOW_SEQUENCE_ENABLE |
| Middle | 3 | 3K | TB97 | LOW_SEQUENCE_ENABLE |
| Middle | Ground | G3 | TB98 | PE |
| Lower | 4 | 4A | TB83 | CONTROL_ESTOP_CONTACT_LINK |
| Lower | 4 | 4B | TB1 | +24V |
| Lower | 4 | 4C | TB2 | +24V |
| Lower | 4 | 4D | TB3 | +24V |
| Lower | Ground | G5 | TB43 | PE |
| Lower | Ground | G6 | TB50 | PE |
| Lower | 5 | 5A | TB40 | L1_SW |
| Lower | 5 | 5B | TB41 | L1_SW |
| Lower | 5 | 5C | TB42 | L2_SW |
| Lower | 5 | 5D | TB30 | L2_SW |
| Lower | 5 | 5E | TB23 | L1_DIR |
| Lower | 5 | 5F | TB24 | L1_DIR |
| Lower | 5 | 5G | TB32 | L2_DIR |
| Lower | 5 | 5H | TB33 | L2_DIR |
| Lower | 5 | 5J | TB70 | L3_DIR |
| Lower | 5 | 5K | TB71 | L3_DIR |
| Lower | Ground | G4 | TB82 | PE |

### Source checkpoint

Pre-renumbering board SHA-256: `c731a221f87b926be2c003654d6b80d86224b43d60473315bae08dab0162202a`.
Renumbered board SHA-256: `b738d5c0a8aec3e600c9eabf21a384ae3e65b1bcc55b7f4382337b39da2ae1b6`.

The 2026-10-28 renumbering retained terminal placement, pad identities, nets and routed geometry. The terminal blocks are PCB-level layout items; the saved electrical schematic contains no terminal-block reference instances to rename.

Right-entry relocation checkpoint, 2026-10-29: board SHA-256 `04f916bcc7674bb8db68ffcfc75c5fe25b5ecf4fd1e167e0c03079a843f9d11f`. Four terminals, the J2 mains-gland proxy, the affected cable-tail/fuse-feed/bonding routes and end-stop placement changed; all contactors remain in place.

FH1 lower-rail checkpoint, 2026-10-30: board SHA-256 `ae6e23858dedb8c8ed8c8496a666fec8cc5d9bbb19f879307e2eaf3af6232123`. 60 terminal blocks; 123 complete generated wire records. Saved schematic unchanged.

## Control signal naming reference

> The signal tables retain the 8 October naming update. Later owner-reported jumper removals and the installation sequence above govern physical installation; references here to retained links are historical assumptions.

The shared signal naming standard (historical reference)
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

### Operator connections

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

### Other named control nets

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

### Verification of the naming update

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

## Preparation source notes

The connector inventory and strip-setting chart are retained in PDF pages 3 and 5 of the wire installation guide. FA / McMaster 7950K16 accepts 22-20 AWG. FE is Phoenix 3202533 (14 AWG, 10 mm contact, strip 13 mm). FF is the supplied Weidmüller 1476290000 / McMaster 7950K31 (12 AWG, 10 mm contact, strip 12 mm). Historical per-end counts in the older preparation research are superseded by the saved current schedule.

FG-FK have 8 mm barrels and strip settings. RE-RI and SA-SF use the recorded 9.5 mm project setting based on matching 3M terminal-family instructions; their exact loose-piece OEM identity remains unverified. RJ and SG use their identified 3M parts' 3/8 inch instruction, displayed as 9.5 mm.

### Manufacturer evidence retained from the preparation research

- American Electrical: [catalog](https://www.americanelectrical.com/uploads/catalog/American-Electrical-_-Insulated-Wire-Ferrules.pdf) and [installation instructions](https://www.americanelectrical.com/asset/wireferrule_install.pdf). The identified 10/10/6 mm ferrules use the corresponding 10/10/6 mm strip lengths.
- Phoenix Contact: [3202533 manufacturer page](https://www.phoenixcontact.com/en-us/products/ferrule-ai-25-10-bu-3202533) specifies a 10 mm contact barrel and 13 mm strip.
- Weidmüller: [1476290000 manufacturer page](https://eshop.weidmueller.com/en/h4018d-gr-sp/p/1476290000) explicitly states 10 mm contact length and 12 mm strip; the supplied bag independently prints 12 mm.
- Black McMaster ferrule: [7950K24 supplier page](https://www.mcmaster.com/7950K24/) lists UL E499744, polypropylene, black16 AWG and 0.39 inch pin. Its drawing gives approximately 16 mm overall, 10 mm metal tube, 4 mm collar and 1.7 mm bore. The [UL certificate](https://assets.dam.weidmueller.com/assets/api/373ae775-5041-4cff-8c58-ca5b2d312ae6/original/E499744-Certificate-of-Compliace-Wire-End-Ferrules.pdf) identifies Weidmüller. These dimensions and registration match [H1,5/16 DS SW, 2092490000](https://eshop.weidmueller.com/en/h1516-ds-sw/p/2092490000), whose manufacturer specifies 12 mm stripping. This manufacturer model identification is inferred from registration and the complete listed geometry; the bag itself prints only McMaster7950K24. The operator schedule retains the actual supplier SKU.
- Panduit: [A41187 rev10A drawing](https://cdn.shopify.com/s/files/1/0843/1616/0235/files/Panduit-PMV6-5R-L-Ring-Terminal-Part-Drawings.pdf) specifies 5/16 inch nominal strip (7.9 mm) with +0.8/-0 mm tolerance. The project setting is **8 mm**, within 7.9–8.7 mm. PMV6-5R-L replaces the former PV10-10R-L inference.
- 3M blue rings: manufacturer instructions for 3M 12-8-P and 12-10-P explicitly list12-8-P and12-10-P with 0.33 inch width and specify3/8 inch stripping. The yellow123-56-NB [manufacturer instructions](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2293/123-6S_500-NB.pdf) also specify3/8 inch. The project uses **9.5 mm**, rounded from9.525 mm;10 mm has not been substituted.

### Bare-wire starting-setting research basis

- [Schneider Electric instruction 1378322_01A55-10](https://download.se.com/files?p_Doc_Ref=1378322_01A55&p_File_Name=1378322_01A55-10.pdf&p_enDocType=Instruction+sheet), page 1, gives **10 mm** on comparable small IEC contactor power terminals and **8 mm** on control terminals. This supports the project starting settings for HMC/HTOR/HMX1; it does not establish that these devices share a manufacturer or identical terminals.
- [Panduit LAMA mechanical-lug drawing 03468NBA/00](https://www.panduit.com/content/dam/panduit/en/products/media/7/77/277/1277/111251277.pdf) gives **9.7 mm strip** on the LAMA6-14-C aluminum set-screw lug, with 26.9 mm overall length and 12.7 mm width. This is dimensional guidance for the WGNDKT's **10 mm** project starting setting, not an identification of the supplied lug as a Panduit part.
- Owner literature photos IMG_4277/4278 confirm HMC/HTOR conductor ranges and torque but contain no strip length. Their 9.6/7.6 mm dimensions are maximum ring widths. IMG_4286 gives K3's small captive-screw connection and 0.5 Nm torque but no strip length; **8 mm** is a project starting choice for that terminal. No exact-model strip requirement was found in the online sources checked.
- Owner photo IMG_4281 explicitly confirms **7 mm** stripping on RK7817 timers, for stranded wire with or without ferrules. TD1/TD2 retain that documented setting.

Other documented settings remain Q1 **12 mm** per [Eaton instructions](https://www.eaton.com/content/dam/eaton/technicaldocumentation/il/circuit-breakers/miniature-circuit-breakers-mcb/eaton-mcb-faz-na-rt-du-il0191333zu.pdf), PS1 **5 mm**, TD1/TD2 **7 mm**, SW1 **12 mm** and WAGO **13 mm**. Existing crimp-part preparations above are unchanged. Six factory-terminated ends are retained without a new stripping instruction. Four J2 plug ends omit preparation details at the owner’s direction.
