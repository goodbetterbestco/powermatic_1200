#!/usr/bin/env python3
"""Verify the native KiCad S2 export against all ten source screw-head rims."""
from pathlib import Path
import json
import math

from OCP.STEPControl import STEPControl_Reader
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle

WORK = Path('/private/tmp/powermatic-s2-model')


def main():
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(WORK / 'S2-native.step')).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    shape = reader.OneShape()
    assert BRepCheck_Analyzer(shape).IsValid()
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    bounds = [list(box.CornerMin().Coord()), list(box.CornerMax().Coord())]
    geom = json.loads((WORK / 'assets/geometry.json').read_text())
    source = geom['bounds_mm']
    delta = [600, -120, 1.595]
    for corner in range(2):
        for axis in range(3):
            assert abs(bounds[corner][axis] - source[corner][axis] - delta[axis]) < .002
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    count = 0
    while explorer.More():
        count += 1
        explorer.Next()
    assert count == 35
    centers = []
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while explorer.More():
        curve = BRepAdaptor_Curve(TopoDS.Edge(explorer.Current()))
        if curve.GetType() == GeomAbs_Circle and abs(curve.Circle().Radius() - 4.053989) < 1e-5:
            centers.append(list(curve.Circle().Location().Coord()))
        explorer.Next()
    checks = []
    for pad in geom['pads']:
        target = [pad['model_head_rim_center_mm'][axis] + delta[axis] for axis in range(3)]
        error = min(math.dist(target, center) for center in centers)
        assert error < .002, (pad['number'], target, error)
        checks.append({'pin': pad['number'], 'source_screw': pad['model_screw'],
                       'native_rim_center_error_mm': error})
    report = {'native_bounds_mm': bounds, 'all_35_valid_solids_preserved': True,
              'physical_dimensions_preserved': True, 'base_at_top_component_plane_z_mm': bounds[0][2],
              'native_placement_translation_mm': delta, 'screw_checks': checks,
              'max_screw_center_error_mm': max(p['native_rim_center_error_mm'] for p in checks)}
    (WORK / 'native-alignment.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'screw_checks'}, indent=2))


if __name__ == '__main__':
    main()
