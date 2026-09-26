#!/usr/bin/env python3
"""OCP visible-front projection. Args: model basename, normal CSV, right CSV, output stem.
Curves retain lines/circles/arcs; other curves are chorded to 0.005 mm.
"""
import sys,json,math
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.HLRBRep import HLRBRep_Algo,HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2,gp_Pnt,gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line,GeomAbs_Circle
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
name=sys.argv[1];n=list(map(float,sys.argv[2].split(',')));u=list(map(float,sys.argv[3].split(',')));out=Path(sys.argv[4])
r=STEPControl_Reader();r.ReadFile(str(Path.home()/'Projects/_parts/3dmodels/Controls'/name));r.TransferRoots();s=r.OneShape()
a=HLRBRep_Algo();a.Add(s);a.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*n),gp_Dir(*u))));a.Update();a.Hide();h=HLRBRep_HLRToShape(a)
pr=[];lines=[];bounds=[]
def pt(p):return [p.X(),-p.Y()]
for visible in [h.VCompound(),h.OutLineVCompound()]:
 if visible.IsNull():continue
 ex=TopExp_Explorer(visible,TopAbs_EDGE)
 while ex.More():
  c=BRepAdaptor_Curve(TopoDS.Edge(ex.Current()));f=c.FirstParameter();l=c.LastParameter();t=c.GetType()
  if t==GeomAbs_Line:kind='line';pts=[pt(c.Value(f)),pt(c.Value(l))]
  elif t==GeomAbs_Circle:
   if abs(abs(l-f)-2*math.pi)<1e-5:
    kind='circle';ci=c.Circle();p=ci.Location();pts=[pt(p),pt(gp_Pnt(p.X()+ci.Radius(),p.Y(),p.Z()))]
   else:kind='arc';pts=[pt(c.Value(f)),pt(c.Value((f+l)/2)),pt(c.Value(l))]
  else:
   q=GCPnts_QuasiUniformDeflection(c,.005,f,l);assert q.IsDone();p=[pt(q.Value(i)) for i in range(1,q.NbPoints()+1)];pr.extend(['line',[aa,bb]] for aa,bb in zip(p,p[1:]));kind=None
  if kind:pr.append([kind,pts])
  q=GCPnts_QuasiUniformDeflection(c,.02,f,l)
  if q.IsDone():
   p=[pt(q.Value(i)) for i in range(1,q.NbPoints()+1)];bounds+=p;lines.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in p)+'"/>')
  ex.Next()
mi=[min(p[i] for p in bounds) for i in range(2)];ma=[max(p[i] for p in bounds) for i in range(2)];w=ma[0]-mi[0];hh=ma[1]-mi[1]
out.with_suffix('.json').write_text(json.dumps(pr))
out.with_suffix('.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{mi[0]-2} {mi[1]-2} {w+4} {hh+4}" width="800" height="1000"><g fill="none" stroke="#222" stroke-width="0.12">'+''.join(lines)+'</g></svg>')
print(name,'view',n,u,'bounds',mi,ma,'primitives',len(pr),flush=True)
