# Powermatic 1200 Drill Press Controls Retrofit

**Machine:** 1967 Powermatic 1200, 3-phase tapping/drilling drill press  
**Owner / designer:** Evan Thayer - GoodBetterBestCo  
**Document revision:** M
**Date:** 2026-08-07
**Design references:** NFPA 79, UL 508A construction practices

This document defines the Rev M control-system design. Revision L is intentionally
skipped.

---

## 1. Design Intent

The retrofit replaces the original line-voltage control system with a modern
low-voltage control architecture while retaining the machine's normal mechanical
use model.

Design objectives:

1. Remove line voltage from operator controls, limit switches, selector devices,
   and operator indicators.
2. Use a VFD to command spindle direction, controlled stopping, speed preset
   selection, and electronic motor overload.
3. Add single-cycle TAP mode using the existing travel limits as sequence inputs.
4. Preserve normal DRILL behavior with latched forward and reverse operation.
5. Provide setup inching through a deliberate jog mode.
6. Retain one vintage Furnas contactor only as an unloaded audible "chunk"
   device.
7. Keep the safety stop independent of the PLC.
8. Provide a hardwired DB-resistor thermal stop that commands controlled
   deceleration before removing VFD input power.

The PLC controls operating sequence only. It is not the safety system and is not
credited with making the machine safe after an E-stop.

---

## 2. Power Topology

### 2.1 Line Power Path

```
208 VAC, 3-phase
  -> ABB OT30F3 non-fused UL 98 disconnect
  -> Littelfuse LFT300603C Class T fuse block, 3 x TJN35 fuses
  -> Schneider LC1D18BD Contactor A
  -> AutomationDirect GS23-22P0 VFD
  -> Powermatic motor, wired permanent 4-pole delta
```

The enclosure disconnect is the sole disconnecting means for the retrofit
control system. It is padlockable in OFF.

### 2.2 Motor Topology

The motor is wired permanently in its 4-pole delta high-speed configuration and
is treated as a 3-lead 1750 RPM motor. The original pole-change function is not
used.

The VFD provides the two electrical speed ranges:

| Range command | VFD frequency | Function |
|---|---:|---|
| HIGH | 60 Hz | Reproduces the original high range through the belts/CVT |
| LOW | 30 Hz | Reproduces the original low range through the belts/CVT |

The operator still selects the belt position and Reeves variable-speed setting
mechanically. The retained drum switch becomes a 24 VDC selector/permissive with
three meaningful states:

| Drum state | Controller meaning |
|---|---|
| OFF | No spindle motion permitted |
| LOW | Run permitted, 30 Hz preset selected |
| HIGH | Run permitted, 60 Hz main frequency selected |

### 2.3 Control Power

The control system uses 24 VDC for PLC inputs, PLC outputs, relay coils,
operator controls, safety relay control, and status lamps. The 24 V bus is
provided by the Mean Well NDR-240-24 supply and is protected at the supply
output.

The NDR-240-24 output is operated as a grounded control circuit. Supply `-V`
feeds the 0 V distribution bus, and one intentional 0V-to-PE bond is installed
adjacent to the supply. No other 0V-to-PE bond is permitted. Grounded 0 V
conductors are white with permanent blue identification at both terminations;
ungrounded `+24 VDC` control conductors are blue.

Both CLICK PLUS `C2-14D2` modules have sourcing transistor outputs. On the
used Slot 0 module, `V1` and `V2` connect to the protected `+24 VDC` bus and
`CO` connects to grounded 0 V. Each energized output therefore applies
`+24 VDC` to its load, and the load returns directly to the grounded 0 V bus.

The white power-on lamp is wired directly from the protected 24 V bus. It is on
whenever the disconnect is closed and the 24 V bus is energized, including fault
conditions where the PLC is stopped, faulted, or not commanding outputs.

The DB-resistor thermal-control branch is protected by `DB-FU`, a 1 A
Bussmann `GMC1` fuse in a `DN-F10MN` holder. This branch supplies the
`TD-DB` timer continuously and feeds the resistor thermostat, `CR-DB`, and
PLC input `X012`. The timer manufacturer's installation limit is 4 A maximum;
the selected 1 A branch fuse satisfies that requirement.

### 2.4 Contactor Roles

| Device | Role | Control authority |
|---|---|---|
| Contactor A, Schneider `LC1D18BD` | Safety/line contactor feeding the VFD input | BH5928 delayed output in series with `TD-DB` thermal-delay contact |
| Contactor B, vintage Furnas | Unloaded audible feedback contactor | PLC output `Y004` through interposing relay `CR-B` |

Contactor A is never driven by the PLC. `TD-DB` can only interrupt the
Contactor A coil path; it cannot energize the contactor when BH5928 contact
47-48 is open. Contactor B switches no motor current and no VFD input or output
current.

The original overload heaters are removed. Motor overload protection is provided
by the VFD electronic thermal model using the motor nameplate FLA.

---

## 3. Safety System

### 3.1 Safety Function

The E-stop safety function is a Stop Category 1 sequence:

1. Immediately remove both VFD run commands from the drive terminals.
2. Command a controlled deceleration through the VFD stopping path.
3. After the validated relay delay, remove VFD input power and both STO
   channels.

The safety path is hardwired through the Dold safety relay and does not depend on
PLC scan, PLC outputs, PLC state, or PLC program correctness.

### 3.2 Safety Relay

Safety relay: **Dold BH5928-92-61-24-1**.

Required characteristics:

| Function | Requirement |
|---|---|
| Supply | 24 V |
| Reset | Manual monitored reset |
| E-stop input | Dual-channel N.C. positive-opening contacts |
| Immediate safety outputs | Two N.O. contacts |
| Delayed safety outputs | Three release-delayed N.O. contacts |
| Monitoring output | One instantaneous N.C. monitoring contact |
| Delay range | 0.1-1.0 s |

The safety relay starts commissioning at 1.00 s release delay. The final delay is
set only after measured worst-case stopping performance is known. The intended
final value is about 0.75 s if worst-case spindle stop time is no more than
0.50 s, preserving margin between completed deceleration and torque/power
removal.

The selected BH5928 variant has no adjustment above 1.00 s. If the required
stop-time margin cannot be demonstrated within that range, do not release the
machine; correct the braking/drive configuration or perform a formal safety-
timing redesign using a different relay variant.

### 3.3 Safety Inputs

The E-stop station is the sole safety input.

| Input path | Device |
|---|---|
| Channel 1 | E-stop N.C. contact 1 |
| Channel 2 | E-stop N.C. contact 2 |
| Reset/EDM loop | Black `SAFETY RESET` pushbutton in series with Contactor A mirror N.C. |

The TAP bottom and top travel limits are sequence inputs, not safety relay
inputs. TAP mode uses the limits during normal operation, so they cannot be in
the hardwired E-stop loop.

No door interlock is part of the safety relay circuit.

### 3.4 Immediate Outputs

The two instantaneous N.O. safety contacts are wired in series with the VFD run
commands:

| Safety contact | Controlled circuit |
|---|---|
| 13-14 | PLC `Y001` to VFD DI1, Run-FWD |
| 23-24 | PLC `Y002` to VFD DI2, Run-REV |

Opening either run-command path causes the GS20 to execute its configured ramp
stop. The DB resistor is part of this stopping path.

The BH5928 instantaneous N.C. monitoring contact drives two interposing relays:

| Relay | Function |
|---|---|
| `CR-S1` | Applies +24 V to GS20 DI4 Force to Stop on a safety trip |
| `CR-S2` | Reports immediate safety trip to PLC input `X013` |

`CR-S1`, `CR-S2`, DI4, and `X013` are supplementary control/indication paths.
They are not credited as independent safety outputs.

### 3.5 Delayed Outputs

The three delayed N.O. safety contacts establish the final safe state:

| Safety contact | Controlled circuit |
|---|---|
| 47-48 | Contactor A coil through the series `TD-DB` N.O. contact |
| 57-58 | VFD STO1 |
| 67-68 | VFD STO2 |

STO1 and STO2 remain separate channels. They are not paralleled on one relay
contact.

Rev M does not include a mechanical brake. No delayed safety output remains
spare.

### 3.6 Monitoring

| Signal | Source | Meaning |
|---|---|---|
| `X011` | Contactor A mechanically linked N.O. auxiliary | Contactor A energized; falls after a safety delay or DB thermal delay |
| `X013` | `CR-S2` from BH5928 immediate monitoring contact | Immediate safety trip active |

`X011` falls when either the BH5928 delayed output or the `TD-DB` delayed
thermal contact opens Contactor A. The PLC uses it as a run permissive and
state-clear signal. `X013` distinguishes an immediate safety trip from a DB
thermal shutdown.

No auto-restart is permitted. After an E-stop or power interruption, the safety
relay requires manual reset and the PLC sequence requires a fresh operator start
command. GS20 parameter `P02.35` is fixed at `0`, so a run command that remains
present during drive reset or reboot cannot start the drive. Rev M does not use
a separate Drive Ready feedback input; the line-start lockout setting and the
commissioning power-cycle tests are mandatory.

### 3.7 DB-Resistor Thermal Protection

The Crohm `BR-N1-280W50` N.C. thermostat is an equipment-protection input, not
a safety-rated input. Its hardware path does not depend on PLC scan or PLC
outputs:

1. With the thermostat healthy, `X012` and `TD-DB` control input `B1` receive
   fused +24 V and `CR-DB` is energized.
2. If the thermostat opens, `X012` falls and `CR-DB` de-energizes immediately.
   The de-energized `CR-DB` N.C. contact applies fused +24 V to DI4, commanding
   Force to Stop with deceleration time 2.
3. `TD-DB`, Phoenix Contact `2910140`, remains powered at `A1-A2`. Loss of its
   `A1-B1` control signal starts the release delay while output contact 11-14
   remains closed.
4. After the commissioned delay, nominally about 1.00 s, `TD-DB` contact 11-14
   opens the Contactor A coil circuit. The BH5928 still controls the same circuit
   in series and independently controls STO1 and STO2.
5. When the thermostat recloses, `CR-DB`, `TD-DB`, and Contactor A recover
   automatically. The PLC holds `C11` for 10 seconds of continuously healthy
   `X012`, then clears the thermal state. A fresh motion command is required.

Configure `TD-DB` with `S4=ON`, `S3=OFF` (`Rs`, release delay with control
contact) and `S2=OFF`, `S1=OFF` (0.1-10 s range). Begin commissioning at a
nominal 1.00 s setting and measure the actual Contactor A dropout time. The
timer's setting accuracy is specified as 2.5% of the 10 s range end, so the
final setting must be based on measured operation rather than dial position
alone.

---

## 4. Sequence of Operations

### 4.1 Common Run Permissives

Spindle motion requires all of the following:

| Permissive | Required state |
|---|---|
| Final safety state | `X011 = 1` |
| Immediate safety trip | `X013 = 0` |
| Drum switch | LOW or HIGH selected |
| STOP pushbutton | Released |
| Hard fault | Not active |
| DB over-temperature | Not active |

TAP mode also requires the feed lever to be proved OFF before a cycle can start.

### 4.2 Mode Selection

The door-mounted DRILL/TAP selector is a mode request, not a run command.

| Selector action | Required behavior |
|---|---|
| Select DRILL while stopped | DRILL commands are accepted |
| Select TAP while stopped | TAP start commands are accepted if TAP entry permissives are true |
| Change selector during motion | Current DRILL latch or TAP state is dropped |
| Select TAP by itself | No spindle motion |

TAP always starts from IDLE on a fresh FWD press. Selecting TAP never starts a
cycle by itself.

### 4.3 DRILL Mode

DRILL mode provides latched forward and reverse spindle operation.

| Operator action | Required behavior |
|---|---|
| FWD press/release | Latch forward run if permissives are true |
| REV press | Latch reverse run if permissives are true |
| STOP press | Stop and clear both DRILL latches |
| Opposite direction press while running | Stop the current direction only |
| Second opposite direction press after stop | Start the opposite direction if permissives are true |

The controller does not plug-reverse the spindle under power. Direction changes
require a stop-first transition.

If the bottom travel limit is reached while running forward in DRILL mode, the
PLC latches a hard fault. Reverse over-travel is handled by the VFD
over-torque/stall backstop rather than a ladder bottom-limit fault.

### 4.4 TAP Mode

TAP mode performs one self-leading tap cycle per fresh FWD command.

```
IDLE -> TAP_DOWN -> BACK_OUT -> IDLE
```

| State | Motor command | Exit condition |
|---|---|---|
| IDLE | Off | Fresh FWD press with TAP selected, permissives true, and feed lever OFF |
| TAP_DOWN | Forward | Bottom travel limit reached |
| BACK_OUT | Reverse | Top travel limit reached |

The feed lever must be proved OFF before TAP_DOWN starts. The same signal is
monitored during TAP_DOWN and BACK_OUT; if the lever is engaged during the
cycle, the PLC latches a hard fault and stops the cycle.

If STOP, E-stop, loss of safety permissive, loss of TAP selection, drum OFF, hard
fault, or DB over-temperature occurs during TAP, the TAP state clears to IDLE.
After reset/recovery, a fresh FWD press is required.

### 4.5 JOG Mode

Jog mode is a setup/inching mode entered by holding FWD for at least 5 seconds
while the controller is fully permissive and no DRILL or TAP run state is
active. The five-second timer does not accumulate during `DRILL_RUN`,
`DRILL_REV`, `TAP_DOWN`, or `BACK_OUT`. Entering jog mode never starts the
spindle.

Required jog behavior:

| Condition | Required behavior |
|---|---|
| FWD held for at least 5 s while safe and fully stopped | Arm jog mode and consume that FWD press |
| FWD held during any DRILL or TAP run state | Do not time or arm jog mode |
| FWD still held after jog arms | No spindle motion from the entry hold |
| Fresh FWD press while jog armed | Momentary forward jog |
| Fresh REV press while jog armed | Momentary reverse jog |
| FWD/REV released | Stop jog motion |
| Drum OFF while jog armed | Jog remains armed; spindle motion inhibited |
| Drum LOW or HIGH while jog armed | Momentary jog motion permitted if other permissives are true |

Jog speed is forced to the 30 Hz preset. Normal latched DRILL starts and TAP
starts are inhibited while jog mode is armed.

Jog exits on any STOP press, 60 seconds of jog inactivity, any hard fault, DB
over-temperature, E-stop, or loss of final safety state. STOP has no long-hold
distinction in jog mode; any STOP press exits jog.

### 4.6 Operator Indicators

The machine-front green lamp, machine-front red lamp, and enclosure-panel red
lamp are PLC outputs and are advisory. The two red lamps are wired in parallel
to `Y006` and always show the same state. They do not perform a safety function.

| State | Indication |
|---|---|
| Safe, no fault, not jogging | Green solid |
| Jog armed | Green blink |
| DB resistor over-temperature or cooldown | Both red lamps blink |
| Safety trip, Contactor A not proved for a nonthermal reason, or latched hard fault | Both red lamps solid |

Red solid has priority over red blink. Red blink has priority over green blink.
Green blink has priority over green solid.

The white power-on lamp is not a PLC output. It remains on whenever the
disconnect is closed and the 24 V bus is energized.

The enclosure controls are labeled `SAFETY RESET`, `DRILL / TAP`, `CONTROL
POWER`, and `FAULT / NOT READY`. The black safety-reset button resets only the
BH5928/EDM safety circuit. PLC hard fault `C10` clears with STOP while fully
stopped, and DB thermal state `C11` clears automatically; therefore the red lamp
must not be labeled `RESET REQUIRED`.

---

## 5. I/O Assignments

### 5.1 CLICK PLUS Hardware

Controller: **CLICK PLUS C2-01CPU-2** with two **C2-14D2** option modules.

The `C2-14D2` input commons are configured for sinking inputs. Field contacts
and the PNP sensor source 24 V into the input points. The outputs are 24 VDC
sourcing outputs rated 0.1 A per point and 0.6 A per common. Slot 0 output
terminals `V1` and `V2` receive protected +24 V and `CO` receives grounded 0 V.

The CLICK System Configuration shall be set to the following physical mapping
before ladder transcription or download:

| CPU location | Module | Input allocation | Output allocation |
|---|---|---|---|
| Option Slot 0 | `C2-14D2` | `X001-X008` | `Y001-Y006`, all used |
| Option Slot 1 | `C2-14D2` | `X009-X016` | Unused and reserved; verify displayed addresses before future use |

The field wire numbers remain the build identifiers regardless of software
address notation. Enable the CLICK startup I/O configuration check so a module
or slot mismatch prevents RUN mode.

### 5.2 Inputs

| Addr | Signal | Field device | Logic state |
|---|---|---|---|
| `X001` | Mode DRILL | Door selector N.O. contact | 1 = DRILL selected |
| `X002` | Mode TAP | Door selector N.O. contact | 1 = TAP selected |
| `X003` | FWD / START / jog entry | Pendant FWD N.O. pushbutton | 1 = pressed |
| `X004` | STOP | Pendant STOP N.C. pushbutton | 1 = released, 0 = stop request or broken circuit |
| `X005` | REV | Pendant REV N.O. pushbutton | 1 = pressed |
| `X006` | Bottom travel limit | Existing SPDT limit, N.C. side | 1 = not at bottom, 0 = bottom reached or broken circuit |
| `X007` | Top travel limit | Existing SPDT limit, N.C. side | 1 = not at top, 0 = top reached or broken circuit |
| `X008` | Drum LOW | Retained drum switch contact | 1 = LOW selected |
| `X009` | Drum HIGH | Retained drum switch contact | 1 = HIGH selected |
| `X010` | Feed-lever-OFF proof | PNP-NO proximity sensor | 1 = feed lever confirmed OFF |
| `X011` | Contactor A energized | Contactor A mechanically linked N.O. auxiliary | 1 = Contactor A energized |
| `X012` | DB resistor thermal OK | DB resistor N.C. thermal switch | 1 = normal, 0 = over-temperature or broken circuit |
| `X013` | Immediate safety trip | `CR-S2` interposing relay | 1 = safety relay tripped |

### 5.3 Outputs

| Addr | Signal | Controlled device | Required behavior |
|---|---|---|---|
| `Y001` | VFD Run-FWD | GS20 DI1 through BH5928 instantaneous contact | Forward command only |
| `Y002` | VFD Run-REV | GS20 DI2 through BH5928 instantaneous contact | Reverse command only |
| `Y003` | VFD Preset LOW | GS20 DI3 | On = 30 Hz preset |
| `Y004` | Contactor B chunk | `CR-B` interposing relay | Pulsed on run/direction transitions |
| `Y005` | Green lamp | Machine-front green 24 V pilot | Solid all-good, blink jog armed |
| `Y006` | Red lamps | Machine-front and enclosure-panel red 24 V pilots in parallel | Solid safety/hard fault, blink DB over-temp |

Contactor A is not a PLC output.

PLC internal bits, timers, rung order, and Boolean output equations are defined
in the ladder-logic document.

---

## 6. VFD Configuration

Drive: **AutomationDirect GS23-22P0**, 2 HP, 230 V class, 3-phase input.

Motor data basis: 208 V, 60 Hz, 6.42 A FLA, permanent 4-pole delta connection.

| Function | Setting | Design requirement |
|---|---|---|
| Motor rated current | 6.42 A | Enables electronic thermal overload |
| Motor rated voltage/frequency | 208 V / 60 Hz | Motor base point |
| Command source | External terminals | PLC and safety relay own the commands |
| Frequency source | Preset / multi-speed | Drum LOW/HIGH selects 30/60 Hz behavior |
| Main frequency | 60 Hz | HIGH range |
| Preset 1 frequency | 30 Hz | LOW range and jog |
| DI1 | Run-FWD | Commanded by `Y001`, interrupted by safety relay |
| DI2 | Run-REV | Commanded by `Y002`, interrupted by safety relay |
| DI3 | Preset 1 select | Commanded by `Y003` |
| DI4 | Function 18, Force to Stop | Commanded by `CR-S1` on safety trip or de-energized `CR-DB` on DB over-temperature |
| Stop method `P00.22` | 0, ramp to stop | Loss of run command decelerates instead of coasting |
| Decel time 1 `P01.13` | 0.50 s initial | Normal stop ramp basis |
| Decel time 2 `P01.15` | 0.50 s initial | E-stop force-stop ramp basis |
| Decel S-curve `P01.26` / `P01.27` | 0.00 s / 0.00 s | Prevents hidden extension of stop time |
| EF/force-stop selection `P07.20` | 2 | DI4 function 18 uses decel time 2 |
| External operation after reset/reboot `P02.35` | 0, disabled | A maintained RUN command cannot start the drive after reset or reboot |
| Braking chopper | Enabled | DB resistor absorbs decel/reversal energy |
| STO | STO1 and STO2 separate | Both opened after relay delay |
| Over-torque/stall detection | Enabled | Backstop for failed tap reversal/stop or jam |
| DI mode | PNP selector; drive inputs are sinking loads | `C2-14D2` outputs and relay contacts apply external +24 V; DCM is grounded 0 V |

DI function 28 is not used for E-stop because it removes drive output
immediately and produces a coast/free-run stop.

GS20 `DCM` connects to the grounded 0 V bus. `Y001`, `Y002`, and `Y003`
source external +24 V to DI1, DI2, and DI3. `CR-S1` and `CR-DB` independently
source external +24 V to DI4. The drive's internal `+24 V` terminal is not used
for DI1-DI4 command power.

The braking resistor thermal switch drives the independent `CR-DB`/`TD-DB`
hardware stop and is monitored at `X012`. Over-temperature immediately commands
DI4 controlled deceleration, opens Contactor A after the measured timer delay,
inhibits run, and produces red blink indication through the thermal trip and
10-second healthy cooldown. Recovery is automatic, but motion requires a fresh
operator command.

---

*End of document - GoodBetterBestCo, Rev M, 2026-08-07.*
