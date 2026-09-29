#!/usr/bin/env python3
"""Native KiCad validation/export, using temporary boards only."""
import json
import itertools
import math
from pathlib import Path
import subprocess
import pcbnew

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = Path.home()/'Projects/_parts/footprints/Controls.pretty'
PARTS = Path.home()/'Projects/_parts'
WORK = Path('/tmp/powermatic-left-wall')
WORK.mkdir(exist_ok=True)
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'


def point(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


records = []
for s in json.loads((HERE/'geometry.json').read_text()):
    fp = pcbnew.FootprintLoad(str(LIB), s['name'])
    prior = pcbnew.FootprintLoad(str(LIB), s['part']+'_Front')
    assert fp and prior
    ids = [p.GetNumber() for p in fp.Pads()]
    assert len(ids) == len(set(ids))
    assert sorted(ids) == sorted(p.GetNumber() for p in prior.Pads())
    for a, b in itertools.combinations(fp.Pads(), 2):
        aa, bb = a.GetPosition(), b.GetPosition()
        assert math.hypot(aa.x-bb.x, aa.y-bb.y) > pcbnew.FromMM(3.1)
    assert all(g.GetLayer() == pcbnew.Dwgs_User for g in fp.GraphicalItems())
    assert len(list(fp.Models())) == 1
    model = list(fp.Models())[0]
    assert [model.m_Scale.x, model.m_Scale.y, model.m_Scale.z] == [1, 1, 1]
    board = pcbnew.BOARD()
    board.Add(fp)
    fp.SetPosition(point(100, 100))
    fp.SetReference(s['ref'])
    box = fp.GetBoundingBox()
    lo, hi = box.GetPosition(), box.GetEnd()
    corners = [(lo.x/1e6-2,lo.y/1e6-2),(hi.x/1e6+2,lo.y/1e6-2),
               (hi.x/1e6+2,hi.y/1e6+2),(lo.x/1e6-2,hi.y/1e6+2)]
    for a, b in zip(corners, corners[1:]+corners[:1]):
        line = pcbnew.PCB_SHAPE()
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(point(*a)); line.SetEnd(point(*b))
        line.SetLayer(pcbnew.Edge_Cuts); line.SetWidth(pcbnew.FromMM(.05)); board.Add(line)
    bp = WORK/(s['name']+'.kicad_pcb')
    pcbnew.SaveBoard(str(bp), board)
    commands = [
        ['pcb','export','svg','--layers','Dwgs.User,F.Cu','--page-size-mode','2',
         '--exclude-drawing-sheet','--drill-shape-opt','2','--mode-single',
         '--output',str(WORK/(s['name']+'.svg')),str(bp)],
        ['pcb','export','step','--force','--user-origin','100x100mm',
         '--define-var',f'PARTS_LIB={PARTS}','--output',str(WORK/(s['name']+'.step')),str(bp)],
        ['pcb','render','--width','1000','--height','1000','--side','top','--zoom','0.65',
         '--light-top','0.25','--light-bottom','0.1','--light-side','0.25','--light-camera','0.15',
         '--define-var',f'PARTS_LIB={PARTS}','--output',str(WORK/(s['name']+'-3d.png')),str(bp)]
    ]
    for args in commands:
        r = subprocess.run([CLI]+args, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout+r.stderr
    records.append(dict(name=s['name'], terminal_ids=ids, native_load=True,
                        native_svg=True, native_step=True, native_render=True))
    print(s['name'], 'native validation passed', flush=True)
(HERE/'validation.json').write_text(json.dumps(records, indent=2)+'\n')
