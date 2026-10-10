# Wire schedule metadata repair

The saved board lacked footprint-owned termination fields on the contactors,
overloads, glands, fuse holder and H2. Without direct-mounted classifications,
the extractor treated coincident K4.2 / OL4.IN1 pads as competing wire terminals
and aborted Refresh, preserving the empty CSV.

After the owner saved and closed the PCB editor, 135 hidden fields were added
to 11 existing footprints. Missing selections were recovered from the Git
checkpoint and the recorded termination migration, with matching current part
identities and terminal inventories. Current schematic Part Name fields were
used where available. Existing fields were retained. No shared library,
extractor, browser code, placement, pad, net, model or trace was changed.

Structured before/after comparison verified that only these new fields differ.
Native extraction passed and the running review server's Refresh endpoint
returned HTTP 200 and overwrote the live Wire_schedule.csv with 17 rows.
The schematic remained byte-identical. Browser capture/control was discontinued
at the owner's request; the final browser display was not inspected.

The routing review remains incomplete: 133 unfinished trace endpoints and
trace-only components were reported. AWG is missing on TB43.1 to TB51.2 and
TB50.1 to TB52.2. The J2 route is a panel tail; external cord length is excluded.
No electrical, ERC/DRC or assembly signoff is implied.

Keep project-specific Termination fields when updating or replacing footprints.
restored_fields.json records the added selections; validation.json records
the current check results. No historical CSV export is retained.
