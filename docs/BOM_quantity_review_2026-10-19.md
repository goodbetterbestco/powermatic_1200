# BOM quantity review — 2026-10-19

## Bonding revision — 2026-10-20

This revision supersedes the affected quantities in the historical audit below.
Added PCB-only PE terminal TB98 on the middle rail, moved only its right end
bracket 6 mm outward, and routed a 12 AWG green/yellow jumper from TB52.2 to
TB98.1. The existing TB43.2–TB51.2 jumper remains in place. The owner confirms
that the backplate mounts on four enclosure grounding lugs/studs; the current
connection table and installation checks are in `WIRING_STANDARD.md` under
**Rail and enclosure bonding connections — 2026-10-20**.

| Requirement | Previous | Revised | Purchase effect |
|---|---:|---:|---|
| KN-G12SP-10 PE blocks | 5 | 6 | Existing 10-pack covers the addition. |
| Terminal marker positions | 62 | 63 | Existing 250-pack covers the addition. |
| 12 AWG single ferrules, 7950K31 | 12 | 15 | Two for TB52–TB98 and one reserved for TB50-to-lug; existing 100-pack covers them. |
| 12 AWG green/yellow loose wire, 6513T633 | 8.6 ft | 9.8 ft | Adds the 360 mm routed-jumper cut estimate; existing 50 ft purchase is unchanged. |

The TB50.1-to-grounding-lug jumper is planned but not yet routed. Its cut
length and stud-compatible ring must be confirmed on the enclosure, then its
length added to the wire requirement. No imaginary lug location, ring-stud
size or cut length was introduced into KiCad or the trace-derived schedule.
The ferrule requirement already reserves its terminal-block end. GBB provides
the stud-compatible ring and mounting/bonding hardware. Purchase quantities,
prices and receipt flags are preserved; the purchase total remains $2,203.28.

Regenerated `Wire_schedule.csv` from the saved PCB with the documented
installed-conduit lengths and end allowances. The result has 125 rows: all
124 prior wire rows are retained and TB52–TB98 is added at 360 mm. Fixed
terminal jumper bars and PE-bank hardware are excluded from loose-wire rows.
`Wire_length_totals.csv` is recalculated from those same paths and installed-run
assumptions, including the previously audited 14 AWG PE and 16 AWG control-wire
corrections. Its loose-wire total is 91.580 m across 115 wires. Factory cable
cores, pigtails and two 10 AWG factory bonding spans remain outside loose stock.

Native KiCad connectivity reports zero unconnected items. All 1,253 pre-existing
track objects are byte-for-byte unchanged; the new jumper adds three segments
and two 5 mm-radius bends. Only TB50/TB52 endpoint metadata and the rail-2 right
end bracket change among existing footprints. The schematic is unchanged.
The legacy schematic-coverage audit still reports the same 15 uncovered logical
nets seen before this revision, including metadata-only and retained-connection
endpoints; this update does not claim ERC or full schematic/layout reconciliation.

## Original audit — 2026-10-19

The 62-row `BOM_other.csv` does not show a general quantity-column scramble. The saved component and termination counts reconcile. The two stale wire requirements and unresolved WAGO row have now been corrected. All six loose-wire QUA values round upward to one decimal place. Its saved purchase total is **$2,203.28** after the owner's final 221-612 selection.

## Resolved deviations and remaining hardware check

| Item | Saved BOM | Current evidence | Disposition |
| --- | --- | --- | --- |
| 16 AWG blue wire, `9874T12` | QUA **58.7 ft** | Saved routes plus existing installation/end allowances require 58.695 ft | Corrected from 58.498 ft. ORDER 1 × PACK 100 ft still covers it. |
| 14 AWG green/yellow wire, `6513T531` | QUA **7.2 ft** | Same method requires 7.153 ft | Corrected from 7.087 ft. ORDER 1 × PACK 10 ft still covers it. |
| Two-port WAGO, `221-612` | QUA **6**, PACK **50**, ORDER 1, LINE **$30.50** | Owner selects the smaller purchase pack for six motor-lead splices, one for each T1–T6 conductor | Six required connectors and 44 spares. PCB termination fields and the saved schedule now specify 13 mm stripping for these six ends. |
| Three-port WAGO, `221-613` | QUA 2, PACK 30, ORDER 1 | One explicit GS1 splice and the motor PE splice represented by M1.PE | Two intended splices are supported by the wiring policy, although only one has its own part reference. |
| Speed/direction gland proxy, `BSPBX-22-W` | No purchase required | J3 is a drawing proxy superseded by the selected LFNC-B fittings | The initial audit incorrectly classified it as missing. Existing conduit/fitting rows cover this run. |
| Motor gland proxy, `BSPDX-23-W` | No purchase required | J4 is a drawing proxy superseded by the selected LFNC-B fittings | The initial audit incorrectly classified it as missing. Retain the distinct mains-gland purchase. |
| Frame/motor-bell PE hardware | No dedicated `Frame_PE_Lug_20mm` row | J5 and J7 are separate mechanical bonding points | Verify the applicable GBB/on-hand hardware allocation. The footprint is a bonding-location model, not an established purchasing SKU. |

The owner selected `221-612` for the six motor power splices on 2026-10-19 after comparing its 50-piece pack at $30.50 with the 100-piece `221-412` pack at $34.00. Both accept the specified 14 AWG conductors; `221-612` uses 12–14 mm stripping, with 13 mm selected here. Two `221-613` connectors remain required: the motor PE junction and GS1 at S3. Their existing one-pack purchase is unchanged. [AutomationDirect pack and price, checked 2026-10-19](https://www.automationdirect.com/adc/shopping/catalog/wire_-a-_cable_termination/splicing_connectors/splicing_connectors/221-612).

The gland resolution follows the existing **External conduit runs** policy in `WIRING_STANDARD.md`: J3/J4 artwork is excluded from BOM auto-add. The BOM already specifies 6 ft of LFNC-B, four `9106K422` straight fittings, two `9106K522` elbows and one `44605K262` reducer. Adding the old gland SKUs would duplicate superseded hardware.

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
| 18 AWG blue | 9874T11 | 93.8 | 93.734 | 100 |
| 16 AWG blue | 9874T12 | 58.7 | 58.695 | 100 |
| 14 AWG black | 9874T13 | 119.5 | 119.456 | 150 |
| 12 AWG black | 9874T14 | 11.7 | 11.680 | 50 |
| 14 AWG green/yellow | 6513T531 | 7.2 | 7.153 | 10 |
| 12 AWG green/yellow | 6513T633 | 8.6 | 8.563 | 50 |

Calculated needs in the evidence column round upward to 0.001 ft; saved wire QUA values round upward to **0.1 ft**, as requested. All six purchased stock amounts exceed the aggregate requirements. The 18 AWG blue stock has the least margin against the rounded BOM requirement, 6.2 ft. Individual spool cut allocation was not re-optimized in this review.

The current saved PCB yields 124 routed wire rows. Loose stock excludes four factory M12 pigtails, four mains-cable tails, and two supplied 10 AWG bonding-assembly spans. Loose-stock total is 91,220 mm (about 299.278 ft before per-group rounding). Motor/station installation estimates retain the owner's 2026-10-15 run assumptions and normal termination/service allowances, rather than illustrative exterior PCB tracks.

All rows now have numeric QUA. `PACK × ORDER ≥ QUA`, except GBB items which are explicitly on hand and retain ORDER 0. All 62 saved LINE values equal `ORDER × COST`. No purchase shortage was established for the listed requirements; the separate mechanical bonding-hardware check above remains open.

## Review app defect

The current flat-file editing path recalculated LINE using QUA × COST even when ORDER existed. For example, the 57-terminal requirement could display $2,080.50 instead of the actual $36.50 one-pack purchase. The saved BOM still contains the correct ORDER-based totals. The app was changed to use **ORDER × COST** when ORDER exists, falling back to QUA × COST for CSVs without ORDER. QUA, PACK and ORDER remain separate editable values.

The Open controls were replaced by a Documents dropdown listing root CSV names. Selection changes the loaded document and guarded Overwrite destination. Refresh reloads that selected CSV. Unsaved changes require confirmation before switching; stale saves and paths outside the project are rejected. `Project Review.app` launches the separate `~/Projects/bom_review` application. No JLCPCB BOM was invented; that document appears in the selector when a real `BOM_jlcpcb.csv` is added.

Validation: 58 Python tests and 30 JavaScript tests passed, including document listing, selected-file overwrite, stale-version rejection, path/symlink restrictions and ORDER-based calculations. Initial browser checks used a temporary two-document project: cancelling a switch retained edits, Overwrite changed only the selected fixture, and switching back restored the initial BOM total. The authorized BOM edits corrected six wire QUA cells, the two WAGO display names and the two-port splice quantity. The final selection retains `221-612` with PACK 50 and COST/LINE $30.50. The reviewer preserves the saved one-decimal wire quantities through CSV round trips.

## Evidence and limits

Read from saved native KiCad files and the saved CSV on 2026-10-19. After the quantity audit, the owner confirmed KiCad saved/closed and editing paused, then authorized changing only M1's six `Termination.T1`–`Termination.T6` strip lengths from 11 mm to 13 mm. No geometry, routes, nets or other fields changed during that edit. The schematic remains unchanged. PCB hashes below distinguish the quantity-audit source from the subsequent metadata-only update.

- Schematic SHA-256: `12b9fa941a7652fee1bd74d6e6d22fc3da00cab96878a638435029767531ea08`
- PCB SHA-256 at quantity audit, before the six strip-length changes: `7f5b2e1cfd71b2cc3ed4f97316e5b6db836d21878b8d2bba4aadcff2a669dc4a`
- Current saved PCB SHA-256 after the six strip-length changes: `1da240703884273b00e2b56d1f831ba2b2c82cd253d6ff8adf267b0575b25d8c`
- The route reader found complete drawing connectivity and warned that the external mains cord length is not included. This is a quantity audit, not an ERC/DRC, physical fit, supplier-stock or installation signoff.
- The cleanup is published as `cac6076`; existing uncommitted KiCad changes were left unstaged. Old committed tools/reports are recoverable from Git. Untracked reports and automatic backups removed by the requested cleanup were not added to Git.
