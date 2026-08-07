# Powermatic 1200 Retrofit — Wire Schedule
*Revision M · 2026-08-07 · Revision L intentionally skipped · all-new wire · number each conductor at both ends (ferrule = wire no.)*

> **Rev M safety and thermal architecture.** The Dold
> **BH5928-92-61-24-1** Stop Category 1 sequence uses instantaneous N.O. contacts to independently open
> FWD and REV commands. The instantaneous N.C. monitoring contact supplements that action by asserting
> GS20 DI4 function 18 (Force to Stop). Three delayed safety contacts independently open KA, STO1,
> and STO2 after the validated braking interval. `X011` now comes from a linked KA N.O. auxiliary;
> PLC input `X013` follows the immediate trip-monitor signal through two Phoenix Contact `2966265`
> (`PLC-RSC-24DC/21AU`) SPDT hard-gold interposing relay modules. `CR-S1` sources +24 V to DI4 and
> `CR-S2` sources +24 V to `X013` for annunciation/state clearing. Rev M retains
> `DB-FU`, `CR-DB`, and `TD-DB`: an open DB-resistor thermostat immediately drops `CR-DB` to assert DI4,
> then the release-delay timer opens the KA coil path after the commissioned delay. The hardware recovers
> automatically when the thermostat recloses, but the PLC clears motion state and requires a fresh command.

> **Rev M control topology.** Both option modules are `C2-14D2`. The used Slot 0 outputs source
> external +24 V to their loads; Slot 1 outputs remain unused and unpowered. Set the GS20 input selector
> to PNP: Y001-Y003 and the DI4 relay contacts apply external +24 V, while DCM is the grounded 0 V
> reference. PLC input groups remain sinking and accept +24 V from field contacts and the PNP-NO
> Carlo Gavazzi ICF12. Supply `-V` is bonded to PE once, adjacent to the PSU. Do not add any other
> 0V-to-PE bond.

## Conventions & assumptions
- **Type:** all **stranded** (Str), MTW/THHN 600 V 90 °C — NFPA 79 practice for machine tools.
- **Colors:** **BLK** = line/motor power (208/240 V, disconnect-controlled) · **RED** = fused 240 V control after the tap OCPD · **BLU** = ungrounded +24 VDC and switched/source control · **WHT/BLU-ID** = grounded 0 V, using white wire with permanent blue heat-shrink identification at both ends · **GN/YE** = protective earth (PE). E-stop wires 41–44 are the factory M12 cordset colors (BN/WH/BU/BK).
- **Gauge:** power/motor **12 AWG**; 240 V coil & PSU primary **16 AWG**; 24 VDC control **18 AWG**; PE **12 AWG** (power) / **14 AWG** (small bonds).
- **Runs to the machine** are tagged **(mach)** — home-run to the panel, no field j-boxes. Everything else is in-panel or on the panel door.
- **Terminal assignments in this schedule are the build authority.** Before energization, verify the received-device markings agree with the schedule for the BH5928 S/Y terminals, GS20 STO/DI/DCM, LC1D18BD 13-14 N.O. and 21-22 mirror N.C., Phoenix relay A1+/A2- and 11/12/14, Phoenix timer A1/A2/B1 and 11/12/14, and C2-14D2 C1/C2/V1/V2/CO terminals. Stop and resolve any mismatch; do not silently reinterpret a row.
- Tags: JB rear j-box · DISC disconnect · FB fuse block · KA Contactor A · KB Contactor B · CRB chunk interposing relay · **CRS1 VFD safety force-stop relay** · **CRS2 PLC trip-monitor relay** · **CRDB DB-thermal force-stop relay** · **TDDB DB-thermal release-delay timer** · **TB-DBOK three-pole jumpered distribution block** · VFD drive · MOT motor · DBR brake resistor · PSU NDR-240 · SR safety relay · PLC CLICK PLUS · EST e-stop · RST `SAFETY RESET` · SEL selector · PND pendant · DRM drum · LSB/LST limits · PRX prox · GRN/RED-M/RED-P/WHT pilots · **PSU-FU** PSU primary fuse · **KB-FU** Contactor-B tap fuse · **24V-FU/SR-FU/DB-FU** bus/safety/thermal fuses · **FAN** stirring fan · **+24 / 0V** DC buses · **GND** ground bus.

| NO | FROM | TO | SIGNAL | COLOR | AWG | TYPE |
|---|---|---|---|---|---|---|
|  | **Incoming line & power distribution** |  |  |  |  |  |
| 1 | JB : L1 (mach) | DISC : line 1 | Line L1 | BLK | 12 | Str |
| 2 | JB : L2 (mach) | DISC : line 3 | Line L2 | BLK | 12 | Str |
| 3 | JB : L3 (mach) | DISC : line 5 | Line L3 | BLK | 12 | Str |
| 4 | JB : PE (mach) | GND bus | Supply PE | GN/YE | 12 | Str |
| 5 | DISC : load 2 | FB : line L1 | L1 switched | BLK | 12 | Str |
| 6 | DISC : load 4 | FB : line L2 | L2 switched | BLK | 12 | Str |
| 7 | DISC : load 6 | FB : line L3 | L3 switched | BLK | 12 | Str |
| 8 | FB : load L1 | KA : line 1 | L1 fused | BLK | 12 | Str |
| 9 | FB : load L2 | KA : line 3 | L2 fused | BLK | 12 | Str |
| 10 | FB : load L3 | KA : line 5 | L3 fused | BLK | 12 | Str |
| 11 | KA : load 2 | VFD : R/L1 | L1 to drive in | BLK | 12 | Str |
| 12 | KA : load 4 | VFD : S/L2 | L2 to drive in | BLK | 12 | Str |
| 13 | KA : load 6 | VFD : T/L3 | L3 to drive in | BLK | 12 | Str |
|  | **Motor & brake resistor** |  |  |  |  |  |
| 14 | VFD : U | MOT : T1 (mach) | Motor U — shielded cable | BLK | 12 | Str |
| 15 | VFD : V | MOT : T2 (mach) | Motor V — shielded cable | BLK | 12 | Str |
| 16 | VFD : W | MOT : T3 (mach) | Motor W — shielded cable | BLK | 12 | Str |
| 17 | VFD : PE | MOT : frame (mach) | Motor PE — cable + shield to PE clamp at drive | GN/YE | 12 | Str |
| 18 | VFD : + (B1) | DBR : R1 | DB resistor + | BLK | 12 | Str |
| 19 | VFD : BR (B2) | DBR : R2 | DB resistor return | BLK | 12 | Str |
| 20 | +24 bus | DB-FU : in (1 A, GMC1) | Dedicated DB thermal-control branch | BLU | 18 | Str |
| 20A | DB-FU : out | TDDB : A1 (+) | Timer continuous supply; installation OCPD ≤4 A | BLU | 18 | Str |
| 20B | TDDB : A2 (-) | 0V bus | Timer supply return | WHT/BLU-ID | 18 | Str |
| 20C | DB-FU : out | DBR : TS2 | DB thermostat feed | BLU | 18 | Str |
| 20D | DBR : TS1 | TB-DBOK : 1 | DB thermal OK to poles 1-3 of `KN-4J12`; fourth pole unused | BLU | 18 | Str |
| 20E | TB-DBOK : 1 | PLC : X012 | DB thermal OK (1 = healthy) | BLU | 18 | Str |
| 20F | TB-DBOK : 2 | CRDB : A1 (+) | CR-DB energized while thermostat is healthy | BLU | 18 | Str |
| 20G | CRDB : A2 (-) | 0V bus | CR-DB polarized coil return; internal flywheel diode | WHT/BLU-ID | 18 | Str |
| 20H | TB-DBOK : 3 | TDDB : B1 | Timer control; open starts release delay (`Rs`) | BLU | 18 | Str |
|  | **Contactor B — theater (240 V, no load) — tap fused at origin** |  |  |  |  |  |
| 22 | FB : load L1 | KB-FU : P1 line | 240 V tap A (2-pole GMC3 at tap origin) | BLK | 16 | Str |
| 22A | KB-FU : P1 load | CRB : contact COM | Fused tap to chunk-relay contact | RED | 16 | Str |
| 23 | CRB : contact N.O. | KB : coil A1 | Switched to Furnas coil | RED | 16 | Str |
| 24 | FB : load L2 | KB-FU : P2 line | 240 V tap B | BLK | 16 | Str |
| 24A | KB-FU : P2 load | KB : coil A2 | Fused return to Furnas coil | RED | 16 | Str |
|  | **PSU primary & 24 V distribution** |  |  |  |  |  |
| 25 | FB : load L1 | PSU-FU : P1 in | PSU primary, pole 1 (2-pole, 2× GMC3) | BLK | 16 | Str |
| 26 | PSU-FU : P1 out | PSU : L | PSU line L | BLK | 16 | Str |
| 27 | FB : load L2 | PSU-FU : P2 in | PSU primary, pole 2 (2nd phase, 208 V L-L) | BLK | 16 | Str |
| 28 | PSU-FU : P2 out | PSU : N | PSU line N (see note — 1-pole/120 V if neutral) | BLK | 16 | Str |
| 29 | PSU : GND | GND bus | PSU PE | GN/YE | 14 | Str |
| 30 | PSU : +V | 24V-FU : in (5 A, GMC5) | +24 to main bus fuse | BLU | 16 | Str |
| 31 | 24V-FU : out | +24 bus | +24 bus feed | BLU | 16 | Str |
| 32 | PSU : −V | 0V bus | Grounded 0 V bus feed | WHT/BLU-ID | 16 | Str |
| 32A | 0V bus | GND bus | Single intentional 0V-to-PE bond adjacent to PSU | WHT/BLU-ID | 16 | Str |
| 33 | +24 bus | PLC : CPU +24 | CPU power | BLU | 18 | Str |
| 34 | 0V bus | PLC : CPU 0V | CPU power return | WHT/BLU-ID | 18 | Str |
| 35 | +24 bus | PLC Slot 0 : V1 | C2-14D2 output field power, Y001-Y004 | BLU | 18 | Str |
| 35A | +24 bus | PLC Slot 0 : V2 | C2-14D2 output field power, Y005-Y006 | BLU | 18 | Str |
| 35B | PLC Slot 0 : CO | 0V bus | C2-14D2 output common/reference | WHT/BLU-ID | 18 | Str |
| 36 | +24 bus | WHT : X1 (+) | White "power on" lamp (by DISC) | BLU | 18 | Str |
| 37 | WHT : X2 (−) | 0V bus | White lamp return | WHT/BLU-ID | 18 | Str |
|  | **Safety relay — supply, e-stop, reset/EDM, outputs** |  |  |  |  |  |
| 38 | +24 bus | SR-FU : in (3 A, GMC3) | Dedicated safety supply | BLU | 18 | Str |
| 39 | SR-FU : out | SR : A1 (+24) | SR supply + | BLU | 18 | Str |
| 40 | 0V bus | SR : A2 (0V) | SR supply − | WHT/BLU-ID | 18 | Str |
| 41 | EST : M12 pin 1 (mach) | SR : S11 (ch1) | E-stop ch1 — M12 cordset | BN | 18 | Str |
| 42 | EST : M12 pin 2 (mach) | SR : S12 (ch1) | E-stop ch1 return | WH | 18 | Str |
| 43 | EST : M12 pin 3 (mach) | SR : S31 (ch2 source) | E-stop ch2 | BU | 18 | Str |
| 44 | EST : M12 pin 4 (mach) | SR : S32 (ch2 return) | E-stop ch2 return | BK | 18 | Str |
| 44A | SR : S21 | SR : S22 | BH5928 cross-fault configuration jumper | BLU | 18 | Str |
| 44B | SR : Y39 | SR : Y40 | Enable release-delay timing (seal after validation) | BLU | 18 | Str |
| 45 | SR : S34 | RST : NO-a (door) | `SAFETY RESET` loop start | BLU | 18 | Str |
| 46 | RST : NO-b (door) | KA : 21 (mirror N.C.) | `SAFETY RESET` in series w/ EDM | BLU | 18 | Str |
| 47 | KA : 22 (mirror N.C.) | SR : S33 | EDM feedback (welded KA blocks reset) | BLU | 18 | Str |
| 48 | +24 bus | SR : 47 | Delayed KA output common | BLU | 18 | Str |
| 49 | SR : 48 | TDDB : 11 (COM) | KA path after BH5928 validated delay | BLU | 18 | Str |
| 49A | TDDB : 14 (N.O.) | KA : coil A1 | KA coil +; thermal release-delay interrupt | BLU | 18 | Str |
| 50 | KA : coil A2 (-) | 0V bus | KA coil return; LC1D18BD suppression is built in | WHT/BLU-ID | 18 | Str |
| 51 | +24 bus | SR : 57 | Delayed STO1 output common | BLU | 18 | Str |
| 52 | SR : 58 | VFD : STO1 | STO ch1; remove factory STO jumper | BLU | 18 | Str |
| 53 | +24 bus | SR : 67 | Delayed STO2 output common | BLU | 18 | Str |
| 53A | SR : 68 | VFD : STO2 | STO ch2; independent delayed contact | BLU | 18 | Str |
| 54 | VFD : STO-COM | 0V bus | STO common | WHT/BLU-ID | 18 | Str |
| 55 | +24 bus | KA : 13 (linked N.O.) | KA status source | BLU | 18 | Str |
| 56 | KA : 14 (linked N.O.) | PLC : X011 | KA proved (1 = energized; falls after safety or thermal delay) | BLU | 18 | Str |
|  | **PLC inputs (field contacts and PNP prox source +24 V into sinking input groups)** |  |  |  |  |  |
| 57 | 0V bus | PLC Slot 0 : C1 | Input common for X001-X004 | WHT/BLU-ID | 18 | Str |
| 57A | 0V bus | PLC Slot 0 : C2 | Input common for X005-X008 | WHT/BLU-ID | 18 | Str |
| 58 | +24 bus | SEL : COM (door) | Selector feed | BLU | 18 | Str |
| 59 | SEL : NO1 (door) | PLC : X001 | DRILL selected | BLU | 18 | Str |
| 60 | SEL : NO2 (door) | PLC : X002 | TAP selected | BLU | 18 | Str |
| 61 | +24 bus | PND : COM (mach) | Pendant feed | BLU | 18 | Str |
| 62 | PND : FWD-NO (mach) | PLC : X003 | START/FWD | BLU | 18 | Str |
| 63 | PND : STOP-NC (mach) | PLC : X004 | STOP (N.C., 1 = not pressed) | BLU | 18 | Str |
| 64 | PND : REV-NO (mach) | PLC : X005 | REV jog | BLU | 18 | Str |
| 65 | +24 bus | LSB : COM (mach) | Bottom-limit feed | BLU | 18 | Str |
| 66 | LSB : NC (mach) | PLC : X006 | Bottom limit (N.C. fail-safe) | BLU | 18 | Str |
| 67 | +24 bus | LST : COM (mach) | Top-limit feed | BLU | 18 | Str |
| 68 | LST : NC (mach) | PLC : X007 | Top limit (N.C. fail-safe) | BLU | 18 | Str |
| 69 | +24 bus | DRM : COM (mach) | Drum feed (2 poles used) | BLU | 18 | Str |
| 70 | DRM : LOW (mach) | PLC : X008 | Drum LOW | BLU | 18 | Str |
| 71 | DRM : HIGH (mach) | PLC : X009 | Drum HIGH | BLU | 18 | Str |
| 72 | 0V bus | PLC Slot 1 : C1 | Input common for X009-X012 | WHT/BLU-ID | 18 | Str |
| 72A | 0V bus | PLC Slot 1 : C2 | Input common for X013-X016 | WHT/BLU-ID | 18 | Str |
| 73 | +24 bus | PRX : BN V+ (mach) | Prox supply + | BLU | 18 | Str |
| 74 | 0V bus | PRX : BU V− (mach) | Prox supply − | WHT/BLU-ID | 18 | Str |
| 75 | PRX : BK out (mach) | PLC : X010 | Feed-lever-OFF (**PNP-NO → sourcing device into sinking in**) | BLU | 18 | Str |
|  | **PLC Slot 0 outputs — C2-14D2 sourcing; Slot 1 outputs unused/reserved** |  |  |  |  |  |
| 76 | — | — | Slot 1 V1/V2/CO remain unconnected; verify displayed addresses before future use | — | — | — |
| 77 | — | — | GS20 internal +24 V terminal unused; DI1-DI4 use external control power | — | — | — |
| 78 | PLC : Y001 | SR : 13 | Run-FWD before instantaneous safety contact | BLU | 18 | Str |
| 78A | SR : 14 | VFD : DI1 | Run-FWD after instantaneous safety contact | BLU | 18 | Str |
| 79 | PLC : Y002 | SR : 23 | Run-REV before instantaneous safety contact | BLU | 18 | Str |
| 79A | SR : 24 | VFD : DI2 | Run-REV after instantaneous safety contact | BLU | 18 | Str |
| 79B | +24 bus | SR : 31 | Immediate monitor feed | BLU | 18 | Str |
| 79C | SR : 32 | CRS1 : A1 (+) | Energize CR-S1 when 31-32 closes on safety trip | BLU | 18 | Str |
| 79C1 | SR : 32 | CRS2 : A1 (+) | Energize CR-S2 with CR-S1; separate conductor/ferrule | BLU | 18 | Str |
| 79D | CRS1 : A2 (-) | 0V bus | CR-S1 polarized coil return; internal flywheel diode | WHT/BLU-ID | 18 | Str |
| 79D1 | CRS2 : A2 (-) | 0V bus | CR-S2 polarized coil return; internal flywheel diode | WHT/BLU-ID | 18 | Str |
| 79E | +24 bus | CRS1 : 11 | Safety force-stop source; terminal 12 unused | BLU | 18 | Str |
| 79F | CRS1 : 14 | VFD : DI4 | Force to Stop; DI4 function 18 | BLU | 18 | Str |
| 79F1 | +24 bus | CRDB : 11 (COM) | DB-thermal force-stop source | BLU | 18 | Str |
| 79F2 | CRDB : 12 (N.C.) | VFD : DI4 | Force to Stop immediately when CR-DB de-energizes; parallel with CR-S1 path | BLU | 18 | Str |
| 79G | +24 bus | CRS2 : 11 | PLC trip-monitor source; terminal 12 unused | BLU | 18 | Str |
| 79H | CRS2 : 14 | PLC : X013 | Immediate safety-trip monitor (1 = tripped; advisory, not safety-rated) | BLU | 18 | Str |
| 80 | PLC : Y003 | VFD : DI3 | Preset-LOW (30 Hz) | BLU | 18 | Str |
| 81 | 0V bus | VFD : DCM | Grounded external-control reference; GS20 selector set to PNP | WHT/BLU-ID | 18 | Str |
| 82 | PLC : Y004 | CRB : coil A1 (+) | Sourced chunk-relay command | BLU | 18 | Str |
| 83 | CRB : coil A2 (-) | 0V bus | Chunk-relay return; module includes flywheel diode | WHT/BLU-ID | 18 | Str |
| 84 | PLC : Y005 | GRN : X1 (+) (mach) | Sourced green `all good` command | BLU | 18 | Str |
| 85 | GRN : X2 (−) (mach) | 0V bus | Green lamp return | WHT/BLU-ID | 18 | Str |
| 86 | PLC : Y006 | RED-M : X1 (+) (mach) | Sourced machine-front `FAULT / NOT READY` command | BLU | 18 | Str |
| 86A | PLC : Y006 | RED-P : X1 (+) (door) | Sourced panel `FAULT / NOT READY` command; twin ferrule with wire 86 at Y006 | BLU | 18 | Str |
| 87 | RED-M : X2 (-) (mach) | 0V bus | Machine-front red return | WHT/BLU-ID | 18 | Str |
| 87A | RED-P : X2 (-) (door) | 0V bus | Panel red return | WHT/BLU-ID | 18 | Str |
|  | **Enclosure stirring fan — internal circulation, sealed** |  |  |  |  |  |
| 97 | +24 bus | FAN : + | Stirring fan (80–92 mm, 24 VDC), runs whenever bus is up | BLU | 18 | Str |
| 98 | FAN : − | 0V bus | Fan return | WHT/BLU-ID | 18 | Str |
|  | **Protective earth / bonding** |  |  |  |  |  |
| 88 | GND bus | Back panel stud | Panel bond | GN/YE | 12 | Str |
| 89 | GND bus | Enclosure door | Door bond (flex braid) | GN/YE | 14 | Str |
| 90 | GND bus | DISC frame | Disconnect PE | GN/YE | 14 | Str |
| 91 | GND bus | KA frame | Contactor A PE | GN/YE | 14 | Str |
| 92 | GND bus | KB frame | Contactor B PE | GN/YE | 14 | Str |
| 93 | GND bus | VFD : PE | Drive PE | GN/YE | 12 | Str |
| 94 | GND bus | DIN rail(s) | Rail bond | GN/YE | 14 | Str |
| 95 | GND bus | Enclosure body / wall | Enclosure bond | GN/YE | 12 | Str |
| 96 | GND bus | Machine frame / column (mach) | **Machine PE bond — dedicated, not via motor bolts** | GN/YE | 12 | Str |
