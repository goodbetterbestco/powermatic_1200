from pathlib import Path
import json,math,sys
here=Path(__file__).resolve().parent
parts_root=Path.home()/'Projects/_parts'
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
parts={'HMX1-AUX11-F':([0,1,0],[1,0,0],-1),'22013003':([1,0,0],[0,1,0],1),'HMX1-MI':([0,1,0],[0,0,1],1)}
for part in sys.argv[1:]:
 n,u,ys=parts[part];r=STEPControl_Reader();r.ReadFile(str(parts_root/'3dmodels/Controls'/(part+'.step')));r.TransferRoots();shape=r.OneShape()
 a=HLRBRep_Algo();a.Add(shape);a.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*n),gp_Dir(*u))));a.Update();a.Hide();h=HLRBRep_HLRToShape(a)
 out=[]
 def pt(p):return [p.X(),p.Y()*ys]
 for visible in [h.VCompound(),h.OutLineVCompound()]:
  if visible.IsNull():continue
  ex=TopExp_Explorer(visible,TopAbs_EDGE)
  while ex.More():
   c=BRepAdaptor_Curve(TopoDS.Edge(ex.Current()));f=c.FirstParameter();l=c.LastParameter();typ=c.GetType()
   if typ==GeomAbs_Line:out.append(['line',[pt(c.Value(f)),pt(c.Value(l))]])
   elif typ==GeomAbs_Circle:
    if abs(abs(l-f)-2*math.pi)<1e-5:
     ci=c.Circle();p=ci.Location();out.append(['circle',[pt(p),pt(gp_Pnt(p.X()+ci.Radius(),p.Y(),p.Z()))]])
    else:out.append(['arc',[pt(c.Value(f)),pt(c.Value((f+l)/2)),pt(c.Value(l))]])
   else:
    q=GCPnts_QuasiUniformDeflection(c,0.002,f,l)
    if not q.IsDone():raise RuntimeError('Discretization failed')
    pts=[pt(q.Value(i)) for i in range(1,q.NbPoints()+1)]
    out.extend(['line',[aa,bb]] for aa,bb in zip(pts,pts[1:]))
   ex.Next()
 (here/'sources'/(part+'-projected.json')).write_text(json.dumps(out))
 print(part,len(out),flush=True)
