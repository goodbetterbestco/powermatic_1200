# S2 pushbutton-station integration

`inspect_model.py` measures the owner's complete STEP with OCP, retains the STEP root
solid order, and creates temporary isolated geometry for projection.
`build.py` generates `Controls:50MA3KLE_Top` after confirmation of T/B contact
functions. The original STEP stays byte-identical, including color information.
Its offset is 70,0,89.4 mm; rotation is zero and scale is one.

`stage_station.py` stages the new catalog symbol and S2 metadata in
`/private/tmp/powermatic-s2-model`, using the saved checkpoint in
`reviews/S2_model_2026-10-08/before/`. `place.py` uses KiCad's bundled Python to
serialize only S2 and append it to the existing board at 600,120 mm. Export
the candidate netlist as `kicadxml` before placing. `validate.py` checks exact
preservation of all other board/schematic records, unchanged wiring, catalog
CSV/SQLite parity, and the source STEP hash.

Pads are logical panel-wiring targets, not manufacturing holes. Do not install
staged files while KiCad is being edited; compare hashes against the checkpoint
before installing. The T/B mapping is a required input, never an inferred
normally-open/normally-closed assignment from model height alone.

The current symbol and footprint use physical IDs 1T/2T/1B/2B,
3T/4T/3B/4B and 5T/6T. `renumber.py` stages the matching symbol,
schematic, footprint and board migration; `validate_renumber.py` verifies
connectivity, absolute connection points, standard grids and immutable geometry.
Use `renumber.py --netlist <candidate XML>` after native netlist export,
then validate before its `--install` operation. The initial `validate.py` and
its saved baseline evidence describe the first legacy-ID installation; the
current physical-ID review is in `reviews/S2_model_2026-10-08/pin_numbering/`.

Current device artwork uses F.Silkscreen; the complete source detail remains
on F.Fab. Dwgs.User is reserved for enclosure/backplate/duct/rail information,
and Cmts.User is empty. The shared Q1-style recipes, clipping and native
review evidence are in `../artwork_review/` and
`reviews/artwork_layers_2026-10-08/`.
