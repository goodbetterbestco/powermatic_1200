"""Measure unloaded clip cylinder geometry in the catalog holder STEP (requires OCP)."""
from pathlib import Path
import json
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
r=STEPControl_Reader();r.ReadFile('/Users/evanthayer/Projects/_parts/3dmodels/Controls/RM25030-3SR_DIN35x7p5.step');r.TransferRoots();s=r.OneShape()
e=TopExp_Explorer(s,TopAbs_FACE);rows=[]
while e.More():
 f=TopoDS.Face(e.Current()); a=BRepAdaptor_Surface(f)
 if a.GetType()==GeomAbs_Cylinder:
  c=a.Cylinder();p=c.Location();d=c.Axis().Direction()
  if abs(d.Y())>.99 and 5<c.Radius()<10:
   box=Bnd_Box();BRepBndLib.Add_s(f,box)
   rows.append({'r':round(c.Radius(),6),'axis':[round(p.X(),6),round(p.Y(),6),round(p.Z(),6)],'bounds': [round(getattr(p, a)(),6) for p in [box.CornerMin(),box.CornerMax()] for a in ['X','Y','Z']]})
 e.Next()
print(json.dumps(rows,indent=2));open(Path(__file__).with_name('clip_axes.json'),'w').write(json.dumps(rows,indent=2))
