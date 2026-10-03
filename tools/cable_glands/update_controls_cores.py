#!/usr/bin/env python3
"""Reconcile the user's corrected seven-core controls cable without moving glands."""
from pathlib import Path
import sys,re,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'controls_footprints/left_wall'))
from install import children,key,field,replace
from sexpr import parse,one,prop
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PARTS=Path.home()/'Projects/_parts'
def modify_library(n):
 pins=[cc for _,_,c in children(n) if key(c)=='symbol' for _,_,cc in children(c) if key(cc)=='pin']
 assert len(pins)==10, 'This one-time migration requires the original ten-pin symbol; refusing to move an already updated symbol.'
 ed=[]
 for a,b,c in children(n):
  if key(c)=='symbol':
   ee=[]
   for aa,bb,cc in children(c):
    if key(cc)=='pin':
     p=parse(cc);number=one(p,'number')[1]
     if int(number)>7:ee.append((aa,bb,''))
     else:ee.append((aa,bb,re.sub(r'(\(at -17.78 )([-\d.]+)',lambda m:m[1]+f'{float(m[2])-3.81:.2f}',cc)))
    elif key(cc)=='rectangle':ee.append((aa,bb,cc.replace('13.97','10.16')))
   ed.append((a,b,replace(c,ee)))
  elif key(c)=='property' and c.startswith('(property "Cable cores"'):ed.append((a,b,c.replace('"10"','"7"',1)))
 return replace(n,ed)
def library_file(p):
 s=p.read_text();ed=[(a,b,modify_library(n)) for a,b,n in children(s) if key(n)=='symbol' and parse(n)[1]=='BSPBX-22-W'];assert len(ed)==1;p.write_text(replace(s,ed))
def footprint(p,board=False):
 s=p.read_text()
 def adjust(n):
  ed=[]
  for a,b,c in children(n):
   if key(c)=='pad':
    num=int(parse(c)[1]);ed.append((a,b,'' if num>7 else re.sub(r'(\(at )([-\d.]+)( -8)',lambda m:m[1]+str(round(float(m[2])+3.81,6))+m[3],c, count=1)))
  return replace(n,ed)
 if board:
  ed=[(a,b,adjust(n)) for a,b,n in children(s) if key(n)=='footprint' and field(n,'Reference')=='J5'];assert len(ed)==1;s=replace(s,ed)
 else:s=adjust(s)
 p.write_text(s)
if sys.argv[1]=='catalog':
 library_file(PARTS/'symbols/Controls.kicad_sym');footprint(PARTS/'footprints/Controls.pretty/BSPBX-22-W_BottomWall.kicad_mod')
else:
 p=ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_sch';s=p.read_text();ed=[]
 for a,b,n in children(s):
  k=key(n)
  if k=='lib_symbols':
   ee=[(aa,bb,modify_library(nn)) for aa,bb,nn in children(n) if key(nn)=='symbol' and parse(nn)[1]=='Controls:BSPBX-22-W'];ed.append((a,b,replace(n,ee)))
  elif k=='symbol' and field(n,'Reference')=='J5':
   ee=[]
   for aa,bb,nn in children(n):
    if key(nn)=='pin' and int(parse(nn)[1])>7:ee.append((aa,bb,''))
    elif key(nn)=='property' and nn.startswith('(property "Cable cores"'):ee.append((aa,bb,nn.replace('"10"','"7"',1)))
   ed.append((a,b,replace(n,ee)))
  elif k=='no_connect' and 397<float(one(parse(n),'at')[1])<398:ed.append((a,b,''))
  elif k in ['wire','label','global_label']:
   pts=re.findall(r'\((?:xy|at) ([-\d.]+) ([-\d.]+)',n)
   if pts and all(375<float(x)<398 and 165<float(y)<188 for x,y in pts):ed.append((a,b,re.sub(r'(\((?:xy|at) [-\d.]+ )([-\d.]+)',lambda m:m[1]+str(round(float(m[2])+3.81,6)),n)))
  elif k=='text' and ('6452T44' in n or 'cores 8-10' in n):ed.append((a,b,n.replace('/ 10 cores','/ 7 cores').replace('J5 cores 8-10 spare. ','J5 uses all seven cable cores. ')))
 s=replace(s,ed);s=re.sub(r'^\s+\n','\n',s,flags=re.M);p.write_text(s);Path('/private/tmp/powermatic-glands/candidate.kicad_sch').write_text(s)
 footprint(ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_pcb',True)
 cfg=json.loads((HERE/'config.json').read_text());p=cfg['parts'][2];p['cores']=7;p['pins']=p['pins'][:7];p['signals']=p['signals'][:7];(HERE/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
 pins=json.loads((HERE/'pin_map.json').read_text());pins=[p for p in pins if p['signal']];(HERE/'pin_map.json').write_text(json.dumps(pins,indent=2)+'\n')
 print('Updated only J5 to seven cores; gland geometry and placement retained.')
