#!/usr/bin/env python3
"""Build BACO 222102's project-specific left-wall footprint from original CAD.

Run with cadquery-ocp. The original STEP is read-only. Three handle components
are translated to admit the enclosure wall; all geometry and colors are kept.
Footprint pads are panel-wiring targets, not a PCB or enclosure drill pattern.
"""
from pathlib import Path
import hashlib,json,math,sys
sys.dont_write_bytecode=True
from OCP.STEPControl import STEPControl_Reader,STEPControl_AsIs
from OCP.STEPCAFControl import STEPCAFControl_Reader,STEPCAFControl_Writer
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_Label
from OCP.collections import Sequence_TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_Location
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Trsf,gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]/'kicad/powermatic_1200'
PARTS=Path.home()/'Projects/_parts'
SOURCE=PARTS/'3dmodels/Controls/222102.step'
MODEL=Path.home()/'Projects/_parts/3dmodels/Controls/222102_LeftWall_1p8796mm.step'
MOD=Path.home()/'Projects/_parts/footprints/Controls.pretty/222102_LeftWall.kicad_mod'
WALL=1.8796
SEAT=49.95
OUTER=SEAT+WALL
DEPTH=33.0 # rear-most envelope in the new orientation; shaft 33 mm above it
FAN_RADIUS=6.0
# Product names in the manufacturer's assembly, not inferred body indexes.
HANDLE_COMPONENTS={'S01737000.1','S01737300.1','S01751480.1'}
sys.path.insert(0,str(HERE.parent/'left_wall/assembly'))
from build import project,graphics  # exact visible-edge projection; no main side effects


def name(label):
    value=TDataStd_Name()
    return value.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),value) else ''

def bounds(shape):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(shape,b,False,False)
    return [list(b.CornerMin().Coord()),list(b.CornerMax().Coord())]

def reader_shape(path):
    r=STEPControl_Reader();assert r.ReadFile(str(path)).name=='IFSelect_RetDone'
    r.TransferRoots();return r.OneShape()

def transform():
    # Native +Z points out through handle. +Y stays up. Native +X faces viewer.
    # CAD X=OUTER-sourceZ; CAD Y=sourceY; CAD Z=sourceX+DEPTH.
    t=gp_Trsf();t.SetValues(0,0,-1,OUTER,0,1,0,0,1,0,0,DEPTH);return t


def main():
    source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    d=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'))
    r=STEPCAFControl_Reader();r.SetNameMode(True);r.SetColorMode(True)
    assert r.ReadFile(str(SOURCE)).name=='IFSelect_RetDone';assert r.Transfer(d)
    st=XCAFDoc_DocumentTool.ShapeTool_s(d.Main());roots=Sequence_TDF_Label();st.GetFreeShapes(roots)
    assert roots.Length()==1
    root=roots.Value(1);components=Sequence_TDF_Label();assert st.GetComponents_s(root,components)
    tr=gp_Trsf();tr.SetTranslation(gp_Vec(0,0,WALL));delta=TopLoc_Location(tr)
    moved=[]
    for i in range(1,components.Length()+1):
        l=components.Value(i);n=name(l)
        if n in HANDLE_COMPONENTS:
            before=bounds(st.GetShape_s(l));location=delta.Multiplied(st.GetLocation_s(l))
            XCAFDoc_Location.Set_s(l,location)
            after=bounds(st.GetShape_s(l))
            for old,new in zip(before,after):
                assert abs(new[0]-old[0])<1e-6 and abs(new[1]-old[1])<1e-6
                assert abs(new[2]-old[2]-WALL)<1e-6, (n,before,after,old,new)
            moved.append({'component':n,'before_bounds':before,'after_bounds':after})
    assert {m['component'] for m in moved}==HANDLE_COMPONENTS
    st.UpdateAssemblies();MODEL.parent.mkdir(exist_ok=True)
    w=STEPCAFControl_Writer();w.SetColorMode(True);w.SetNameMode(True)
    assert w.Transfer(d,STEPControl_AsIs);assert w.Write(str(MODEL)).name=='IFSelect_RetDone'
    source=reader_shape(SOURCE);shape=reader_shape(MODEL)
    # The derivative must preserve all 80 solids and validity.
    solid_counts=[]
    for s in [source,shape]:
        ex=TopExp_Explorer(s,TopAbs_SOLID);n=0
        while ex.More():n+=1;ex.Next()
        solid_counts.append(n);assert BRepCheck_Analyzer(s).IsValid()
    assert solid_counts==[80,80]
    projected=BRepBuilderAPI_Transform(shape,transform(),True).Shape()
    curves=project(projected);bb=bounds(projected)
    # Front-access terminal screw heads, from manufacturer cylinder axes.
    # Seen facing the operating handle: L1/L2/L3 left-to-right, line bank above.
    terminals=[('1',[-13.5,28.35,27.42086449]),('3',[0,28.35,27.42086449]),('5',[13.5,28.35,27.42086449]),
               ('2',[-13.5,-28.35,27.42086466]),('4',[0,-28.35,27.42086466]),('6',[13.5,-28.35,27.42086466])]
    pads=[]
    for i,(number,p) in enumerate(terminals):
        actual=[OUTER-p[2],-p[1]];angle=-math.pi/2+2*math.pi*(i%3)/3
        target=[actual[0]+FAN_RADIUS*math.cos(angle),actual[1]+FAN_RADIUS*math.sin(angle)]
        pads.append(dict(number=number,source_xyz_mm=p,projected_center_mm=actual,
                         depth_mm=p[0]+DEPTH,center_mm=target))
    for i,p in enumerate(pads):
        for q in pads[i+1:]:assert math.dist(p['center_mm'],q['center_mm'])>3.2
    def fmt(x):return f'{x:.6f}'.rstrip('0').rstrip('.') if abs(x)>5e-7 else '0'
    def xy(p):return ' '.join(map(fmt,p))
    lines=['(footprint "222102_LeftWall"',' (version 20241229)',' (generator "pcbnew")',' (generator_version "9.0")',' (layer "F.Cu")',
           ' (descr "BACO 222102 / 0172001 left-wall assembly; 1.8796 mm wall; origin at outer wall/shaft axis; 14 AWG wiring targets")',
           ' (tags "Controls BACO left wall panel mount")',' (attr exclude_from_pos_files)',
           ' (property "Reference" "REF**" (at 11.8 -18) (layer "Dwgs.User") (effects (font (size 2.5 2.5) (thickness 0.15))))',
           ' (property "Value" "222102" (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))',
           ' (property "Datasheet" "${PARTS_LIB}/datasheets/222102_Datasheet.pdf" (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))']
    lines+=graphics(curves)
    # Wall reference lines only: no wall solid in the component's STEP.
    for x in [0,WALL]:
        lines.append(f' (fp_line (start {fmt(x)} -40) (end {fmt(x)} 40) (stroke (width 0.05) (type dash)) (layer "Dwgs.User"))')
    for p in pads:lines.append(f' (pad "{p["number"]}" thru_hole circle (at {xy(p["center_mm"])}) (size 3 3) (drill 2) (layers "*.Cu" "*.Mask"))')
    lines += [' (model "${PARTS_LIB}/3dmodels/Controls/222102_LeftWall_1p8796mm.step"',
              f'  (offset (xyz {OUTER} 0 {DEPTH})) (scale (xyz 1 1 1)) (rotate (xyz 0 90 0)))',')','']
    MOD.write_text('\n'.join(lines))
    report={'part':'222102','footprint':'Controls:222102_LeftWall','original_step':str(SOURCE),'original_sha256':source_hash,
            'model':'${PARTS_LIB}/3dmodels/Controls/'+MODEL.name,'wall_thickness_mm':WALL,
            'origin_xy':'outside enclosure wall face at operating shaft center',
            'model_z_datum':'rear-most envelope is Z=0; shaft is Z=33 mm. Final wall depth above backplate remains a placement choice.',
            'native_mounting_face_z_mm':SEAT,'native_outer_wall_z_mm':OUTER,
            'transform_3d':[[0,0,-1,OUTER],[0,1,0,0],[1,0,0,DEPTH]],
            'kicad_footprint_xy':['OUTER - source_Z','-source_Y'],
            'model_offset_mm':[OUTER,0,DEPTH],'model_rotation_degrees':[0,90,0],
            'source_bounds_mm':bounds(source),'adjusted_native_bounds_mm':bounds(shape),'oriented_bounds_mm':bb,
            'side_envelope_mm':[bb[1][0]-bb[0][0],bb[1][1]-bb[0][1]],
            'moved_handle_components':moved,'solid_counts_before_after':solid_counts,'pads':pads,'fan_radius_mm':FAN_RADIUS,
            'source_terminals':'Front-access screw head cylinder axes; source head bounding planes. Other end of each clamp is not an additional independently numbered terminal.',
            'manufacture_drawing_comparison':{'handle_face_mm':{'drawing':66,'model':66},'height_mm':{'drawing':75.4,'model':75.15},'mount_face_to_body_rear_mm':{'drawing':55,'model':55.1600005},'handle_projection_mm':{'drawing':33,'model':32.95}},
            'original_preserved':hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash,'projected_curve_count':len(curves)}
    (HERE/'geometry.json').write_text(json.dumps(report,indent=2)+'\n')
    print('BACO side envelope',report['side_envelope_mm'],'curves',len(curves),'pads',len(pads),flush=True)

if __name__=='__main__':main()
