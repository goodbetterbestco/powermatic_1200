# Powermatic 1200 Controls Retrofit

Rev P is the current contactor-based design. Operator controls use 24 VDC; motor-power switching is in the panel enclosure. Schematic, layout and commissioning work remain open.

Backplate layout and DIN-rail/wire-duct installation are complete, as reported on 2026-10-27. All 20 mounting holes were drilled and tapped 10-24; the specified 10-24 fasteners worked well. See the [installation record](docs/WIRING_STANDARD.md#current-document-set---2026-11-09).

Modules and terminal blocks were reported placed on 2026-10-28. The 2026-10-30 saved layout places FH1 at the lower rail’s right end, after 5K, G4 and the existing end stop. Incoming phase blocks 4E/4F/4G are removed; the cable phases now terminate directly at FH1. G4 remains. The mains entry is on the right wall; the two alternate right-face motor/control holes are recorded in the enclosure drawing. Two McMaster 9357K15 gasketed plugs with hex retaining nuts cover the unused motor/control pair. Terminal labels use module number + letter, skipping I/O, with G1-G6 for grounding blocks. Jumper installation is the next assembly step.

## Active files

- [BOM](BOM_other.csv): project requirements and purchasing quantities. `BOM_jlcpcb.csv` is reserved for a separate JLCPCB BOM when needed.
- [KiCad project](kicad/powermatic_1200/powermatic_1200.kicad_pro) and [schematic](kicad/powermatic_1200/powermatic_1200.kicad_sch).

The `docs/` folder contains eight essential files:

- [Panel drawings](docs/Panel_drawings.pdf): module layout, terminal jumpers and markers, approved backpanel drilling sheet, and enclosure holes. The enclosure sheet is PDF page 6; print it at 96% for 1:1 details. The earlier BB1/BB2 busbar artwork is superseded by the six K1/K2 wire jumpers in the wiring guide.
- [Wire installation guide](docs/Wire_installation_guide.pdf): labeling, connector identification and strip settings on PDF pages 2-5, followed by the 131-row installation checklist on pages 6-8.
- [Wiring standard and reference notes](docs/WIRING_STANDARD.md): wiring policy, installation sequence, terminal numbering, signal names, preparation sources, and the two supplemental pendant-jumper records.
- [Saved wire schedule](docs/Wire_schedule.csv): 129 native wires; the printable guide also includes two supplemental pendant jumpers.
- [Wire length totals](docs/Wire_length_totals.csv).
- [Connector inventory](docs/Wire_connector_bins.csv), [installation order](docs/Wire_installation_groups.json), and [termination-code mapping](docs/Wire_termination_types.json): required inputs for Project Review Refresh.

Refresh updates the saved schedule and wire totals. Rebuild and reconcile the PDF guide after changing the native wiring; Refresh does not rebuild it. Preserve the two supplemental pendant rows recorded in the wiring standard.

## Project Review

Double-click **Project Review.app** to launch the separate [bom_review editor](https://github.com/goodbetterbestco/bom_review), installed at `~/Projects/bom_review`. **Documents** lists root CSVs plus the saved wire schedule and wire-length totals in `docs/`. **Overwrite** saves the selected document; **Save file** downloads a copy. For **Wire_schedule.csv**, **Refresh** regenerates the schedule and length totals from saved KiCad; for other documents it reloads the saved CSV. The extractor and project configuration live in `~/Projects/bom_review/adapters/powermatic_1200/`, outside this hardware repository.

`QUA` is the project requirement in pieces or feet. `PACK` is the amount per purchase unit, `ORDER` is the number of purchase units, and `COST` is the price per purchase unit. `LINE = ORDER × COST`. GBB items are on hand and keep `ORDER = 0`. The CSV is manually reviewed; the launcher does not regenerate it from KiCad.

`FLAG` and `FLAG DESCRIPTION` retain the review selection and its document-wide description in the CSV. The app displays them through the checkbox and Description controls. Use **Overwrite** to save changes; reopening or Refresh restores the saved flags. Flags indicate the purpose stated in Description and do not change purchasing quantities.

## Shared parts

Reusable symbols, footprints, models and datasheets belong in the sibling `_parts` repository. The enclosure selection is Hammond EN4SD30208GY with EP3020 backplate. Verify the saved schematic, board and physical fit independently before fabrication or procurement.

## Repository policy

See [AGENTS.md](AGENTS.md). Supporting documents belong in `docs/`; temporary tools, generated reviews and automatic backup folders are removed. Earlier scripts and reports remain available in Git history when previously committed.
