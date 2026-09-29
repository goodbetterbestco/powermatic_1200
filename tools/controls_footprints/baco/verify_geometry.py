#!/usr/bin/env python3
"""Compare native KiCad STEP export with the independently transformed model."""
from pathlib import Path
import hashlib, json, math
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
g=json.loads((HERE/'geometry.json').read_text())

def read(path):
    r=STEPControl_Reader();assert r.ReadFile(str(path)).name=='IFSelect_RetDone'
    r.TransferRoots();return r.OneShape()

def boxes(shape):
    result=[];e=TopExp_Explorer(shape,TopAbs_SOLID)
    while e.More():
        b=Bnd_Box();BRepBndLib.AddOptimal_s(e.Current(),b,False,False)
        result.append(list(b.CornerMin().Coord())+list(b.CornerMax().Coord()))
        e.Next()
    return result

assert hashlib.sha256(Path(g['original_step']).read_bytes()).hexdigest()==g['original_sha256']
t=gp_Trsf();t.SetValues(*[x for row in g['transform_3d'] for x in row])
expected=boxes(BRepBuilderAPI_Transform(read(Path(g['model'].replace('${PARTS_LIB}',str(Path.home()/'Projects/_parts')))),t,True).Shape())
actual=boxes(read('/tmp/baco-leftwall/native.step'))
board=[b for b in actual if abs(b[3]-b[0]-100)<1e-5 and abs(b[4]-b[1]-88)<1e-5]
assert len(board)==1
actual.remove(board[0]);assert len(actual)==len(expected)==80
# KiCad locates models on the review board's front surface. Compare all 80
# solid envelopes after removing that one common PCB surface offset.
dz=min(b[2] for b in actual)-min(b[2] for b in expected)
assert 1.5<dz<1.7, dz
for b in actual:b[2]-=dz;b[5]-=dz
errors=[]
for b in expected:
    i=min(range(len(actual)),key=lambda j:max(abs(x-y) for x,y in zip(b,actual[j])))
    errors.append(max(abs(x-y) for x,y in zip(b,actual.pop(i))))
assert max(errors)<0.00005, max(errors)
for ids in [('1','3','5'),('2','4','6')]:
    ps=[p for p in g['pads'] if p['number'] in ids]
    center=[sum(p['center_mm'][i] for p in ps)/3 for i in (0,1)]
    assert math.dist(center,ps[0]['projected_center_mm'])<1e-6
    assert all(abs(math.dist(center,p['center_mm'])-6)<1e-6 for p in ps)
report={'native_export_solid_count':81,'model_solid_count':80,
        'review_board_surface_offset_mm':dz,
        'maximum_model_solid_bounds_difference_mm':max(errors),
        'original_step_hash_matches':True,'two_equilateral_fanouts':True,
        'scope':'All model solids compared after native KiCad export; review board removed. No final enclosure placement implied.'}
(HERE/'alignment_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
