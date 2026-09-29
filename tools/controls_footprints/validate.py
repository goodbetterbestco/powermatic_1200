#!/usr/bin/env python3
"""Run with KiCad's bundled Python (pcbnew); write native review SVGs."""
from pathlib import Path
import itertools,json,math,re,subprocess,sys
import pcbnew
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LIB=Path.home()/'Projects/_parts/footprints/Controls.pretty'
config=json.loads((HERE/'config.json').read_text())
# A lightweight reader keeps exact pin strings, including dots and '+'.
def sexpr(path):
 stack=[]
 for t in re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',path.read_text()):
  if t=='(':stack.append([])
  elif t==')':
   x=stack.pop()
   if stack:stack[-1].append(x)
   else:return x
  else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
def children(x,key):return [v for v in x if isinstance(v,list) and v and v[0]==key]
sym_path=Path(sys.argv[1]) if len(sys.argv)>1 else Path.home()/'Projects/_parts/symbols/Controls.kicad_sym'
root=sexpr(sym_path);symbol_pins={}
for sym in children(root,'symbol'):
 symbol_pins[sym[1]]=[children(p,'number')[0][1] for unit in children(sym,'symbol') for p in children(unit,'pin')]
work=Path('/tmp/powermatic-controls-native');work.mkdir(exist_ok=True)
preview=HERE/'previews';preview.mkdir(exist_ok=True)
cli='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
result=[]
for spec in config['footprints']:
 f=pcbnew.FootprintLoad(str(LIB),spec['name']);assert f,spec['name']
 pads=list(f.Pads());ids=[p.GetNumber() for p in pads]
 expected=spec.get('expected_pads',[p['number'] for p in spec['pads']])
 assert sorted(ids)==sorted(expected),(spec['name'],ids,expected)
 assert len(ids)==len(set(ids)),spec['name']
 for a,b in itertools.combinations(pads,2):
  pa,pb=a.GetPosition(),b.GetPosition()
  dist=math.hypot(pa.x-pb.x,pa.y-pb.y)/1e6
  assert dist>3.1,(spec['name'],'overlap',a.GetNumber(),b.GetNumber(),dist)
 for p in pads:
  assert p.GetDrillSize().x==pcbnew.FromMM(2)
  assert p.GetSize().x==pcbnew.FromMM(3)
  assert p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH
 for g in f.GraphicalItems():assert g.GetLayer()==pcbnew.Dwgs_User,(spec['name'],g.GetLayer())
 match=None
 if spec['part'] in symbol_pins:
  assert sorted(ids)==sorted(symbol_pins[spec['part']]),(spec['name'],ids,symbol_pins[spec['part']])
  match=True
 board=pcbnew.BOARD();board.Add(f);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(200),pcbnew.FromMM(200)))
 bp=work/(spec['name']+'.kicad_pcb');pcbnew.SaveBoard(str(bp),board)
 subprocess.run([cli,'pcb','export','svg','--layers','Dwgs.User,F.Cu','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','2','--mode-single','--output',str(preview/(spec['name']+'.svg')),str(bp)],check=True,stdout=subprocess.DEVNULL)
 result.append({'name':spec['name'],'pad_count':len(ids),'pads':ids,'native_load':True,'native_svg_export':True,'catalog_pin_set_matches':match})
 print(spec['name'],len(ids),'pads',flush=True)
(HERE/'native_validation.json').write_text(json.dumps({'kicad_version':pcbnew.GetBuildVersion(),'footprints':result,'total_pads':sum(x['pad_count'] for x in result)},indent=2)+'\n')
