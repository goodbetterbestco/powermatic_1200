# Schematic connection sizing

Sizes are custom Wire.Sizes symbol fields in the schematic. These declarations
classify connected terminals; they do not choose physical terminal routes,
create jumpers between internally common pins or define cut lengths.

Connected terminals classified: 172/172.
Connection sizing complete: True.
Physical conductor schedule and terminal allocation remain pending.

| Terminal | Net | Scope | AWG | Color |
|---|---|---|---|---|
| FH1.P1.A | L1_IN | panel_power | 14 | Black |
| FH1.P1.B | /L1_FUSED | panel_power | 14 | Black |
| FH1.P2.A | L2_IN | panel_power | 14 | Black |
| FH1.P2.B | /L2_FUSED | panel_power | 14 | Black |
| FH1.P3.A | L3_IN | panel_power | 14 | Black |
| FH1.P3.B | /L3_FUSED | panel_power | 14 | Black |
| H1.X1 | +24V | panel_control | 18 | Blue |
| H1.X2 | 0V | panel_control | 18 | Blue |
| J1.1 | +24V | factory_pigtail | 22 | Brown |
| J1.2 | /ESTOP_JUMPER | factory_pigtail | 22 | White |
| J1.3 | /ESTOP_JUMPER | factory_pigtail | 22 | Blue |
| J1.4 | ESTOP_ENABLE | factory_pigtail | 22 | Black |
| J2.G | PE | incoming_cable | 12 |  |
| J2.X | L1_IN | incoming_cable | 12 |  |
| J2.Y | L2_IN | incoming_cable | 12 |  |
| J2.Z | L3_IN | incoming_cable | 12 |  |
| J6.1 | +24V | connector_interface | — |  |
| J6.2 | /ESTOP_JUMPER | connector_interface | — |  |
| J6.3 | /ESTOP_JUMPER | connector_interface | — |  |
| J6.4 | ESTOP_ENABLE | connector_interface | — |  |
| K1.1 | L1_SW | panel_power | 14 | Black |
| K1.2 | L1_DIR | panel_power | 14 | Black |
| K1.3 | L2_SW | panel_power | 14 | Black |
| K1.31 | REV_CMD | panel_control | 18 | Blue |
| K1.32 | /REV_COIL | panel_control | 18 | Blue |
| K1.4 | L2_DIR | panel_power | 14 | Black |
| K1.43 | SPEED_SET | panel_control | 18 | Blue |
| K1.44 | FWD_CMD | panel_control | 18 | Blue |
| K1.5 | L3_SW | panel_power | 14 | Black |
| K1.6 | L3_DIR | panel_power | 14 | Black |
| K1.A1.BOT | /FWD_COIL | panel_control | 18 | Blue |
| K1.A1.TOP | /FWD_COIL | panel_control | 18 | Blue |
| K1.A2.BOT | 0V | panel_control | 18 | Blue |
| K1.A2.TOP | 0V | panel_control | 18 | Blue |
| K2.1 | L1_SW | panel_power | 14 | Black |
| K2.2 | L3_DIR | panel_power | 14 | Black |
| K2.3 | L2_SW | panel_power | 14 | Black |
| K2.31 | FWD_CMD | panel_control | 18 | Blue |
| K2.32 | /FWD_COIL | panel_control | 18 | Blue |
| K2.4 | L2_DIR | panel_power | 14 | Black |
| K2.43 | SPEED_SET | panel_control | 18 | Blue |
| K2.44 | REV_CMD | panel_control | 18 | Blue |
| K2.5 | L3_SW | panel_power | 14 | Black |
| K2.6 | L1_DIR | panel_power | 14 | Black |
| K2.A1.BOT | /REV_COIL | panel_control | 18 | Blue |
| K2.A1.TOP | /REV_COIL | panel_control | 18 | Blue |
| K2.A2.BOT | 0V | panel_control | 18 | Blue |
| K2.A2.TOP | 0V | panel_control | 18 | Blue |
| K3.13 | +24V | panel_control | 18 | Blue |
| K3.14 | /K3_JUMPER | panel_control | 18 | Blue |
| K3.23 | /K3_JUMPER | panel_control | 18 | Blue |
| K3.24 | +24V_EN | panel_control | 18 | Blue |
| K3.A1+ | ESTOP_ENABLE | panel_control | 18 | Blue |
| K3.A2 | 0V | panel_control | 18 | Blue |
| K4.1 | L1_DIR | panel_power | 14 | Black |
| K4.2 | /L1_LOW | direct_mount | — |  |
| K4.3 | L2_DIR | panel_power | 14 | Black |
| K4.31 | HIGH_CMD | panel_control | 18 | Blue |
| K4.32 | /HS_COIL | panel_control | 18 | Blue |
| K4.4 | /L2_LOW | direct_mount | — |  |
| K4.43 | STOP_RELEASED | panel_control | 18 | Blue |
| K4.44 | SPEED_SET | panel_control | 18 | Blue |
| K4.5 | L3_DIR | panel_power | 14 | Black |
| K4.6 | /L3_LOW | direct_mount | — |  |
| K4.A1.BOT | /LOW_COIL | panel_control | 18 | Blue |
| K4.A1.TOP | /LOW_COIL | panel_control | 18 | Blue |
| K4.A2.BOT | 0V | panel_control | 18 | Blue |
| K4.A2.TOP | 0V | panel_control | 18 | Blue |
| K5.1 | /HS_SHORT | panel_power | 14 | Black |
| K5.2 | M1_T1 | panel_power | 14 | Black |
| K5.3 | /HS_SHORT | panel_power | 14 | Black |
| K5.31 | LOW_K6_OK | panel_control | 18 | Blue |
| K5.32 | /LOW_COIL | panel_control | 18 | Blue |
| K5.4 | M1_T2 | panel_power | 14 | Black |
| K5.43 | /HS_COIL | panel_control | 18 | Blue |
| K5.44 | HIGH_COIL | panel_control | 18 | Blue |
| K5.5 | /HS_SHORT | panel_power | 14 | Black |
| K5.6 | M1_T3 | panel_power | 14 | Black |
| K5.A1.BOT | /HS_COIL | panel_control | 18 | Blue |
| K5.A1.TOP | /HS_COIL | panel_control | 18 | Blue |
| K5.A2.BOT | 0V | panel_control | 18 | Blue |
| K5.A2.TOP | 0V | panel_control | 18 | Blue |
| K6.1 | L1_DIR | panel_power | 14 | Black |
| K6.2 | /L1_HIGH | direct_mount | — |  |
| K6.3 | L2_DIR | panel_power | 14 | Black |
| K6.31 | LOW_CMD | panel_control | 18 | Blue |
| K6.32 | LOW_K6_OK | panel_control | 18 | Blue |
| K6.4 | /L2_HIGH | direct_mount | — |  |
| K6.43 | STOP_RELEASED | panel_control | 18 | Blue |
| K6.44 | SPEED_SET | panel_control | 18 | Blue |
| K6.5 | L3_DIR | panel_power | 14 | Black |
| K6.6 | /L3_HIGH | direct_mount | — |  |
| K6.A1.BOT | HIGH_COIL | panel_control | 18 | Blue |
| K6.A1.TOP | HIGH_COIL | panel_control | 18 | Blue |
| K6.A2.BOT | 0V | panel_control | 18 | Blue |
| K6.A2.TOP | 0V | panel_control | 18 | Blue |
| M1.PE | PE | motor_conduit | 12 | Green/Yellow |
| M1.T1 | M1_T1 | motor_conduit | 14 | Black |
| M1.T2 | M1_T2 | motor_conduit | 14 | Black |
| M1.T3 | M1_T3 | motor_conduit | 14 | Black |
| M1.T4 | M1_T4 | motor_conduit | 14 | Black |
| M1.T5 | M1_T5 | motor_conduit | 14 | Black |
| M1.T6 | M1_T6 | motor_conduit | 14 | Black |
| OL4.2 | M1_T1 | panel_power | 14 | Black |
| OL4.4 | M1_T2 | panel_power | 14 | Black |
| OL4.6 | M1_T3 | panel_power | 14 | Black |
| OL4.95 | +24V_EN | panel_control | 18 | Blue |
| OL4.96 | OL4_OK | panel_control | 18 | Blue |
| OL4.IN1 | /L1_LOW | direct_mount | — |  |
| OL4.IN2 | /L2_LOW | direct_mount | — |  |
| OL4.IN3 | /L3_LOW | direct_mount | — |  |
| OL6.2 | M1_T4 | panel_power | 14 | Black |
| OL6.4 | M1_T5 | panel_power | 14 | Black |
| OL6.6 | M1_T6 | panel_power | 14 | Black |
| OL6.95 | OL4_OK | panel_control | 18 | Blue |
| OL6.96 | OVERLOAD_OK | panel_control | 18 | Blue |
| OL6.IN1 | /L1_HIGH | direct_mount | — |  |
| OL6.IN2 | /L2_HIGH | direct_mount | — |  |
| OL6.IN3 | /L3_HIGH | direct_mount | — |  |
| PS1.1_BOT | PE | panel_pe | 14 | Green/Yellow |
| PS1.1_TOP | 0V | panel_control | 18 | Blue |
| PS1.2_BOT | /L2_PSU | panel_power | 14 | Black |
| PS1.2_TOP | 0V | panel_control | 18 | Blue |
| PS1.3_BOT | /L1_PSU | panel_power | 14 | Black |
| PS1.3_TOP | +24V | panel_control | 18 | Blue |
| PS1.4_TOP | +24V | panel_control | 18 | Blue |
| Q1.1 | L1_SW | panel_power | 14 | Black |
| Q1.2 | /L1_PSU | panel_power | 14 | Black |
| Q1.3 | L2_SW | panel_power | 14 | Black |
| Q1.4 | /L2_PSU | panel_power | 14 | Black |
| S1.1 | +24V | estop_assembly | — |  |
| S1.2 | /ESTOP_JUMPER | estop_assembly | — |  |
| S1.3 | /ESTOP_JUMPER | estop_assembly | — |  |
| S1.4 | ESTOP_ENABLE | estop_assembly | — |  |
| S2.L2 | SPEED_SET | controls_conduit | 16 | Blue |
| S2.L4 | SPEED_SET | retained_link | — |  |
| S2.L5 | STOP_RELEASED | controls_conduit | 16 | Blue |
| S2.R1 | FWD_CMD | controls_conduit | 16 | Blue |
| S2.R2 | Net-(S2-FWD_NC_2) | retained_link | — |  |
| S2.R3 | REV_CMD | controls_conduit | 16 | Blue |
| S2.R4 | Net-(S2-FWD_NC_2) | retained_link | — |  |
| S2.R5 | OVERLOAD_OK | controls_conduit | 16 | Blue |
| S3.1.L | STOP_RELEASED | controls_conduit | 16 | Blue |
| S3.1.U | LOW_CMD | controls_conduit | 16 | Blue |
| S3.2.L | STOP_RELEASED | retained_link | — |  |
| S3.2.U | HIGH_CMD | controls_conduit | 16 | Blue |
| S3.3.L | Net-(S3-HI3_L) | retained_link | — |  |
| S3.3.U | LOW_CMD | retained_link | — |  |
| S3.4.L | Net-(S3-HI3_L) | retained_link | — |  |
| S3.4.U | Net-(S3-HI6_U) | retained_link | — |  |
| S3.5.L | Net-(S3-HI3_L) | retained_link | — |  |
| S3.5.U | Net-(S3-HI5_U) | retained_link | — |  |
| S3.6.U | Net-(S3-HI6_U) | retained_link | — |  |
| S3.7.L | Net-(S3-HI8_L) | retained_link | — |  |
| S3.7.U | Net-(S3-HI5_U) | retained_link | — |  |
| S3.8.L | Net-(S3-HI8_L) | retained_link | — |  |
| SP1.1 | /FWD_COIL | suppressor_lead | — |  |
| SP1.2 | 0V | suppressor_lead | — |  |
| SP2.1 | /REV_COIL | suppressor_lead | — |  |
| SP2.2 | 0V | suppressor_lead | — |  |
| SP4.1 | /LOW_COIL | suppressor_lead | — |  |
| SP4.2 | 0V | suppressor_lead | — |  |
| SP5.1 | /HS_COIL | suppressor_lead | — |  |
| SP5.2 | 0V | suppressor_lead | — |  |
| SP6.1 | HIGH_COIL | suppressor_lead | — |  |
| SP6.2 | 0V | suppressor_lead | — |  |
| SW1.1 | /L1_FUSED | panel_power | 14 | Black |
| SW1.2 | L1_SW | panel_power | 14 | Black |
| SW1.3 | /L2_FUSED | panel_power | 14 | Black |
| SW1.4 | L2_SW | panel_power | 14 | Black |
| SW1.5 | /L3_FUSED | panel_power | 14 | Black |
| SW1.6 | L3_SW | panel_power | 14 | Black |

## Planned PE conductors

| Plan | AWG | Status |
|---|---|---|
| enclosure-door-bond | 10 | proposed |
| motor-body-bond | 10 | proposed |
| machine-frame-bond | 10 | proposed |

The existing Wire.Wxxx physical-wire records still require reconciliation
with the PCB-only terminal model. Fixed lead sizes and conductor protection
must be checked against the actual component and installation.
