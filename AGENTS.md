# Project file policy

- Allowed root documents: `BOM_jlcpcb.csv`, `BOM_other.csv`, `AGENTS.md`, `README.md`.
- `Project Review.app` is the root launcher for the separate `~/Projects/bom_review` app.
- Keep all other project documents in `docs/`. Keep native KiCad source files in `kicad/`.
- Keep software and temporary scripts out of this hardware repository. Retrieve old tools from Git when needed.
- Do not retain `powermatic_1200-backups/`, `output/`, `outputs/`, or `reviews/` directories.
- BOM `QUA` is the required number of pieces or feet. `PACK` is the amount per purchase unit. `ORDER` is purchase units. `LINE = ORDER × COST`. GBB items are on hand and retain `ORDER = 0`.
- Keep loose-wire `QUA` in feet to one decimal place, rounding upward so the saved requirement covers the calculated length.
- Audit the saved design before changing BOM quantities. Identify deviations before applying uncertain corrections.
- Preserve unrelated placement, routing, and local edits. Prefer native files and command-line checks over screen sharing.
