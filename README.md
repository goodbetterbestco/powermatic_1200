# Powermatic 1200 Controls Retrofit

Rev P is the current contactor-based design. Operator controls use 24 VDC; motor-power switching is in the panel enclosure. Schematic, layout and commissioning work remain open.

## Active files

- [BOM](BOM_other.csv): project requirements and purchasing quantities. `BOM_jlcpcb.csv` is reserved for a separate JLCPCB BOM when needed.
- [KiCad project](kicad/powermatic_1200/powermatic_1200.kicad_pro)
- [Schematic](kicad/powermatic_1200/powermatic_1200.kicad_sch)
- [Wiring standard](docs/WIRING_STANDARD.md)
- [Signal names](docs/SIGNAL_NAMING.md)
- [Saved wire schedule](docs/Wire_schedule.csv)
- [Wire length totals](docs/Wire_length_totals.csv)
- [BOM quantity review](docs/BOM_quantity_review_2026-10-19.md)

## Project Review

Double-click **Project Review.app** to launch the separate [bom_review editor](https://github.com/goodbetterbestco/bom_review), installed at `~/Projects/bom_review`. Use **Documents** to select a CSV in this project root. **Overwrite** saves the selected document; **Save file** downloads a copy. Refresh reloads the selected saved CSV.

`QUA` is the project requirement in pieces or feet. `PACK` is the amount per purchase unit, `ORDER` is the number of purchase units, and `COST` is the price per purchase unit. `LINE = ORDER × COST`. GBB items are on hand and keep `ORDER = 0`. The CSV is manually reviewed; the launcher does not regenerate it from KiCad.

## Shared parts

Reusable symbols, footprints, models and datasheets belong in the sibling `_parts` repository. The enclosure selection is Hammond EN4SD30208GY with EP3020 backplate. Verify the saved schematic, board and physical fit independently before fabrication or procurement.

## Repository policy

See [AGENTS.md](AGENTS.md). Supporting documents belong in `docs/`; temporary tools, generated reviews and automatic backup folders are removed. Earlier scripts and reports remain available in Git history when previously committed.
