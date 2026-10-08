# Cable metadata removal — 2026-10-07

Removed `Cable MPN`, `Cable cores` and `Cable OD mm` from PCB footprints J3, J4 and J5: nine properties total. The owner authorized removal following the saved/paused editor checkpoint established earlier in this chat.

The complete PCB S-expression tree is identical to the checkpoint after filtering only those three property names. Footprint placement, pads, nets, artwork, model transforms and all other fields are unchanged. The schematic contains none of these fields and was not edited. Cable documentation and shared library assets were not edited.

`before/` preserves the exact saved board before this edit; `validation.json` records hashes and the removed cable specifications.

The final saved PCB passed native KiCad parsing through a successful position export.
