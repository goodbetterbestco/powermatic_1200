# Powermatic 1200 Controls Retrofit

Rev P is the current contactor-based design. Operator controls use 24 VDC; motor-power switching is in the panel enclosure. Schematic, layout and commissioning work remain open.

Backplate layout and DIN-rail/wire-duct installation are complete, as reported on 2026-10-27. All 20 mounting holes were drilled and tapped 10-24; the specified 10-24 fasteners worked well. See the [installation record](docs/Backpanel_screw_locations_source.md#installation-record--2026-10-27).

Modules and terminal blocks are placed, as reported on 2026-10-28. Terminal labels use module number + letter, skipping I/O, with G1-G6 for grounding blocks. Jumper installation is the next assembly step.

## Active files

- [BOM](BOM_other.csv): project requirements and purchasing quantities. `BOM_jlcpcb.csv` is reserved for a separate JLCPCB BOM when needed.
- [KiCad project](kicad/powermatic_1200/powermatic_1200.kicad_pro)
- [Schematic](kicad/powermatic_1200/powermatic_1200.kicad_sch)
- [Wiring standard](docs/WIRING_STANDARD.md)
- [Signal names](docs/SIGNAL_NAMING.md)
- [Terminal numbering and legacy cross-reference](docs/Terminal_numbering.md)
- [11 x 17 terminal jumper guide](docs/Terminal_jumper_installation_guide.pdf)
- [DIN-rail module layout](docs/DIN_rail_module_layout.pdf)
- [Saved wire schedule](docs/Wire_schedule.csv)
- [Wire length totals](docs/Wire_length_totals.csv)
- [BOM quantity review](docs/BOM_quantity_review_2026-10-19.md)

## Project Review

Double-click **Project Review.app** to launch the separate [bom_review editor](https://github.com/goodbetterbestco/bom_review), installed at `~/Projects/bom_review`. **Documents** lists root CSVs plus the saved wire schedule and wire-length totals in `docs/`. **Overwrite** saves the selected document; **Save file** downloads a copy. For **Wire_schedule.csv**, **Refresh** regenerates the schedule and length totals from saved KiCad; for other documents it reloads the saved CSV. The extractor and project configuration live in `~/Projects/bom_review/adapters/powermatic_1200/`, outside this hardware repository.

`QUA` is the project requirement in pieces or feet. `PACK` is the amount per purchase unit, `ORDER` is the number of purchase units, and `COST` is the price per purchase unit. `LINE = ORDER × COST`. GBB items are on hand and keep `ORDER = 0`. The CSV is manually reviewed; the launcher does not regenerate it from KiCad.

`FLAG` and `FLAG DESCRIPTION` retain the review selection and its document-wide description in the CSV. The app displays them through the checkbox and Description controls. Use **Overwrite** to save changes; reopening or Refresh restores the saved flags. Flags indicate the purpose stated in Description and do not change purchasing quantities.

## Shared parts

Reusable symbols, footprints, models and datasheets belong in the sibling `_parts` repository. The enclosure selection is Hammond EN4SD30208GY with EP3020 backplate. Verify the saved schematic, board and physical fit independently before fabrication or procurement.

## Repository policy

See [AGENTS.md](AGENTS.md). Supporting documents belong in `docs/`; temporary tools, generated reviews and automatic backup folders are removed. Earlier scripts and reports remain available in Git history when previously committed.
