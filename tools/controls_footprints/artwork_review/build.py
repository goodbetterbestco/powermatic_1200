#!/usr/bin/env python3
"""Generate Q1-style switch elevation artwork without changing physical models.

Silkscreen shows casing, buttons, terminals, brackets and plain screw rims.
Detailed source projections remain unchanged on F.Fab. Proxy cylinders remove
engraved lettering and screw slots from the drawing only, never from the STEP.
"""
from pathlib import Path
import importlib.util
import json
import math
import re
import sys
from collections import defaultdict

sys.dont_write_bytecode = True
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_EDGE
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.BRep import BRep_Builder
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Trsf, gp_Vec

HERE = Path(__file__).resolve().parent
PARTS = Path.home() / 'Projects/_parts'
WORK = Path('/private/tmp/powermatic-layer-review')
WIDTH = .25
TOLERANCE = .075


def load_named(path):
    names = re.findall(r'MANIFOLD_SOLID_BREP\(\x27([^\x27]+)\x27', path.read_text())
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    solids = []
    explorer = TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    while explorer.More():
        solids.append(explorer.Current())
        explorer.Next()
    assert len(names) == len(solids)
    return dict(zip(names, solids))


def compound(shapes):
    builder = BRep_Builder()
    result = TopoDS_Compound()
    builder.MakeCompound(result)
    for shape in shapes:
        builder.Add(result, shape)
    return result


def plain_head(shape):
    rims = []
    seen = set()
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while explorer.More():
        curve = BRepAdaptor_Curve(TopoDS.Edge(explorer.Current()))
        if curve.GetType() == GeomAbs_Circle:
            circle = curve.Circle()
            if abs(circle.Radius() - 4.053989) < 1e-5:
                center = list(circle.Location().Coord())
                direction = list(circle.Axis().Direction().Coord())
                identity = tuple(round(v, 6) for v in center)
                if identity not in seen:
                    seen.add(identity)
                    rims.append((center, direction, circle.Radius()))
        explorer.Next()
    assert len(rims) == 1
    center, normal, radius = rims[0]
    if normal[2] < 0:
        normal = [-v for v in normal]
    # A thin plain head preserves its measured rim and top projection while
    # excluding slots/threads. It is used only as a drawing proxy.
    base = [center[i] - normal[i] * .4 for i in range(3)]
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*base), gp_Dir(*normal)), radius, .4).Shape()


def distance_to_line(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) + abs(dy) < 1e-12:
        return math.dist(p, a)
    return abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / math.hypot(dx, dy)


def rdp(points):
    if len(points) < 3:
        return points
    index, distance = max(((i, distance_to_line(p, points[0], points[-1]))
                           for i, p in enumerate(points[1:-1], 1)), key=lambda item: item[1])
    if distance <= TOLERANCE:
        return [points[0], points[-1]]
    return rdp(points[:index + 1])[:-1] + rdp(points[index:])


def simplify(curves):
    adjacency = defaultdict(list)
    lines = []
    others = []
    unique = set()
    for kind, points in curves:
        points = tuple(tuple(round(v, 6) for v in p) for p in points)
        identity = (kind, min(points, tuple(reversed(points))) if kind != 'circle' else points)
        if identity in unique:
            continue
        unique.add(identity)
        if kind != 'line':
            others.append((kind, points))
            continue
        index = len(lines)
        lines.append(points)
        for p in points:
            adjacency[p].append(index)
    used = set()
    output = list(others)
    def walk(index, start):
        chain = [start]
        current = start
        while index not in used:
            used.add(index)
            a, b = lines[index]
            current = b if a == current else a
            chain.append(current)
            if len(adjacency[current]) != 2:
                break
            choices = [i for i in adjacency[current] if i not in used]
            if not choices:
                break
            index = choices[0]
        for a, b in zip(rdp(chain), rdp(chain)[1:]):
            if math.dist(a, b) > 1e-5:
                output.append(('line', (a, b)))
    for point, incident in adjacency.items():
        if len(incident) != 2:
            for index in incident:
                if index not in used:
                    walk(index, point)
    for index, points in enumerate(lines):
        if index not in used:
            walk(index, points[0])
    return output


def make_curves(ref, path):
    spec = importlib.util.spec_from_file_location('projection', HERE.parent / 'left_wall/assembly/build.py')
    projection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(projection)
    shapes = load_named(path)
    selected = []
    for name, shape in shapes.items():
        if name.startswith('screw_'):
            selected.append(plain_head(shape))
        elif ref == 'S2' and (name == 'bakelight' or name.startswith('tab_')):
            selected.append(shape)
        elif ref == 'S2' and name.startswith('button_cap'):
            bounds = projection.bounds(shape)
            cx, cy = [(bounds[0][i] + bounds[1][i]) / 2 for i in [0, 1]]
            radius = (bounds[1][0] - bounds[0][0]) / 2
            selected.append(BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(cx, cy, bounds[0][2]), gp_Dir(0, 0, 1)),
                                                     radius, bounds[1][2] - bounds[0][2]).Shape())
        elif ref == 'S3' and name.startswith(('enclosure', 'shaft', 'body', 'bracket', 'electrode', 'jumper')):
            selected.append(shape)
    shape = compound(selected)
    if ref == 'S2':
        transform = gp_Trsf()
        transform.SetTranslation(gp_Vec(70, 0, 89.4))
        shape = BRepBuilderAPI_Transform(shape, transform, True).Shape()
    original = projection.project(shape)
    curves = simplify(original)
    report = {'model': path.name, 'selected_proxy_shapes': len(selected),
              'raw_primitives': len(original), 'silkscreen_primitives_before_clipping': len(curves),
              'simplification_tolerance_mm': TOLERANCE,
              'retained': 'Casing, button faces, terminal plates, brackets, contact body, shafts, jumpers, plain measured screw rims',
              'omitted': 'Screw slots, threads, engraved legends/numbers, nail heads and fine tessellation',
              'model_and_F_Fab_unchanged': True}
    return curves, report


def main():
    report = {}
    for ref, model in [('S2', 'Furnas_50MA3KLE.step'), ('S3', 'AB_365-TAV2111.step')]:
        curves, details = make_curves(ref, PARTS / '3dmodels/Controls' / model)
        (WORK / f'{ref}-silk-curves.json').write_text(json.dumps(curves, indent=2) + '\n')
        report[ref] = details
    (WORK / 'artwork-source.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
