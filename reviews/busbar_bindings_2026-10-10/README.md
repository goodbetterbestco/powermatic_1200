# Busbar bindings and wiring refresh

Completed 2026-10-11. BB1 and BB2 now bind host A to K1 and host B to K2 by
the placed contactors' UUIDs. Native KiCad loading and schedule extraction
verify all twelve contact positions and nets exactly; see
`contact-validation.json`.

| Kit piece | Contact pairs | Verified host-terminal pairs |
| --- | --- | --- |
| BB1 TOP | A1–B1, A3–B3, A5–B5 | K1.1–K2.1, K1.3–K2.3, K1.5–K2.5 |
| BB2 BOT | A2–B6, A4–B4, A6–B2 | K1.2–K2.6, K1.4–K2.4, K1.6–K2.2 |

The three duplicate right-side A2/A4/A6 pads were removed from the shared
BOT footprint and placed BB2. Each half now has six uniquely numbered contacts.
BB2.A2's missing net is set to its host net, L1_DIR. Other contact nets match
the saved schematic and the intended reversing-pole mapping.

BB1 logical pads move +0.001395 mm in X to match the integer-grid host targets.
BB2's origin moves from (315, 130.0625) to host A's datum (315, 130). Its artwork
and fields translate +0.0625 mm locally, preserving their saved global positions.
Its six logical pads consequently move -0.0625 mm in global Y to the screws.
Both shared footprint descriptions now correctly describe the existing 58 mm
logical host span. No contactor, source-body outline, 3D model or S3 placement
changes. This establishes CAD target/net consistency; it adds no physical
busbar-fit or bench qualification.

The placed contactors K1/K2/K4/K5/K6 were also missing their termination fields.
Seventy selections were restored from
`reviews/footprint_terminations_2026-10-08/provenance.json`, after checking every
footprint UUID, pin ID and current Wire.Sizes gauge. Existing selected ferrule
types and TBD lengths are retained; nothing is restored over an existing field.

Two S2 three-arm wire junctions had been drawn off the actual terminals.
Four segment endpoints now terminate at S2.2B and S2.3T; two shared short
spurs are removed. Nets, layers, widths and terminal endpoint relationships
are preserved. Every other track is unchanged.

The installed S2 1T–3T and 3T–5T links are declared in the footprint's explicit
`Wire.RetainedLinks` metadata, using the pre-existing installation notes.
The extractor validates their terminal IDs and schematic nets, treats them
as retained hardware and excludes them from cut-wire rows and conductor counts.
S2's required 2B–4B jumper remains a new wire row; its 4B termination selection
is still pending, so that Term 2 cell is blank. This classification does not
exclude arbitrary same-net wiring or infer links from a termination label.

The live `Wire_schedule.csv` refresh succeeds with 18 completed wire rows.
The purchased busbar kit remains quantity 1 (TOP 1, BOT 0). Two routed retained
S2 links are omitted. S3's native jumper groups remain unchanged and generate
no cut-wire rows.

Routing remains partial: 43 unrouted nets, 115 unfinished trace endpoints,
and trace-only loops/components without two terminal pads. The J2 lengths
cover panel tails only, without the external mains cord. These are preserved
in `schedule-report.json`; no manufacturing or complete-wiring claim is made.

Final ERC reports zero violations. DRC drops from 149 to 121 findings:
20 clearance findings and eight shorting findings are removed, with no new
findings. The remaining 121 comprise 109 dangling-track and 12 shorting
findings. Unconnected items drop from 83 to 82; the nine pre-existing
schematic-parity findings are unchanged. The full schematic netlist is unchanged.
Eight supplier/retained-link tests pass, including mismatched-net rejection
and preservation of external wires and conductor counts.

Native exported artwork was inspected. Full physical fit and manufacturing
qualification remain outside this repair. Catalog/database associations are
unchanged, so no database rebuild is required. Changes are local and uncommitted.
