#!/usr/bin/env python3
"""Build the owner-measured Furnas station's top-view panel wiring footprint.

Keep the colored source STEP unchanged. Its front already faces +Z; translate
the mounting face to Z=0 and center the station in X/Y with the model offset.
Pads are logical wire targets, not PCB manufacturing holes.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil

from OCP.STEPControl import STEPControl_Reader
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.gp import gp_Trsf, gp_Vec

HERE = Path(__file__).resolve().parent
NAME = '50MA3KLE_Top'
MODEL = 'Furnas_50MA3KLE.step'
OFFSET = [70, 0, 89.4]


def load(path):
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    return reader.OneShape()


def translated(shape):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(*OFFSET))
    return BRepBuilderAPI_Transform(shape, transform, True).Shape()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--inspection', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--top-contact', choices=['NO', 'NC'], required=True)
    args = parser.parse_args()
    inspection = json.loads((args.inspection / 'named-shapes.json').read_text())
    circles = json.loads((args.inspection / 'screw-circles.json').read_text())
    shape = translated(load(args.source))
    assert BRepCheck_Analyzer(shape).IsValid()
    spec = importlib.util.spec_from_file_location('projection', HERE.parent / 'left_wall/assembly/build.py')
    projection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(projection)
    spec = importlib.util.spec_from_file_location('graphics', HERE.parent / 'drum_switch/build.py')
    graphics = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graphics)
    bounds = graphics.bounds(shape)
    assert abs(bounds[0][2]) < 1e-6
    properties = {'Reference': 'REF**', 'Value': NAME, 'MPN': '50MA3KLE',
                  'Manufacturer': 'Furnas', 'Part Name': 'Button\nStation',
                  'Mounting': 'machine', 'Category': 'switch',
                  'Package': 'Machine-mounted pushbutton station 52 x 116 x 44.7 mm',
                  'Datasheet': '', 'Description': 'Vintage forward/reverse/stop pushbutton station; forward and reverse each 1NO+1NC, stop 1NC.'}
    lines = [f'(footprint "{NAME}" (version 20260206) (generator "pcbnew")',
             ' (generator_version "10.0") (layer "F.Cu")',
             ' (descr "Furnas 50MA3KLE machine-mounted station, 10 screw terminals, 52 x 116 x 44.7 mm assembly; approved owner-STEP-derived top elevation and logical wiring targets")',
             ' (tags "Furnas 50MA3KLE 10-terminal 52x116mm machine-mounted top-elevation")',
             ' (attr exclude_from_pos_files)']
    for name, value in properties.items():
        visible = name == 'Reference'
        lines.append(f' (property {json.dumps(name)} {json.dumps(value)} '
                     f'(at 0 {-7.5 if visible else 0} 0) '
                     f'(layer "{"F.SilkS" if visible else "F.Fab"}")'
                     f'{"" if visible else " (hide yes)"} '
                     f'(effects (font (size {2.5 if visible else 1} {2.5 if visible else 1}) (thickness 0.15))))')
    lines += graphics.graphics(projection.project(shape), 'F.Fab', .05)
    outline = [(-26, -58), (26, -58), (26, 58), (-26, 58)]
    points = ' '.join(f'(xy {x} {y})' for x, y in outline)
    lines.append(f' (fp_poly (pts {points}) (stroke (width 0) (type solid)) (fill solid) (layer "F.Adhes"))')
    pads = []
    nc, no = ('T', 'B') if args.top_contact == 'NC' else ('B', 'T')
    # Physical terminal IDs follow the owner's named STEP screws.
    contacts = [(f'{section}{tier}', section, tier) for section in range(1, 5)
                for tier in [nc, no]] + [('5T', 5, 'T'), ('6T', 6, 'T')]
    for number, section, tier in contacts:
        screw = f'screw_{section}{tier}'
        rims = [feature for feature in circles[screw] if abs(feature[0] - 4.053989) < 1e-5]
        assert len(rims) == 1, (screw, rims)
        source = rims[0][1]
        center = [source[i] + OFFSET[i] for i in range(3)]
        pads.append({'number': number, 'model_screw': screw,
                     'source_head_rim_center_mm': source,
                     'model_head_rim_center_mm': center,
                     'pad_center_mm': [center[0], -center[1]]})
        lines.append(f' (pad "{number}" thru_hole circle (at {center[0]} {-center[1]}) (size 3 3) (drill 2) (layers "*.Cu" "*.Mask"))')
    # Match the reviewed Q1-style device artwork; preserve the detailed Fab.
    spec = importlib.util.spec_from_file_location('switch_art', HERE.parent / 'artwork_review/build.py')
    art = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(art)
    spec = importlib.util.spec_from_file_location('switch_layers', HERE.parent / 'artwork_review/stage.py')
    layers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layers)
    ref = "S2"
    silk, _ = art.make_curves(ref, args.source)
    targets = [['pad', row['number'], ['at', *row['pad_center_mm']], ['size', 3, 3]] for row in pads]
    silk = layers.clip(silk, targets)
    lines += layers.graphics(silk, 'library:' + NAME)
    lines.append(f' (model "${{PARTS_LIB}}/3dmodels/Controls/{MODEL}" (offset (xyz 70 0 89.4)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    lines += [')', '']
    model_dir = args.output / '3dmodels/Controls'
    fp_dir = args.output / 'footprints/Controls.pretty'
    model_dir.mkdir(parents=True, exist_ok=True)
    fp_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.source, model_dir / MODEL)
    (fp_dir / (NAME + '.kicad_mod')).write_text('\n'.join(lines))
    report = {'source': str(args.source), 'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'source_preserved_byte_identical': True, 'model_valid': True, 'solid_count': 35,
              'footprint': 'Controls:' + NAME, 'bounds_mm': bounds,
              'size_mm': [bounds[1][i] - bounds[0][i] for i in range(3)],
              'offset_mm': OFFSET, 'rotation_deg': [0, 0, 0], 'scale': [1, 1, 1],
              'top_contact': args.top_contact, 'pads': pads, 'position_mm': [600, 120]}
    (args.output / 'geometry.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['footprint', 'bounds_mm', 'top_contact']}))


if __name__ == '__main__':
    main()
