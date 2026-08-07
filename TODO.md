# TODO

Open build and validation items for the Powermatic 1200 controls retrofit.

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

## VFD / Safety Validation

- Enter motor nameplate data, including 6.42 A FLA.
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
