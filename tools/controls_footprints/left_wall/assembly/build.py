#!/usr/bin/env python3
"""Build SW1's project-only wall assembly with OCP; preserve manual fields/pads.

The sheet-metal bracket is a layout envelope, not a fabrication drawing.
Manufacturer switch/handle geometry is rigidly transformed, never scaled.
The stock shaft is cut at its plain end, keeping the factory cross pin.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Circle
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax2

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from install import children, key, replace

ROOT = HERE.parents[3]
PROJECT = ROOT/'kicad/powermatic_1200'
PARTS = Path.home()/'Projects/_parts'
MOD = PROJECT/'Controls_Review.pretty/22013003_LeftWall.kicad_mod'
MODEL = PROJECT/'3dmodels/22013003_LeftWall_Assembly.step'
WALL = 1.8796  # parallel faces measured in Wiegmann N412201608C.STEP
BACK = 31.9854575040437
AXIS_Z = 38.8079943182333
COUPLING = BACK-75.0  # 534924I nominal mounting plane to coupling end
X_GAP = 25.0          # 534924I arrangement C minimum
INNER = COUPLING-X_GAP
OUTER = INNER-WALL
SHAFT_LENGTH = X_GAP+32.0  # 534924I, S0/S00 front operation
BRACKET_T = 3.0
BRACKET_HALF_HEIGHT = 110.0
BRACKET_ARM_Y = 90.0
BRACKET_DEPTH = 80.0


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(part):
    path = PARTS/'3dmodels/Controls'/f'{part}.step'
    r = STEPControl_Reader()
    assert r.ReadFile(str(path)).name == 'IFSelect_RetDone'
    r.TransferRoots()
    return r.OneShape()


def transform(shape, values):
    t = gp_Trsf(); t.SetValues(*values)
    return BRepBuilderAPI_Transform(shape, t, True).Shape()


def bounds(shape):
    box = Bnd_Box(); BRepBndLib.AddOptimal_s(shape, box, False, False)
    return [list(box.CornerMin().Coord()), list(box.CornerMax().Coord())]


def box(x, y, z, dx, dy, dz):
    return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),dx,dy,dz).Shape()


def compound(shapes):
    builder = BRep_Builder(); c = TopoDS_Compound(); builder.MakeCompound(c)
    for shape in shapes:
        builder.Add(c,shape)
    return c


def project(shape):
    algo = HLRBRep_Algo(); algo.Add(shape)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(),gp_Dir(0,0,1),gp_Dir(1,0,0))))
    algo.Update(); algo.Hide()
    hlr = HLRBRep_HLRToShape(algo)
    curves, seen = [], set()
    def point(p): return (round(p.X(),6),round(-p.Y(),6))
    def add(kind, pts):
        pts = tuple(pts)
        if kind == 'line' and math.dist(*pts) < 1e-5: return
        k = (kind,pts if kind == 'circle' else min(pts,tuple(reversed(pts))))
        if k not in seen:
            seen.add(k); curves.append((kind,pts))
    for visible in [hlr.VCompound(),hlr.OutLineVCompound()]:
        if visible.IsNull(): continue
        ex = TopExp_Explorer(visible,TopAbs_EDGE)
        while ex.More():
            c = BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
            a,b = c.FirstParameter(),c.LastParameter()
            if c.GetType() == GeomAbs_Line:
                add('line',[point(c.Value(a)),point(c.Value(b))])
            elif c.GetType() == GeomAbs_Circle:
                if abs(abs(b-a)-2*math.pi) < 1e-5:
                    cc=c.Circle(); p=cc.Location()
                    add('circle',[point(p),point(gp_Pnt(p.X()+cc.Radius(),p.Y(),p.Z()))])
                else: add('arc',[point(c.Value(a)),point(c.Value((a+b)/2)),point(c.Value(b))])
            else:
                q=GCPnts_QuasiUniformDeflection(c,.002,a,b); assert q.IsDone()
                pts=[point(q.Value(i)) for i in range(1,q.NbPoints()+1)]
                for p0,p1 in zip(pts,pts[1:]): add('line',[p0,p1])
            ex.Next()
    return curves


def graphics(curves):
    out=[]
    def xy(p): return ' '.join(f'{v:.6f}' for v in p)
    for kind,pts in curves:
        if kind=='line': coords=f'(start {xy(pts[0])}) (end {xy(pts[1])})'
        elif kind=='arc': coords=f'(start {xy(pts[0])}) (mid {xy(pts[1])}) (end {xy(pts[2])})'
        else: coords=f'(center {xy(pts[0])}) (end {xy(pts[1])})'
        fill=' (fill none)' if kind=='circle' else ''
        out.append(f'\t(fp_{kind} {coords} (stroke (width 0.05) (type solid)){fill} (layer "Dwgs.User"))')
    return out


def main():
    original=MOD.read_text()
    body=transform(read('22013003'),[-1,0,0,-480.6679870053242,
                                    0,0,1,1081.593859069632,
                                    0,1,0,-854.8441356423])
    handle=transform(read('148E1111'),[0,1,0,OUTER,0,0,1,2.44997,1,0,0,AXIS_Z-3.71987])
    stock=read('14070532')
    trimmed=BRepAlgoAPI_Common(stock,box(160-SHAFT_LENGTH,-20,-20,SHAFT_LENGTH+1,40,40)).Shape()
    shaft_end=COUPLING+15.0
    shaft=transform(trimmed,[1,0,0,shaft_end-160,0,1,0,0,0,0,1,AXIS_Z])

    # Sharp-corner hat-section envelope: wall feet, arms and rear mounting web.
    # Bend radii, reliefs and fasteners are intentionally not fabrication-ready.
    b=BRACKET_T; a=BRACKET_ARM_Y; h=BRACKET_HALF_HEIGHT; d=BRACKET_DEPTH
    plates=[box(BACK,-a-b,0,b,2*(a+b),d),
            box(INNER,a,0,BACK-INNER+b,b,d),
            box(INNER,-a-b,0,BACK-INNER+b,b,d),
            box(INNER,a,0,b,h-a,d),
            box(INNER,-h,0,b,h-a,d)]
    bracket=plates[0]
    for p in plates[1:]: bracket=BRepAlgoAPI_Fuse(bracket,p).Shape()
    # Switch's two STEP mounting-hole centers, plus provisional wall fasteners.
    holes=[(BACK,65.65,25.8079943182,2.9),(BACK,-65.65,51.8079943182,2.9)]
    holes += [(INNER,y,z,3.25) for y in [-101.5,101.5] for z in [15,65]]
    for x,y,z,r in holes:
        drill=BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x-1,y,z),gp_Dir(1,0,0)),r,b+2).Shape()
        bracket=BRepAlgoAPI_Cut(bracket,drill).Shape()
    shapes={'switch':body,'handle':handle,'cut_shaft':shaft,'provisional_bracket':bracket}
    assert all(BRepCheck_Analyzer(s).IsValid() for s in shapes.values())
    sb=bounds(shaft)
    assert abs(sb[1][0]-sb[0][0]-SHAFT_LENGTH)<1e-5
    assembly=compound(shapes.values())
    w=STEPControl_Writer(); w.Transfer(assembly,STEPControl_AsIs)
    assert w.Write(str(MODEL)).name=='IFSelect_RetDone'

    # Preserve the saved body lines and user-edited properties/pads verbatim.
    base=(HERE/'body.kicad_mod').read_text()
    body_graphics=[n for _,_,n in children(base) if key(n).startswith('fp_')]
    # HLR the handle and shaft together, so the inserted shaft is hidden.
    added=graphics(project(compound([handle,shaft])))+graphics(project(bracket))
    # Wall section is only a two-line drawing reference, never a solid obstruction.
    for x in [OUTER,INNER]:
        for y0,y1 in [(-118,-12),(12,118)]:
            added += graphics([('line',[(x,y0),(x,y1)])])
    model='\t(model "${KIPRJMOD}/3dmodels/22013003_LeftWall_Assembly.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'
    edits=[]
    for start,end,node in children(original):
        if key(node).startswith('fp_') or key(node)=='model': edits.append((start,end,''))
        elif key(node)=='descr': edits.append((start,end,'(descr "Socomec disconnect, handle, shaft and provisional left-wall bracket assembly")'))
    new=replace(original,edits).rstrip()[:-1].rstrip()+'\n'+'\n'.join(body_graphics+added+[model])+'\n)\n'
    for k in ['property','pad']:
        assert [n for _,_,n in children(original) if key(n)==k]==[n for _,_,n in children(new) if key(n)==k]
    assert MOD.read_text()==original,'Concurrent footprint save; rerun'
    MOD.write_text(new)
    report={
        'footprint':'Controls_Review:22013003_LeftWall',
        'units':'mm','wall_thickness':WALL,'wall_inner_x':INNER,'wall_outer_x':OUTER,
        'switch_rear_mounting_x':BACK,'coupling_end_nominal_x':COUPLING,
        'front_coupling_to_inner_wall':X_GAP,'shaft_length':SHAFT_LENGTH,
        'shaft_length_status':'layout cut length from manufacturer formula; verify actual engagement before cutting',
        'handle_flange_to_inner_wall':WALL,
        'coupling':'75 mm nominal envelope reserved; coupling absent from manufacturer bare STEP and not redrawn',
        'bracket':{'thickness':b,'height':2*h,'depth':d,'reach_to_switch_mounting_face':BACK-INNER,
                   'status':'provisional sharp-corner envelope; bend allowance, reliefs, fasteners and wiring clearance require fabrication review'},
        'sources':{p:digest(PARTS/'3dmodels/Controls'/f'{p}.step') for p in ['22013003','148E1111','14070532']},
        'source_documents':['Socomec_534924.pdf page 2 arrangement C','22013003_CAD_Drawing.pdf','148E1111_CAD_Drawing.pdf','Wiegmann N412201608C.STEP wall faces'],
        'component_bounds':{name:bounds(s) for name,s in shapes.items()},
        'model_sha256':digest(MODEL),'footprint_sha256':digest(MOD),
        'properties_and_pads_preserved':True,'solids_valid':True,
    }
    (HERE/'dimensions.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'model':str(MODEL),'added_graphics':len(added),'wall':WALL,'shaft':SHAFT_LENGTH}))


if __name__=='__main__': main()
