# Powermatic 1200 Drill Press Controls Retrofit

**Machine:** 1967 Powermatic 1200, 3-phase tapping/drilling drill press  
**Owner / designer:** Evan Thayer - GoodBetterBestCo  
**Document revision:** J  
**Date:** 2026-08-05  
**Design references:** NFPA 79, UL 508A construction practices

This document defines the Rev J control-system design.

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

The white power-on lamp is wired directly from the protected 24 V bus. It is on
whenever the disconnect is closed and the 24 V bus is energized, including fault
conditions where the PLC is stopped, faulted, or not commanding outputs.

### 2.4 Contactor Roles

| Device | Role | Control authority |
|---|---|---|
| Contactor A, Schneider `LC1D18BD` | Safety/line contactor feeding the VFD input | Safety relay delayed output only |
| Contactor B, vintage Furnas | Unloaded audible feedback contactor | PLC output `Y004` through interposing relay `CR-B` |

Contactor A is never driven by the PLC. Contactor B switches no motor current
and no VFD input or output current.

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

### 3.3 Safety Inputs

The E-stop station is the sole safety input.

| Input path | Device |
|---|---|
| Channel 1 | E-stop N.C. contact 1 |
| Channel 2 | E-stop N.C. contact 2 |
| Reset/EDM loop | Manual reset pushbutton in series with Contactor A mirror N.C. |

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
| `CR-S1` | Commands GS20 DI4 Force to Stop |
| `CR-S2` | Reports immediate safety trip to PLC input `X013` |

`CR-S1`, `CR-S2`, DI4, and `X013` are supplementary control/indication paths.
They are not credited as independent safety outputs.

### 3.5 Delayed Outputs

The three delayed N.O. safety contacts establish the final safe state:

| Safety contact | Controlled circuit |
|---|---|
| 47-48 | Contactor A coil |
| 57-58 | VFD STO1 |
| 67-68 | VFD STO2 |

STO1 and STO2 remain separate channels. They are not paralleled on one relay
contact.

Rev J does not include a mechanical brake. No delayed safety output remains
spare.

### 3.6 Monitoring

| Signal | Source | Meaning |
|---|---|---|
| `X011` | Contactor A mechanically linked N.O. auxiliary | Final safety state proved OK after reset |
| `X013` | `CR-S2` from BH5928 immediate monitoring contact | Immediate safety trip active |

`X011` falls only after the delayed output opens Contactor A. The PLC uses it as
a run permissive and state-clear signal. `X013` reports the immediate trip
interval before `X011` falls.

No auto-restart is permitted. After an E-stop or power interruption, the safety
relay requires manual reset and the PLC sequence requires a fresh operator start
command.

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

Jog mode is a setup/inching mode entered by holding FWD for at least 5 seconds.
Entering jog mode never starts the spindle.

Required jog behavior:

| Condition | Required behavior |
|---|---|
| FWD held for at least 5 s while safe | Arm jog mode and consume that FWD press |
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

The machine-front green and red lamps are PLC outputs and are advisory. They do
not perform a safety function.

| State | Indication |
|---|---|
| Safe, no fault, not jogging | Green solid |
| Jog armed | Green blink |
| DB resistor over-temperature | Red blink |
| Safety trip or latched hard fault | Red solid |

Red solid has priority over red blink. Red blink has priority over green blink.
Green blink has priority over green solid.

The white power-on lamp is not a PLC output. It remains on whenever the
disconnect is closed and the 24 V bus is energized.

---

## 5. I/O Assignments

### 5.1 CLICK PLUS Hardware

Controller: **CLICK PLUS C2-01CPU-2** with two **C2-14D1** option modules.

The C2-14D1 input commons are configured for sinking inputs. Field contacts and
PNP sensors source 24 V into the input points. C2-14D1 outputs are sinking
outputs.

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
| `X011` | Final safety/KA OK | Contactor A mechanically linked N.O. auxiliary | 1 = Contactor A energized after safety reset |
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
| `Y006` | Red lamp | Machine-front red 24 V pilot | Solid safety/hard fault, blink DB over-temp |

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
| DI4 | Function 18, Force to Stop | Commanded by `CR-S1` on safety trip |
| Stop method `P00.22` | 0, ramp to stop | Loss of run command decelerates instead of coasting |
| Decel time 1 `P01.13` | 0.50 s initial | Normal stop ramp basis |
| Decel time 2 `P01.15` | 0.50 s initial | E-stop force-stop ramp basis |
| Decel S-curve `P01.26` / `P01.27` | 0.00 s / 0.00 s | Prevents hidden extension of stop time |
| EF/force-stop selection `P07.20` | 2 | DI4 function 18 uses decel time 2 |
| Braking chopper | Enabled | DB resistor absorbs decel/reversal energy |
| STO | STO1 and STO2 separate | Both opened after relay delay |
| Over-torque/stall detection | Enabled | Backstop for failed tap reversal/stop or jam |
| DI mode | NPN/sink internal-power mode | Compatible with CLICK sinking outputs and safety contacts |

DI function 28 is not used for E-stop because it removes drive output
immediately and produces a coast/free-run stop.

The braking resistor thermal switch is monitored at `X012`. Over-temperature
inhibits run and produces red blink indication until the thermal condition
clears.

---

*End of document - GoodBetterBestCo, Rev J, 2026-08-05.*
