#!/usr/bin/env python3
"""Build the three remaining electrical Controls elevation footprints.

Projection caches come from unscaled manufacturer STEP files. The archived
models are attached unchanged; KiCad applies the recorded rigid transform.
"""
from pathlib import Path
import hashlib
import json
import math
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = Path.home()/'Projects/_parts/footprints/Controls.pretty'
PARTS = Path.home() / 'Projects/_parts'
CONFIG = json.loads((HERE / 'config.json').read_text())


def fmt(v):
    return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v) > .0000005 else '0'


def xy(p):
    return ' '.join(fmt(v) for v in p)


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def build(spec):
    cx, cy = spec['projection_center']
    up = cross(spec['normal'], spec['right'])
    def project(p):
        return [dot(p, spec['right'])-cx, -dot(p, up)-cy]
    shapes = []
    seen = set()
    for kind, points in json.loads((HERE / 'sources' / spec['projection']).read_text()):
        pts = tuple(tuple(round(v, 6) for v in [p[0]-cx, p[1]-cy]) for p in points)
        if kind == 'line' and pts[0] == pts[1]:
            continue
        key = (kind, pts if kind == 'circle' else min(pts, tuple(reversed(pts))))
        if key in seen:
            continue
        seen.add(key)
        shapes.append((kind, pts))
    pads = [{'number': number, 'source_xyz_mm': p, 'center_mm': project(p)} for number, p in spec['pads']]
    # Pads mark true physical projected centers; none of these parts needs fan-out.
    for i, a in enumerate(pads):
        for b in pads[i+1:]:
            assert math.dist(a['center_mm'], b['center_mm']) > CONFIG['pad_mm']+.1
    extent = max(abs(p[1]) for _, pts in shapes for p in pts)
    text_y = math.ceil((extent+2)/1.27)*1.27
    name = spec['part']+'_Front'
    lines = [f'(footprint "{name}"', '  (version 20241229)',
             '  (generator "pcbnew")', '  (generator_version "9.0")', '  (layer "F.Cu")',
             f'  (descr "{spec["part"]} panel-layout front elevation")',
             '  (tags "Controls panel elevation")', '  (attr exclude_from_pos_files)',
             f'  (property "Reference" "REF**" (at 0 {fmt(-text_y)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))',
             f'  (property "Value" "{name}" (at 0 {fmt(text_y)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))']
    for kind, pts in shapes:
        if kind == 'line':
            coords = f'(start {xy(pts[0])}) (end {xy(pts[1])})'
        elif kind == 'arc':
            coords = f'(start {xy(pts[0])}) (mid {xy(pts[1])}) (end {xy(pts[2])})'
        else:
            coords = f'(center {xy(pts[0])}) (end {xy(pts[1])})'
        lines.append(f'  (fp_{kind} {coords} (stroke (width 0.05) (type solid))'+
                     (' (fill none)' if kind == 'circle' else '')+' (layer "Dwgs.User"))')
    for p in pads:
        lines.append(f'  (pad "{p["number"]}" thru_hole circle (at {xy(p["center_mm"])}) '
                     f'(size {CONFIG["pad_mm"]} {CONFIG["pad_mm"]}) (drill {CONFIG["drill_mm"]}) (layers "*.Cu" "*.Mask"))')
    lines += [f'  (model "${{PARTS_LIB}}/3dmodels/Controls/{spec["model"]}"',
              f'    (offset (xyz {xy(spec["offset"])}))', '    (scale (xyz 1 1 1))',
              f'    (rotate (xyz {xy(spec["rotation"])})))', ')', '']
    path = LIB / (name+'.kicad_mod')
    path.write_text('\n'.join(lines))
    subprocess.run(['/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9',
                    str(HERE.parent/'label_references.py'), str(path), '--write'], check=True)
    return dict(spec, name=name, pads=pads, graphics_count=len(shapes),
                model_sha256=hashlib.sha256((PARTS/'3dmodels/Controls'/spec['model']).read_bytes()).hexdigest(),
                footprint_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    review = [build(spec) for spec in CONFIG['parts']]
    (HERE/'geometry_review.json').write_text(json.dumps(review, indent=2)+'\n')
    for r in review:
        print(r['name'], len(r['pads']), 'pads;', r['graphics_count'], 'graphics')
