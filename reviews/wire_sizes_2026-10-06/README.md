# Wire-size population — applied 2026-10-06

Applied after the owner replied “paused” to the saved-editor checkpoint request.
The candidate was rebuilt from that latest save, retaining the new motor PE pin
and the owner's schematic placement/wire edits rather than installing the older
staged snapshot. `before/` preserves the exact pre-application project files.

Custom `Wire.Sizes` fields now classify all 172 connected terminals on 25 symbols:
128 numeric AWG assignments and 44 fixed/interface classifications. Each entry
binds the saved symbol UUID/pin, native net name, application scope and gauge.
Panel power wiring is 14 AWG; panel controls are 18 AWG; incoming cable is 12 AWG;
M1 T1–T6 conduit wires are 14 AWG and M1.PE is 12 AWG; S2 has five 16 AWG external
conductors and S3 has three. J1's four supplied pigtails retain 22 AWG. Fixed switch
links, suppressor connections, connector interfaces and direct-mounted overload
connections have no guessed loose-wire gauge. Duplicate coil and PSU terminals
do not imply additional jumpers.

`Wire.SizePlan` retains the three proposed 10 AWG prefabricated bonding assemblies.
The motor-conduit PE is now recorded on the owner's connected M1.PE terminal,
not a separate invented pin or a duplicate mechanical-plan conductor.

Validation: all 24 wiring tests pass. Native KiCad exports preserve all 27 added
sizing/plan fields and every electrical net membership. Removing only the two
custom field types from the candidate's parsed source gives the exact original
schematic structure: existing symbol fields, cached libraries, pins, wires,
labels, junctions and all other objects are unchanged. Native ERC of the latest
pre-application save, candidate and installed schematic each has zero errors
and zero warnings under the existing project settings. PCB and project settings
are byte-identical to the checkpoint; no shared library or BOM was changed.

`sizing.md` and `sizing.json` are generated from the installed schematic fields.
`validation.json` records before/candidate/installed hashes and checks. The
`candidate/` copy matches the installed update. Reload the active schematic with
File → Revert before editing so the open editor reads the external metadata.
The native file export is verified. Automatic desktop editor reload was not
performed; the owner requested no screen sharing or desktop UI interaction.

These are connection sizing declarations, not a complete physical wire schedule.
PCB-only terminal allocation, conductor endpoint routing and cut lengths remain
pending. Existing stale `Wire.Wxxx` physical-wire records are retained for that
separate migration, so the older physical-wire generator remains incomplete.
This metadata update is not electrical or installation signoff.

## Color population and overload-output correction

The schematic now stores the discrete wire colors: 12 AWG Green/Yellow;
14 AWG Black; 14 AWG Green/Yellow; 16 AWG Blue; 18 AWG Blue. This extends
the existing BOM color convention to the new motor PE and control-conduit
conductors. J1's supplied 22 AWG Brown/White/Blue/Black leads keep their
pin-specific colors; incoming cable colors remain as supplied.

OL4 and OL6 output terminals 2/4/6 were previously misclassified as panel
controls. All six are corrected to 14 AWG Black motor-power wiring. The
`color_update/` snapshot preserves the exact source before this correction.
Only custom sizing fields were changed; all other parsed source objects are
identical. Retained jumpers and supplied assemblies now have neutral notes;
the derived AWG column uses a dash for these separate categories. No new
verification obligation is assigned to them. Installed native ERC remains
zero errors and zero warnings; PCB and project settings remain unchanged.
