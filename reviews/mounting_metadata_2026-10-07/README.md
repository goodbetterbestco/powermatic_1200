# Mounting metadata and canonical fuse-holder name — 2026-10-07

The owner confirmed that `din_top` and `din_bot` identify the upper and lower DIN rails. Added a hidden `Mounting` instance property with one of `din_top`, `din_bot`, `panel`, or `machine` to all 88 PCB footprints and all 25 physical schematic component instances. Virtual power symbols receive no mounting property; cached library symbols receive no instance-specific mounting assignment.

| Value | PCB footprints | Schematic instances |
| --- | ---: | ---: |
| din_top | 41 | 5 |
| din_bot | 34 | 11 |
| panel | 12 | 3 |
| machine | 1 | 6 |

DIN-mounted accessories, including fuses, covers, suppressors, overloads and interlocks, inherit their parent rail group. `panel` covers DIN rails themselves, wiring ducts, cable glands, enclosure-wall controls and the M12 panel socket. `machine` covers the enclosure footprint and the schematic's external motor, E-stop, speed/direction controls and cable plugs (M1, S1–S3, J2, J6). The enclosure is classified as the machine-level assembly. These assignments describe layout location rather than a verified attachment method or mechanical fit.

Changed RM25030-3SR's `Part Name` from `Class R\nFuse Holder` to `Fuse Holder` in the PCB, placed schematic instance, cached symbol, shared Controls symbol and non-LCSC catalog. The technical Description, class information, keywords and manufacturer identifiers remain intact. Rebuilt the shared non-LCSC SQLite database from the changed authoritative CSV using `database/rebuild_db.py` in staging. Both catalog databases passed CSV/SQLite parity, unique-key and integrity checks; only the changed non-LCSC database was installed.

Removed all `WireName` overrides from the project PCB and schematic. Every wiring-generator display name is unchanged: FH1 now obtains `Fuse Holder` directly from `Part Name`; J2 obtains `Mains Plug` by normalizing its existing two-line `Part Name`.

Complete S-expression comparisons confirm that all project data outside these requested fields is unchanged. Shared Controls symbol comparison confirms that only the target Part Name changed; the catalog comparison confirms that only the RM25030-3SR Part Name cell changed. Staged project files passed native KiCad parsing; the shared symbol passed native SVG export. `validation.json` records assignments, hashes and verification. `before/` and `shared-before/` preserve the exact pre-edit files and database. `symbol-preview/` contains the native exported symbol.

The shared source edit follows the user instruction for the canonical name. `SYM-META-001/002` are checked through exact device-field comparisons; the requested single-line `Fuse Holder` label is an explicit exception to `SYM-TEXT-006`'s default two/three-line preference. No pins, body geometry, pin types, field placement or models changed. `SYM-VIS-001` live symbol-editor inspection was not performed; this metadata edit does not claim a full library or electrical review.

Final saved project files also passed native KiCad parsing. Final shared CSV/SQLite equality and database integrity passed. The rendered native symbol SVG was inspected: `Fuse Holder` is readable and separated from the body/pins.
