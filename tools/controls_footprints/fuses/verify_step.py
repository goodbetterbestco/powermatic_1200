#!/usr/bin/env python3
"""Check fuse axes after a native KiCad STEP export (requires OCP)."""
from pathlib import Path
import sys,json,math
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
p=Path(sys.argv[1]);r=STEPControl_Reader();assert r.ReadFile(str(p)).name=='IFSelect_RetDone';r.TransferRoots()
e=TopExp_Explorer(r.OneShape(),TopAbs_FACE);axes=set()
while e.More():
 a=BRepAdaptor_Surface(TopoDS.Face(e.Current()))
 if a.GetType()==GeomAbs_Cylinder:
  c=a.Cylinder();d=c.Axis().Direction()
  if abs(c.Radius()-7.112)<1e-5 and abs(d.Y())>.999:
   o=c.Location();axes.add((round(o.X(),6),round(o.Z(),6)))
 e.Next()
placements=json.loads(Path(__file__).with_name('placement.json').read_text())
# KiCad uses the top board surface as the footprint plane: 1.595 mm in this stackup.
checks=[]
for row in placements['placements']:
 x=row['position_mm'][0];target=(x,30.414015+1.595)
 err=min(math.dist(target,a) for a in axes);assert err<1e-4,(row,target,axes)
 checks.append({'reference':row['reference'],'axis_error_mm':err,'native_export_axis_mm':[x,-row['position_mm'][1],target[1]]})
print(json.dumps({'native_export_fuse_axes':sorted(axes),'checks':checks},indent=2))
Path(__file__).with_name('step_validation.json').write_text(json.dumps({'native_export_fuse_axes':sorted(axes),'checks':checks},indent=2)+'\n')
