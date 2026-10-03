#!/usr/bin/env python3
"""Build bottom-wall gland STEP derivatives and front projections from official CAD.
Requires OCP. Writes only a staging directory until install_catalog.py is run.
"""
from pathlib import Path
import sys,json,hashlib,math
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.STEPControl import STEPControl_Reader
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID,TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Trsf,gp_Ax2,gp_Pnt,gp_Dir
from OCP.HLRBRep import HLRBRep_Algo,HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
HERE=Path(__file__).resolve().parent
CFG=json.loads((HERE/'config.json').read_text());WORK=Path(sys.argv[1]);STAGE=WORK/'stage'
def bounds(s):
 b=Bnd_Box();BRepBndLib.AddOptimal_s(s,b);return [*b.CornerMin().Coord(),*b.CornerMax().Coord()]
def read(p):
 r=STEPControl_Reader();assert r.ReadFile(str(p)).name=='IFSelect_RetDone';r.TransferRoots();return r.OneShape()
def fmt(v):return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>1e-7 else '0'
def xy(p):return ' '.join(map(fmt,p))
def main():
 report=[]
 for p in CFG['parts']:
  part=p['part'];name=part+'_BottomWall';src=WORK/(p['source']+'.STEP');shape=read(src);assert BRepCheck_Analyzer(shape).IsValid()
  source_bounds=bounds(shape);models=STAGE/'3dmodels/Controls';fps=STAGE/'footprints/Controls.pretty';review=STAGE/'reviews/Controls/CableGlands';docs=STAGE/'datasheets'
  for d in [models,fps,review,docs]:d.mkdir(parents=True,exist_ok=True)
  (models/(part+'.step')).write_bytes(src.read_bytes());(docs/(part+'_Drawing.pdf')).write_bytes((WORK/(p['source']+'-drawing.pdf')).read_bytes())
  height=CFG['back_edge_model_z_mm']+CFG['centerline_from_back_mm']
  doc=TDocStd_Document(TCollection_ExtendedString('BinXCAF'));st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
  # Source +Y points out of the gland. Rotate 180 degrees about X so it
  # points out of the enclosure bottom. Seat the washer on the outer wall.
  e=TopExp_Explorer(shape,TopAbs_SOLID);n=0;nut_moves=[]
  while e.More():
   solid=e.Current();bb=bounds(solid);shift=0
   if bb[4]<-.1 and bb[4]-bb[1]>4:
    shift=p['washer_rear_y_mm']-CFG['wall_thickness_mm']-bb[4];nut_moves.append(shift)
   t=gp_Trsf();t.SetValues(1,0,0,0,0,-1,0,p['washer_rear_y_mm']-shift,0,0,-1,height)
   placed=BRepBuilderAPI_Transform(solid,t,True).Shape();assert BRepCheck_Analyzer(placed).IsValid()
   label=st.AddShape(placed,False);TDataStd_Name.Set_s(label,TCollection_ExtendedString(part+(' locknut seated' if shift else ' component')+str(n)))
   ct.SetColor(label,Quantity_Color(.09,.09,.09,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen);n+=1;e.Next()
  assert n==5 and len(nut_moves)==1
  writer=STEPCAFControl_Writer();writer.SetColorMode(True);writer.SetNameMode(True);assert writer.Transfer(doc);target=models/(name+'.step');assert writer.Write(str(target)).name=='IFSelect_RetDone'
  placed=read(target);assert BRepCheck_Analyzer(placed).IsValid();bb=bounds(placed)
  algo=HLRBRep_Algo();algo.Add(placed);algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(),gp_Dir(0,0,1),gp_Dir(1,0,0))));algo.Update();algo.Hide();hlr=HLRBRep_HLRToShape(algo);segments=set()
  for visible in [hlr.VCompound(),hlr.OutLineVCompound()]:
   if visible.IsNull():continue
   e=TopExp_Explorer(visible,TopAbs_EDGE)
   while e.More():
    c=BRepAdaptor_Curve(TopoDS.Edge(e.Current()));a,b=c.FirstParameter(),c.LastParameter()
    if c.GetType()==GeomAbs_Line:points=[c.Value(a),c.Value(b)]
    else:
     sam=GCPnts_QuasiUniformDeflection(c,.08,a,b);assert sam.IsDone();points=[sam.Value(i) for i in range(1,sam.NbPoints()+1)]
    for u,v in zip(points,points[1:]):
     pair=tuple((round(q.X(),6),round(-q.Y(),6)) for q in [u,v])
     if math.dist(*pair)>.001:segments.add(min(pair,tuple(reversed(pair))))
    e.Next()
  lines=[f'(footprint "{name}" (version 20241229) (generator pcbnew) (layer "F.Cu")',f'(descr "Bimed {part}; manufacturer CAD bottom-wall projection; centerline 75 mm from Hammond EN4SD20208GY rear exterior. Pads are logical cable-core wiring targets, not gland contacts or drilling locations.")','(attr exclude_from_pos_files)',f'(property "Reference" "REF**" (at 0 -30) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.15))))',f'(property "Value" "{part}" (at 0 -26) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness .15))))']
  for a,b in sorted(segments):lines.append(f'(fp_line (start {xy(a)}) (end {xy(b)}) (stroke (width .05) (type default)) (layer "F.Fab"))')
  # Simplified front envelope; mounting face is local Y=0.
  lines.append(f'(fp_rect (start {fmt(bb[0])} {fmt(-bb[4])}) (end {fmt(bb[3])} {fmt(-bb[1])}) (stroke (width .15) (type default)) (fill none) (layer "F.SilkS"))')
  lines.append(f'(fp_line (start {fmt(bb[0])} 0) (end {fmt(bb[3])} 0) (stroke (width .15) (type default)) (layer "F.SilkS"))')
  for i,pin in enumerate(p['pins']):
   x=(i-(len(p['pins'])-1)/2)*2.54
   lines.append(f'(pad "{pin}" smd circle (at {fmt(x)} -8) (size 1 1) (layers "F.Cu"))')
  lines.append(f'(model "${{PARTS_LIB}}/3dmodels/Controls/{name}.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
  (fps/(name+'.kicad_mod')).write_text('\n '.join(lines)+'\n)\n')
  report.append({**p,'source_url':'https://ftp.automationdirect.com/support/drawings/3d/step/'+part+'.STEP','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_bounds_mm':source_bounds,'derived_bounds_mm':bb,'axis_height_above_footprint_mm':height,'locknut_translation_source_y_mm':nut_moves[0],'solids':n,'fab_segments':len(segments),'zero_model_offsets':True})
 (review/'geometry.json').write_text(json.dumps({'datum':CFG,'parts':report},indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
