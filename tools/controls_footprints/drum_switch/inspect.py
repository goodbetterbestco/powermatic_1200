#!/usr/bin/env python3
"""Measure named STEP solids and screw-head rims without altering the source.

Individual solid views are temporary STEP copies with a narrowed root shape
representation. This avoids relying on translator-dependent solid order.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

from OCP.STEPControl import STEPControl_Reader
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
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
    assert len(names) == 46
    assert {name for entity, name in names if name.startswith('screw_')} == {
        f'screw_{section}{tier}' for section in range(1, 9) for tier in ['T', 'B']}
    output = args.output.resolve()
    isolated = output / 'isolated-solids'
    isolated.mkdir(parents=True, exist_ok=True)
    rows, circles = [], {}
    for entity, name in names:
        path = isolated / (entity + '.step')
        path.write_text(source[:root.start(2)] + '#' + entity + source[root.end(2):])
        reader = STEPControl_Reader()
        assert reader.ReadFile(str(path)).name == 'IFSelect_RetDone'
        reader.TransferRoots()
        shape = reader.OneShape()
        assert not shape.IsNull()
        rows.append({'name': name, 'step_entity': entity, 'bounds': bounds(shape),
                     'valid': BRepCheck_Analyzer(shape).IsValid()})
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
        elif name not in {'enclosure', 'shaft'}:
            path.unlink()
    report = {'source': str(args.source.resolve()),
              'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'isolated_dir': str(isolated), 'solids': rows}
    (output / 'named-shapes.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'screw-circles.json').write_text(json.dumps(circles, indent=2) + '\n')
    print('Measured 46 named solids and 16 labelled terminal screws.')


if __name__ == '__main__':
    main()
