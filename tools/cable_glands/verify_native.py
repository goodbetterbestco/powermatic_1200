#!/usr/bin/env python3
"""Verify gland axes in KiCad's native assembly STEP export (requires OCP)."""
from pathlib import Path
import sys,json,math
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE,TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
HERE=Path(__file__).resolve().parent;CFG=json.loads((HERE/'config.json').read_text());r=STEPControl_Reader();assert r.ReadFile(sys.argv[1]).name=='IFSelect_RetDone';r.TransferRoots();shape=r.OneShape();e=TopExp_Explorer(shape,TopAbs_FACE);axes=set()
while e.More():
 a=BRepAdaptor_Surface(TopoDS.Face(e.Current()))
 if a.GetType()==GeomAbs_Cylinder:
  c=a.Cylinder()
  if abs(c.Axis().Direction().Y())>.999:axes.add((round(c.Location().X(),6),round(c.Location().Z(),6)))
 e.Next()
e=TopExp_Explorer(shape,TopAbs_SOLID);body=[]
while e.More():
 b=Bnd_Box();BRepBndLib.AddOptimal_s(e.Current(),b);lo,hi=b.CornerMin(),b.CornerMax()
 if abs(hi.X()-lo.X()-508)<.01 and abs(hi.Y()-lo.Y()-508)<.01:body.append([*lo.Coord(),*hi.Coord()])
 e.Next()
assert len(body)==1,body;rear=body[0][2];checks=[]
for p in CFG['parts']:
 target=(p['x_mm'],rear+75);axis=min(axes,key=lambda a:math.dist(a,target));err=math.dist(axis,target);assert err<1e-4,(p['ref'],target,axis,err)
 checks.append({'reference':p['ref'],'axis_x_z_mm':axis,'axis_error_mm':err,'distance_from_rear_mm':axis[1]-rear})
result={'native_enclosure_body_bounds_mm':body[0],'native_rear_edge_z_mm':rear,'checks':checks};(HERE/'native_step_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
