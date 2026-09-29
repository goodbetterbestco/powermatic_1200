#!/usr/bin/env python3
"""Native KiCad load, label placement and review exports; no working PCB save."""
from pathlib import Path
import json,subprocess,sys,math
sys.dont_write_bytecode=True
import pcbnew
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]/'kicad/powermatic_1200'
WORK=Path('/tmp/baco-leftwall');WORK.mkdir(exist_ok=True)
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
sys.path.insert(0,str(HERE.parent));from label_references import placement,edit_footprint
name='222102_LeftWall';path=Path.home()/'Projects/_parts/footprints/Controls.pretty'/f'{name}.kicad_mod'
fp=pcbnew.FootprintLoad(str(path.parent),name);assert fp
fp.SetReference('SW1');label=placement(fp);path.write_text(edit_footprint(path.read_text(),label))
fp=pcbnew.FootprintLoad(str(path.parent),name);assert fp
assert sorted(p.GetNumber() for p in fp.Pads())==['1','2','3','4','5','6']
assert all(g.GetLayer()==pcbnew.Dwgs_User for g in fp.GraphicalItems())
assert not fp.Value().IsVisible() and fp.Reference().IsVisible()
assert fp.Reference().GetTextSize().x==2500000 and fp.Reference().GetTextSize().y==2500000
for p in fp.Pads():assert p.GetSize().x==3000000 and p.GetDrillSize().x==2000000
assert len(list(fp.Models()))==1
fp.Models()[0].m_Filename=str(Path.home()/'Projects/_parts/3dmodels/Controls/222102_LeftWall_1p8796mm.step')
b=pcbnew.BOARD();b.Add(fp)
def point(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
fp.SetPosition(point(100,100));fp.SetReference('SW1')
# Fixed review frame centered around the complete side envelope.
a=(-38,-44);z=(62,44)
ps=[a,(z[0],a[1]),z,(a[0],z[1])]
for a,z in zip(ps,ps[1:]+ps[:1]):
 l=pcbnew.PCB_SHAPE();l.SetShape(pcbnew.SHAPE_T_SEGMENT);l.SetStart(point(100+a[0],100+a[1]));l.SetEnd(point(100+z[0],100+z[1]));l.SetLayer(pcbnew.Edge_Cuts);l.SetWidth(pcbnew.FromMM(.05));b.Add(l)
p=WORK/'review.kicad_pcb';pcbnew.SaveBoard(str(p),b)
commands=[
 ['pcb','export','svg','--layers','Dwgs.User,F.Cu','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','2','--mode-single','--output',str(WORK/'review.svg'),str(p)],
 # KiCad 9 requires a board body in this assembly export; geometry validation
 # removes the one known review-board solid before comparing model bounds.
 ['pcb','export','step','--force','--user-origin','100x100mm','--output',str(WORK/'native.step'),str(p)],
 ['pcb','render','--width','1500','--height','1300','--side','top','--zoom','0.7','--light-top','0.35','--light-bottom','0.1','--light-side','0.35','--light-camera','0.3','--output',str(WORK/'review-3d.png'),str(p)],
 ['pcb','render','--width','1500','--height','1300','--side','top','--rotate=330,0,340','--zoom','0.65','--light-top','0.35','--light-bottom','0.1','--light-side','0.35','--light-camera','0.3','--output',str(WORK/'review-3d-angled.png'),str(p)]
]
for i,args in enumerate(commands):
 r=subprocess.run([CLI]+args,capture_output=True,text=True);(WORK/f'native-{i}.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stdout+r.stderr;print('Passed',' '.join(args[:3]),flush=True)
report=dict(native_load=True,svg_export=True,step_export=True,render=True,terminal_ids=['1','2','3','4','5','6'],label=label)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
