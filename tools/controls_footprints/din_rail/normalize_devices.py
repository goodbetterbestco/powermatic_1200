#!/usr/bin/env python3
"""Prepare rail-datum library candidates without modifying the parts library.

Run with OCP installed. A rigid root placement preserves STEP assemblies/colors.
The source CAD is never overwritten. Footprint translations are idempotent.
"""
import argparse
import hashlib
import json
import math
import re
from itertools import product
from pathlib import Path

from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepGProp import BRepGProp
from OCP.BRep import BRep_Tool
from OCP.GProp import GProp_GProps
from OCP.STEPCAFControl import STEPCAFControl_Reader, STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_SOLID, TopAbs_FACE, TopAbs_VERTEX
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.collections import Sequence_TDF_Label
from OCP.gp import gp_Trsf

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')
XY = re.compile(r'\((at|start|end|mid|center|xy)\s+([-+\d.eE]+)\s+([-+\d.eE]+)')


def children(text):
    depth = 0
    for m in TOKEN.finditer(text):
        if m[0] == '(':
            if depth == 1:
                start = m.start()
            depth += 1
        elif m[0] == ')':
            depth -= 1
            if depth == 1:
                yield start, m.end(), text[start:m.end()]
    assert depth == 0


def read_shape(path):
    r = STEPControl_Reader()
    assert r.ReadFile(str(path)).name == 'IFSelect_RetDone'
    assert r.TransferRoots()
    return r.OneShape()


def transform(matrix, offset):
    t = gp_Trsf()
    t.SetValues(*[n for row, v in zip(matrix, offset) for n in [*row, v]])
    assert abs(t.ScaleFactor()-1) < 1e-10
    return t


def bounds(shape):
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, b)
    return None if b.IsVoid() else [*b.CornerMin().Coord(), *b.CornerMax().Coord()]


def mass(shape):
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, g)
    return g.Mass()


def count(shape, kind):
    n = 0
    e = TopExp_Explorer(shape, kind)
    while e.More():
        n += 1
        e.Next()
    return n


def vertices(shape):
    points = set()
    e = TopExp_Explorer(shape, TopAbs_VERTEX)
    while e.More():
        points.add(BRep_Tool.Pnt_s(TopoDS.Vertex(e.Current())).Coord())
        e.Next()
    return points


def vertex_error(expected, actual, tolerance=0.0001):
    """Check every exported vertex against the rigidly transformed source."""
    buckets = {}
    for v in vertices(expected):
        buckets.setdefault(tuple(math.floor(x/tolerance) for x in v), []).append(v)
    maximum = 0
    for v in vertices(actual):
        k = tuple(math.floor(x/tolerance) for x in v)
        nearby = [p for delta in product([-1,0,1],repeat=3)
                  for p in buckets.get(tuple(a+b for a,b in zip(k,delta)),[])]
        assert nearby, ('Unmatched STEP vertex',v)
        distance = min(math.dist(v,p) for p in nearby)
        assert distance < tolerance, (v,distance)
        maximum = max(maximum,distance)
    return maximum


def write_placed_step(source, destination, trsf):
    doc = TDocStd_Document(TCollection_ExtendedString('BinXCAF'))
    r = STEPCAFControl_Reader()
    r.SetColorMode(True)
    r.SetNameMode(True)
    assert r.ReadFile(str(source)).name == 'IFSelect_RetDone'
    assert r.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    roots = Sequence_TDF_Label()
    tool.GetFreeShapes(roots)
    for i in range(1, roots.Length()+1):
        assert tool.SetLocation(roots.Value(i), TopLoc_Location(trsf), TDF_Label())
    tool.UpdateAssemblies()
    w = STEPCAFControl_Writer()
    w.SetColorMode(True)
    w.SetNameMode(True)
    assert w.Transfer(doc)
    assert w.Write(str(destination)).name == 'IFSelect_RetDone'


def footprint(text, spec, applied_translation_mm=None):
    already = spec['derived_model'] in text
    dx, dy = spec['shift'][0], -spec['shift'][1]
    if already:
        assert applied_translation_mm is not None, 'Missing installed footprint datum record'
        dx -= applied_translation_mm[0]
        dy -= applied_translation_mm[1]
    edits = []
    for a, b, node in children(text):
        k = next(TOKEN.finditer(node[1:]))[0]
        if k == 'model':
            edits.append((a, b, ''))
        elif (dx or dy) and (k.startswith('fp_') or k in ['pad', 'property']):
            def move(m):
                x = f'{float(m[2])+dx:.9f}' if dx else m[2]
                y = f'{float(m[3])+dy:.9f}' if dy else m[3]
                return f'({m[1]} {x} {y}'
            new = XY.sub(move, node)
            edits.append((a, b, new))
    for a, b, new in reversed(edits):
        text = text[:a]+new+text[b:]
    if spec['part'] == 'HC3096N-52-900-24':
        # This is an electrical component, not a PCB-only mechanical item.
        text = text.replace('(attr board_only exclude_from_pos_files exclude_from_bom)', '(attr through_hole)')
    model = '\n  (model "${PARTS_LIB}/3dmodels/Controls/'+spec['derived_model']+'"\n    (offset (xyz 0 0 0))\n    (scale (xyz 1 1 1))\n    (rotate (xyz 0 0 0)))\n'
    return text[:text.rfind(')')].rstrip()+model+')\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parts', type=Path, default=Path.home()/'Projects/_parts')
    p.add_argument('--output', type=Path, default=Path('/tmp/powermatic-din-normalized'))
    p.add_argument('--part', action='append', help='Process only this part; repeat to select more')
    args = p.parse_args()
    config = json.loads(Path(__file__).with_name('device_datums.json').read_text())
    installed_report = args.parts/'reviews/Controls/DIN35x7p5/validation.json'
    installed = {s['part']: s for s in json.loads(installed_report.read_text())['parts']} if installed_report.exists() else {}
    if args.part:
        assert set(args.part) <= {s['part'] for s in config['parts']}, 'Unknown requested part'
    models = args.output/'3dmodels/Controls'
    fps = args.output/'footprints/Controls.pretty'
    models.mkdir(parents=True, exist_ok=True)
    fps.mkdir(parents=True, exist_ok=True)
    original_rail = read_shape(args.parts/'3dmodels/Controls'/config['rail'])
    rail = BRepBuilderAPI_Transform(original_rail, transform([[0,1,0],[-1,0,0],[0,0,1]], [0,0,0]), True).Shape()
    results = []
    for s in config['parts']:
        if args.part and s['part'] not in args.part:
            continue
        source = args.parts/'3dmodels/Controls'/s['model']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == s['source_sha256']
        trsf = transform(s['matrix'], s['new_offset'])
        expected = BRepBuilderAPI_Transform(read_shape(source), trsf, True).Shape()
        out = models/s['derived_model']
        write_placed_step(source, out, trsf)
        actual = read_shape(out)
        errors = [abs(a-b) for a,b in zip(bounds(expected), bounds(actual))]
        assert max(errors) < 1e-5, (s['part'], errors)
        expected_volume, actual_volume = mass(expected), mass(actual)
        # STEP reparameterization changes OCCT's approximate volume integration
        # slightly. Check topology, vertices and bounds independently as well.
        relative_volume_error = abs(expected_volume-actual_volume)/abs(expected_volume)
        assert relative_volume_error < 0.0001
        max_vertex_error = max(vertex_error(expected,actual),vertex_error(actual,expected))
        assert count(expected,TopAbs_SOLID) == count(actual,TopAbs_SOLID)
        assert count(expected,TopAbs_FACE) == count(actual,TopAbs_FACE)
        fp = args.parts/'footprints/Controls.pretty'/(s['footprint']+'.kicad_mod')
        applied = installed.get(s['part'], {}).get('footprint_translation_mm')
        (fps/fp.name).write_text(footprint(fp.read_text(),s,applied))
        common = BRepAlgoAPI_Common(actual,rail).Shape()
        results.append(dict(part=s['part'], footprint=s['footprint'], source=s['model'],
                            source_sha256=s['source_sha256'], derived_model=out.name,
                            derived_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                            transform_matrix=s['matrix'], transform_offset_mm=s['new_offset'],
                            footprint_translation_mm=[s['shift'][0],-s['shift'][1]],
                            model_offset_mm=[0,0,0],model_rotation_deg=[0,0,0],model_scale=[1,1,1],
                            bounds_mm=bounds(actual), bounds_error_mm=max(errors),
                            solid_count=count(actual,TopAbs_SOLID),face_count=count(actual,TopAbs_FACE),
                            volume_mm3=actual_volume,relative_volume_error=relative_volume_error,
                            max_vertex_error_mm=max_vertex_error,nominal_rail_overlap_mm3=mass(common),
                            overlap_bounds_mm=bounds(common),
                            datum_evidence=s['datum_evidence'],datasheet=s['datasheet']))
        if 'bench_measurements' in s:
            results[-1]['bench_measurements'] = s['bench_measurements']
        print('Verified rigid transform:',s['part'],flush=True)
    (args.output/'validation.json').write_text(json.dumps(dict(parts=results, exceptions=config['exceptions'],
        rail_profile_mm=[35,7.5],scope='Nominal panel-layout placement; original clip states retained. Not an interference-free fit or manufacturing approval.'),indent=2)+'\n')


if __name__ == '__main__':
    main()
