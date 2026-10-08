#!/usr/bin/env python3
"""Measure all 35 source solids and ten screw rims without editing the source.

Preserve STEP root order and write isolated temporary copies for projection.
Use the complete source transfer so all shared geometric references resolve.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle


def bounds(shape):
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    return [list(box.CornerMin().Coord()), list(box.CornerMax().Coord())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.read_text()
    pattern = r'(ADVANCED_BREP_SHAPE_REPRESENTATION\(\x27\x27,\()(.+?)(\),#\d+\);)'
    root = re.search(pattern, source, re.S)
    assert root
    names = re.findall(r'#(\d+)=MANIFOLD_SOLID_BREP\(\x27([^\x27]+)\x27', source)
    assert len(names) == 35
    assert re.findall(r'#(\d+)', root.group(2)) == [entity for entity, name in names]
    assert {name for entity, name in names if name.startswith('screw_')} == {
        f'screw_{section}{tier}' for section in range(1, 5) for tier in ['T', 'B']} | {'screw_5T', 'screw_6T'}
    output = args.output.resolve()
    isolated = output / 'isolated-solids'
    isolated.mkdir(parents=True, exist_ok=True)
    rows, circles = [], {}
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(args.source)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    assert BRepCheck_Analyzer(reader.OneShape()).IsValid()
    explorer = TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    shapes = []
    while explorer.More():
        shapes.append(explorer.Current())
        explorer.Next()
    assert len(shapes) == len(names)
    # STEP root lists these named solids in this order; preserve that root order.
    for (entity, name), shape in zip(names, shapes):
        assert not shape.IsNull()
        assert BRepCheck_Analyzer(shape).IsValid(), name
        envelope = bounds(shape)
        assert all(abs(v) < 10000 for corner in envelope for v in corner)
        path = isolated / (entity + '.step')
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        assert writer.Write(str(path)).name == 'IFSelect_RetDone'
        rows.append({'name': name, 'step_entity': entity, 'bounds': envelope,
                     'valid': True})
        if name.startswith('screw_'):
            edges = TopExp_Explorer(shape, TopAbs_EDGE)
            features = set()
            while edges.More():
                curve = BRepAdaptor_Curve(TopoDS.Edge(edges.Current()))
                if curve.GetType() == GeomAbs_Circle:
                    circle = curve.Circle()
                    features.add((round(circle.Radius(), 6),
                                  tuple(round(x, 6) for x in circle.Location().Coord()),
                                  tuple(round(x, 6) for x in circle.Axis().Direction().Coord())))
                edges.Next()
            circles[name] = sorted(features, reverse=True)
        # Keep temporary isolated geometry for footprint projection.
    report = {'source': str(args.source.resolve()),
              'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'isolated_dir': str(isolated), 'solids': rows}
    (output / 'named-shapes.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'screw-circles.json').write_text(json.dumps(circles, indent=2) + '\n')
    print('Measured 35 named solids and 10 labelled terminal screws.')


if __name__ == '__main__':
    main()
