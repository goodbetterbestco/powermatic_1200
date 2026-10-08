from pathlib import Path
import json,math
from OCP.STEPControl import STEPControl_Reader
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE,TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Circle
from OCP.BRepCheck import BRepCheck_Analyzer
w=Path('/private/tmp/powermatic-s3-model')
def load(path):
 r=STEPControl_Reader();assert r.ReadFile(str(path)).name=='IFSelect_RetDone';r.TransferRoots();return r.OneShape()
def bounds(s):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(s,b,False,False);return [list(b.CornerMin().Coord()),list(b.CornerMax().Coord())]
shape=load(w/'S3-native.step');plate=load(w/'pcb-top-datum.step');bb=bounds(shape);platebb=bounds(plate)
assert BRepCheck_Analyzer(shape).IsValid()
# KiCad's zero-offset F.Cu component datum is 1.595 mm for this 1.6 mm stack.
# The board-only export excludes copper/mask, so its dielectric top is lower.
assert abs(bb[0][2]-1.595)<1e-5,(bb,platebb)
geom=json.loads((w/'assets/geometry.json').read_text());src=geom['bounds_mm'];delta=[bb[0][i]-src[0][i] for i in range(3)]
assert abs(delta[0]-600)<1e-5 and abs(delta[1]+231.241)<1e-5
for i in range(3):assert abs((bb[1][i]-bb[0][i])-(src[1][i]-src[0][i]))<1e-5
ex=TopExp_Explorer(shape,TopAbs_EDGE);centers=[]
while ex.More():
 c=BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
 if c.GetType()==GeomAbs_Circle and abs(c.Circle().Radius()-4.053989)<1e-5:centers.append(list(c.Circle().Location().Coord()))
 ex.Next()
checks=[]
for p in geom['pads']:
 target=[p['source_head_rim_center_mm'][i]+delta[i] for i in range(3)]
 error=min(math.dist(target,c) for c in centers)
 assert error<.002,(p['number'],target,error)
 checks.append({'pin':p['number'],'source_screw':p['model_screw'],'native_rim_center_error_mm':error})
ex=TopExp_Explorer(shape,TopAbs_SOLID);n=0
while ex.More():n+=1;ex.Next()
assert n==46
report={'native_component_bounds_mm':bb,'native_board_bounds_mm':platebb,'model_base_and_KiCad_top_component_plane_z_mm':bb[0][2],'native_transform_mm':delta,'all_46_solids_preserved':True,'size_preserved':True,'screw_checks':checks,'max_screw_center_error_mm':max(c['native_rim_center_error_mm'] for c in checks)}
(w/'native-alignment.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='screw_checks'},indent=2))
