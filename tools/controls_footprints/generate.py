#!/usr/bin/env python3
"""Extract reviewed supplier elevations without rescaling their dimensions.

Requires ezdxf. Run from any directory. See README.md for the review boundary.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import os
import subprocess

os.environ.setdefault('XDG_CACHE_HOME', '/tmp/powermatic-cache')
import ezdxf
from ezdxf.math import Vec3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LIB = Path.home()/'Projects/_parts/footprints/Controls.pretty'
CONFIG = json.loads((HERE / 'config.json').read_text())


def fmt(x):
    return f'{x:.6f}'.rstrip('0').rstrip('.') if abs(x) > 0.0000005 else '0'


def xy(p):
    return ' '.join(fmt(v) for v in p)


def fan_out(pads, diameter):
    """Displace only coincident wiring targets; never move physical graphics."""
    groups = {}
    for pad in pads:
        groups.setdefault(tuple(round(v, 3) for v in pad['true_center_mm']), []).append(pad)
    for group in groups.values():
        if len(group) == 1:
            group[0]['center_mm'] = group[0]['true_center_mm'][:]
            continue
        n = len(group)
        screw_radius = max(p.get('screw_radius_mm', 2.5) for p in group)
        radius = max(screw_radius + diameter / 2 + .3,
                     (diameter + .3) / (2 * math.sin(math.pi / n)))
        for i, pad in enumerate(group):
            angle = math.pi + i * math.pi if n == 2 else -math.pi / 2 + i * 2 * math.pi / n
            x, y = pad['true_center_mm']
            pad['center_mm'] = [x + radius * math.cos(angle), y + radius * math.sin(angle)]
            pad['fan_out_radius_mm'] = radius


def generate(spec):
    output = LIB / (spec['name'] + '.kicad_mod')
    if spec.get('preserve_existing'):
        assert output.exists(), 'The approved sample must already exist'
        return {'name': spec['name'], 'part': spec['part'], 'preserved': True,
                'size_mm': spec['size_mm'], 'expected_pads': spec['expected_pads'],
                'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
    bmin, bmax = spec['bounds']
    cx, cy = [(a + b) / 2 for a, b in zip(bmin[:2], bmax[:2])]
    scale = spec['scale']
    rotate = math.radians(spec['rotation_deg'])

    def point(p):
        x, y = (p[0] - cx) * scale, (cy - p[1]) * scale
        return [round(x * math.cos(rotate) - y * math.sin(rotate), 6),
                round(x * math.sin(rotate) + y * math.cos(rotate), 6)]

    shapes = []
    seen = set()
    counts = Counter()

    def add(kind, points):
        pts = tuple(tuple(point(p)) for p in points)
        if kind == 'line' and pts[0] == pts[1]:
            counts['zero_length_removed'] += 1
            return
        key = (kind, pts if kind == 'circle' else min(pts, tuple(reversed(pts))))
        if key in seen:
            counts['duplicate_primitives_removed'] += 1
            return
        seen.add(key)
        shapes.append((kind, pts))

    def convert(entity):
        kind = entity.dxftype()
        if kind == 'LINE':
            add('line', [entity.dxf.start, entity.dxf.end])
        elif kind == 'ARC':
            assert entity.dxf.extrusion.isclose(Vec3(0, 0, 1))
            start = entity.dxf.start_angle
            span = (entity.dxf.end_angle - start) % 360
            add('arc', list(entity.vertices([start, start + span / 2, start + span])))
        elif kind == 'CIRCLE':
            add('circle', [entity.dxf.center, entity.dxf.center + Vec3(entity.dxf.radius, 0, 0)])
        elif kind in ('LWPOLYLINE', 'POLYLINE'):
            for child in entity.virtual_entities():
                convert(child)
        elif kind == 'SPLINE':
            spline = entity.construction_tool()
            if entity.dxf.degree == 3 and not len(entity.weights):
                for cp in spline.bezier_decomposition():
                    assert len(cp) == 4
                    add('curve', cp)
            else:
                pts = list(spline.flattening(.001 / scale))
                for a, b in zip(pts, pts[1:]):
                    add('line', [a, b])
                counts['flattened_splines'] += 1
        elif kind == 'ELLIPSE':
            ellipse = entity.construction_tool()
            n = max(1, math.ceil(ellipse.param_span / (math.pi / 8)))
            def pos(t):
                return ellipse.center + ellipse.major_axis * math.cos(t) + ellipse.minor_axis * math.sin(t)
            def tangent(t):
                return -ellipse.major_axis * math.sin(t) + ellipse.minor_axis * math.cos(t)
            for i in range(n):
                t0 = ellipse.start_param + ellipse.param_span * i / n
                t1 = ellipse.start_param + ellipse.param_span * (i + 1) / n
                k = 4 / 3 * math.tan((t1 - t0) / 4)
                add('curve', [pos(t0), pos(t0) + k * tangent(t0),
                              pos(t1) - k * tangent(t1), pos(t1)])
        else:
            raise ValueError(f'Unsupported selected entity: {kind}')

    if 'projection' in spec:
        for kind, points in json.loads((HERE / spec['projection']).read_text()):
            add(kind, points)
    else:
        doc = ezdxf.readfile(ROOT / (spec['part'] + '.dxf'))
        assert (doc.units == 1 and scale == 25.4) or (doc.units == 4 and scale == 1)
        for handle in spec['handles']:
            convert(doc.entitydb[handle])

    width, height = [(b - a) * scale for a, b in zip(bmin[:2], bmax[:2])]
    if spec['rotation_deg'] == 90:
        width, height = height, width
    pads = [dict(p, true_center_mm=point(p['source_center'])) for p in spec['pads']]
    diameter = CONFIG['pad_diameter_mm']
    fan_out(pads, diameter)
    text_edge = max([height / 2 + .025] +
                    [abs(p['center_mm'][1]) + diameter / 2 for p in pads])
    text_y = math.ceil((text_edge + .5) / 1.27) * 1.27
    assert len({p['number'] for p in pads}) == len(pads)
    for i, a in enumerate(pads):
        for b in pads[i + 1:]:
            assert math.dist(a['center_mm'], b['center_mm']) > diameter + .1, (spec['name'], a, b)

    lines = [f'(footprint "{spec["name"]}"', '  (version 20241229)',
             '  (generator "pcbnew")', '  (generator_version "9.0")', '  (layer "F.Cu")',
             f'  (descr "{spec["part"]} panel-layout elevation; {width:.3f} x {height:.3f} mm")',
             '  (tags "Controls panel elevation review")',
             '  (attr board_only exclude_from_pos_files exclude_from_bom)',
             f'  (property "Reference" "REF**" (at 0 {fmt(-text_y)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))',
             f'  (property "Value" "{spec["name"]}" (at 0 {fmt(text_y)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))']
    for kind, pts in shapes:
        if kind == 'line':
            coords = f'(start {xy(pts[0])}) (end {xy(pts[1])})'
        elif kind == 'arc':
            coords = f'(start {xy(pts[0])}) (mid {xy(pts[1])}) (end {xy(pts[2])})'
        elif kind == 'circle':
            coords = f'(center {xy(pts[0])}) (end {xy(pts[1])})'
        else:
            coords = '(pts ' + ' '.join('(xy ' + xy(p) + ')' for p in pts) + ')'
        lines.append(f'  (fp_{kind} {coords} (stroke (width 0.05) (type solid))' +
                     (' (fill none)' if kind == 'circle' else '') + ' (layer "Dwgs.User"))')
    for pad in pads:
        lines.append(f'  (pad "{pad["number"]}" thru_hole circle (at {xy(pad["center_mm"])}) '
                     f'(size {fmt(diameter)} {fmt(diameter)}) (drill {fmt(CONFIG["drill_mm"])}) (layers "*.Cu" "*.Mask"))')
    output.write_text('\n'.join(lines + [')', '']))
    subprocess.run(['/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9',
                    str(HERE/'label_references.py'), str(output), '--write'], check=True)
    return {'name': spec['name'], 'part': spec['part'], 'size_mm': [width, height],
            'source_center': [cx, cy], 'rotation_deg': spec['rotation_deg'],
            'source_kind': 'STEP visible-edge projection' if 'projection' in spec else 'DXF selected elevation',
            'shapes': dict(Counter(k for k, _ in shapes)), 'cleanup': dict(counts),
            'pads': pads, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    LIB.mkdir(exist_ok=True)
    for part, evidence in CONFIG['parts'].items():
        assert hashlib.sha256((ROOT / (part + '.dxf')).read_bytes()).hexdigest() == evidence['dxf_sha256'], part
        for check in evidence['checks']:
            check['delta_mm'] = check['measured_mm'] - check['published_mm']
            # This is agreement with printed decimal rounding, not a part tolerance.
            check['within_drawing_rounding'] = abs(check['delta_mm']) <= .05001
            assert check['within_drawing_rounding'], (part, check)
    results = []
    for spec in CONFIG['footprints']:
        result = generate(spec)
        results.append(result)
        print(result['name'], [round(v, 3) for v in result['size_mm']], flush=True)
    (HERE / 'dimension_review.json').write_text(json.dumps(
        {'purpose': CONFIG['purpose'], 'parts': CONFIG['parts'], 'footprints': results}, indent=2) + '\n')
