#!/usr/bin/env python3
"""Apply the reviewed project artwork recipes, using KiCad's bundled Python.

Default: prepare candidates and validate source preservation. --install applies
only those candidates after checking every live source hash. --verify checks the
installed candidates. The approved fuse-holder pilot and background rail remain
untouched. Original imported artwork is retained on F.Fab verbatim apart from
its layer. Artwork coordinates never change pads, nets, placements or models.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
import uuid
from collections import Counter
from pathlib import Path

import pcbnew

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = Path.home()/'Projects/_parts/footprints/Controls.pretty'
BOARD = ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_pcb'
WORK = Path('/private/tmp/powermatic-artwork-rollout')
CANDIDATES = WORK/'Controls.pretty'
REPORT = HERE/'project_validation.json'
RECIPES = json.loads((HERE/'project_traces.json').read_text())
spec = importlib.util.spec_from_file_location('sexpr', HERE.parent/'left_wall/install.py')
sx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sx)
GRAPHICS = {'fp_line','fp_arc','fp_curve','fp_circle','fp_rect','fp_poly'}
NAMESPACE = uuid.UUID('804d7e49-c74d-437f-a9b3-eac5543aeb99')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def xy(p):
    return ' '.join(f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>.0000005 else '0' for v in p)


def signature(text, layer='Dwgs.User'):
    """Compare original physical drawings despite save formatting/UUID changes."""
    rows = []
    for _,_,n in sx.children(text):
        if sx.key(n) in GRAPHICS and f'(layer "{layer}")' in n:
            coords = tuple((k,round(float(x),5),round(float(y),5)) for k,x,y in
                           re.findall(r'\((at|start|end|mid|center|xy)\s+([-+\d.eE]+)\s+([-+\d.eE]+)\)',n))
            rows.append((sx.key(n),coords))
    return sorted(rows)


def alignment(board_text, library_text):
    """Find an existing rigid drawing translation; allow native arc reversal."""
    def rows(text):
        out=[]
        for _,_,n in sx.children(text):
            if sx.key(n) not in GRAPHICS or '(layer "Dwgs.User")' not in n:continue
            pts=[tuple(map(float,p)) for p in re.findall(r'\((?:start|end|mid|center|xy)\s+([-+\d.eE]+)\s+([-+\d.eE]+)\)',n)]
            out.append((sx.key(n),pts))
        return out
    a,b=rows(board_text),rows(library_text)
    assert len(a)==len(b)
    offset=tuple(min(p[i] for _,ps in a for p in ps)-min(p[i] for _,ps in b for p in ps) for i in [0,1])
    buckets={}
    for kind,ps in b:
        center=[sum(p[i] for p in ps)/len(ps) for i in [0,1]]
        key=(kind,len(ps),math.floor(center[0]*10),math.floor(center[1]*10))
        buckets.setdefault(key,[]).append(ps)
    error=0
    for kind,ps in a:
        pts=[(p[0]-offset[0],p[1]-offset[1]) for p in ps]
        cx,cy=[math.floor(sum(p[i] for p in pts)/len(pts)*10) for i in [0,1]]
        matches=[]
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                key=(kind,len(pts),cx+dx,cy+dy)
                for j,qs in enumerate(buckets.get(key,[])):
                    err=min(max(abs(x-y) for p,q in zip(pts,order) for x,y in zip(p,q)) for order in [qs,list(reversed(qs))])
                    if err<.00005:matches.append((err,key,j))
        assert matches, (kind,pts,offset)
        err,key,j=min(matches);buckets[key].pop(j);error=max(error,err)
    assert not any(buckets.values())
    return offset,error


def additions(name, instance, offset=(0,0)):
    s = RECIPES[name];nodes = []
    for i,(kind,points) in enumerate(s['shapes']):
        points=[(p[0]+offset[0],p[1]+offset[1]) for p in points]
        keys = {'line':['start','end'],'arc':['start','mid','end'],'circle':['center','end']}[kind]
        coords = ' '.join(f'({k} {xy(p)})' for k,p in zip(keys,points))
        ident = uuid.uuid5(NAMESPACE,f'{instance}:outline:{i}')
        nodes.append(f'(fp_{kind} {coords} (stroke (width 0.25) (type solid))'
                     + (' (fill none)' if kind=='circle' else '')
                     +f' (layer "F.SilkS") (uuid "{ident}"))')
    for i,points in enumerate(s['fills']):
        points=[(p[0]+offset[0],p[1]+offset[1]) for p in points]
        ident = uuid.uuid5(NAMESPACE,f'{instance}:fill:{i}')
        nodes.append('(fp_poly (pts '+' '.join(f'(xy {xy(p)})' for p in points)+') '
                     +f'(stroke (width 0) (type solid)) (fill solid) (layer "F.Adhes") (uuid "{ident}"))')
    return nodes


def transform(original, name, instance, offset=(0,0)):
    edits = [];extra = [];moved = 0
    for a,b,node in sx.children(original):
        key = sx.key(node)
        if key in GRAPHICS and '(layer "Dwgs.User")' in node:
            edits.append((a,b,node.replace('(layer "Dwgs.User")','(layer "F.Fab")')));moved += 1
            if name=='222102_LeftWall' and '(type dash)' in node:
                # The original datum remains in the archived drawing; a copy
                # stays on the background drawing layer for enclosure layout.
                ident=uuid.uuid5(NAMESPACE,f'{instance}:wall:{len(extra)}')
                datum=re.sub(r'\(uuid "[^"]*"\)',f'(uuid "{ident}")',node)
                if '(uuid ' not in datum:datum=datum[:-1]+f' (uuid "{ident}"))'
                extra.append(datum)
        elif key=='property' and '(layer "Dwgs.User")' in node:
            layer='F.SilkS' if node.startswith('(property "Reference"') else 'F.Fab'
            edits.append((a,b,node.replace('(layer "Dwgs.User")',f'(layer "{layer}")')))
        elif key=='fp_text' and '(layer "Dwgs.User")' in node:
            edits.append((a,b,node.replace('(layer "Dwgs.User")','(layer "F.Fab")')))
    assert moved==RECIPES[name]['source_graphics'], (name,moved)
    out=sx.replace(original,edits).rstrip()[:-1].rstrip()+'\n  '+'\n  '.join(additions(name,instance,offset)+extra)+'\n)'
    old=[n for _,_,n in sx.children(original)];new=[n for _,_,n in sx.children(out)]
    assert len(new)==len(old)+len(additions(name,instance,offset))+len(extra)
    for before,after in zip(old,new):
        key=sx.key(before)
        if key in GRAPHICS:
            assert before.replace('(layer "Dwgs.User")','(layer "F.Fab")')==after
        elif key not in {'property','fp_text'}:assert before==after, key
        else:
            assert before.replace('(layer "Dwgs.User")','(layer "F.SilkS")' if before.startswith('(property "Reference"') else '(layer "F.Fab")')==after
    assert signature(original)==signature(out,'F.Fab')
    return out


def check_native(path, name):
    f=pcbnew.FootprintLoad(str(path.parent),path.stem)
    assert f
    counts=Counter(g.GetLayerName() for g in f.GraphicalItems() if isinstance(g,pcbnew.PCB_SHAPE))
    s=RECIPES[name]
    assert counts['F.Fab']==s['source_graphics']
    assert counts['F.Silkscreen']==len(s['shapes'])
    assert counts['F.Adhesive']==len(s['fills'])
    assert f.Reference().GetLayer()==pcbnew.F_SilkS
    for g in f.GraphicalItems():
        if isinstance(g,pcbnew.PCB_SHAPE) and g.GetLayer()==pcbnew.F_Adhes:
            assert g.IsFilled() and g.GetWidth()==0
            assert g.GetPolyShape().OutlineCount()==1
    return dict(layers=dict(counts),pads=len(list(f.Pads())))


def prepare():
    WORK.mkdir(exist_ok=True);CANDIDATES.mkdir(exist_ok=True)
    backup=WORK/'before';backup.mkdir(exist_ok=True)
    jobs=[];parts={};oldlib={}
    def job(path,data,new):
        dest=CANDIDATES/path.name if path.suffix=='.kicad_mod' else WORK/'candidate.kicad_pcb'
        bak=backup/path.name
        if bak.exists():assert bak.read_bytes()==data, 'Do not overwrite changed backup'
        else:bak.write_bytes(data)
        dest.write_text(new)
        jobs.append(dict(source=str(path),candidate=str(dest),backup=str(bak),before_sha256=sha(data),after_sha256=sha(dest.read_bytes())))
    for name,s in RECIPES.items():
        path=LIB/(name+'.kicad_mod');data=path.read_bytes()
        assert sha(data)==s['source_sha256'], (name,'source has changed')
        oldlib[name]=data.decode()
        job(path,data,transform(data.decode(),name,'library:'+name)+'\n')
        parts[name]=check_native(CANDIDATES/path.name,name)
        parts[name]['references']=[]
        parts[name]['outline_reduction_percent']=round(100*(1-len(s['shapes'])/s['source_graphics']),1)
    data=BOARD.read_bytes();text=data.decode();edits=[]
    for a,b,node in sx.children(text):
        if sx.key(node)!='footprint':continue
        name=re.match(r'\(footprint "Controls:([^"]+)"',node)
        if not name or name[1] not in RECIPES:continue
        name=name[1];ref=sx.field(node,'Reference')
        offset,error=alignment(node,oldlib[name])
        parts[name].setdefault('instance_artwork_offsets_mm',{})[ref]=list(offset)
        parts[name].setdefault('max_source_match_error_mm',0)
        parts[name]['max_source_match_error_mm']=max(parts[name]['max_source_match_error_mm'],error)
        parts[name]['references'].append(ref)
        edits.append((a,b,transform(node,name,ref,offset)))
    assert sum(len(p['references']) for p in parts.values())==55
    out=sx.replace(text,edits)
    old=[n for _,_,n in sx.children(text)];new=[n for _,_,n in sx.children(out)]
    assert len(old)==len(new)
    assert sum(a!=b for a,b in zip(old,new))==55
    job(BOARD,data,out)
    board=pcbnew.LoadBoard(str(WORK/'candidate.kicad_pcb'));assert board
    for name,record in parts.items():
        for ref in record['references']:
            f=board.FindFootprintByReference(ref);assert f
            assert str(f.GetFPID().GetLibItemName())==name
            assert f.Reference().GetLayer()==pcbnew.F_SilkS
    report=dict(installed=False,updated_footprint_types=len(parts),updated_board_instances=55,
                source_graphics_to_fab=sum(s['source_graphics'] for s in RECIPES.values()),
                line_width_mm=.25,outline_layer='F.SilkS',fill_layer='F.Adhes',source_layer='F.Fab',
                source_graphics_exact_except_layer=True,pads_nets_models_placement_exact=True,
                other_board_records_exact=True,existing_fuse_pilot_and_rails_exact=True,
                native_library_and_board_load=True,parts=parts,files=jobs)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['parts','files']},indent=2))
    # Standalone native review sheet; the real project's placements are intact.
    demo=pcbnew.BOARD()
    for i,name in enumerate(RECIPES):
        f=pcbnew.FootprintLoad(str(CANDIDATES),name)
        f.SetReference(parts[name]['references'][0]);x=70+(i%4)*120;y=85+(i//4)*155
        f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)));demo.Add(f)
        for dy in [-17.5,-12.5,12.5,17.5]:
            g=pcbnew.PCB_SHAPE(demo);g.SetShape(pcbnew.SHAPE_T_SEGMENT)
            g.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x-50),pcbnew.FromMM(y+dy)))
            g.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x+65),pcbnew.FromMM(y+dy)))
            g.SetWidth(pcbnew.FromMM(.2));g.SetLayer(pcbnew.Dwgs_User);demo.Add(g)
    pcbnew.SaveBoard(str(WORK/'project-artwork-review.kicad_pcb'),demo)


def install():
    report=json.loads(REPORT.read_text())
    for job in report['files']:
        assert sha(Path(job['source']).read_bytes())==job['before_sha256'], 'Concurrent source change'
        assert sha(Path(job['candidate']).read_bytes())==job['after_sha256'], 'Candidate changed'
    for job in report['files']:
        Path(job['source']).write_bytes(Path(job['candidate']).read_bytes())
    report['installed']=True
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    verify()


def verify():
    r=json.loads(REPORT.read_text());assert r['installed']
    for job in r['files']:
        assert sha(Path(job['source']).read_bytes())==job['after_sha256']
    for name in RECIPES:check_native(LIB/(name+'.kicad_mod'),name)
    assert pcbnew.LoadBoard(str(BOARD))
    print('Verified installed 12 shared footprints and 55 placed instances; all candidate hashes match.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--verify',action='store_true');a=p.parse_args()
    if a.install:install()
    elif a.verify:verify()
    else:prepare()
