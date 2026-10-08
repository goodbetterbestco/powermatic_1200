# PCB update preflight — 2026-10-06

No update was applied to the production PCB. This directory preserves the saved board and a position/orientation/layer/UUID manifest for every existing footprint. The board remains the established visual placement artifact.

## Findings

- There are 19 schematic-enabled physical parts; the six external symbols are excluded from the board.
- Six physical parts retain matching schematic UUIDs. The other 13 need explicit relinking after the redraw.
- Board-to-new-schematic reference mapping: OL1→OL4, OL2→OL6, SP3→SP4, SP4→SP5, SP5→SP6. Apply the suppressor renames as one mapped operation to avoid intermediate reference collisions.
- Existing rail, duct, enclosure, fuse and accessory footprints already use `board_only`. Removed terminal symbols, MI1/MI2 and J3–J5 remain linked ordinary footprints in the saved board and need `board_only` before enabling deletion of unmatched footprints. The earlier MI/gland edits were staged, not applied.
- PS1's saved board pads still use TB1.x/TB2.x; its current symbol uses 1_BOT/2_BOT/3_BOT and 1_TOP/2_TOP/3_TOP/4_TOP. Relinking alone will not fix these pad numbers. Rename the existing pads in place or perform a separately verified footprint refresh, preserving placement.

## Procedure

1. Save both editors and pause editing before external file changes. Preserve the newest board, schematic and complete placement manifest as the checkpoint; this snapshot covers saved files only.
2. Mark the intentional PCB-only parts `Not in schematic` and detach obsolete symbol paths, preserving their footprint UUIDs, coordinates, angles and layers. Finish the staged MI/gland conversions against that newest checkpoint.
3. Reconcile the five changed references above, then relink all 19 existing physical footprints to their current schematic symbols. Preserve the footprint objects, models and placement. The selected footprint library IDs already agree after the reference mapping.
4. Reconcile PS1 pad numbering. Update PCB-only terminal/gland pad nets deliberately; those parts have no schematic symbol from which KiCad can derive their assignments. Existing obsolete net names require mapping, not position changes.
5. Perform a trial schematic update on a copied project. For the initial update, keep **Delete footprints with no symbols**, **Replace footprints with those specified by symbols**, **Override locks**, **Group footprints based on symbol group**, and **Remove footprint fields not found in symbols** off. After explicit UUID repair, keep reference-based relinking off. If relinking in the native dialog instead, enable reference-based relinking for that one repair update only, after reconciling references.
6. Inspect Changes To Be Applied. None of the 19 already-placed physical parts should appear as additions, deletions or replacements. No intentional PCB-only part should be deleted. Net and expected field changes are normal.
7. Compare every retained footprint's UUID, position, angle and layer with the checkpoint; verify no duplicate footprints and current pad-net membership. Run current native ERC/DRC and separate pre-existing layout violations from synchronization faults. Only then apply the verified update to the saved working board and reload it in the editor.

KiCad's footprint lock is additional protection against deletion/replacement when Override locks is disabled; it does not repair broken schematic links. `Not in schematic` protects PCB-only parts from the unmatched-footprint deletion option. Updating matching footprint nets does not require moving their established placements.

References: [KiCad Update PCB from Schematic](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#update-pcb-from-schematic-forward-annotation), [PCB footprint attributes](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#footprint-attributes).
