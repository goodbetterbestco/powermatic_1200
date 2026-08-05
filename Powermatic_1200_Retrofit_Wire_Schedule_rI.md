# Powermatic 1200 Retrofit — Wire Schedule
*Revision I · all-new wire · number each conductor at both ends (ferrule = wire no.)*

> **Rev H change (prox NPN → PNP).** The feed-lever prox is now a **PNP-NO** unit (P&F NBN8-12GM50-E2-V1). It
> sources +24 to `X010` on target, so it lands on the **sinking** input common like every other +24-fed contact —
> the dedicated sourcing common of Rev G is deleted. Only the PLC-input common wiring changes (rows 57 / 72 / 75);
> all other conductors are unchanged from Rev G. Ladder/indicator changes in Rev H are firmware-only (no new wire).

> **Rev I changes (fusing + GS20 DI + fan).**
> 1. **Row 77 deleted.** The GS20 DIs run in **NPN (sink) mode with internal power** — the drive's factory-default
>    switch position. The CLICK's sinking outputs pull DI1–DI3 to 0 V and the only common conductor is row 81
>    (CLICK 0 V → DCM). **Never land +24 V on DCM**: DCM and the STO common (SCM) share potential inside the drive,
>    so external +24 on DCM with SCM at 0 V (row 54) is a dead short through the drive.
> 2. **Contactor B tap now fused.** Rows 22/22A/24/24A route both 240 V legs through **KB-FU** (2× GMC-3 in
>    DN-F10MN) at the **tap origin** off the branch fuses — same rationale as the PSU-primary fuses (a 16 AWG tap
>    cannot be protected by the 35 A branch).
> 3. **Fuse elements pinned (per BOM):** branch = 3× **JKS-35** (Class J) in US6J1 blocks · 24V-FU = **GMC-5** ·
>    SR-FU = **GMC-3** (spec was 2 A) · PSU-FU = 2× **GMC-3** · KB-FU = 2× **GMC-3**. Blocks used: 6 of 10 DN-F10MN.
> 4. **Enclosure stirring fan added** (rows 97–98) — internal circulation only, no enclosure penetration; NEMA 12
>    rating unaffected. Mount the DB resistor high in the enclosure (short heat path to the lid).
> 5. Feed-lever prox per BOM is the **Carlo Gavazzi ICF12** (PNP-NO, SIO mode) — wiring, colors, and logic sense
>    identical to the P&F unit named in Rev H; rows 73–75 unchanged.

## Conventions & assumptions
- **Type:** all **stranded** (Str), MTW/THHN 600 V 90 °C — NFPA 79 practice for machine tools.
- **Colors (per doc §9):** **BLK** = line/motor power (208/240 V, disconnect-controlled) · **BLU** = 24 VDC control · **GN/YE** = protective earth (PE). E-stop wires 41–44 are the factory M12 cordset colors (BN/WH/BU/BK).
- **Gauge:** power/motor **12 AWG**; 240 V coil & PSU primary **16 AWG**; 24 VDC control **18 AWG**; PE **12 AWG** (power) / **14 AWG** (small bonds).
- **Runs to the machine** are tagged **(mach)** — home-run to the panel, no field j-boxes. Everything else is in-panel or on the panel door.
- **Terminal designations are typical** — verify against each device's own diagram (MSR127 S-terminals, GS20 STO/DI/DCM, CWBS12 mirror aux).
- Tags: JB rear j-box · DISC disconnect · FB fuse block · KA Contactor A · KB Contactor B · CRB interposing relay · VFD drive · MOT motor · DBR brake resistor · PSU NDR-240 · SR safety relay · PLC CLICK PLUS · EST e-stop · RST reset · SEL selector · PND pendant · DRM drum · LSB/LST limits · PRX prox · GRN/RED/WHT pilots · **PSU-FU** PSU primary fuse · **KB-FU** Contactor-B tap fuse · **24V-FU/SR-FU** bus/safety fuses · **FAN** stirring fan · **+24 / 0V** DC buses · **GND** ground bus.

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
| 20 | DBR : TS1 | PLC : X012 (spare in) | DB over-temp N.C. | BLU | 18 | Str |
| 21 | DBR : TS2 | +24 bus | DB over-temp feed | BLU | 18 | Str |
|  | **Contactor B — theater (240 V, no load) — tap fused at origin (Rev I)** |  |  |  |  |  |
| 22 | FB : load L1 | KB-FU : P1 line | 240 V tap A (2-pole GMC-3 at tap origin) | BLK | 16 | Str |
| 22A | KB-FU : P1 load | CRB : contact COM | Fused tap to chunk-relay contact | BLK | 16 | Str |
| 23 | CRB : contact N.O. | KB : coil A1 | Switched to Furnas coil | BLK | 16 | Str |
| 24 | FB : load L2 | KB-FU : P2 line | 240 V tap B | BLK | 16 | Str |
| 24A | KB-FU : P2 load | KB : coil A2 | Fused return to Furnas coil | BLK | 16 | Str |
|  | **PSU primary & 24 V distribution** |  |  |  |  |  |
| 25 | FB : load L1 | PSU-FU : P1 in | PSU primary, pole 1 (2-pole, 2× GMC-3) | BLK | 16 | Str |
| 26 | PSU-FU : P1 out | PSU : L | PSU line L | BLK | 16 | Str |
| 27 | FB : load L2 | PSU-FU : P2 in | PSU primary, pole 2 (2nd phase, 208 V L-L) | BLK | 16 | Str |
| 28 | PSU-FU : P2 out | PSU : N | PSU line N (see note — 1-pole/120 V if neutral) | BLK | 16 | Str |
| 29 | PSU : GND | GND bus | PSU PE | GN/YE | 16 | Str |
| 30 | PSU : +V | 24V-FU : in (5 A, GMC-5) | +24 to main bus fuse | BLU | 16 | Str |
| 31 | 24V-FU : out | +24 bus | +24 bus feed | BLU | 16 | Str |
| 32 | PSU : −V | 0V bus | 0 V bus feed | BLU | 16 | Str |
| 33 | +24 bus | PLC : CPU +24 | CPU power | BLU | 18 | Str |
| 34 | 0V bus | PLC : CPU 0V | CPU power return | BLU | 18 | Str |
| 35 | +24 bus | PLC : output-module field +V | Output field power | BLU | 18 | Str |
| 36 | +24 bus | WHT : X1 (+) | White "power on" lamp (by DISC) | BLU | 18 | Str |
| 37 | WHT : X2 (−) | 0V bus | White lamp return | BLU | 18 | Str |
|  | **Safety relay — supply, e-stop, reset/EDM, outputs** |  |  |  |  |  |
| 38 | +24 bus | SR-FU : in (3 A, GMC-3) | Dedicated safety supply | BLU | 18 | Str |
| 39 | SR-FU : out | SR : A1 (+24) | SR supply + | BLU | 18 | Str |
| 40 | 0V bus | SR : A2 (0V) | SR supply − | BLU | 18 | Str |
| 41 | EST : M12 pin 1 (mach) | SR : S11 (ch1) | E-stop ch1 — M12 cordset | BN | 18 | Str |
| 42 | EST : M12 pin 2 (mach) | SR : S12 (ch1) | E-stop ch1 return | WH | 18 | Str |
| 43 | EST : M12 pin 3 (mach) | SR : S21 (ch2) | E-stop ch2 | BU | 18 | Str |
| 44 | EST : M12 pin 4 (mach) | SR : S22 (ch2) | E-stop ch2 return | BK | 18 | Str |
| 45 | SR : S34 | RST : NO-a (door) | Reset loop start | BLU | 18 | Str |
| 46 | RST : NO-b (door) | KA : mirror N.C.-a | Reset in series w/ EDM | BLU | 18 | Str |
| 47 | KA : mirror N.C.-b | SR : S33 | EDM feedback (welded KA blocks reset) | BLU | 18 | Str |
| 48 | +24 bus | SR : 13 | Output 13-14 common | BLU | 18 | Str |
| 49 | SR : 14 | KA : coil A1 | KA coil + (dropped by SR) | BLU | 18 | Str |
| 50 | KA : coil A2 | 0V bus | KA coil − (fit surge suppressor A1-A2) | BLU | 18 | Str |
| 51 | +24 bus | SR : 23 | Output 23-24 common | BLU | 18 | Str |
| 52 | SR : 24 | VFD : STO1 | STO ch1 (remove factory STO jumper) | BLU | 18 | Str |
| 53 | SR : 24 | VFD : STO2 | STO ch2 | BLU | 18 | Str |
| 54 | VFD : STO-COM | 0V bus | STO common | BLU | 18 | Str |
| 55 | +24 bus | SR : 33 | Output 33-34 common | BLU | 18 | Str |
| 56 | SR : 34 | PLC : X011 | Safety-OK to PLC (1 = safe) | BLU | 18 | Str |
|  | **PLC inputs (all dry contacts AND the PNP prox fed/sourced from +24 → single sinking common to 0V)** |  |  |  |  |  |
| 57 | 0V bus | PLC : IN-COM (sinking groups) | Sinking input common | BLU | 18 | Str |
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
| 72 | 0V bus | PLC : IN-COM (X009–X012 bank) | Sinking common — prox now PNP, shares 0V common | BLU | 18 | Str |
| 73 | +24 bus | PRX : BN V+ (mach) | Prox supply + | BLU | 18 | Str |
| 74 | 0V bus | PRX : BU V− (mach) | Prox supply − | BLU | 18 | Str |
| 75 | PRX : BK out (mach) | PLC : X010 | Feed-lever-OFF (**PNP-NO → sourcing device into sinking in**) | BLU | 18 | Str |
|  | **PLC outputs — VFD, chunk, lamps (C2-14D1 sinking)** |  |  |  |  |  |
| 76 | 0V bus | PLC : OUT-COM (C3/C4) | Output common (sinking) | BLU | 18 | Str |
| 77 | — | — | **Deleted (Rev I)** — GS20 DIs use internal power, NPN mode; no +24 lands on the drive | — | — | — |
| 78 | PLC : Y001 | VFD : DI1 | Run-FWD | BLU | 18 | Str |
| 79 | PLC : Y002 | VFD : DI2 | Run-REV | BLU | 18 | Str |
| 80 | PLC : Y003 | VFD : DI3 | Preset-LOW (30 Hz) | BLU | 18 | Str |
| 81 | 0V bus | VFD : DCM | CLICK 0 V → DCM — sole DI common (NPN internal-power mode; **never** +24 on DCM) | BLU | 18 | Str |
| 82 | +24 bus | CRB : coil A1 | Chunk relay + | BLU | 18 | Str |
| 83 | PLC : Y004 | CRB : coil A2 | Chunk relay (flyback diode across coil) | BLU | 18 | Str |
| 84 | +24 bus | GRN : X1 (+) (mach) | Green "all good" + | BLU | 18 | Str |
| 85 | GRN : X2 (−) (mach) | PLC : Y005 | Green return | BLU | 18 | Str |
| 86 | +24 bus | RED : X1 (+) (mach) | Red "not good" + | BLU | 18 | Str |
| 87 | RED : X2 (−) (mach) | PLC : Y006 | Red return | BLU | 18 | Str |
|  | **Enclosure stirring fan (Rev I — internal circulation, sealed)** |  |  |  |  |  |
| 97 | +24 bus | FAN : + | Stirring fan (80–92 mm, 24 VDC), runs whenever bus is up | BLU | 18 | Str |
| 98 | FAN : − | 0V bus | Fan return | BLU | 18 | Str |
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
