#!/usr/bin/env python3
"""Native load and review exports, without resaving the working PCB/library."""
import json
from pathlib import Path
import subprocess
import pcbnew

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[3]/'kicad/powermatic_1200'
WORK=Path('/tmp/powermatic-disconnect-assembly')
WORK.mkdir(exist_ok=True)
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
name='22013003_LeftWall'
fp=pcbnew.FootprintLoad(str(PROJECT/'Controls_Review.pretty'),name)
assert fp
assert sorted(p.GetNumber() for p in fp.Pads())==['1','2','3','4','5','6']
assert all(g.GetLayer()==pcbnew.Dwgs_User for g in fp.GraphicalItems())
assert len(list(fp.Models()))==1
models=fp.Models()
models[0].m_Filename=str(PROJECT/'3dmodels/22013003_LeftWall_Assembly.step')
assert fp.Models()[0].m_Filename==str(PROJECT/'3dmodels/22013003_LeftWall_Assembly.step')
board=pcbnew.BOARD(); board.Add(fp)
def point(x,y): return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
fp.SetPosition(point(150,150)); fp.SetReference('SW1')
bb=fp.GetBoundingBox(); lo,hi=bb.GetPosition(),bb.GetEnd()
corners=[(lo.x/1e6-2,lo.y/1e6-2),(hi.x/1e6+2,lo.y/1e6-2),
         (hi.x/1e6+2,hi.y/1e6+2),(lo.x/1e6-2,hi.y/1e6+2)]
for a,b in zip(corners,corners[1:]+corners[:1]):
    line=pcbnew.PCB_SHAPE(); line.SetShape(pcbnew.SHAPE_T_SEGMENT)
    line.SetStart(point(*a));line.SetEnd(point(*b));line.SetLayer(pcbnew.Edge_Cuts)
    line.SetWidth(pcbnew.FromMM(.05));board.Add(line)
bp=WORK/'review.kicad_pcb';pcbnew.SaveBoard(str(bp),board)
commands=[
 ['pcb','export','svg','--layers','Dwgs.User,F.Cu','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','2','--mode-single','--output',str(WORK/'review.svg'),str(bp)],
 ['pcb','export','step','--force','--user-origin','150x150mm','--output',str(WORK/'review.step'),str(bp)],
 ['pcb','render','--width','1200','--height','1400','--side','top','--zoom','0.75','--light-top','0.25','--light-bottom','0.1','--light-side','0.25','--light-camera','0.15','--output',str(WORK/'review-3d.png'),str(bp)],
]
for i,args in enumerate(commands):
    r=subprocess.run([CLI]+args,capture_output=True,text=True)
    (WORK/f'export-{i}.log').write_text(r.stdout+r.stderr)
    assert r.returncode==0,r.stdout+r.stderr
    print(args[1:3], 'passed',flush=True)
report={'native_load':True,'svg_export':True,'step_export':True,'render':True,
        'pads':[{'number':p.GetNumber(),'x':p.GetPosition().x/1e6-150,'y':p.GetPosition().y/1e6-150} for p in fp.Pads()],
        'model_count':len(list(fp.Models())),'drawing_layer':'Dwgs.User'}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
