# Generated wire schedule

This is a generated section review. Wire records in the saved schematic are authoritative.
Only recorded assembly wires are included; unrecorded sections are not inferred from global net names.

Assembly wires: **6**. Full-schematic coverage: **partial**.

## Sections

| Section | Wires |
|---|---:|
| 01 Incoming phases | 6 |

## Current review

| ID | From | To | AWG | Cut estimate, mm | Route, mm | State |
|---|---|---|---:|---:|---:|---|
| W001 | J2.X | TB40.BOT | 12 | 450 | 216.781 | pending |
| W002 | TB40.TOP | FH1.P1.A | 14 | 1200 | 999.938 | pending |
| W003 | J2.Y | TB41.BOT | 12 | 450 | 224.321 | pending |
| W004 | TB41.TOP | FH1.P2.A | 14 | 1200 | 970.426 | pending |
| W005 | J2.Z | TB42.BOT | 12 | 450 | 231.861 | pending |
| W006 | TB42.TOP | FH1.P3.A | 14 | 1150 | 940.913 | pending |

Panel-cable-core lengths cover the panel tail only. Overall external cable allowances remain in the project BOM.
Automatic lengths use modeled duct routing, a cut allowance and rounding; they are estimates for review.

## Coverage

| Net | Physical connection records complete |
|---|---|
| +24V | Not yet recorded |
| +24V_CTRL | Not yet recorded |
| +24V_EN | Not yet recorded |
| +24V_RUN | Not yet recorded |
| /L1_FUSED | Not yet recorded |
| /L1_PSU | Not yet recorded |
| /L2_FUSED | Not yet recorded |
| /L2_PSU | Not yet recorded |
| /L3_FUSED | Not yet recorded |
| 0V | Not yet recorded |
| ESTOP_ENABLE | Not yet recorded |
| FWD_CMD | Not yet recorded |
| HIGH_CMD | Not yet recorded |
| HS_SHORT | Not yet recorded |
| L1_DIR | Not yet recorded |
| L1_IN | Yes |
| L1_SW | Not yet recorded |
| L2_DIR | Not yet recorded |
| L2_IN | Yes |
| L2_SW | Not yet recorded |
| L3_DIR | Not yet recorded |
| L3_IN | Yes |
| L3_SW | Not yet recorded |
| LOW_CMD | Not yet recorded |
| M1_T1 | Not yet recorded |
| M1_T2 | Not yet recorded |
| M1_T3 | Not yet recorded |
| M1_T4 | Not yet recorded |
| M1_T5 | Not yet recorded |
| M1_T6 | Not yet recorded |
| Net-(J1-Pad2) | Not yet recorded |
| Net-(K1A-A1_BOT) | Not yet recorded |
| Net-(K1A-AUX_NC_2) | Not yet recorded |
| Net-(K3-NO1-Pad14) | Not yet recorded |
| Net-(K4A-A1_BOT) | Not yet recorded |
| Net-(K4A-AUX_NC_2) | Not yet recorded |
| Net-(K4B-T1) | Not yet recorded |
| Net-(K4B-T2) | Not yet recorded |
| Net-(K4B-T3) | Not yet recorded |
| Net-(K5A-AUX_NC_1) | Not yet recorded |
| Net-(K5A-AUX_NO_2) | Not yet recorded |
| Net-(K6B-T1) | Not yet recorded |
| Net-(K6B-T2) | Not yet recorded |
| Net-(K6B-T3) | Not yet recorded |
| Net-(OL1B-TRIP_NC_2) | Not yet recorded |
| Net-(S2A-FWD_NC_2) | Not yet recorded |
| Net-(S3-HI3_L) | Not yet recorded |
| Net-(S3-HI5_U) | Not yet recorded |
| Net-(S3-HI6_U) | Not yet recorded |
| Net-(S3-HI8_L) | Not yet recorded |
| PE | Not yet recorded |
| REV_CMD | Not yet recorded |
| STOP_CHAIN | Not yet recorded |

Edit schematic wire records with `tools/wiring/records.py`, then regenerate. The generated CSV is a read-only review.
