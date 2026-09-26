#!/usr/bin/env python3
"""Run with KiCad's bundled Python; validate pads and export review artifacts."""
import itertools
import json
import math
import re
import subprocess
from pathlib import Path
import pcbnew

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = ROOT/'kicad/powermatic_1200/Controls_Review.pretty'
PARTS = Path.home()/'Projects/_parts'
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
WORK = Path('/tmp/powermatic-three-controls')
WORK.mkdir(exist_ok=True)


def sexpr(text):
    stack = []
    for t in re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', text):
        if t == '(':
            stack.append([])
        elif t == ')':
            x = stack.pop()
            if stack:
                stack[-1].append(x)
            else:
                return x
        else:
            stack[-1].append(json.loads(t) if t.startswith('"') else t)


def children(x, key):
    return [v for v in x if isinstance(v, list) and v and v[0] == key]


def point(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


root = sexpr((PARTS/'symbols/Controls.kicad_sym').read_text())
pins = {sym[1]: [children(p, 'number')[0][1] for unit in children(sym, 'symbol')
                 for p in children(unit, 'pin')] for sym in children(root, 'symbol')}
result = []
for spec in json.loads((HERE/'geometry_review.json').read_text()):
    fp = pcbnew.FootprintLoad(str(LIB), spec['name'])
    assert fp
    pads = list(fp.Pads())
    ids = [p.GetNumber() for p in pads]
    assert len(ids) == len(set(ids))
    assert sorted(ids) == sorted(pins[spec['part']])
    for p in pads:
        assert p.GetDrillSize().x == pcbnew.FromMM(2)
        assert p.GetSize().x == pcbnew.FromMM(3)
        assert p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH
    for a, b in itertools.combinations(pads, 2):
        aa, bb = a.GetPosition(), b.GetPosition()
        assert math.hypot(aa.x-bb.x, aa.y-bb.y) > pcbnew.FromMM(3.1)
    for g in fp.GraphicalItems():
        assert g.GetLayer() == pcbnew.Dwgs_User
    assert len(list(fp.Models())) == 1
    model = list(fp.Models())[0]
    assert Path(str(model.m_Filename).replace('${PARTS_LIB}', str(PARTS))).is_file()
    assert [model.m_Scale.x, model.m_Scale.y, model.m_Scale.z] == [1, 1, 1]
    board = pcbnew.BOARD()
    board.Add(fp)
    fp.SetPosition(point(100, 100))
    fp.SetReference('TEST1')
    # A temporary review substrate only, not an enclosure or drill template.
    box = fp.GetBoundingBox()
    lo, hi = box.GetPosition(), box.GetEnd()
    xy = [(lo.x/1e6-2,lo.y/1e6-2),(hi.x/1e6+2,lo.y/1e6-2),
          (hi.x/1e6+2,hi.y/1e6+2),(lo.x/1e6-2,hi.y/1e6+2)]
    for a, b in zip(xy, xy[1:]+xy[:1]):
        s = pcbnew.PCB_SHAPE()
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(point(*a)); s.SetEnd(point(*b))
        s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(pcbnew.FromMM(.05)); board.Add(s)
    bp = WORK/(spec['name']+'.kicad_pcb')
    pcbnew.SaveBoard(str(bp), board)
    subprocess.run([CLI,'pcb','export','svg','--layers','Dwgs.User,F.Cu',
                    '--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','2',
                    '--mode-single','--output',str(HERE/'previews'/(spec['name']+'.svg')),str(bp)],
                   check=True, stdout=subprocess.DEVNULL)
    step = WORK/(spec['name']+'.step')
    log = subprocess.run([CLI,'pcb','export','step','--force',
                          '--user-origin','100x100mm','--define-var',f'PARTS_LIB={PARTS}',
                          '--output',str(step),str(bp)],capture_output=True,text=True)
    assert log.returncode == 0, log.stdout+log.stderr
    assert step.is_file()
    (WORK/(spec['name']+'-export.log')).write_text(log.stdout+log.stderr)
    subprocess.run([CLI,'pcb','render','--width','1000','--height','1000','--side','top',
                    '--output',str(HERE/'previews'/(spec['name']+'-3d.png')),str(bp)],
                   check=True, stdout=subprocess.DEVNULL)
    result.append({'name':spec['name'],'pins':ids,'symbol_pad_match':True,
                   'native_svg':True,'native_step_export':True,'model_scale':[1,1,1]})
    print(spec['name'], 'native load, pin map, SVG and STEP passed', flush=True)
(HERE/'native_validation.json').write_text(json.dumps({'kicad':pcbnew.GetBuildVersion(),
                                                      'parts':result},indent=2)+'\n')
