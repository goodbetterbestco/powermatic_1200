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

H2 is the red Schneider XB4BVB4 E-stop/control-disabled indicator below SW1.
Connect raw `+24V` to K3.31, K3.32 to H2.X1 on
`CONTROL_ESTOP_DISABLED_FB`, and H2.X2 to `0V`. The two new K3 terminal
connections and both H2 terminals use blue 18 AWG panel-control wiring with
ferrule terminations. The existing E-stop connector/conduit wiring is unchanged.
Physical routes and cut lengths remain pending, as for the other panel wires.

| Actual size | Component / use | Treatment |
|---|---|---|
| 10 AWG | Proposed Hammond GRDKIT01 prefabricated bonding jumpers | Record the supplied assembly and its installed terminations separately. The enclosure–door jumper retains ring lugs at both ends. For each motor-end jumper, remove the Wago-end lug if present and terminate the correctly stripped 10 AWG conductor in a suitable Wago; retain the far-end ring lug for the motor body or machine-frame bond. Two kits supply four 12-inch assemblies, one spare for the three planned bonds, subject to usable length after modification and stud fit. These are not loose-wire stock and cannot terminate in KN-G12SP-10 clamps. |
| Manufacturer-defined | Suppressor leads, retained switch straps and other fixed device wiring | Keep the actual supplied conductor specification. Do not assign an unverified stock gauge or create an extra assembly wire for a factory/internal connection. |

KN-G12SP-10 accepts 26–12 AWG. Use separate suitable clamps for the incoming cable PE, the 12 AWG motor-conduit PE and PSU PE wire. Its two wire clamps and conductive rail foot are electrically common. Prepare each conductor according to the terminal manufacturer's instructions. The 10 AWG bonding-jumper ends use compatible studs or a wire-splicing connector rated for that conductor; they do not enter these KN-G12SP-10 clamps.

All feedthrough-terminal and grounding-block wire clamps use ferrules: one
conductor in a clamp uses a single ferrule; two conductors sharing one clamp use
a twin ferrule sized for the actual conductors. This owner requirement is stored
in each block footprint's `Wire.TerminationPolicy`. Individual
`Termination.<terminal>` fields describe the part's termination capability:
`Ferrule or twin ferrule as required`. They do not assign a conductor gauge,
barrel length or wire count to an available routing resource. Blocks and unused
jumpers are allocated only when needed during physical routing; available clamps
do not constitute missing wiring data. Select ferrule size, barrel length and
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

The owner specifies Wago splices for the six 14 AWG motor-conduit conductors to the corresponding T1–T6 motor leads, and a separate Wago PE splice. Each power splice connects only its corresponding conduit conductor and motor lead. Select its connector against the actual supplied motor-lead size/type and the 14 AWG conduit conductor; do not assume the power and PE splices require identical connector models.

The PE splice needs at least three suitable ports, one conductor per port:

1. Motor-conduit PE conductor: 12 AWG.
2. Modified jumper to motor body: 10 AWG if GRDKIT01 is selected.
3. Modified jumper to machine frame: 10 AWG if GRDKIT01 is selected.

The owner confirms that the connector model is not yet selected and directs that connector selection remain open while the wire-standard work proceeds. The PE splice must accept one 12 AWG conduit PE conductor and two 10 AWG jumper conductors, one per port. Record the exact model and its prescribed conductor preparation when selected; no connector SKU or strip length is assumed here. The gauge policy and confirmed jumper-end modifications do not depend on selecting that model now.

The insulated Wago forms a wire-to-wire PE junction; placing it inside a metal motor junction box does not itself bond that box. Account for the box-to-motor-body bond through a verified conductive attachment or an explicit separate bonding connection. Motor-body and frame bonding attachment hardware/locations remain to be defined and verified.

## Where information belongs

1. **Policy:** this document owns preferred gauge classes, application defaults and explicit exceptions. Root README and tools/wiring/README link here; avoid duplicating a second policy table in the BOM or generator.
2. **KiCad data:** custom schematic `Wire.Sizes` fields record per-terminal conductor sizing and `Wire.SizePlan` retains proposed bonding assemblies. M1.PE records 12 AWG motor-conduit PE. Saved PCB trace paths own physical wire endpoints and route geometry; the old schematic `Wire.Wxxx` fields are no longer the schedule source. One combined `Termination.<pin>` field on each placed footprint owns the termination selection at that terminal. TERM 1 and TERM 2 are read from the source and destination footprints. M1, J2, S1 and J6 use metadata-only footprints without physical geometry, excluded from BOM and position exports. Mechanical stud descriptions live on the enclosure footprint and rail lug descriptions on rail footprints. Reports and wire records do not own duplicate termination selections. These fields do not define routes or wire allocation; Completed routed paths generate wire rows; missing gauge assignments and unrouted connections are reported.
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
