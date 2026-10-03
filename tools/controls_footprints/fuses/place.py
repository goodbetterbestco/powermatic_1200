#!/usr/bin/env python3
"""Place three board-only fuses at the requested 25 mm pitch, preserving PCB text.

Run using KiCad's bundled Python. Existing schematic/BOM own electrical topology
and purchase quantity; these pad-free PCB objects are assembly representations.
"""
from pathlib import Path
import sys, json, hashlib, math
import pcbnew
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'left_wall'))
from install import children,key,field
BOARD=HERE.parents[2]/'kicad/powermatic_1200/powermatic_1200.kicad_pcb'
PARTS=Path.home()/'Projects/_parts'
WORK=Path('/private/tmp/powermatic-frn-fuses');WORK.mkdir(exist_ok=True)
NAME='FRN-R-10_RM25030-3SR_Front'
source=BOARD.read_text();b=pcbnew.LoadBoard(str(BOARD))
assert not any(p.GetReference() in {'F1','F2','F3'} for p in b.GetFootprints()),'Fuse references already exist'
holder=next(p for p in b.GetFootprints() if p.GetReference()=='FH1')
assert holder.GetValue()=='RM25030-3SR'
a=math.radians(holder.GetOrientationDegrees());hx,hy=[pcbnew.ToMM(v) for v in [holder.GetPosition().x,holder.GetPosition().y]]
# Center between the paired inner cylindrical clip surfaces in the holder STEP.
center_x=.484112
review=pcbnew.BOARD();placements=[]
for i,dx in enumerate([-25.,0.,25.],1):
 localx=center_x+dx
 x=hx+localx*math.cos(a); y=hy-localx*math.sin(a)
 f=pcbnew.FootprintLoad(str(PARTS/'footprints/Controls.pretty'),NAME);assert f
 f.SetFPID(pcbnew.LIB_ID('Controls',NAME));f.SetReference('F'+str(i));f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
 f.SetOrientationDegrees(holder.GetOrientationDegrees());review.Add(f)
 placements.append({'reference':f.GetReference(),'position_mm':[pcbnew.ToMM(f.GetPosition().x),pcbnew.ToMM(f.GetPosition().y)],'rotation_deg':f.GetOrientationDegrees(),'pole_index':i,'clip_center_error_mm':abs(dx-[-24.5126065,0,24.512607][i-1])})
pcbnew.SaveBoard(str(WORK/'fuses-only.kicad_pcb'),review)
nodes=[n for _,_,n in children((WORK/'fuses-only.kicad_pcb').read_text()) if key(n)=='footprint'];assert len(nodes)==3
updated=source[:source.rfind(')')].rstrip()+'\n\t'+'\n\t'.join(nodes)+'\n)\n'
oldnodes=[n for _,_,n in children(source)];newnodes=[n for _,_,n in children(updated)]
assert newnodes[:-3]==oldnodes
(WORK/'before.kicad_pcb').write_text(source);(WORK/'candidate.kicad_pcb').write_text(updated)
parsed=pcbnew.LoadBoard(str(WORK/'candidate.kicad_pcb'))
assert len(list(parsed.GetFootprints()))==len(list(b.GetFootprints()))+3
assert BOARD.read_text()==source,'Concurrent PCB save'
BOARD.write_text(updated)
report={'holder_position_mm':[hx,hy],'pitch_mm':25,'requested_spacing_choice':'25 mm pitch selected by user','centerline_above_footprint_plane_mm':30.414015,'other_top_level_nodes_unchanged':True,'placements':placements,'before_sha256':hashlib.sha256(source.encode()).hexdigest(),'after_sha256':hashlib.sha256(updated.encode()).hexdigest()}
(HERE/'placement.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
