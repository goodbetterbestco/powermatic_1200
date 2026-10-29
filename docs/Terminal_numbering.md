# Terminal numbering

Approved 2026-10-28. This is the current installed-label scheme for all 63 terminal blocks.

The module number identifies one physically separate terminal strip. Module numbers run top to bottom, then left to right. Letters run left to right within each strip and restart at A. Uppercase I and O are skipped. Ground blocks use G1-G6 in the same physical reading order and do not consume letters.

| Module | Location | Labels | Gray blocks |
| --- | --- | --- | --- |
| 1 | Upper rail, right of K1/K2 | 1A-1Z, skipping I/O | 24 |
| 2 | Middle rail, left of K6 | 2A-2F | 6 |
| 3 | Middle rail, right of TD1/TD2 | 3A-3K, skipping I | 10 |
| 4 | Lower left 4A-4D; incoming 4E-4G relocated to lower right | 4A-4G | 7 |
| 5 | Lower rail, right of PS1 | 5A-5K, skipping I | 10 |

Grounds: upper G1/G2, middle G3, lower-right G5/G6 and relocated G4. The physical left-to-right order at the lower right ends with 4E, 4F, 4G, G4.

Relocation exception, 2026-10-29: the owner requested retaining 4E/4F/4G/G4 when moving them to the lower right. Module 4 is therefore split across the two lower strips, and G4 no longer follows ground-number reading order. All existing terminal labels remain valid.

The module number identifies physical location, not electrical commonality. Jumper sections remain independently defined in the jumper guide. In particular, 4E/4F/4G are three separate incoming phase circuits.

Wire-schedule endpoint labels use the new reference followed by the existing clamp identifier, such as `1A_TOP`, `2F_BOT`, or `G1_2`. Pad numbers and electrical connections are unchanged.

## Current labels and legacy cross-reference

Legacy TB labels are retained in this table only for migration. Current design references, guides, and wire schedules use the new labels.

| Rail | Module | Current label | Previous label | Circuit |
| --- | --- | --- | --- | --- |
| Upper | 1 | 1A | TB60 | M1_T1 |
| Upper | 1 | 1B | TB61 | M1_T1 |
| Upper | 1 | 1C | TB63 | M1_T2 |
| Upper | 1 | 1D | TB64 | M1_T2 |
| Upper | 1 | 1E | TB66 | M1_T3 |
| Upper | 1 | 1F | TB67 | M1_T3 |
| Upper | 1 | 1G | TB31 | M1_T4 |
| Upper | 1 | 1H | TB69 | M1_T5 |
| Upper | 1 | 1J | TB72 | M1_T6 |
| Upper | Ground | G1 | TB51 | PE |
| Upper | Ground | G2 | TB52 | PE |
| Upper | 1 | 1K | TB20 | DIRECTION_ENABLE |
| Upper | 1 | 1L | TB21 | DIRECTION_ENABLE |
| Upper | 1 | 1M | TB22 | DIRECTION_ENABLE |
| Upper | 1 | 1N | TB73 | DIRECTION_FWD_CMD |
| Upper | 1 | 1P | TB74 | DIRECTION_FWD_CMD |
| Upper | 1 | 1Q | TB75 | DIRECTION_REV_CMD |
| Upper | 1 | 1R | TB76 | DIRECTION_REV_CMD |
| Upper | 1 | 1S | TB77 | CONTROL_RUN_ENABLE |
| Upper | 1 | 1T | TB78 | CONTROL_RUN_ENABLE |
| Upper | 1 | 1U | TB62 | SPEED_HIGH_CMD |
| Upper | 1 | 1V | TB65 | SPEED_LOW_CMD |
| Upper | 1 | 1W | TB68 | CONTROL_OVERLOAD_ENABLE |
| Upper | 1 | 1X | TB84 | SPEED_LOW_TIMED_ENABLE |
| Upper | 1 | 1Y | TB85 | HIGH_SEQUENCE_ENABLE |
| Upper | 1 | 1Z | TB86 | HIGH_SEQUENCE_TRIGGER |
| Middle | 2 | 2A | TB10 | 0V |
| Middle | 2 | 2B | TB11 | 0V |
| Middle | 2 | 2C | TB12 | 0V |
| Middle | 2 | 2D | TB13 | 0V |
| Middle | 2 | 2E | TB14 | 0V |
| Middle | 2 | 2F | TB87 | 0V |
| Middle | 3 | 3A | TB88 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3B | TB89 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3C | TB90 | CONTROL_RUN_ENABLE |
| Middle | 3 | 3D | TB91 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3E | TB92 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3F | TB93 | HIGH_SEQUENCE_ENABLE |
| Middle | 3 | 3G | TB94 | HIGH_SEQUENCE_TRIGGER |
| Middle | 3 | 3H | TB95 | HIGH_SEQUENCE_TRIGGER |
| Middle | 3 | 3J | TB96 | LOW_SEQUENCE_ENABLE |
| Middle | 3 | 3K | TB97 | LOW_SEQUENCE_ENABLE |
| Middle | Ground | G3 | TB98 | PE |
| Lower | 4 | 4A | TB83 | CONTROL_ESTOP_CONTACT_LINK |
| Lower | 4 | 4B | TB1 | +24V |
| Lower | 4 | 4C | TB2 | +24V |
| Lower | 4 | 4D | TB3 | +24V |
| Lower | 4 | 4E | TB79 | L1_IN |
| Lower | 4 | 4F | TB80 | L2_IN |
| Lower | 4 | 4G | TB81 | L3_IN |
| Lower | Ground | G4 | TB82 | PE |
| Lower | Ground | G5 | TB43 | PE |
| Lower | Ground | G6 | TB50 | PE |
| Lower | 5 | 5A | TB40 | L1_SW |
| Lower | 5 | 5B | TB41 | L1_SW |
| Lower | 5 | 5C | TB42 | L2_SW |
| Lower | 5 | 5D | TB30 | L2_SW |
| Lower | 5 | 5E | TB23 | L1_DIR |
| Lower | 5 | 5F | TB24 | L1_DIR |
| Lower | 5 | 5G | TB32 | L2_DIR |
| Lower | 5 | 5H | TB33 | L2_DIR |
| Lower | 5 | 5J | TB70 | L3_DIR |
| Lower | 5 | 5K | TB71 | L3_DIR |

## Source checkpoint

Pre-renumbering board SHA-256: `c731a221f87b926be2c003654d6b80d86224b43d60473315bae08dab0162202a`.
Renumbered board SHA-256: `b738d5c0a8aec3e600c9eabf21a384ae3e65b1bcc55b7f4382337b39da2ae1b6`.

The 2026-10-28 renumbering retained terminal placement, pad identities, nets and routed geometry. The terminal blocks are PCB-level layout items; the saved electrical schematic contains no terminal-block reference instances to rename.

Right-entry relocation checkpoint, 2026-10-29: board SHA-256 `04f916bcc7674bb8db68ffcfc75c5fe25b5ecf4fd1e167e0c03079a843f9d11f`. Four terminals, the J2 mains-gland proxy, the affected cable-tail/fuse-feed/bonding routes and end-stop placement changed; all contactors remain in place.
