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

## Electrical Verification

- Verify disconnect order: line -> ABB OT30F3 -> Class T fuse block -> Contactor
  A -> VFD.
- Verify Contactor A mirror N.C. contact is in the safety-relay EDM/reset loop.
- Verify Contactor A N.O. auxiliary drives `X011`.
- Verify `CR-S1` commands GS20 DI4 and `CR-S2` commands PLC `X013`.
- Verify STO1 and STO2 are on separate delayed BH5928 contacts.
- Verify the white power-on lamp is fed directly from the protected 24 V bus.
- Verify the DB resistor thermal switch opens `X012` on over-temperature.
- Verify the GS20 DI mode is NPN/sink internal-power mode and no external +24 V
  is landed on DCM.

## VFD / Safety Validation

- Enter motor nameplate data, including 6.42 A FLA.
- Set 60 Hz main frequency and 30 Hz preset-1.
- Set `P00.22=0`, `P01.13=0.50 s`, `P01.15=0.50 s`, `P01.26=0.00 s`,
  `P01.27=0.00 s`, and `P07.20=2`.
- Enable the braking chopper and verify DB resistor operation.
- Enable over-torque/stall detection and tune it just above real tapping torque.
- Start BH5928 commissioning at 1.00 s release delay.
- Measure worst-case spindle stop time across the required speed range,
  directions, and tool/chuck inertias.
- Set and seal the final BH5928 delay only after measured stop-time data proves
  adequate margin.
- Prove no auto-restart after E-stop, safety reset, or power interruption.
- Prove EDM prevents safety reset with Contactor A simulated welded.

## Sequence Validation

- Verify DRILL FWD and REV latch independently and stop on STOP.
- Verify opposite-direction press while running performs stop-first behavior and
  never plug-reverses.
- Verify TAP will not start unless the feed lever is proved OFF.
- Verify TAP clears to IDLE on STOP, E-stop, lost permissive, loss of TAP
  selection, hard fault, or DB over-temperature.
- Verify jog enters only after a 5 second FWD hold and the entry hold cannot
  start spindle motion.
- Verify every STOP press exits jog mode.
- Verify drum OFF inhibits jog motion without exiting jog mode.
- Verify indicator priority: red solid, red blink, green blink, green solid.
