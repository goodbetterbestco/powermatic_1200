# Recheck — 2026-10-06, 13:16

Latest saved schematic hash: `462dfc2d9a394fd04e105236802ed6419120693a99164f15736c836764cc3889`.

- K5.44 correctly feeds K6 A1.TOP/A1.BOT and SP6.1 via HIGH_COIL.
- K5.43 remains on HS_COIL with K4.32, K5 A1.TOP/A1.BOT and SP5.1.
- K5.44 is removed from SPEED_SET; K6's NO auxiliary retains STOP_RELEASED to SPEED_SET.
- K5's dangling wire warning is cleared.
- OL1_OK was renamed OL4_OK without changing endpoints.
- All other exported net memberships match the earlier reviewed snapshot.
- Native KiCad 10.0.6 ERC: **0 errors, 0 warnings**, under the project's existing check configuration.

The PE documentation gap and stale Wire.W001/W003/W005 records remain. The wire generator still fails on deleted/replaced destination UUID 782cabbe-a58e-46f3-9f97-d5cf96f2f77e. The high-speed motor phase-to-lead mapping remains as noted in the original review; it is a cyclic permutation of the photographed plate.

No schematic, PCB or library was edited. This confirms the saved schematic corrections, not physical wiring or PCB synchronization.
