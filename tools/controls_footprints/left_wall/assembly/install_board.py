#!/usr/bin/env python3
"""Install SW1 assembly graphics/model only; preserve every field, pad and net."""
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from install import children,key,field,replace

PROJECT=HERE.parents[3]/'kicad/powermatic_1200'
board=PROJECT/'powermatic_1200.kicad_pcb'
lib=PROJECT/'Controls_Review.pretty/22013003_LeftWall.kicad_mod'
old=board.read_text(); fresh=lib.read_text()
physical={'fp_line','fp_arc','fp_circle','fp_rect','fp_poly','fp_curve','model'}
geometry=[n for _,_,n in children(fresh) if key(n) in physical]
targets=[(a,b,n) for a,b,n in children(old) if key(n)=='footprint' and field(n,'Reference')=='SW1']
assert len(targets)==1
a,b,node=targets[0]
assert node.startswith('(footprint "Controls_Review:22013003_LeftWall"')
edits=[(s,e,'') for s,e,n in children(node) if key(n) in physical]
updated=replace(node,edits).rstrip()[:-1].rstrip()+'\n\t\t'+'\n\t\t'.join(geometry)+'\n\t)'
assert [n for _,_,n in children(node) if key(n) not in physical]==[n for _,_,n in children(updated) if key(n) not in physical]
new=replace(old,[(a,b,updated)])
for (_,_,prior),(_,_,after) in zip(children(old),children(new)):
    if prior!=node: assert prior==after
backup=Path('/tmp/powermatic-disconnect-assembly/before.kicad_pcb')
if not backup.exists(): backup.write_text(old)
assert board.read_text()==old,'Concurrent PCB save; rerun'
board.write_text(new)
report={'reference':'SW1','changed':'footprint graphics and single assembly model',
        'other_top_level_nodes_unchanged':True,'all_fields_pads_nets_placement_unchanged':True,
        'before_sha256':hashlib.sha256(old.encode()).hexdigest(),
        'after_sha256':hashlib.sha256(new.encode()).hexdigest()}
(HERE/'installation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
