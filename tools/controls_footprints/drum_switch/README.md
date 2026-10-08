# S3 drum-switch model and footprint

The owner supplied a measured STEP with all sixteen screws named. The installed footprint is `Controls:365-TAV2111_Top`, linked to the unchanged `AB_365-TAV2111.step` in the shared parts library. Review and checkpoints: `reviews/S3_model_2026-10-07/`.

The scripts build/stage only. `inspect.py` and `build.py` require OCP 8; `place.py` requires KiCad's bundled Python. `stage.py` and `validate.py` use Python's standard library. Stage in a writable temporary directory; save/pause KiCad before installing. Inspect and rebuild from the labelled source:

```sh
python inspect.py --source /path/to/labelled.step --output /private/tmp/s3-inspection
python build.py --source /path/to/labelled.step --inspection /private/tmp/s3-inspection/named-shapes.json --circles /private/tmp/s3-inspection/screw-circles.json --output /private/tmp/powermatic-s3-model/assets
python stage.py --work /private/tmp/powermatic-s3-model
```

Export the candidate schematic netlist to the staging directory, then run `place.py --work <stage> --netlist <xml>`. Placement defaults to X=600, Y=231.241 mm and preserves every existing PCB record. `validate.py` checks the staged project and catalog data before installation. The native alignment check uses the staged S3-only component export and board datum export, with the original pin-net snapshot retained in `/private/tmp/ab365-current-netlist.xml`. The review JSONs remain useful evidence after temporary intermediates are removed; rerun inspection to regenerate any discarded per-solid temporary copies.

Pads are logical panel-wiring targets, not a drill pattern. Source T/B labels correspond to the saved schematic U/L terminal IDs. The STEP has a Z=0 base and a unity, zero-offset footprint model transform. Existing schematic termination fields remain intact pending the S2/S3 migration.

Current device artwork uses F.Silkscreen; the complete source detail remains
on F.Fab. Dwgs.User is reserved for enclosure/backplate/duct/rail information,
and Cmts.User is empty. The shared Q1-style recipes, clipping and native
review evidence are in `../artwork_review/` and
`reviews/artwork_layers_2026-10-08/`.
