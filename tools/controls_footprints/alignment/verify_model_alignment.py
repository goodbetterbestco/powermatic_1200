#!/usr/bin/env python3
"""Check source terminal centers survive KiCad's STEP export at pad XY.

Run with OCP (cadquery-ocp). Native review export includes the temporary board;
KiCad puts the model origin at Z=1.595 mm for this default stackup.
"""
from pathlib import Path
import json, math
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle
HERE=Path(__file__).resolve().parent
WORK=Path('/tmp/powermatic-aligned-controls')

def circles(path):
    r=STEPControl_Reader(); assert r.ReadFile(str(path)).name == 'IFSelect_RetDone'
    r.TransferRoots(); ex=TopExp_Explorer(r.OneShape(),TopAbs_EDGE); result=[]
    while ex.More():
        c=BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
        if c.GetType()==GeomAbs_Circle:
            p=c.Circle().Location(); result.append([p.X(),p.Y(),p.Z()])
        ex.Next()
    return result

def plane_centers(path):
    from OCP.TopAbs import TopAbs_FACE
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Plane
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    r=STEPControl_Reader();r.ReadFile(str(path));r.TransferRoots()
    ex=TopExp_Explorer(r.OneShape(),TopAbs_FACE);result=[]
    while ex.More():
        face=TopoDS.Face(ex.Current())
        if BRepAdaptor_Surface(face).GetType()==GeomAbs_Plane:
            prop=GProp_GProps();BRepGProp.SurfaceProperties_s(face,prop);p=prop.CentreOfMass()
            result.append([p.X(),p.Y(),p.Z()])
        ex.Next()
    return result

results=[]
for spec in json.loads((HERE/'geometry_review.json').read_text()):
    actual=circles(WORK/(spec['name']+'.step'))
    # Blade-tip centers are planar-face centroids, not circular edges.
    actual += plane_centers(WORK/(spec['name']+'.step'))
    pad_checks=[]
    for p in spec['pads']:
        x,y=p['center_mm']
        depth=sum(a*b for a,b in zip(p['source_xyz_mm'],spec['normal']))+spec['offset'][2]+1.595
        target=[x,-y,depth]
        error=min(math.dist(target,c) for c in actual)
        assert error<.03,(spec['name'],p['number'],target,error)
        pad_checks.append({'pin':p['number'],'exported_center_error_mm':error})
    results.append({'name':spec['name'],'checks':pad_checks})
    print(spec['name'], 'pad/model centers agree within',max(p['exported_center_error_mm'] for p in pad_checks),'mm')
(HERE/'model_alignment.json').write_text(json.dumps(results,indent=2)+'\n')
