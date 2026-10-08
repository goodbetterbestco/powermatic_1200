#!/usr/bin/env python3
"""Build S3's top-view wiring footprint from the owner's labelled STEP.

The STEP stays byte-identical. Pads are panel-layout wiring targets, not a
manufacturing drill pattern. Run with OCP 8 and provide the inspection JSONs.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import shutil

from OCP.STEPControl import STEPControl_Reader
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer

HERE = Path(__file__).resolve().parent
NAME = '365-TAV2111_Top'
MODEL = 'AB_365-TAV2111.step'
FAN_RADIUS = 6.0


def bounds(shape):
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    return [list(box.CornerMin().Coord()), list(box.CornerMax().Coord())]


def fmt(value):
    return f'{value:.6f}'.rstrip('0').rstrip('.') if abs(value) > 5e-7 else '0'


def xy(point):
    return ' '.join(fmt(value) for value in point)


def graphics(curves, layer, width):
    output = []
    for kind, points in curves:
        if kind == 'line':
            coordinates = f'(start {xy(points[0])}) (end {xy(points[1])})'
        elif kind == 'arc':
            coordinates = (f'(start {xy(points[0])}) (mid {xy(points[1])}) '
                           f'(end {xy(points[2])})')
        else:
            coordinates = f'(center {xy(points[0])}) (end {xy(points[1])})'
        fill = ' (fill none)' if kind == 'circle' else ''
        output.append(f' (fp_{kind} {coordinates} (stroke (width {width}) '
                      f'(type solid)){fill} (layer "{layer}"))')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--inspection', type=Path, required=True)
    parser.add_argument('--circles', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    model_dir = args.output / '3dmodels/Controls'
    footprint_dir = args.output / 'footprints/Controls.pretty'
    model_dir.mkdir(parents=True, exist_ok=True)
    footprint_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.source, model_dir / MODEL)
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(args.source)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    shape = reader.OneShape()
    assert BRepCheck_Analyzer(shape).IsValid()
    envelope = bounds(shape)
    assert abs(envelope[0][2]) < 1e-7, 'Owner model must mount at Z=0.'
    solids = TopExp_Explorer(shape, TopAbs_SOLID)
    count = 0
    while solids.More():
        count += 1
        solids.Next()
    assert count == 46
    inspection = json.loads(args.inspection.read_text())
    assert len(inspection['solids']) == count
    assert all(row['valid'] for row in inspection['solids'])
    circles = json.loads(args.circles.read_text())
    assert set(circles) == {f'screw_{section}{tier}'
                            for section in range(1, 9) for tier in ['T', 'B']}
    # The 4.053989 mm rim is a physical circular edge of every screw head.
    # Some larger circles are construction/slot curves, not the head rim.
    heads = {}
    for label, features in circles.items():
        rim = [feature for feature in features if abs(feature[0] - 4.053989) < 1e-5]
        assert len(rim) == 1, (label, rim)
        heads[label] = rim[0][1]
    pads = []
    for section in range(1, 9):
        upper, lower = heads[f'screw_{section}T'], heads[f'screw_{section}B']
        assert abs(upper[0] - lower[0]) < 1e-6
        center = [upper[0], -(upper[1] + lower[1]) / 2]
        for tier, source, sign in [('U', upper, -1), ('L', lower, 1)]:
            pads.append({'number': f'{section}.{tier}',
                         'model_screw': f'screw_{section}{"T" if tier == "U" else "B"}',
                         'source_head_rim_center_mm': source,
                         'true_projected_center_mm': [source[0], -source[1]],
                         'fan_center_mm': center,
                         'pad_center_mm': [center[0] + sign * FAN_RADIUS, center[1]]})
    for index, pad in enumerate(pads):
        for other in pads[index + 1:]:
            assert math.dist(pad['pad_center_mm'], other['pad_center_mm']) >= 4.99
    module_path = HERE.parent / 'left_wall/assembly/build.py'
    spec = importlib.util.spec_from_file_location('controls_projection', module_path)
    projection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(projection)
    curves = projection.project(shape)
    properties = {'Reference': 'REF**', 'Value': NAME, 'Datasheet': '',
                  'Description': '', 'MPN': '365-TAV2111',
                  'Manufacturer': 'Allen-Bradley', 'Part Name': 'Speed\nSwitch',
                  'Mounting': 'machine'}
    lines = [f'(footprint "{NAME}" (version 20260206) (generator "pcbnew")',
             ' (generator_version "10.0") (layer "F.Cu")',
             ' (descr "Allen-Bradley 365-TAV2111 owner-measured top view; '
             '156 x 73 x 75 mm assembly, 16 logical terminal targets; '
             '6 mm symmetric fan-out for overlapping screw rows; base Z=0")',
             ' (tags "Allen-Bradley 365-TAV2111 16-terminal machine top view")',
             ' (attr exclude_from_pos_files)']
    for name, value in properties.items():
        visible = name == 'Reference'
        position = [10.5, -31.75] if visible else [0, 0]
        layer = 'F.SilkS' if visible else 'F.Fab'
        hidden = '' if visible else ' (hide yes)'
        size = 2.5 if visible else 1
        lines.append(f' (property {json.dumps(name)} {json.dumps(value)} '
                     f'(at {xy(position)} 0) (layer "{layer}"){hidden} '
                     f'(effects (font (size {size} {size}) (thickness 0.15))))')
    lines += graphics(curves, 'F.Fab', 0.05)
    # Opaque display envelope, following the case and the protruding shaft.
    outline = [[-67.5, -36.5], [67.5, -36.5], [67.5, -3.625],
               [88.5, -3.625], [88.5, 3.625], [67.5, 3.625],
               [67.5, 36.5], [-67.5, 36.5]]
    points = ' '.join(f'(xy {xy(point)})' for point in outline)
    lines.append(f' (fp_poly (pts {points}) (stroke (width 0) (type solid)) '
                 '(fill solid) (layer "F.Adhes"))')
    for pad in pads:
        source = pad['source_head_rim_center_mm']
        # Preserve the actual projected screw geometry beside the fan-out targets.
        radius = 4.053989
        # Upper screw-head axes are parallel to Z; these circles are exact.
        lines.append(f' (pad "{pad["number"]}" thru_hole circle '
                     f'(at {xy(pad["pad_center_mm"])}) (size 3 3) '
                     '(drill 2) (layers "*.Cu" "*.Mask"))')
    # Match the reviewed Q1-style device artwork; preserve the detailed Fab.
    spec = importlib.util.spec_from_file_location('switch_art', HERE.parent / 'artwork_review/build.py')
    art = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(art)
    spec = importlib.util.spec_from_file_location('switch_layers', HERE.parent / 'artwork_review/stage.py')
    layers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layers)
    ref = "S3"
    silk, _ = art.make_curves(ref, args.source)
    targets = [['pad', row['number'], ['at', *[float(fmt(v)) for v in row['pad_center_mm']]], ['size', 3, 3]] for row in pads]
    silk = layers.clip(silk, targets)
    lines += layers.graphics(silk, 'library:' + NAME)
    lines += [f' (model "${{PARTS_LIB}}/3dmodels/Controls/{MODEL}" '
              '(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))', ')', '']
    (footprint_dir / (NAME + '.kicad_mod')).write_text('\n'.join(lines))
    report = {'source': str(args.source),
              'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'model': str(model_dir / MODEL), 'model_is_byte_identical': True,
              'footprint': 'Controls:' + NAME, 'bounds_mm': envelope,
              'size_mm': [envelope[1][i] - envelope[0][i] for i in range(3)],
              'model_solids': count, 'model_valid': True,
              'model_transform': {'offset': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': [1, 1, 1]},
              'projected_primitives': len(curves), 'pads': pads,
              'pad_mapping': 'Source screw_NT -> N.U; screw_NB -> N.L',
              'fan_out_radius_mm': FAN_RADIUS,
              'placement_mm': [600, 231.241],
              'enclosure_right_edge_mm': 484.759,
              'model_left_edge_mm': 532.5,
              'clearance_to_enclosure_mm': 47.741}
    (args.output / 'geometry.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['footprint', 'size_mm', 'model_solids',
                                                 'projected_primitives', 'placement_mm']}, indent=2))


if __name__ == '__main__':
    main()
