#!/usr/bin/env python3
"""Generate a dimension-backed FRN-R-10 assembly representation (requires OCP).

No PCB pads: FH1 owns the electrical connections. Overall envelope comes from
Bussmann data sheet 1019; cap/body subdivisions are illustrative, not tooling CAD.
"""
from pathlib import Path
import argparse, json, hashlib
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.STEPControl import STEPControl_Reader
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

NAME='FRN-R-10_RM25030-3SR_Front'
MODEL='FRN-R-10_RM25030-3SR.step'
HEIGHT=30.414015
RADIUS=7.112
HALF_LENGTH=25.4
CAP_LENGTH=12.7
BODY_RADIUS=6.8

def bounds(shape):
 b=Bnd_Box();BRepBndLib.Add_s(shape,b)
 return [getattr(p,a)() for p in [b.CornerMin(),b.CornerMax()] for a in ['X','Y','Z']]

def model(path, height):
 doc=TDocStd_Document(TCollection_ExtendedString('BinXCAF'))
 st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
 for name, radius, y, length, rgb in [
  ('Fiberglass body (simplified)',BODY_RADIUS,-12.7,25.4,(.39,.34,.24)),
  ('End cap A (simplified)',RADIUS,-HALF_LENGTH,CAP_LENGTH,(.76,.77,.78)),
  ('End cap B (simplified)',RADIUS,12.7,CAP_LENGTH,(.76,.77,.78))]:
  s=BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0,y,height),gp_Dir(0,1,0)),radius,length).Shape()
  assert BRepCheck_Analyzer(s).IsValid()
  label=st.AddShape(s,False);TDataStd_Name.Set_s(label,TCollection_ExtendedString(name))
  ct.SetColor(label,Quantity_Color(*rgb,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
 w=STEPCAFControl_Writer();w.SetColorMode(True);w.SetNameMode(True)
 assert w.Transfer(doc);assert w.Write(str(path)).name=='IFSelect_RetDone'
 r=STEPControl_Reader();assert r.ReadFile(str(path)).name=='IFSelect_RetDone';r.TransferRoots();s=r.OneShape()
 assert BRepCheck_Analyzer(s).IsValid()
 actual=bounds(s);expected=[-RADIUS,-HALF_LENGTH,height-RADIUS,RADIUS,HALF_LENGTH,height+RADIUS]
 assert max(abs(a-b) for a,b in zip(actual,expected))<1e-5
 return actual

def footprint():
 lines=[f'(footprint "{NAME}"', '(version 20241229)', '(generator pcbnew)', '(layer "F.Cu")',
 '(descr "Eaton Bussmann FRN-R-10, 10 A Class RK5, 50.8 x 14.224 mm; pad-free fuse representation for RM25030-3SR DIN35x7p5 holder. Simplified cap detail.")',
 '(tags "FRN-R-10 Allfuses Eaton Bussmann Class RK5 cartridge fuse")',
 '(property "Reference" "REF**" (at 0 0) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.15))))',
 '(property "Value" "FRN-R-10" (at 0 28) (layer "F.Fab") (hide yes) (effects (font (size 1.27 1.27) (thickness 0.15))))',
 '(property "Datasheet" "${PARTS_LIB}/datasheets/FRN-R-10_FRN-R_1019_Archive.pdf" (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))',
 '(attr board_only exclude_from_pos_files exclude_from_bom)']
 def rect(x,y,x2,y2,layer,width):
  lines.append(f'(fp_rect (start {x} {y}) (end {x2} {y2}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))')
 # Analytic orthographic projection of the three cylinders.
 rect(-BODY_RADIUS,-12.7,BODY_RADIUS,12.7,'F.Fab',.05)
 rect(-RADIUS,-25.4,RADIUS,-12.7,'F.Fab',.05)
 rect(-RADIUS,12.7,RADIUS,25.4,'F.Fab',.05)
 # Simplified assembly outline and end-cap boundaries.
 rect(-RADIUS,-25.4,RADIUS,25.4,'F.SilkS',.15)
 for y in [-12.7,12.7]:
  lines.append(f'(fp_line (start {-RADIUS} {y}) (end {RADIUS} {y}) (stroke (width 0.15) (type default)) (layer "F.SilkS"))')
 lines.append(f'(model "${{PARTS_LIB}}/3dmodels/Controls/{MODEL}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
 return '\n  '.join(lines)+'\n)\n'

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 models=args.output/'3dmodels/Controls';fps=args.output/'footprints/Controls.pretty';review=args.output/'reviews/Controls/FRN-R-10'
 for d in [models,fps,review]:d.mkdir(parents=True,exist_ok=True)
 b=model(models/MODEL,HEIGHT);model(models/'FRN-R-10.step',0)
 (fps/(NAME+'.kicad_mod')).write_text(footprint())
 report={'part':'FRN-R-10','supplier':'Allfuses','manufacturer':'Eaton Bussmann','source':'datasheets/FRN-R-10_FRN-R_1019_Archive.pdf, family drawing for 0-30 A','nominal_length_mm':50.8,'nominal_diameter_mm':14.224,'axis':'Y','centerline_height_mm':HEIGHT,'model_bounds_mm':b,'holder_model':'RM25030-3SR_DIN35x7p5.step','holder_pole_centers_x_mm':[-24.0284945,.484112,24.996719],'holder_pitch_mm':24.51260675,'rounded_pitch_mm':25,'model_offset_mm':[0,0,0],'model_rotation_deg':[0,0,0],'model_scale':[1,1,1],'pads':0,'simplifications':['Cap length 12.7 mm and body diameter 13.6 mm are illustrative subdivisions.','Class R rejection groove, labels and internal elements omitted.','Holder clips are shown in unloaded spring state; fuse/clip visual overlap is not a physical fit test.'],'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [models/MODEL,models/'FRN-R-10.step',fps/(NAME+'.kicad_mod')]}}
 (review/'geometry.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
