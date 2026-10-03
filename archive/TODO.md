# Open work

Use [Rev P](Powermatic_BOM_revP.csv) and the saved KiCad project for current work.

- Complete the 24 VDC direction-holding, speed-selection, STOP and E-stop schematic using the verified drum-switch and button-station terminal maps in `_parts`.
- Keep KF/KR and KL/KS interlocked; develop the KH/KS high-speed operation and allocate the available auxiliary contacts in the final schematic.
- Include both overload trip contacts and the coil-enable relay in the final control design. Verify stopped behavior after STOP, overload, E-stop clearing and power restoration against the agreed operating behavior.
- Verify the completed power circuit, six motor-lead connections, protection coordination, supply/coil demand, wire sizing and enclosure/motor bonding before construction and commissioning.
- Review STEP axes, mounting datums, dimensions and actual terminal positions; create the Controls layout footprints if KiCad is used for panel layout.
- Place the panel components, rail and duct, then select enclosure/backplate dimensions and determine rail lengths, duct lengths and disconnect shaft length.
- Replace the single provisional feedthrough-terminal quantity with a final terminal and wiring-accessory takeoff after routing the circuit.
- Record procurement and receipt status as parts are ordered.

External L15-20 plug, drum-switch and button-station modeling is deferred. The fuse model is not required. A terminal-marker model remains unavailable in the sourced set.

Previous reports, model acquisition records and superseded design tasks are available in Git history, including archive commit `8ceac95`.
