#!/usr/bin/env python3
"""Prepare the RM25030-3SR layout-artwork pilot; run with KiCad Python.

F.Fab retains the complete imported drawing. F.SilkS carries 0.25 mm visible
feature outlines; F.Adhes carries an opaque body silhouette with open mounting
slots. Select F.SilkS and hide F.Fab for the enclosure-layout view.

This is deliberately limited to one library part and its FH1 board instance.
It preserves every other board record, and all pads, nets, models and placement.
Candidates and pre-edit backups go to /private/tmp; --install applies the
already-reviewed candidates only if both sources still match their backups.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
import uuid

import pcbnew

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORK = Path('/private/tmp/powermatic-fuse-silkscreen')
LIB = Path.home() / 'Projects/_parts/footprints/Controls.pretty'
NAME = 'RM25030-3SR_Front'
BOARD = ROOT / 'kicad/powermatic_1200/powermatic_1200.kicad_pcb'
spec = importlib.util.spec_from_file_location('sexpr', HERE.parent/'left_wall/install.py')
sexpr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sexpr)
GEOMETRY = {'fp_line', 'fp_arc', 'fp_curve', 'fp_circle', 'fp_poly', 'fp_rect'}
NAMESPACE = uuid.UUID('7c0b791a-6345-4f36-870e-524180f0b70f')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def xy(point):
    return ' '.join(f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v) > 0.0000005 else '0' for v in point)


def artwork():
    """Trace major contours at source coordinates; discard molding detail."""
    shapes = []
    def line(a, b):
        shapes.append(('line', [a, b]))
    def arc(a, m, b):
        shapes.append(('arc', [a, m, b]))
    def chain(points, closed=False):
        for a, b in zip(points, points[1:] + ([points[0]] if closed else [])):
            line(a, b)
    def rect(x0, y0, x1, y1):
        chain([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], True)
    def circle(x, y, radius):
        shapes.append(('circle', [(x,y),(x+radius,y)]))
    def capsule(cx, cy, half_straight, radius):
        line((cx-half_straight,cy-radius),(cx+half_straight,cy-radius))
        arc((cx+half_straight,cy-radius),(cx+half_straight+radius,cy),(cx+half_straight,cy+radius))
        line((cx+half_straight,cy+radius),(cx-half_straight,cy+radius))
        arc((cx-half_straight,cy+radius),(cx-half_straight-radius,cy),(cx-half_straight,cy-radius))

    # Envelope follows the imported drawing, including end clips. Small draft
    # taper and edge fillets are reduced to single contours, never scaled.
    outer = [(-35.790895,-40.200001),(36.759120,-40.200001),
             (37.123,-39.836),(37.123,-29.2),(37.245415,-29.145757),
             (37.245415,-23.854243),(37.123,-23.8),(37.123,-4.434431),
             (36.752,-3.669149),(36.752,3.669149),(37.123,4.434431),
             (37.123,23.8),(37.245415,23.854243),(37.245415,29.145759),
             (37.123,29.2),(37.123,39.836),(36.759120,40.200001),
             (-35.790895,40.200001),(-36.155,39.836),(-36.155,29.35),
             (-37.245415,29.35),(-37.245415,23.65),(-36.155,24.75),
             (-36.155,3.669149),(-37.183,3.669149),(-37.183,-3.669149),
             (-36.155,-3.669149),(-36.155,-24.75),(-37.245415,-23.65),
             (-37.245415,-29.35),(-36.155,-29.35),(-36.155,-39.836)]
    chain(outer, True)
    # Three poles remain distinct without all the parallel wall/rib edges.
    for x in (-11.7071245,12.6753495):
        line((x,-40.200001),(x,40.200001))

    holes = []
    for dx in (-24.382474,0,24.382474):
        cx = 0.484112 + dx
        # Raised mounting boss and actual keyhole-like mounting opening.
        capsule(cx, 0, 4.1, 5.212)
        hole = [
            ('line',[(-3.365888,-2.447837),(-1.158397,-2.447837)]),
            ('arc',[(-1.158397,-2.447837),(0.484112,-2.947837),(2.126622,-2.447837)]),
            ('line',[(2.126622,-2.447837),(4.334112,-2.447837)]),
            ('arc',[(4.334112,-2.447837),(6.781951,0),(4.334112,2.447838)]),
            ('line',[(4.334112,2.447838),(2.126622,2.447838)]),
            ('arc',[(2.126622,2.447838),(0.484112,2.947838),(-1.158397,2.447838)]),
            ('line',[(-1.158397,2.447838),(-3.365888,2.447838)]),
            ('arc',[(-3.365888,2.447838),(-5.813724,0),(-3.365888,-2.447837)]),
        ]
        shifted = [(kind,[(x+dx,y) for x,y in pts]) for kind,pts in hole]
        shapes.extend(shifted)
        holes.append(sample_path(shifted))
        for sign in (-1,1):
            def p(x, y):
                return (cx+x, sign*y)
            # End terminal plate and plain screw head; screwdriver slot omitted.
            screw_x = cx + (-0.09 if sign < 0 else 0.09)
            rect(screw_x-5.3955,sign*28.077,screw_x+5.3955,sign*38.687)
            circle(screw_x,sign*33.03,3.105)
            # Clip crossbar, two spring sides and the central fuse-contact area.
            # The outline is clipped at overlaps, so rear edges do not show
            # through the foreground contact area.
            chain([p(-5.3955,28.077),p(-10.2563,28.077),p(-10.2563,26.4262),
                   p(-5.35,26.4262),p(-5.35,25.56),p(-6.6,25.56),
                   p(-6.6,21.3863),p(-10.2563,21.3863),p(-10.2563,12.5),
                   p(10.2563,12.5),p(10.2563,21.3863),p(6.6,21.3863),
                   p(6.6,25.56),p(5.35,25.56),p(5.35,26.4262),
                   p(10.2563,26.4262),p(10.2563,28.077),p(5.3955,28.077)])
            line(p(-5.35,25.56),p(-5.35,12.5))
            line(p(5.35,25.56),p(5.35,12.5))

    # Fracture bridges allow holes in native KiCad fp_poly, with no stroke
    # along the bridges. These openings remain genuinely transparent.
    poly = pcbnew.SHAPE_POLY_SET()
    poly.NewOutline()
    for x,y in outer:
        poly.Append(round(x*1e6),round(y*1e6))
    for points in holes:
        h = poly.NewHole()
        for x,y in reversed(points):
            poly.Append(round(x*1e6),round(y*1e6),0,h)
    poly.Fracture()
    assert poly.OutlineCount() == 1
    contour = poly.COutline(0)
    fill = [(contour.CPoint(i).x/1e6,contour.CPoint(i).y/1e6) for i in range(contour.PointCount())]
    return shapes, fill


def sample_path(shapes):
    out = []
    for kind,points in shapes:
        if kind == 'line':
            out.append(points[0]); continue
        (x1,y1),(x2,y2),(x3,y3) = points
        z = 2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))
        cx = ((x1*x1+y1*y1)*(y2-y3)+(x2*x2+y2*y2)*(y3-y1)+(x3*x3+y3*y3)*(y1-y2))/z
        cy = ((x1*x1+y1*y1)*(x3-x2)+(x2*x2+y2*y2)*(x1-x3)+(x3*x3+y3*y3)*(x2-x1))/z
        r = math.hypot(x1-cx,y1-cy)
        a,b,c = [math.atan2(y-cy,x-cx) for x,y in points]
        span = (c-a)%(2*math.pi)
        if (b-a)%(2*math.pi) > span:
            span -= 2*math.pi
        count = max(4,math.ceil(abs(span)/0.07))
        out.extend((cx+r*math.cos(a+span*i/count),cy+r*math.sin(a+span*i/count)) for i in range(count))
    return out


def additions(shapes, fill, instance):
    nodes = []
    for i,(kind,points) in enumerate(shapes):
        keys = {'line':['start','end'],'arc':['start','mid','end'],'circle':['center','end']}[kind]
        coords = ' '.join(f'({key} {xy(p)})' for key,p in zip(keys,points))
        ident = uuid.uuid5(NAMESPACE,f'{instance}:outline:{i}')
        nodes.append(f'(fp_{kind} {coords} (stroke (width 0.25) (type solid))'
                     + (' (fill none)' if kind == 'circle' else '')
                     + f' (layer "F.SilkS") (uuid "{ident}"))')
    ident = uuid.uuid5(NAMESPACE,f'{instance}:body-fill')
    nodes.append('(fp_poly (pts '+' '.join(f'(xy {xy(p)})' for p in fill)+') '
                 +f'(stroke (width 0) (type solid)) (fill solid) (layer "F.Adhes") (uuid "{ident}"))')
    return nodes


def transform(original, shapes, fill, instance):
    edits = []
    moved = 0
    for a,b,node in sexpr.children(original):
        key = sexpr.key(node)
        if key in GEOMETRY and '(layer "Dwgs.User")' in node:
            edits.append((a,b,node.replace('(layer "Dwgs.User")','(layer "F.Fab")')))
            moved += 1
        elif key == 'property' and node.startswith('(property "Reference"'):
            new = node.replace('(layer "Dwgs.User")','(layer "F.SilkS")')
            new = re.sub(r'\(at [^)]*\)', '(at 0 -20.1125 0)', new, count=1)
            edits.append((a,b,new))
        elif key == 'property' and '(layer "Dwgs.User")' in node:
            edits.append((a,b,node.replace('(layer "Dwgs.User")','(layer "F.Fab")')))
    assert moved == 20376, moved
    new = sexpr.replace(original,edits)
    new = new.rstrip()[:-1].rstrip()+'\n  '+'\n  '.join(additions(shapes,fill,instance))+'\n)\n'
    old_nodes = [n for _,_,n in sexpr.children(original)]
    new_nodes = [n for _,_,n in sexpr.children(new)]
    for old,after in zip(old_nodes,new_nodes):
        key = sexpr.key(old)
        if key in GEOMETRY:
            assert old.replace('(layer "Dwgs.User")','(layer "F.Fab")') == after
        elif key != 'property':
            assert old == after, key
    # Exact preservation of connection/placement/identity/model records.
    for key in ['pad','model','at','uuid','path','attr']:
        assert [n for n in old_nodes if sexpr.key(n)==key] == [n for n in new_nodes if sexpr.key(n)==key]
    return new


def prepare():
    WORK.mkdir(exist_ok=True)
    candidates = WORK/'Controls.pretty'
    candidates.mkdir(exist_ok=True)
    shapes,fill = artwork()
    jobs = []
    for source, candidate, kind in [(LIB/(NAME+'.kicad_mod'),candidates/(NAME+'.kicad_mod'),'library'),
                                    (BOARD,WORK/'candidate.kicad_pcb','board')]:
        original = source.read_bytes()
        backup = WORK/('before-'+source.name)
        if backup.exists():
            assert backup.read_bytes() == original, 'Source changed; do not replace the original backup'
        else:
            backup.write_bytes(original)
        text = original.decode()
        if kind == 'library':
            new = transform(text,shapes,fill,'library')
        else:
            matches = [(a,b,n) for a,b,n in sexpr.children(text) if sexpr.key(n)=='footprint' and sexpr.field(n,'Reference')=='FH1']
            assert len(matches)==1
            a,b,old = matches[0]
            assert old.startswith('(footprint "Controls:'+NAME+'"')
            new = text[:a]+transform(old,shapes,fill,'FH1').rstrip()+text[b:]
            before_nodes = [n for _,_,n in sexpr.children(text)]
            after_nodes = [n for _,_,n in sexpr.children(new)]
            assert len(before_nodes)==len(after_nodes)
            assert sum(a!=b for a,b in zip(before_nodes,after_nodes))==1
        candidate.write_text(new)
        jobs.append(dict(source=str(source),candidate=str(candidate),backup=str(backup),
                         before_sha256=sha(original),after_sha256=sha(candidate.read_bytes())))
    f = pcbnew.FootprintLoad(str(candidates),NAME)
    assert f and len(list(f.Pads()))==6
    b = pcbnew.LoadBoard(str(WORK/'candidate.kicad_pcb'))
    assert b and b.FindFootprintByReference('FH1')
    report = dict(part=NAME,reference='FH1',source_graphics_moved_to_fab=20376,
                  simplified_silk_primitives=len(shapes),body_fill_polygons=1,
                  open_mounting_slots=3,native_load=True,
                  other_board_records_preserved=True,pads_nets_models_placement_preserved=True,
                  fill_layer='F.Adhes',outline_layer='F.SilkS',outline_width_mm=.25,
                  display='F.SilkS active; F.Adhes visible; F.Fab hidden; filled shapes opacity 1.0',
                  installed=False,files=jobs)
    (WORK/'prepared.json').write_text(json.dumps(report,indent=2)+'\n')
    # Compact standalone native board proves DIN rail occlusion, without moving
    # the user's placed FH1 or any existing rail on the actual project board.
    demo = pcbnew.BOARD()
    f.SetReference('FH1')
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100),pcbnew.FromMM(100)))
    demo.Add(f)
    rail_names = [p.stem for p in LIB.glob('*') if '35' in p.stem and ('rail' in p.stem.lower() or 'din' in p.stem.lower())]
    report['available_rail_footprints'] = rail_names
    # Review rail: correct 35 mm width, extended outside the body for comparison.
    for y in (-17.5,-12.5,12.5,17.5):
        g = pcbnew.PCB_SHAPE(demo)
        g.SetShape(pcbnew.SHAPE_T_SEGMENT)
        g.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(45),pcbnew.FromMM(100+y)))
        g.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(155),pcbnew.FromMM(100+y)))
        g.SetLayer(pcbnew.Dwgs_User);g.SetWidth(pcbnew.FromMM(.4));demo.Add(g)
    pcbnew.SaveBoard(str(WORK/'fuse-holder-review.kicad_pcb'),demo)
    (WORK/'prepared.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))


def install():
    report = json.loads((WORK/'prepared.json').read_text())
    for job in report['files']:
        assert sha(Path(job['source']).read_bytes()) == job['before_sha256'], 'Concurrent source change'
        assert sha(Path(job['candidate']).read_bytes()) == job['after_sha256'], 'Candidate changed'
    for job in report['files']:
        Path(job['source']).write_bytes(Path(job['candidate']).read_bytes())
        assert sha(Path(job['source']).read_bytes()) == job['after_sha256']
    report['installed'] = True
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Installed only the fuse-holder library footprint and FH1 artwork.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--install',action='store_true')
    args = p.parse_args()
    install() if args.install else prepare()
