# TODO

Open build and validation items for the Powermatic 1200 controls retrofit.

## Scope reset — current work

- Use [Rev P CSV](Powermatic_BOM_revP.csv) for live changes. The basic design is five HMC-9B30-11-DS contactors with 24 VDC coils, two HMX1-MI interlocks, the existing 24 VDC supply, a three-pole disconnect followed by the selected Class R motor fuse block, and the existing drum switch and pendant. [Current scope](docs/Scope_Reset_2026-09-23.md#rev-o-basic-contactor-bom-current).
- Keep all operator-control wiring at 24 VDC. Move motor winding reconnection into the panel and bring all six motor leads back to it.
- Draw separate KH supply and KS shorting functions for HIGH; these replace the former five-pole KH specification. Place mechanical interlocks between KF/KR and KL/KS. KH and KS operate together.
- Allocate the built-in 1 NO + 1 NC contacts per contactor and the two NC contacts per HMX1-MI before adding auxiliary blocks. HMX1-AUX11-F is recorded at $8.50 with quantity zero pending that allocation. One HMX1-BBREV reversing busbar kit is selected at $17.00 for KF/KR, including line-side and load-side bars. Reuse NDR-240-24; confirm selected coil demand.
- Motor fuses/block selected: three FRN-R-10 (10 A, 250 VAC, dual-element time-delay Class RK5), one RM25030-3SR and three CVR-RH-25030 covers. Upstream disconnect selected: Socomec 22013003 with 148E1111 S0 handle, 14070532 shaft and one 22943016 two-cover pack. Owner will order the eBay handle; record purchase/receipt when confirmed. AD switch showed backorder to earliest October 14, 2026 when checked September 24. Determine shaft cut length from enclosure layout. Do not reinstate the old Class T block or 35 A VFD fuses. [Fuse sizing](docs/Fuse_Selection_2026-09-24.md) and [disconnect sourcing](Disconnect_Distributor_Comparison_2026-09-24.md).
- PSU AC-input breaker selected: CB-PS1, Eaton FAZ-D4-2-NA-L, 4 A, two-pole D curve, UL 489, $55 from AD. Feed PS1 L/N from two DS1 load-side phases through both breaker poles; FG connects directly to PE. Complete input wire sizing and verify cold starting at 208 V. Separate 24 VDC branch fuses/breakers are omitted per owner; check final wire/device ratings against available PSU output current.
- Motor overloads selected: two HTOR32-6-S, OL-L at 4.0 A on KL and OL-H at 4.4 A on KH; both manual reset. Draw both NC 95–96 contacts in the common run-enable path and require a fresh start after a trip/reset. Connect KS to motor-side T1/T2/T3 downstream of OL-L. Validate both speed paths, starting at 208 V and the complete overload/contactor/fuse coordination. Check available fault current against the HMC manufacturer's 5 kA short-circuit rating; the fuse's 200 kA interrupt rating does not establish the panel SCCR.
- Fit one HMX1-SSVRC-DC suppressor across each of the five contactor coils. Add white XB4BVB1 CONTROL POWER lamp across PS1 upstream of the run/stop chain. Source PL1 from DigiKey as 4008-XB4BVB1-ND; the US listing showed two available at the September 24 check. [Selection and wiring intent](docs/Overload_Indicator_Suppression_2026-09-24.md).
- Develop the 24 VDC direction-holding and speed-selection schematic around the measured drum and pendant contacts. Exact operating sequence and wiring remain to be drawn.
- K-EN selected: one Dold HC3096N-52-900-24 coil-enable relay, $46.50 from AD. Draw its NO contact upstream of the common +24 V feed to all five contactor coils and direction seal-in paths, with the E-stop dropping K-EN. Clearing the E-stop with direction buttons released must leave the motor stopped; the owner accepts restart if a direction button is held during clearing. The module has force-guided contacts but no monitoring logic; complete schematic and wiring validation.
- Rev O has 20 unique-part rows and a $735.24 current component total: $205.00 contactors/interlocks/reversing busbars plus $119.22 fuses/block/covers plus $122.50 Socomec disconnect assembly plus $55.00 PSU input breaker plus $63.00 overloads plus $60.00 suppressors plus $52.92 indicator plus $46.50 coil-enable relay plus $11.10 M12 panel socket. All included rows are priced; only the conditional auxiliary-block row has quantity zero. This is not a complete installed project total. Prices exclude tax, shipping and Allfuses' $5 small-order fee.
- J-ESTOP selected: DigiKey A125513-ND / TE T4171310004-001, one female four-contact A-coded M12 panel socket with 200 mm leads, $11.10. Catalog symbol Controls:T4171310004-001 already exists. Assign wiring by pin number; TE lead colors on pins 3 and 4 differ from the existing E-stop assembly.
- Add enclosure and installation-material quantities after the basic circuit and layout are developed. Previous stocking allowances are preserved in Rev N, not included in Rev O.
- Update wiring documents and generated drawings to the new architecture before treating them as current. The Rev M procurement approval and implementation checks below are historical.

## Historical Rev M tasks

All remaining sections record the former design and are superseded for current work by Rev O above. They do not authorize reinstating removed components or applying the old VFD settings to the new contactor circuit.

## Procurement Gate

**Historical Rev M basis; superseded for the current redesign by the scope reset above.**

The Rev M BOM is **GO for Phase 1 procurement** of the internal electrical and
control components plus the selected panel-front devices needed for controls
layout. Owner-approved facts do not need to be reopened: the motor nameplate and
two WAGO `221-413` splices are verified; McMaster `6513T5` / `6513T6` are
accepted MTW; all `GBB` items are verified on-hand; wire quantities are stocking
estimates; and RS `70008070` is the Schneider `XB4BVB1` white pilot. Retain the
Rev M front controls and indication exactly as designed, with no panel-side
clearing of PLC fault `C10`. Furnas coil suppression is not a procurement
blocker; the powered-layout test below determines whether to add it.

All enclosure-dependent scope remains a **hard NO-GO** until the complete
controls layout passes. Hold the enclosure, cooling/ventilation, backpanel, DIN
rail and duct, cable-entry hardware, permanent mounting and door-bonding
hardware, and any still-unselected disconnect shaft/hardware; already-sourced
front controls and handle may be used as layout articles. The BOM subtotal is
not a final installed cost, and procurement approval does not release the
machine for service: all build, stop-time, safety, and sequence validation below
remains mandatory.

## Mechanical / Installation

- Select the ABB-compatible external disconnect handle and shaft after enclosure
  wall thickness, switch offset, and handle location are fixed.
- Confirm the feed-lever-OFF proximity sensor mounting geometry and target
  material before final bracket fabrication.
- Set the depth-rod metal stop so the stop takes the load before either travel
  limit lever reaches its internal over-travel limit.
- Confirm the bottom and top travel-limit tags are slightly shy of the
  mechanical stop positions.
- Remove the front-of-machine Allen-Bradley AH7810 line-voltage switch and its
  cable loop during installation.
- Confirm the enclosure is fed directly from the rear line-entry junction box.
- Confirm the machine-front red/green lamp mounting location between the travel
  limits.
- Confirm the enclosure-panel layout for `SAFETY RESET`, `DRILL / TAP`,
  `CONTROL POWER`, `FAULT / NOT READY`, and the disconnect handle.

## Electrical Verification

- Motor terminal inventory resolved: six T1-T6 leads; no grounding lug per owner.
  Fixed HIGH plan is U/T6, V/T4, W/T5 and insulated T1/T2/T3 splice.
  Verify individual lead markings and provide the planned motor-frame bond.
  Owner adopts HIGH nameplate motor data: 4.4 A, 220 V, 60 Hz, 1710 RPM.
  Historical 6.42 A is superseded; actual line supply remains 208 V.

- Drum 365-TAV2111: all 24 contact states confirm OFF=open, 1=LOW, 2=HIGH.
  Proposed physical interface: +24 to 1.L, common link 1.L-2.L, LOW 1.U to X008,
  HIGH 2.U to X009. Owner measures 1.L-2.L at 0.2 ohm in OFF, 1 and 2, confirming the permanent common-feed link.
  Owner confirms no separate enclosure ground/bond terminal; enclosure bonding remains installation work. Verify installed PLC indications and settled/transition behavior
  during commissioning; no powered operation has been performed by this review.

- Furnas KB: **all 15 represented electrical terminal functions are bench-mapped.**
  Interlock owner labels 3/TB = COM, 1/BF = NC, 2/TF = NO; coil windings V-C3 =
  283 ohm and C2-W = 282 ohm. All P1/P2/P3/AUX pairs read OL released and
  approximately 0.2 ohm manually raised, confirming four NO contacts.
  Restore the original V-C2 and C3-W links after measurement (not yet confirmed).
  Capture the full assembly identity and resolve the frame/subplate bonding method.
  Owner reports the individual subplate formerly mounted on the common two-contactor
  plate, no obvious grounding point, and about 6-8 unused small holes. Hole purpose
  and bonding continuity are unverified; no additional PE terminal is inferred.
  Contact condition, insulation and powered operation remain commissioning
  matters; the terminal-function measurements do not certify them.

- Verify installed PLC mode indication: selector contacts are owner-confirmed, DRILL = left NC 1-2 closed and TAP = right NO 3-4 closed. Wire 59 connects left 2 to X001; wire 60 connects right 4 to X002. External feed link remains NO 3 to NC 1. Contact-state clarification is complete; PLC indication is the remaining commissioning check.

- Verify disconnect order: line -> ABB OT30F3 -> Class T fuse block -> Contactor
  A -> VFD.
- Verify Contactor A mirror N.C. contact is in the safety-relay EDM/reset loop.
- Verify Contactor A N.O. auxiliary drives `X011`.
- Verify both option modules are `C2-14D2`; CLICK System Configuration shows
  Slot 0 as `X001-X008` / `Y001-Y006` and Slot 1 as `X009-X016`; enable the
  startup I/O configuration check before ladder download.
- Verify Slot 0 `V1` and `V2` receive protected +24 V, `CO` receives grounded
  0 V, and Slot 1 output-power terminals remain unconnected.
- Verify the GS20 selector is set to PNP, `Y001-Y003` source external +24 V to
  DI1-DI3, `CR-S1` sources +24 V to DI4, and `CR-S2` sources +24 V to `X013`.
- Verify `DB-FU` is a `GMC1` 1 A fuse in a `DN-F10MN` holder and supplies
  `TD-DB` continuously plus the DB thermostat branch.
- Verify `CR-DB` is energized when the DB thermostat is healthy and its N.C.
  11-12 contact asserts GS20 DI4 immediately when the thermostat opens.
- Verify BH5928 47-48 and `TD-DB` 11-14 are in series with the Contactor A coil;
  neither device can bypass the other.
- Verify STO1 and STO2 are on separate delayed BH5928 contacts.
- Verify the white power-on lamp is fed directly from the protected 24 V bus.
- Verify the DB resistor thermal switch simultaneously drops `X012`, `CR-DB`
  A1, and `TD-DB` B1 on over-temperature.
- Verify the machine-front and enclosure-panel red pilots are wired in parallel
  to `Y006`, draw no more than 36 mA total, and always indicate identically.
- Verify the NDR-240-24 `-V` has one and only one bond to PE adjacent to the
  supply; verify no second 0V-to-PE bond exists with downstream devices lifted.
- Verify every grounded 0 V conductor is white with permanent blue heat-shrink
  identification at both terminations; verify fused 240 V control conductors
  22A, 23, and 24A are red.
- Verify VFD `DCM` is the grounded external-control reference and the drive's
  internal +24 V terminal is unused for DI1-DI4.
- Clean/burnish as appropriate and measure continuity/contact resistance of the
  retained drum switch, pendant, and travel-limit contacts before landing them
  on the PLC's low-current input circuits.
- During powered controls-layout testing, exercise the `Y004` / `CR-B` 300 ms
  Contactor B pulse and check for PLC, I/O, or communications disturbance and
  excessive `CR-B` contact arcing. If observed, install a rated 208/240 VAC RC
  suppressor directly across the Furnas `D2936-32` coil, record the selected
  part and values, and repeat the test.

## VFD / Safety Validation

- Enter and verify HIGH motor nameplate data: 4.4 A, 220 V, 60 Hz, 1710 RPM.
  These supersede the former 6.42 A / 208 V motor-rated entries; supply remains 208 V.
- Set 60 Hz main frequency and 30 Hz preset-1.
- Set `P00.22=0`, `P01.13=0.50 s`, `P01.15=0.50 s`, `P01.26=0.00 s`,
  `P01.27=0.00 s`, `P02.35=0`, and `P07.20=2`.
- Enable the braking chopper and verify DB resistor operation.
- Enable over-torque/stall detection and tune it just above real tapping torque.
- Start BH5928 commissioning at 1.00 s release delay.
- Configure `TD-DB` as `Rs` release delay (`S4=ON`, `S3=OFF`) on the 0.1-10 s
  range (`S2=OFF`, `S1=OFF`), beginning near 1.00 s.
- Measure actual `TD-DB` Contactor A dropout time; do not rely on the dial
  because setting accuracy is specified against the 10 s range end.
- Measure worst-case spindle stop time across the required speed range,
  directions, and tool/chuck inertias.
- Set and seal the final BH5928 delay only after measured stop-time data proves
  adequate margin.
- Prove no auto-restart after E-stop, safety reset, or power interruption.
- With a RUN command deliberately present during drive reset and power-up,
  prove `P02.35=0` blocks motion. Remove the command and prove that only a fresh
  operator command can start the spindle.
- Prove EDM prevents safety reset with Contactor A simulated welded.
- Force the DB thermostat circuit open while running: DI4 must assert
  immediately, the spindle must complete its ramp, and Contactor A must drop
  only after the measured `TD-DB` delay.
- Restore the DB thermostat circuit and prove automatic hardware recovery,
  10 seconds of healthy `X012` before `C11` clears, and no spindle restart
  without a fresh motion command.

## Sequence Validation

- Verify DRILL FWD and REV latch independently and stop on STOP.
- Verify opposite-direction press while running performs stop-first behavior and
  never plug-reverses.
- Verify TAP will not start unless the feed lever is proved OFF.
- Verify TAP clears to IDLE on STOP, E-stop, lost permissive, loss of TAP
  selection, hard fault, or DB over-temperature.
- Verify jog enters only after a 5 second FWD hold at full permissive and
  standstill, and the entry hold cannot start spindle motion.
- During each of `DRILL_RUN`, `DRILL_REV`, `TAP_DOWN`, and `BACK_OUT`, hold FWD
  longer than 5 seconds and verify the timer does not accumulate and jog cannot
  arm or force the 30 Hz preset.
- Verify every STOP press exits jog mode.
- Verify a DB thermal trip exits jog mode.
- Verify drum OFF inhibits jog motion without exiting jog mode.
- Verify indicator priority: red solid, red blink, green blink, green solid.
- Verify both red pilots blink throughout a thermal trip/cooldown even after
  `TD-DB` drops Contactor A and `X011`.
- Verify `SAFETY RESET` resets only the BH5928/EDM circuit; hard fault `C10`
  clears with STOP while stopped and thermal state `C11` clears automatically.
