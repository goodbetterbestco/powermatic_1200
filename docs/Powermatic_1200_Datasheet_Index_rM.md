# Powermatic 1200 Rev M datasheet collection

The shared `_parts` repository contains the authoritative PDFs and KiCad references.

- [Complete 30-part document index](../../../_parts/datasheets/Controls_Datasheet_Index.md)
- [Source URLs, retrieval dates and SHA-256 hashes](../../../_parts/database/non_lcsc_datasheet_sources.json)
- [Shared Controls symbol library](../../../_parts/symbols/Controls.kicad_sym)
- [Terminal review, pin maps and KiCad checklist](../../../_parts/reviews/Controls/README.md)

The collection contains 28 original PDFs: 26 identify the exact part directly or within a family document, and 2 are partial references (E-stop contact blocks and Bulletin 365 drum-switch family). The Furnas contactor and unselected enclosure fan remain pending. The retained motor is an additional symbol outside the 30 BOM part types.

The terminal review adds 13 manufacturer wiring/manual PDFs and populates 27 of the 31 Controls symbols with 220 pins. All 44 symbol units were parsed and visually inspected in KiCad. The Furnas contactor, drum switch, fan and retained motor remain pinless pending exact terminal documentation. Two populated maps are partial (C2-14D2 and ICF12L45N08M1IO); provisional terminal IDs and the design-defined E-stop assembly mapping are called out in the review.

The review also records the GMC5 voltage-rating and XB4BD21 contact-configuration discrepancies. The BH5928 manual defines S31 as an input, conflicting with the channel-2 source description on wire 43; the symbol follows the manufacturer and the circuit needs a separate review. No simulation models or machine wiring changes are included.
