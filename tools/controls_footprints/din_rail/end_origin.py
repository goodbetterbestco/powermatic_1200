#!/usr/bin/env python3
"""Prepare left-end rail/duct footprints and rigidly placed STEP copies.

Runs with the existing OCP environment. Original source models are preserved.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Circle
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_SOLID, TopAbs_EDGE, TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from normalize_devices import (
    XY, bounds, children, count, read_shape, transform, vertex_error,
    write_placed_step,
)


def mass(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props, 1e-9, True, False)
    return props.Mass()


def model_node(name):
    return ('  (model "${PARTS_LIB}/3dmodels/Controls/'+name+'"\n'
            '    (offset (xyz 0 0 0))\n    (scale (xyz 1 1 1))\n'
            '    (rotate (xyz 0 0 0)))\n')


def shift_rail(text):
    if 'DN-R35S1_350mm_LeftOrigin.step' in text:
        return text
    edits = []
    for a, b, node in children(text):
        if node.startswith('(model '):
            edits.append((a, b, ''))
        elif node.startswith('(fp_') or node.startswith('(property '):
            edits.append((a, b, XY.sub(lambda m: f'({m[1]} {float(m[2])+175:.9f} {m[3]}', node)))
    for a, b, node in reversed(edits):
        text = text[:a]+node+text[b:]
    text = text.replace('origin at back mounting face center',
                        'origin at center of left rear edge; length along +X')
    return text[:text.rfind(')')].rstrip()+'\n'+model_node('DN-R35S1_350mm_LeftOrigin.step')+')\n'


def project(shape):
    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0), gp_Dir(0,0,1), gp_Dir(1,0,0))))
    algo.Update()
    algo.Hide()
    projection = HLRBRep_HLRToShape(algo)
    graphics, seen = [], set()
    style = '(stroke (width 0.05) (type solid)) (layer "Dwgs.User")'
    def xy(p): return (round(p.X(),6), round(-p.Y(),6))
    def fmt(p): return ' '.join(f'{v:.6f}'.rstrip('0').rstrip('.') if v else '0' for v in p)
    def add_line(a,b):
        key=('line',*sorted([a,b]))
        if math.dist(a,b)>1e-5 and key not in seen:
            seen.add(key)
            graphics.append(f'  (fp_line (start {fmt(a)}) (end {fmt(b)}) {style})')
    for visible in (projection.VCompound(),projection.OutLineVCompound()):
        if visible.IsNull(): continue
        e=TopExp_Explorer(visible,TopAbs_EDGE)
        while e.More():
            c=BRepAdaptor_Curve(TopoDS.Edge(e.Current()))
            first,last=c.FirstParameter(),c.LastParameter()
            a,b=xy(c.Value(first)),xy(c.Value(last))
            if c.GetType()==GeomAbs_Line:
                add_line(a,b)
            elif c.GetType()==GeomAbs_Circle:
                if abs(last-first)>2*math.pi-1e-5:
                    center=xy(c.Circle().Location()); key=('circle',center,a)
                    item=f'  (fp_circle (center {fmt(center)}) (end {fmt(a)}) {style} (fill none))'
                else:
                    mid=xy(c.Value((first+last)/2)); key=('arc',*sorted([a,b]),mid)
                    item=f'  (fp_arc (start {fmt(a)}) (mid {fmt(mid)}) (end {fmt(b)}) {style})'
                if key not in seen:
                    seen.add(key); graphics.append(item)
            else:
                samples=GCPnts_QuasiUniformDeflection(c,0.002,first,last)
                assert samples.IsDone()
                ps=[xy(samples.Value(i)) for i in range(1,samples.NbPoints()+1)]
                for a,b in zip(ps,ps[1:]): add_line(a,b)
            e.Next()
    return graphics


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parts',type=Path,default=Path.home()/'Projects/_parts')
    p.add_argument('--output',type=Path,default=Path('/tmp/powermatic-end-origin'))
    a=p.parse_args()
    models=a.output/'3dmodels/Controls'; fps=a.output/'footprints/Controls.pretty'
    models.mkdir(parents=True,exist_ok=True); fps.mkdir(parents=True,exist_ok=True)
    specs=[
        ('DN-R35S1_350mm.step','DN-R35S1_350mm_LeftOrigin.step',
         [[0,1,0],[-1,0,0],[0,0,1]],[175,0,0],[0,-17.5,0,350,17.5,7.5]),
        ('T1-1530G1-1.step','T1-1530G1-1_1000mm_LeftOrigin.step',
         [[0,0,1],[1,0,0],[0,1,0]],[500,0,0],[0,-20,0,1000,20,80]),
    ]
    report=[]
    for src,dest,matrix,offset,target in specs:
        source=a.parts/'3dmodels/Controls'/src
        original=read_shape(source); trsf=transform(matrix,offset)
        expected=BRepBuilderAPI_Transform(original,trsf,True).Shape()
        output=models/dest
        write_placed_step(source,output,trsf)
        actual=read_shape(output)
        assert BRepCheck_Analyzer(actual).IsValid()
        assert max(abs(x-y) for x,y in zip(bounds(actual),target))<1e-5
        assert count(actual,TopAbs_SOLID)==count(original,TopAbs_SOLID)
        assert count(actual,TopAbs_FACE)==count(original,TopAbs_FACE)
        volume_error=abs(mass(actual)-mass(original))/mass(original)
        # STEP round-trip of the duct's 2540 trimmed faces changes the integrated
        # volume by 13 ppm; bounds and every rigidly transformed vertex match.
        # Retain the source, check topology, and record this writer tolerance.
        assert volume_error<5e-5, volume_error
        err=vertex_error(expected,actual)
        report.append(dict(source=src,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                           derived=dest,bounds_mm=bounds(actual),matrix=matrix,offset_mm=offset,
                           solids=count(actual,TopAbs_SOLID),max_vertex_error_mm=err,
                           relative_volume_error=volume_error))
        if src.startswith('T1'):
            graphics=project(actual)
            name='T1-1530G1-1_1000mm_Front'
            text=f'''(footprint "{name}"
  (version 20241229)
  (generator "pcbnew")
  (generator_version "9.0")
  (layer "F.Cu")
  (descr "Wire duct with cover; 1000 x 40 x 80 mm user STEP envelope; origin at center of left rear edge; length along +X")
  (tags "Controls mechanical wire duct 1000mm")
  (attr board_only exclude_from_pos_files exclude_from_bom)
  (property "Reference" "REF**" (at 500 -10) (layer "Dwgs.User")
    (effects (font (size 2.5 2.5) (thickness 0.15))))
  (property "Value" "{name}" (at 500 22) (layer "Dwgs.User") (hide yes)
    (effects (font (size 2.5 2.5) (thickness 0.15))))
{chr(10).join(graphics)}
{model_node(dest)})
'''
            (fps/(name+'.kicad_mod')).write_text(text)
            report[-1]['graphic_count']=len(graphics)
    rail=a.parts/'footprints/Controls.pretty/DN-R35S1_350mm_Front.kicad_mod'
    (fps/rail.name).write_text(shift_rail(rail.read_text()))
    (a.output/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
