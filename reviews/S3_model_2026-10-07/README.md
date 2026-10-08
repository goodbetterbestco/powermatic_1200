# S3 owner-model footprint and placement — 2026-10-07

Built and installed `Controls:365-TAV2111_Top` for S3 from the owner's updated `/Users/evanthayer/Desktop/Configuration 1.step`. The owner reports that the model was hand drafted against the real switch. The earlier partially labelled STEP was superseded. The installed `AB_365-TAV2111.step` is byte-identical to the updated source; neither Desktop file was edited. There is no model scaling, rotation, translation offset or alteration of the drafted solids.

## Placement and model alignment

- Reference: S3; source symbol UUID: `26502bde-0b19-4cea-bdff-2e8d228f3aae`.
- Footprint position: X=600.000 mm, Y=231.241 mm, angle 0 degrees, F.Cu.
- Mounting: `machine`.
- Overall model envelope: 156 × 73 × 75 mm; case: 135 × 73 × 75 mm.
- Source enclosure bottom: Z=0. The zero-offset model attaches to KiCad's normal top-side component plane, Z=1.595 mm in this project's native STEP export. The board-only dielectric export excludes copper/mask and has a different top extent; it is not the component datum.
- Enclosure right edge: X=484.759 mm. Switch left edge: X=532.500 mm. Clear gap: 47.741 mm. The switch case and enclosure are vertically centred together.
- All 46 model solids remain present and valid. Native exported dimensions are unchanged. Each of the sixteen screw-head rim centres matches the source plus placement transform, with maximum error less than 0.000001 mm.

The top-view footprint has sixteen panel-wiring targets. The owner's `screw_NT`/`screw_NB` labels map to the existing `N.U`/`N.L` pin IDs. Upper/lower screws overlap in top projection, so each pair uses symmetric 6 mm left/right fan-out about the pair's mean projected centre. The true 3D screw coordinates, projected centres and pad locations are in `geometry.json`. These 3 mm targets with 2 mm drill display geometry do not specify switch holes or a PCB land pattern. The original STEP screw geometry and F.Fab projection stay at their true locations; no spokes or leader lines are added.

F.Fab contains the full native visible-edge projection. F.Silkscreen contains the case/shaft and major screw outlines plus the visible 2.5 mm S3 reference. F.Adhes contains the display fill. Value and other metadata are hidden, following the current approved Controls artwork convention. The reference is readable and clear of the terminal targets in the native exported review.

## Scope and preservation

S3 is linked to its schematic symbol and all sixteen pads receive the exact saved schematic net names, functions and electrical types. Only S3's Footprint and Package fields changed in the schematic instance, cached symbol and shared Controls symbol. The non-LCSC source row receives that same footprint association and physical package description; its database was rebuilt with the repository's CSV rebuild script. Both catalog databases passed CSV/SQLite equality, unique-key and integrity checks; only the changed non-LCSC database was installed.

The PCB gains one footprint (88 → 89). Every original top-level PCB record, including all original placements, graphics, pads, models, nets and UUIDs, is preserved. Schematic net membership and all 184 existing Termination fields are unchanged. Project settings and BOM are unchanged. S2 creation and the joint termination-ownership migration remain a separate follow-up; this work implements the supplied S3 model/footprint placement.

`before/` and `shared-before/` preserve exact pre-edit project/library/database files. `staging.json` contains file hashes and preservation checks. `placement.json`, `geometry.json` and `native-alignment.json` contain native and CAD evidence. `previews/` contains the inspected native footprint and whole-layout render.

## Verification and limits

Native KiCad loaded the footprint and updated board, exported their 2D geometry, rendered the complete layout and exported S3's STEP. Final ERC: 0 errors, 10 existing `lib_symbol_mismatch` warnings, identical to the baseline. The temporary staged association warnings disappeared after the shared library was installed. The DRC CLI aborted with exit 134 on both the before and updated boards and produced no report; DRC is unverified. This remains the existing visual-placement artifact and does not establish a PCB fabrication pattern, wiring completion, physical fit or installation signoff.

Applicable library rules: FP-CTRL-001/005 are supported by source/model projection and explicit true terminal coordinates; FP-CTRL-002/003/004 by the sixteen exact IDs, symmetric fan-out and ≥5 mm nearest target-centre spacing. FP-CTRL-006/007/008 are checked through hidden metadata, visible 2.5 mm reference and native visual review. F.Silkscreen is used for the reference under the user's later approved artwork convention, which supersedes the older Dwgs.User preference. FP-META-001/002/003/004/005/007 are checked in the saved footprint; it is deliberately one-to-one. The supplied STEP is owner-drafted source geometry, not a manufacturer land pattern. No electrical or copper-land-pattern compliance is inferred.
