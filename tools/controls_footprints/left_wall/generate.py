#!/usr/bin/env python3
"""Project-local left-wall views; run with cadquery-ocp installed."""
from pathlib import Path
import hashlib
import json
import math
import subprocess

from OCP.STEPControl import STEPControl_Reader
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Circle
from OCP.GCPnts import GCPnts_QuasiUniformDeflection

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = ROOT / 'kicad/powermatic_1200/Controls_Review.pretty'
PARTS = Path.home() / 'Projects/_parts'


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def fmt(x):
    return '0' if abs(x) < 0.0000005 else f'{x:.6f}'.rstrip('0').rstrip('.')


def xy(p):
    return ' '.join(map(fmt, p))


def source_specs():
    old = json.loads((HERE.parent/'alignment/config.json').read_text())['parts']
    sw = next(p for p in old if p['part'] == '22013003')
    yield dict(part=sw['part'], ref='SW1', model=sw['model'], right=[-1, 0, 0],
               normal=[0, 1, 0], rotation=[-90, 0, 180], axis_up=-1081.593859069632,
               terminals=[(p['number'], p['source_xyz_mm']) for p in sw['pads']],
               radius=6.0, height_from_top_mm=120)
    old = json.loads((HERE.parent/'additions/config.json').read_text())['parts']
    for part, ref in [('XB4BVB1', 'H1'), ('T4171310004-001', 'J1')]:
        p = next(p for p in old if p['part'] == part)
        terminals = p['pads']
        if ref == 'J1':
            # Same four contacts, at the modeled rear wire-tail stub ends.
            # These circular ends have the same X/Y coordinates as the contacts.
            terminals = [(number, [xyz[0], xyz[1], -22.4]) for number, xyz in terminals]
        yield dict(part=part, ref=ref, model=p['model'], right=[0, 0, -1],
                   normal=[1, 0, 0], rotation=[0, 90, 0],
                   axis_up=22.4385327718 if ref == 'H1' else 0,
                   terminals=terminals, radius=1.75,
                   height_from_top_mm=None if ref == 'H1' else 508-80)


def build(s):
    path = PARTS/'3dmodels/Controls'/s['model']
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    shape = reader.OneShape()
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    lo, hi = box.CornerMin(), box.CornerMax()
    bounds = [[p.Coord(i) for i in [1, 2, 3]] for p in [lo, hi]]
    corners = [[bounds[a][0], bounds[b][1], bounds[c][2]]
               for a in [0, 1] for b in [0, 1] for c in [0, 1]]
    right, normal = s['right'], s['normal']
    up = cross(normal, right)
    cx = (min(dot(p, right) for p in corners)+max(dot(p, right) for p in corners))/2
    cy = s['axis_up']
    zmin = min(dot(p, normal) for p in corners)
    offset = [-cx, -cy, -zmin]

    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(), gp_Dir(*normal), gp_Dir(*right))))
    algo.Update()
    algo.Hide()
    hlr = HLRBRep_HLRToShape(algo)
    shapes, seen = [], set()

    def point(p):
        return [p.X()-cx, cy-p.Y()]

    def add(kind, points):
        pts = tuple(tuple(round(v, 6) for v in p) for p in points)
        if kind == 'line' and math.dist(*pts) < .00001:
            return
        key = (kind, pts if kind == 'circle' else min(pts, tuple(reversed(pts))))
        if key not in seen:
            seen.add(key)
            shapes.append((kind, pts))

    for visible in [hlr.VCompound(), hlr.OutLineVCompound()]:
        if visible.IsNull():
            continue
        ex = TopExp_Explorer(visible, TopAbs_EDGE)
        while ex.More():
            c = BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
            first, last = c.FirstParameter(), c.LastParameter()
            if c.GetType() == GeomAbs_Line:
                add('line', [point(c.Value(first)), point(c.Value(last))])
            elif c.GetType() == GeomAbs_Circle:
                if abs(abs(last-first)-2*math.pi) < 1e-5:
                    cc = c.Circle(); p = cc.Location()
                    add('circle', [point(p), point(gp_Pnt(p.X()+cc.Radius(), p.Y(), p.Z()))])
                else:
                    add('arc', [point(c.Value(first)), point(c.Value((first+last)/2)), point(c.Value(last))])
            else:
                q = GCPnts_QuasiUniformDeflection(c, .002, first, last)
                assert q.IsDone()
                pts = [point(q.Value(i)) for i in range(1, q.NbPoints()+1)]
                for a, b in zip(pts, pts[1:]):
                    add('line', [a, b])
            ex.Next()

    pads = []
    groups = {}
    for number, p in s['terminals']:
        actual = [dot(p, right)-cx, cy-dot(p, up)]
        pad = dict(number=number, source_xyz_mm=p, projected_center_mm=actual,
                   source_depth_mm=dot(p, normal)-zmin, center_mm=actual[:])
        groups.setdefault(tuple(round(v, 4) for v in actual), []).append(pad)
        pads.append(pad)
    for group in groups.values():
        n = len(group)
        for i, pad in enumerate(group):
            if n == 1:
                continue
            a = math.pi if n == 2 and i == 0 else 0 if n == 2 else -math.pi/2+2*math.pi*i/n
            x, y = pad['projected_center_mm']
            pad['center_mm'] = [x+s['radius']*math.cos(a), y+s['radius']*math.sin(a)]
    for i, p in enumerate(pads):
        for q in pads[i+1:]:
            assert math.dist(p['center_mm'], q['center_mm']) > 3.1

    ymin = cy-max(dot(p, up) for p in corners)
    ymax = cy-min(dot(p, up) for p in corners)
    top = math.floor((ymin-1.5)/1.27)*1.27
    bottom = math.ceil((ymax+1.5)/1.27)*1.27
    name = s['part']+'_LeftWall'
    lines = [f'(footprint "{name}"', '  (version 20241229)', '  (generator "pcbnew")',
             '  (generator_version "9.0")', '  (layer "F.Cu")',
             f'  (descr "{s["part"]} left-wall side elevation; operating face toward -X")',
             '  (tags "Controls left wall side elevation")', '  (attr exclude_from_pos_files)',
             f'  (property "Reference" "REF**" (at 0 {fmt(top)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))',
             f'  (property "Value" "{s["part"]}" (at 0 {fmt(bottom)}) (layer "Dwgs.User") (effects (font (size 1 1) (thickness 0.15))))']
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
                     '(size 3 3) (drill 2) (layers "*.Cu" "*.Mask"))')
    lines += [f'  (model "${{PARTS_LIB}}/3dmodels/Controls/{s["model"]}"',
              f'    (offset (xyz {xy(offset)}))', '    (scale (xyz 1 1 1))',
              f'    (rotate (xyz {xy(s["rotation"])})))', ')', '']
    out = LIB/(name+'.kicad_mod')
    out.write_text('\n'.join(lines))
    subprocess.run(['/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9',
                    str(HERE.parent/'label_references.py'), str(out), '--write'], check=True)
    result = dict(s, name=name, offset=offset, up=up, pads=pads, bounds=bounds,
                  projected_size_mm=[max(dot(p, right) for p in corners)-min(dot(p, right) for p in corners), ymax-ymin],
                  source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  footprint_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    print(name, result['projected_size_mm'], len(pads), 'pads', flush=True)
    return result


if __name__ == '__main__':
    results = [build(s) for s in source_specs()]
    (HERE/'geometry.json').write_text(json.dumps(results, indent=2)+'\n')
