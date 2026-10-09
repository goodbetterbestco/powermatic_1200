# Routing standards — 2026-10-08

The saved project now has six AWG width profiles and functional netclasses for
incoming mains, panel power, motor power, control, direction, speed and PE.
A separate DEVICE_INTERNAL class marks retained straps and direct-mounted
connections without assigning a conductor gauge. See
[WIRING_STANDARD.md](../../WIRING_STANDARD.md#kicad-route-widths-and-netclasses)
for the policy and routing instructions.

KiCad 10.0.7 natively resolved all 53 named nets: 43 have an AWG default and
10 fixed connections retain the Default drawing width. Thirteen nets have
different gauges on different physical wires; select the appropriate AWG preset
for those individual conductors. The six available presets are 0.643, 1.024,
1.290, 1.628, 2.052 and 2.588 mm.

The PCB Editor preference is 90 degree rounded, with free-angle mode disabled.
The project local settings disable width pickup from existing tracks and enable
netclass grouping in Net Inspector. These are saved preferences for the next
editor launch. The corner mode remains selectable through KiCad shortcuts.

Validation: native project loading and netclass resolution passed. Both the
96-footprint PCB and the schematic remain byte-for-byte identical to the
user-saved baseline. The 18 existing 0.2 mm track segments were preserved.
The project diff is limited to netclasses, assignment patterns and width presets;
existing user changes were retained.

The full assignment table, mixed-gauge declarations, native effective widths,
source hashes and preference-backup path are in [assignments.json](assignments.json).

| Net | Functional group | Default AWG | Default width (mm) | Declared AWGs |
|---|---|---:|---:|---|
| `+24V` | `CONTROL` | 18 | 1.024 | 18, 22 |
| `+24V_EN` | `CONTROL` | 18 | 1.024 | 18 |
| `/CONTROL_ESTOP_CONTACT_LINK` | `CONTROL` | 22 | 0.643 | 22 |
| `/CONTROL_K3_CONTACT_LINK` | `CONTROL` | 18 | 1.024 | 18 |
| `/DIRECTION_FWD_COIL` | `DIRECTION` | 18 | 1.024 | 18 |
| `/DIRECTION_REV_COIL` | `DIRECTION` | 18 | 1.024 | 18 |
| `/HS_SHORT` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L1_FUSED` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L1_HIGH` | `MOTOR_POWER` | — | — | fixed |
| `/L1_LOW` | `MOTOR_POWER` | — | — | fixed |
| `/L1_PSU` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L2_FUSED` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L2_HIGH` | `MOTOR_POWER` | — | — | fixed |
| `/L2_LOW` | `MOTOR_POWER` | — | — | fixed |
| `/L2_PSU` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L3_FUSED` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `/L3_HIGH` | `MOTOR_POWER` | — | — | fixed |
| `/L3_LOW` | `MOTOR_POWER` | — | — | fixed |
| `/SPEED_HIGH_SHORTING_COIL` | `SPEED` | 18 | 1.024 | 18 |
| `/SPEED_LOW_COIL` | `SPEED` | 18 | 1.024 | 18 |
| `0V` | `CONTROL` | 18 | 1.024 | 18 |
| `CONTROL_ESTOP_DISABLED_FB` | `CONTROL` | 18 | 1.024 | 18 |
| `CONTROL_ESTOP_ENABLE` | `CONTROL` | 18 | 1.024 | 18, 22 |
| `CONTROL_LOW_OVERLOAD_ENABLE` | `CONTROL` | 18 | 1.024 | 18 |
| `CONTROL_OVERLOAD_ENABLE` | `CONTROL` | 18 | 1.024 | 16, 18 |
| `CONTROL_RUN_ENABLE` | `CONTROL` | 18 | 1.024 | 16, 18 |
| `DIRECTION_ENABLE` | `DIRECTION` | 18 | 1.024 | 16, 18 |
| `DIRECTION_FWD_CMD` | `DIRECTION` | 18 | 1.024 | 16, 18 |
| `DIRECTION_REV_CMD` | `DIRECTION` | 18 | 1.024 | 16, 18 |
| `L1_DIR` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `L1_IN` | `INCOMING_MAINS` | 12 | 2.052 | 12, 14 |
| `L1_SW` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `L2_DIR` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `L2_IN` | `INCOMING_MAINS` | 12 | 2.052 | 12, 14 |
| `L2_SW` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `L3_DIR` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `L3_IN` | `INCOMING_MAINS` | 12 | 2.052 | 12, 14 |
| `L3_SW` | `PANEL_POWER` | 14 | 1.628 | 14 |
| `M1_T1` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `M1_T2` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `M1_T3` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `M1_T4` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `M1_T5` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `M1_T6` | `MOTOR_POWER` | 14 | 1.628 | 14 |
| `Net-(S3-HI3_B)` | `SPEED` | — | — | fixed |
| `Net-(S3-HI5_T)` | `SPEED` | — | — | fixed |
| `Net-(S3-HI6_T)` | `SPEED` | — | — | fixed |
| `Net-(S3-HI8_B)` | `SPEED` | — | — | fixed |
| `PE` | `PE` | 14 | 1.628 | 12, 14 |
| `SPEED_HIGH_CMD` | `SPEED` | 18 | 1.024 | 16, 18 |
| `SPEED_HIGH_COIL` | `SPEED` | 18 | 1.024 | 18 |
| `SPEED_LOW_CMD` | `SPEED` | 18 | 1.024 | 16, 18 |
| `SPEED_LOW_K6_NC_LINK` | `SPEED` | 18 | 1.024 | 18 |
