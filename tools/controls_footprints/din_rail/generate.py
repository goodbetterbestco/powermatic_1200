#!/usr/bin/env python3
"""Project the existing user-supplied rail STEP into a mechanical footprint.

Requires OCP. Writes review candidates only; does not edit libraries or boards.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from OCP.Bnd import Bnd_Box
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepBndLib import BRepBndLib
from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Line
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from normalize_devices import transform, write_placed_step


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parts', type=Path, default=Path.home()/'Projects/_parts')
    parser.add_argument('--output', type=Path, default=Path('/tmp/powermatic-din-rail'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    name = 'DN-R35S1_350mm_Front'
    source = args.parts/'3dmodels/Controls/DN-R35S1_350mm.step'
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(source)).name == 'IFSelect_RetDone'
    reader.TransferRoots()
    shape = reader.OneShape()
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box)
    bounds = [*box.CornerMin().Coord(), *box.CornerMax().Coord()]
    assert all(abs(a-b) < 1e-5 for a, b in zip(bounds, [-17.5, -175, 0, 17.5, 175, 7.5]))
    model_name = 'DN-R35S1_350mm_LeftOrigin.step'
    write_placed_step(source, args.output/model_name,
                      transform([[0,1,0],[-1,0,0],[0,0,1]], [175,0,0]))

    # Source has long axis Y and back mounting face Z=0. KiCad model Z rotation
    # +90 maps source (x,y,z) to model (y,-x,z), hence footprint XY=(y,x).
    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0), gp_Dir(0,0,1), gp_Dir(1,0,0))))
    algo.Update()
    algo.Hide()
    projected = HLRBRep_HLRToShape(algo)
    graphics = []
    seen = set()

    def xy(point):
        return [round(point.Y()+175, 6), round(point.X(), 6)]

    def fmt(point):
        return ' '.join(f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>1e-8 else '0' for v in point)

    style = '(stroke (width 0.05) (type solid)) (layer "Dwgs.User")'
    for visible in [projected.VCompound(), projected.OutLineVCompound()]:
        if visible.IsNull():
            continue
        explorer = TopExp_Explorer(visible, TopAbs_EDGE)
        while explorer.More():
            curve = BRepAdaptor_Curve(TopoDS.Edge(explorer.Current()))
            first, last = curve.FirstParameter(), curve.LastParameter()
            a, b = xy(curve.Value(first)), xy(curve.Value(last))
            kind = curve.GetType()
            if kind == GeomAbs_Line:
                if math.dist(a, b) < 1e-5:
                    explorer.Next()
                    continue
                identity = ('line', *sorted([tuple(a), tuple(b)]))
                item = f'  (fp_line (start {fmt(a)}) (end {fmt(b)}) {style})'
            elif kind == GeomAbs_Circle:
                mid = xy(curve.Value((first+last)/2))
                assert abs(last-first) < 2*math.pi-1e-5, 'Unexpected full circle'
                identity = ('arc', *sorted([tuple(a), tuple(b)]), tuple(mid))
                item = f'  (fp_arc (start {fmt(a)}) (mid {fmt(mid)}) (end {fmt(b)}) {style})'
            else:
                samples = GCPnts_QuasiUniformDeflection(curve, 0.002, first, last)
                assert samples.IsDone(), 'Rail edge approximation failed'
                points = [xy(samples.Value(i)) for i in range(1, samples.NbPoints()+1)]
                for a, b in zip(points, points[1:]):
                    identity = ('line', *sorted([tuple(a), tuple(b)]))
                    if math.dist(a, b) > 1e-5 and identity not in seen:
                        graphics.append(f'  (fp_line (start {fmt(a)}) (end {fmt(b)}) {style})')
                        seen.add(identity)
                explorer.Next()
                continue
            if identity not in seen:
                graphics.append(item)
                seen.add(identity)
            explorer.Next()

    text = f'''(footprint "{name}"
  (version 20241229)
  (generator "pcbnew")
  (generator_version "9.0")
  (layer "F.Cu")
  (descr "DIN rail; DN-R35S1 cut to 350 mm; 35 mm wide x 7.5 mm high; origin at center of left rear edge; length along +X")
  (tags "Controls DIN rail mechanical 35mm 7.5mm 350mm")
  (attr board_only exclude_from_pos_files exclude_from_bom)
  (property "Reference" "REF**" (at 175 -8) (layer "Dwgs.User")
    (effects (font (size 2.5 2.5) (thickness 0.15))))
  (property "Value" "{name}" (at 175 20) (layer "Dwgs.User") (hide yes)
    (effects (font (size 2.5 2.5) (thickness 0.15))))
{chr(10).join(graphics)}
  (model "${{PARTS_LIB}}/3dmodels/Controls/{model_name}"
    (offset (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0)))
)
'''
    destination = args.output/(name+'.kicad_mod')
    destination.write_text(text)
    report = {
        'footprint': name,
        'source': str(source),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'source_bounds_mm': bounds,
        'footprint_bounds_mm': [0, -17.5, 350, 17.5],
        'model_offsets_mm': [0, 0, 0],
        'model_rotation_deg': [0, 0, 0],
        'model_scale': [1, 1, 1],
        'graphic_count': len(graphics),
        'curved_edge_chord_tolerance_mm': 0.002,
        'pad_count': 0,
        'datum': 'Origin is center of left rear edge; +X runs along length; rail lips at Z=7.5 mm.',
        'slot_scope': 'Exact user STEP projection, including partial end slot; not backplate drill instructions.',
        'manufacturer_reference': 'https://cdn.automationdirect.com/static/specs/cutsheet/DN-R35S1_cutsheet.pdf',
    }
    (args.output/'geometry.json').write_text(json.dumps(report, indent=2)+'\n')
    print(destination)
    print(f'{len(graphics)} graphics, no pads, one derived left-origin model, zero model offsets')


if __name__ == '__main__':
    main()
