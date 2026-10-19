# BOM quantity review — 2026-10-19

The 62-row `BOM_other.csv` does not show a general quantity-column scramble. The saved component and termination counts reconcile. Two wire requirements are slightly stale, one splice requirement is blank, and some physical parts need explicit purchasing coverage. No BOM cells were changed during this review. Its saved purchase total is **$2,203.28**.

## Deviations and unresolved coverage

| Item | Saved BOM | Current evidence | Disposition |
| --- | --- | --- | --- |
| 16 AWG blue wire, `9874T12` | QUA 58.498 ft | Saved routes plus existing installation/end allowances require **58.695 ft** | Understated by 0.197 ft. ORDER 1 × PACK 100 ft still covers it. |
| 14 AWG green/yellow wire, `6513T531` | QUA 7.087 ft | Same method requires **7.153 ft** | Understated by 0.066 ft. ORDER 1 × PACK 10 ft still covers it. |
| Two-port WAGO, `221-612` | **Blank QUA**, PACK 50, ORDER 1, LINE $30.50 | No explicit two-port splice was found in the saved schematic/PCB; GS1 is a three-port `221-613` | Requirement remains unknown. Confirm intended use or remove this purchase; do not treat a blank as zero or as a verified requirement. |
| Three-port WAGO, `221-613` | QUA 2, PACK 30, ORDER 1 | One explicit GS1 splice and the motor PE splice represented by M1.PE | Two intended splices are supported by the wiring policy, although only one has its own part reference. |
| Speed/direction gland, `BSPBX-22-W` | No dedicated row | J3 is present on the PCB | Account for **one** of this exact gland or document a compatible substitution/on-hand source. |
| Motor gland, `BSPDX-23-W` | No dedicated row | J4 is present on the PCB | Account for **one** of this exact gland or document a compatible substitution/on-hand source. The `BNSPDX-23-W` mains-gland row does not establish that coverage. |
| Frame/motor-bell PE hardware | No dedicated `Frame_PE_Lug_20mm` row | J5 and J7 are separate mechanical bonding points | Verify the applicable GBB/on-hand hardware allocation. The footprint is a bonding-location model, not an established purchasing SKU. |

The blank `221-612` row is included in the $2,203.28 total because ORDER is 1. Setting ORDER to zero would reduce the total by $30.50, but no such change was made.

## Quantities that reconcile

All **28 KiCad-linked BOM rows** reconcile after accounting for physical pieces versus stock or kits. In particular, the feedthrough count is 57: 54 schematic terminal references plus PCB-only TB79, TB80 and TB81. These three footprints lack the same explicit MPN metadata as the other terminal instances; a simplistic MPN-only extraction would incorrectly report 54.

| Group | Verified project requirement |
| --- | --- |
| Power contactors / interlocks / coil-enable relay | 5 / 2 / 1 |
| Thermal overloads / suppressors / auxiliary contact block | 2 / 5 / 1 |
| Timers / breaker / power fuses / fuse holder / fuse covers | 2 / 1 / 3 / 1 / 3 |
| Feedthrough terminals / PE terminals / end brackets / separators | 57 / 5 / 9 / 28 |
| End covers / marker positions / jumper top covers | 31 / 62 / 44 |
| Ten-pole jumper strips | 5 strips, purchased as one five-strip pack |
| Duct stock | 3 × 1 m lengths; four 400 mm sections and one 650 mm section total 2,250 mm and fit three stock lengths |
| DIN rail / backplate / enclosure | 3 / 1 / 1 |
| Reversing busbar kit | 1 kit; BB1 and BB2 are two supplied pieces of the same kit |
| Bonding assemblies | 3 assemblies; two two-assembly kits provide four, including one spare |

Terminal-bank accessory counts use the saved rigid jumper connections: 31 feedthrough groups, 62 feedthrough/PE terminal marker positions, and 44 feedthrough jumper poles. Eighteen multi-terminal feedthrough groups require jumper sections of thirteen × 2 poles, four × 3 poles and one × 6 poles; these fit five ten-pole strips.

Loose termination requirements also match the BOM's quantities:

| Preparation | BOM SKU | Required pieces |
| --- | --- | ---: |
| 22 AWG ferrule, 10 mm | 7950K16 | 3 |
| 18 AWG ferrule, 6 mm | 7950K71 | 4 |
| 18 AWG ferrule, 10 mm | 7950K73 | 45 |
| 16 AWG ferrule, 10 mm | 7950K24 | 14 |
| 14 AWG ferrule, 10 mm | 3202533 | 32 |
| 12 AWG ferrule, 10 mm | 7950K31 | 12 |
| 16–14 AWG ring, #8 stud preparation | 7113K49 | 13 |
| 14 AWG ring, motor stud preparation | 7113K24 | 3 |
| 12 AWG ring, fuse-holder stud preparation | 8429T62 | 3 |

These are preparation counts; this review does not revalidate the substituted ring SKU's stud/barrel dimensions. The 14 AWG ferrule row deliberately orders 40 individual pieces for 32 required, rather than a fictitious 100-piece pack. Retained supplier terminals and bare wire preparations do not add loose ferrules/rings. Free M12 pigtail ends do count even though the pigtail wire itself is supplied.

## Wire stock reconciliation

| Wire group | SKU | BOM QUA, ft | Current requirement, ft | Purchased stock, ft |
| --- | --- | ---: | ---: | ---: |
| 18 AWG blue | 9874T11 | 93.734 | 93.734 | 100 |
| 16 AWG blue | 9874T12 | 58.498 | **58.695** | 100 |
| 14 AWG black | 9874T13 | 119.456 | 119.456 | 150 |
| 12 AWG black | 9874T14 | 11.680 | 11.680 | 50 |
| 14 AWG green/yellow | 6513T531 | 7.087 | **7.153** | 10 |
| 12 AWG green/yellow | 6513T633 | 8.563 | 8.563 | 50 |

Calculated needs round upward to 0.001 ft. All six purchased stock amounts exceed the aggregate requirements. The 18 AWG blue stock has the least aggregate margin, about 6.266 ft. Individual spool cut allocation was not re-optimized in this review.

The current saved PCB yields 124 routed wire rows. Loose stock excludes four factory M12 pigtails, four mains-cable tails, and two supplied 10 AWG bonding-assembly spans. Loose-stock total is 91,220 mm (about 299.278 ft before per-group rounding). Motor/station installation estimates retain the owner's 2026-10-15 run assumptions and normal termination/service allowances, rather than illustrative exterior PCB tracks.

Across all rows with a numeric QUA, `PACK × ORDER ≥ QUA`, except GBB items which are explicitly on hand and retain ORDER 0. All 62 saved LINE values equal `ORDER × COST`. No purchase shortage was established for the listed, quantified requirements; blank requirements and missing coverage above remain open.

## Review app defect

The current flat-file editing path recalculated LINE using QUA × COST even when ORDER existed. For example, the 57-terminal requirement could display $2,080.50 instead of the actual $36.50 one-pack purchase. The saved BOM still contains the correct ORDER-based totals. The app was changed to use **ORDER × COST** when ORDER exists, falling back to QUA × COST for CSVs without ORDER. QUA, PACK and ORDER remain separate editable values.

The Open controls were replaced by a Documents dropdown listing root CSV names. Selection changes the loaded document and guarded Overwrite destination. Refresh reloads that selected CSV. Unsaved changes require confirmation before switching; stale saves and paths outside the project are rejected. `Project Review.app` launches the separate `~/Projects/bom_review` application. No JLCPCB BOM was invented; that document appears in the selector when a real `BOM_jlcpcb.csv` is added.

Validation: 58 Python tests and 30 JavaScript tests passed, including document listing, selected-file overwrite, stale-version rejection, path/symlink restrictions and ORDER-based calculations. Browser checks used a temporary two-document project: cancelling a switch retained edits, Overwrite changed only the selected fixture, and switching back restored the $2,203.28 BOM total. The real BOM remained byte-identical.

## Evidence and limits

Read from saved native KiCad files and the saved CSV on 2026-10-19. No KiCad file was edited, and the source hashes were checked again after the audit.

- Schematic SHA-256: `12b9fa941a7652fee1bd74d6e6d22fc3da00cab96878a638435029767531ea08`
- PCB SHA-256: `7f5b2e1cfd71b2cc3ed4f97316e5b6db836d21878b8d2bba4aadcff2a669dc4a`
- The route reader found complete drawing connectivity and warned that the external mains cord length is not included. This is a quantity audit, not an ERC/DRC, physical fit, supplier-stock or installation signoff.
- The cleanup is published as `cac6076`; existing uncommitted KiCad changes were left unstaged. Old committed tools/reports are recoverable from Git. Untracked reports and automatic backups removed by the requested cleanup were not added to Git.
