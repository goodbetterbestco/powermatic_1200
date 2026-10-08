# Pin termination draft

One custom `Termination.<pin>` field is stored on each physical schematic symbol.
Descriptions come from existing records, using the current conductor AWG.
Recorded TBD lengths and dimensions remain unchanged for review.

Fields: **184** on **25** symbols.

## Description inventory

| Description | Pin fields |
|---|---:|
| Factory pigtail, 22 AWG (retained) | 4 |
| Ferrule 14 AWG; L=TBD mm | 48 |
| Ferrule 18 AWG; L=TBD mm | 53 |
| M12 mating contact (retained) | 4 |
| N/A — direct-mounted connection | 12 |
| N/A — unused pin | 12 |
| Plug clamp, 12 AWG | 4 |
| Retained jumper | 14 |
| Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm | 8 |
| Supplied assembly connection (retained) | 4 |
| Supplied fork-ended lead (retained) | 10 |
| Twin ferrule 2 × 14 AWG; L=TBD mm | 1 |
| Twin ferrule 2 × 18 AWG; L=TBD mm | 3 |
| Wire-splice connector, 12 AWG | 1 |
| Wire-splice connector, 14 AWG | 6 |

These are pin-field counts, not purchasing quantities. Internally common pins,
retained/supplied connections and unused pins are included in the field inventory.
PCB-only terminal blocks and enclosure studs have no schematic symbols and are
outside this symbol-field population. No terminal allocation or wire route is inferred.

## All pin fields

| Component | Pin | Field | Termination |
|---|---|---|---|
| FH1 | P1.A | `Termination.P1.A` | Ferrule 14 AWG; L=TBD mm |
| FH1 | P1.B | `Termination.P1.B` | Ferrule 14 AWG; L=TBD mm |
| FH1 | P2.A | `Termination.P2.A` | Ferrule 14 AWG; L=TBD mm |
| FH1 | P2.B | `Termination.P2.B` | Ferrule 14 AWG; L=TBD mm |
| FH1 | P3.A | `Termination.P3.A` | Ferrule 14 AWG; L=TBD mm |
| FH1 | P3.B | `Termination.P3.B` | Ferrule 14 AWG; L=TBD mm |
| H1 | X1 | `Termination.X1` | Ferrule 18 AWG; L=TBD mm |
| H1 | X2 | `Termination.X2` | Ferrule 18 AWG; L=TBD mm |
| J1 | 1 | `Termination.1` | Factory pigtail, 22 AWG (retained) |
| J1 | 2 | `Termination.2` | Factory pigtail, 22 AWG (retained) |
| J1 | 3 | `Termination.3` | Factory pigtail, 22 AWG (retained) |
| J1 | 4 | `Termination.4` | Factory pigtail, 22 AWG (retained) |
| J2 | G | `Termination.G` | Plug clamp, 12 AWG |
| J2 | X | `Termination.X` | Plug clamp, 12 AWG |
| J2 | Y | `Termination.Y` | Plug clamp, 12 AWG |
| J2 | Z | `Termination.Z` | Plug clamp, 12 AWG |
| J6 | 1 | `Termination.1` | M12 mating contact (retained) |
| J6 | 2 | `Termination.2` | M12 mating contact (retained) |
| J6 | 3 | `Termination.3` | M12 mating contact (retained) |
| J6 | 4 | `Termination.4` | M12 mating contact (retained) |
| K1 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| K1 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| K1 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| K1 | 31 | `Termination.31` | Ferrule 18 AWG; L=TBD mm |
| K1 | 32 | `Termination.32` | Ferrule 18 AWG; L=TBD mm |
| K1 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| K1 | 43 | `Termination.43` | Ferrule 18 AWG; L=TBD mm |
| K1 | 44 | `Termination.44` | Twin ferrule 2 × 18 AWG; L=TBD mm |
| K1 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| K1 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
| K1 | A1.BOT | `Termination.A1.BOT` | Ferrule 18 AWG; L=TBD mm |
| K1 | A1.TOP | `Termination.A1.TOP` | Ferrule 18 AWG; L=TBD mm |
| K1 | A2.BOT | `Termination.A2.BOT` | Ferrule 18 AWG; L=TBD mm |
| K1 | A2.TOP | `Termination.A2.TOP` | Ferrule 18 AWG; L=TBD mm |
| K2 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| K2 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| K2 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| K2 | 31 | `Termination.31` | Ferrule 18 AWG; L=TBD mm |
| K2 | 32 | `Termination.32` | Ferrule 18 AWG; L=TBD mm |
| K2 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| K2 | 43 | `Termination.43` | Ferrule 18 AWG; L=TBD mm |
| K2 | 44 | `Termination.44` | Twin ferrule 2 × 18 AWG; L=TBD mm |
| K2 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| K2 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
| K2 | A1.BOT | `Termination.A1.BOT` | Ferrule 18 AWG; L=TBD mm |
| K2 | A1.TOP | `Termination.A1.TOP` | Ferrule 18 AWG; L=TBD mm |
| K2 | A2.BOT | `Termination.A2.BOT` | Ferrule 18 AWG; L=TBD mm |
| K2 | A2.TOP | `Termination.A2.TOP` | Ferrule 18 AWG; L=TBD mm |
| K3 | 13 | `Termination.13` | Ferrule 18 AWG; L=TBD mm |
| K3 | 14 | `Termination.14` | Ferrule 18 AWG; L=TBD mm |
| K3 | 23 | `Termination.23` | Ferrule 18 AWG; L=TBD mm |
| K3 | 24 | `Termination.24` | Ferrule 18 AWG; L=TBD mm |
| K3 | 31 | `Termination.31` | N/A — unused pin |
| K3 | 32 | `Termination.32` | N/A — unused pin |
| K3 | 41 | `Termination.41` | N/A — unused pin |
| K3 | 42 | `Termination.42` | N/A — unused pin |
| K3 | A1+ | `Termination.A1+` | Ferrule 18 AWG; L=TBD mm |
| K3 | A2 | `Termination.A2` | Ferrule 18 AWG; L=TBD mm |
| K4 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| K4 | 2 | `Termination.2` | N/A — direct-mounted connection |
| K4 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| K4 | 31 | `Termination.31` | Ferrule 18 AWG; L=TBD mm |
| K4 | 32 | `Termination.32` | Ferrule 18 AWG; L=TBD mm |
| K4 | 4 | `Termination.4` | N/A — direct-mounted connection |
| K4 | 43 | `Termination.43` | Ferrule 18 AWG; L=TBD mm |
| K4 | 44 | `Termination.44` | Ferrule 18 AWG; L=TBD mm |
| K4 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| K4 | 6 | `Termination.6` | N/A — direct-mounted connection |
| K4 | A1.BOT | `Termination.A1.BOT` | Ferrule 18 AWG; L=TBD mm |
| K4 | A1.TOP | `Termination.A1.TOP` | Ferrule 18 AWG; L=TBD mm |
| K4 | A2.BOT | `Termination.A2.BOT` | Ferrule 18 AWG; L=TBD mm |
| K4 | A2.TOP | `Termination.A2.TOP` | Ferrule 18 AWG; L=TBD mm |
| K5 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| K5 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| K5 | 3 | `Termination.3` | Twin ferrule 2 × 14 AWG; L=TBD mm |
| K5 | 31 | `Termination.31` | Ferrule 18 AWG; L=TBD mm |
| K5 | 32 | `Termination.32` | Ferrule 18 AWG; L=TBD mm |
| K5 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| K5 | 43 | `Termination.43` | Twin ferrule 2 × 18 AWG; L=TBD mm |
| K5 | 44 | `Termination.44` | Ferrule 18 AWG; L=TBD mm |
| K5 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| K5 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
| K5 | A1.BOT | `Termination.A1.BOT` | Ferrule 18 AWG; L=TBD mm |
| K5 | A1.TOP | `Termination.A1.TOP` | Ferrule 18 AWG; L=TBD mm |
| K5 | A2.BOT | `Termination.A2.BOT` | Ferrule 18 AWG; L=TBD mm |
| K5 | A2.TOP | `Termination.A2.TOP` | Ferrule 18 AWG; L=TBD mm |
| K6 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| K6 | 2 | `Termination.2` | N/A — direct-mounted connection |
| K6 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| K6 | 31 | `Termination.31` | Ferrule 18 AWG; L=TBD mm |
| K6 | 32 | `Termination.32` | Ferrule 18 AWG; L=TBD mm |
| K6 | 4 | `Termination.4` | N/A — direct-mounted connection |
| K6 | 43 | `Termination.43` | Ferrule 18 AWG; L=TBD mm |
| K6 | 44 | `Termination.44` | Ferrule 18 AWG; L=TBD mm |
| K6 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| K6 | 6 | `Termination.6` | N/A — direct-mounted connection |
| K6 | A1.BOT | `Termination.A1.BOT` | Ferrule 18 AWG; L=TBD mm |
| K6 | A1.TOP | `Termination.A1.TOP` | Ferrule 18 AWG; L=TBD mm |
| K6 | A2.BOT | `Termination.A2.BOT` | Ferrule 18 AWG; L=TBD mm |
| K6 | A2.TOP | `Termination.A2.TOP` | Ferrule 18 AWG; L=TBD mm |
| M1 | PE | `Termination.PE` | Wire-splice connector, 12 AWG |
| M1 | T1 | `Termination.T1` | Wire-splice connector, 14 AWG |
| M1 | T2 | `Termination.T2` | Wire-splice connector, 14 AWG |
| M1 | T3 | `Termination.T3` | Wire-splice connector, 14 AWG |
| M1 | T4 | `Termination.T4` | Wire-splice connector, 14 AWG |
| M1 | T5 | `Termination.T5` | Wire-splice connector, 14 AWG |
| M1 | T6 | `Termination.T6` | Wire-splice connector, 14 AWG |
| OL4 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| OL4 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| OL4 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
| OL4 | 95 | `Termination.95` | Ferrule 18 AWG; L=TBD mm |
| OL4 | 96 | `Termination.96` | Ferrule 18 AWG; L=TBD mm |
| OL4 | 97 | `Termination.97` | N/A — unused pin |
| OL4 | 98 | `Termination.98` | N/A — unused pin |
| OL4 | IN1 | `Termination.IN1` | N/A — direct-mounted connection |
| OL4 | IN2 | `Termination.IN2` | N/A — direct-mounted connection |
| OL4 | IN3 | `Termination.IN3` | N/A — direct-mounted connection |
| OL6 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| OL6 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| OL6 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
| OL6 | 95 | `Termination.95` | Ferrule 18 AWG; L=TBD mm |
| OL6 | 96 | `Termination.96` | Ferrule 18 AWG; L=TBD mm |
| OL6 | 97 | `Termination.97` | N/A — unused pin |
| OL6 | 98 | `Termination.98` | N/A — unused pin |
| OL6 | IN1 | `Termination.IN1` | N/A — direct-mounted connection |
| OL6 | IN2 | `Termination.IN2` | N/A — direct-mounted connection |
| OL6 | IN3 | `Termination.IN3` | N/A — direct-mounted connection |
| PS1 | 1_BOT | `Termination.1_BOT` | Ferrule 14 AWG; L=TBD mm |
| PS1 | 1_TOP | `Termination.1_TOP` | Ferrule 18 AWG; L=TBD mm |
| PS1 | 2_BOT | `Termination.2_BOT` | Ferrule 14 AWG; L=TBD mm |
| PS1 | 2_TOP | `Termination.2_TOP` | Ferrule 18 AWG; L=TBD mm |
| PS1 | 3_BOT | `Termination.3_BOT` | Ferrule 14 AWG; L=TBD mm |
| PS1 | 3_TOP | `Termination.3_TOP` | Ferrule 18 AWG; L=TBD mm |
| PS1 | 4_TOP | `Termination.4_TOP` | Ferrule 18 AWG; L=TBD mm |
| Q1 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| Q1 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| Q1 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| Q1 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| S1 | 1 | `Termination.1` | Supplied assembly connection (retained) |
| S1 | 2 | `Termination.2` | Supplied assembly connection (retained) |
| S1 | 3 | `Termination.3` | Supplied assembly connection (retained) |
| S1 | 4 | `Termination.4` | Supplied assembly connection (retained) |
| S2 | L1 | `Termination.L1` | N/A — unused pin |
| S2 | L2 | `Termination.L2` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S2 | L3 | `Termination.L3` | N/A — unused pin |
| S2 | L4 | `Termination.L4` | Retained jumper |
| S2 | L5 | `Termination.L5` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S2 | R1 | `Termination.R1` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S2 | R2 | `Termination.R2` | Retained jumper |
| S2 | R3 | `Termination.R3` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S2 | R4 | `Termination.R4` | Retained jumper |
| S2 | R5 | `Termination.R5` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S3 | 1.L | `Termination.1.L` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S3 | 1.U | `Termination.1.U` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S3 | 2.L | `Termination.2.L` | Retained jumper |
| S3 | 2.U | `Termination.2.U` | Ring terminal, 16 AWG; stud=#8-32; OD<=9 mm |
| S3 | 3.L | `Termination.3.L` | Retained jumper |
| S3 | 3.U | `Termination.3.U` | Retained jumper |
| S3 | 4.L | `Termination.4.L` | Retained jumper |
| S3 | 4.U | `Termination.4.U` | Retained jumper |
| S3 | 5.L | `Termination.5.L` | Retained jumper |
| S3 | 5.U | `Termination.5.U` | Retained jumper |
| S3 | 6.L | `Termination.6.L` | N/A — unused pin |
| S3 | 6.U | `Termination.6.U` | Retained jumper |
| S3 | 7.L | `Termination.7.L` | Retained jumper |
| S3 | 7.U | `Termination.7.U` | Retained jumper |
| S3 | 8.L | `Termination.8.L` | Retained jumper |
| S3 | 8.U | `Termination.8.U` | N/A — unused pin |
| SP1 | 1 | `Termination.1` | Supplied fork-ended lead (retained) |
| SP1 | 2 | `Termination.2` | Supplied fork-ended lead (retained) |
| SP2 | 1 | `Termination.1` | Supplied fork-ended lead (retained) |
| SP2 | 2 | `Termination.2` | Supplied fork-ended lead (retained) |
| SP4 | 1 | `Termination.1` | Supplied fork-ended lead (retained) |
| SP4 | 2 | `Termination.2` | Supplied fork-ended lead (retained) |
| SP5 | 1 | `Termination.1` | Supplied fork-ended lead (retained) |
| SP5 | 2 | `Termination.2` | Supplied fork-ended lead (retained) |
| SP6 | 1 | `Termination.1` | Supplied fork-ended lead (retained) |
| SP6 | 2 | `Termination.2` | Supplied fork-ended lead (retained) |
| SW1 | 1 | `Termination.1` | Ferrule 14 AWG; L=TBD mm |
| SW1 | 2 | `Termination.2` | Ferrule 14 AWG; L=TBD mm |
| SW1 | 3 | `Termination.3` | Ferrule 14 AWG; L=TBD mm |
| SW1 | 4 | `Termination.4` | Ferrule 14 AWG; L=TBD mm |
| SW1 | 5 | `Termination.5` | Ferrule 14 AWG; L=TBD mm |
| SW1 | 6 | `Termination.6` | Ferrule 14 AWG; L=TBD mm |
