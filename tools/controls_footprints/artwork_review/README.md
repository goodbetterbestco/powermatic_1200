# Q1-style switch artwork and reserved user layers

`build.py` measures the unchanged named source STEP solids with OCP and
projects simplified mechanical drawing proxies. It excludes engraved text,
screw slots/threads and fine tessellation from silkscreen while retaining
complete saved source artwork on F.Fab. `make_curves()` is shared by both
switch footprint generators so their rebuilt drawings reproduce the review.

`stage.py` clips the 0.25 mm Controls strokes to logical circular copper
targets with a nominal 0.15 mm rendered-edge clearance. It stages the two
footprints, PCB layer cleanup and the owner's layer/detail rules. Dwgs.User
is reserved for enclosure/backplate/duct/rail information; Cmts.User is empty.
Source snapshots are in `/private/tmp/powermatic-layer-review/before/`.

`validate.py` checks literal physical/electrical record preservation,
unchanged source F.Fab graphics, permitted user-layer ownership and analytic
stroke-edge clearance. `install.py` requires those checks, current native
visual review and unchanged source hashes before installing candidates and
retaining the before/after evidence in `reviews/artwork_layers_2026-10-08/`.

This is panel-layout artwork, not a PCB manufacturing land-pattern generator.
