#!/usr/bin/env python3
"""Attach unscaled original manufacturer models to reviewed Controls footprints.

Run after the original DXF batch to apply final catalog transforms. Geometry
snapshots make this repeatable without accumulating transformations. The fuse
holder retains its approved DWG outline; pads follow the source STEP screw centers.
"""
from pathlib import Path
import json,hashlib,re,math,subprocess
H=Path(__file__).resolve().parent
ROOT=H.parents[2];LIB=Path.home()/'Projects/_parts/footprints/Controls.pretty'
PARTS=Path.home()/'Projects/_parts'
def fmt(v):return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>.0000005 else '0'
def xy(p):return ' '.join(fmt(x) for x in p)
def graphics(spec):
 result=[];seen=set()
 for kind,points in json.loads((H/'sources'/f'{spec["part"]}-projected.json').read_text()):
  pts=tuple(tuple(round(v,6) for v in [p[0]+spec['offset'][0],p[1]-spec['offset'][1]]) for p in points)
  if kind=='line' and pts[0]==pts[1]:continue
  key=(kind,pts if kind=='circle' else min(pts,tuple(reversed(pts))))
  if key in seen:continue
  seen.add(key)
  if kind=='line':coords=f'(start {xy(pts[0])}) (end {xy(pts[1])})'
  elif kind=='arc':coords=f'(start {xy(pts[0])}) (mid {xy(pts[1])}) (end {xy(pts[2])})'
  else:coords=f'(center {xy(pts[0])}) (end {xy(pts[1])})'
  result.append(f'  (fp_{kind} {coords} (stroke (width 0.05) (type solid))'+(' (fill none)' if kind=='circle' else '')+' (layer "Dwgs.User"))')
 return result
result=[]
for s in json.loads((H/'config.json').read_text())['parts']:
 text=(H/'sources'/(s['name']+'.kicad_mod')).read_text()
 text=re.sub(r'\(attr [^)]*\)','(attr exclude_from_pos_files)',text,count=1)
 if s['part']=='RM25030-3SR':
  text=re.sub(r'\(descr "[^"]*"\)', '(descr "RM25030-3SR uncovered front elevation; reviewed DWG outline 74.491 x 80.400 mm, STEP screw-center wiring targets; 14 AWG review pads")', text)
 if s['replace_projection']:
  text='\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('(fp_'))+'\n'
  text=text.rstrip()[:-1]+'\n'+'\n'.join(graphics(s))+'\n)\n'
  text=re.sub(r'\(descr "[^"]*"\)','(descr "RM25030-3SR uncovered front elevation; manufacturer STEP projection 74.751 x 80.400 mm; six 14 AWG panel wiring targets")',text)
 for p in s['pads']:
  pat=r'(\(pad "'+re.escape(p['number'])+r'"[^\n]*?\(at )[-.\d]+ [-.\d]+(\))'
  text,n=re.subn(pat,lambda m:m[1]+xy(p['center_mm'])+m[2],text,count=1);assert n==1
 text=text.rstrip()[:-1]+f'  (model "${{PARTS_LIB}}/3dmodels/Controls/{s["model"]}"\n    (offset (xyz {xy(s["offset"])}))\n    (scale (xyz 1 1 1))\n    (rotate (xyz {xy(s["rotation"])})))\n)\n'
 dest=LIB/(s['name']+'.kicad_mod');dest.write_text(text)
 subprocess.run(['/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9',str(H.parent/'label_references.py'),str(dest),'--write'],check=True)
 rec=dict(s,model_sha256=hashlib.sha256((PARTS/'3dmodels/Controls'/s['model']).read_bytes()).hexdigest(),footprint_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
 result.append(rec);print(s['part'],len(s['pads']),'pads')
(H/'geometry_review.json').write_text(json.dumps(result,indent=2)+'\n')
