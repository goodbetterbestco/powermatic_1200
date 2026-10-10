# Panel datums and integer wiring-target coordinates

Owner-authorized saved/paused checkpoint, 2026-10-09. Updated J2/J4/J5 glands,
SW1 disconnect, H1/H2 indicators and J1 M12 panel socket. Eight shared library
files include the underlying BNSPDX-23-W gland and its installed mains-plug proxy.

The glands use Y=0 at the outer wall and X=0 at the gland axis. SW1 uses X=0 at
the outer wall and Y=0 at the shaft axis. The lamps move the datum from the old
X=-16.82571 mm bezel underside to X=0. The M12 socket moves its modeled
sealing-ring rear tangent from old X=3 mm to X=0. This is the nominal modeled
seal plane; the STEP represents the uncompressed seal, not installed gasket
compression. The local TE drawing distinguishes the front shoulder, seal and
rear locking nut. The local Schneider drawing places the panel at the bezel
underside, 11 mm behind the operating face.

All 54 library pad centers, including the 46 targets in the seven installed
instances, are nearest-integer X/Y after the datum change; the largest rounding
adjustment on one axis is 0.45 mm. Native KiCad pad coordinates were checked
at an integral origin and at 0/90/180/270 degrees. These are panel-layout wiring
targets; rounding does not alter hardware outlines or manufacture dimensions.

Placed origins compensate the new local datums so the physical X/Y location,
orientation, model X/Y, drawing details and instance text remain fixed. Pad
numbers, nets, sizes, drills and UUIDs are retained. All 89 other instances and
all board text outside the seven edited footprint blocks remain byte-identical.
The current board has 277 pads and zero track segments, retained by the update.

H2 model Z was 0 mm while H1 model Z was 60.05 mm. H2 now uses 60.05 mm as well;
the lamp source's operating axis is 14.95 mm above its transformed model origin,
so both axes are 75 mm above KiCad's component plane, matching the SW1/J1
mounting-axis height. The two lamp library defaults also use 60.05 mm. H1's
placed height and all device wall positions remain fixed.

The five relevant schematic instances already select the same updated library
IDs. J4/J5 are PCB-only mechanical glands. The schematic is retained verbatim;
no symbol-body, wiring or footprint-ID migration is needed for this in-place
library update. Native netlist and ERC comparison checks the saved consuming
schematic. Baseline ERC: zero errors, one H1 library-symbol-mismatch warning.
The baseline DRC CLI aborted with exit 134 before producing a report.

`manifest.json` records exact origins, source/candidate hashes and every rounded
pad. `prepare.py` records the transformation. `layout.svg`/`layout.png` are
native exported isolated-footprint visual evidence: review-only crosses mark
origins; they are not installed device geometry. Appearance was inspected from
this export; no live symbol/editor inspection is claimed.

Applicable shared rules: FP-CTRL-001/005/009/010/011 retain true physical geometry,
full F.Fab detail, existing layer ownership and omitted courtyards. The owner's
explicit closest-integer pad instruction supersedes exact fan-out spacing in
FP-CTRL-002/003 for these wiring targets. FP-CTRL-006/007/008 preserve the existing
reference-only labels and their placed appearance. No electrical symbol geometry
was changed, and this is not a claim of full library-review completion.

Final saved-project checks: native library/board load and serialization/reload pass; all 63 net memberships are unchanged; ERC has zero errors and the unchanged one H1 library warning. Final DRC also aborts with exit 134 and produces no report. No DRC pass is claimed. `before.zip` in the consuming project review restores both project and library source checkpoint files.
