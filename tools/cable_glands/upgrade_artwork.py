#!/usr/bin/env python3
"""Match the hand-finished power gland's artwork style on the compact glands.

Retains CAD F.Fab, pads, models and all board connectivity/placement. The filled
F.Adhes silhouette is display artwork matching the user's power gland, not an
adhesive application instruction. Run after build_assets.py to retain this finish.
"""
import argparse, hashlib, json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'controls_footprints/left_wall'))
from install import children, key, replace, field
from sexpr import parse, one, nodes

SPECS = {
    'BSPDX-23-W': dict(thread=13.335, nut=16.002, lip=17.5006, washer=18.542,
                     body=16.4973, neck=14.2621, cap_start=15.6464,
                     cap_round_start=28.8544, cap_seam=31.5722, seam_width=15.875, end=37.32518068202),
    'BSPBX-22-W': dict(thread=10.668, nut=12.9921, lip=14.2875, washer=14.478,
                     body=11.938, neck=10.2235, cap_start=14.605,
                     cap_round_start=24.4348, cap_seam=26.3779, seam_width=11.7729, end=32.4866),
}
def fmt(v): return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v)>1e-7 else '0'
def point(p): return ' '.join(map(fmt,p))
def rdp(points, tolerance=.06):
    if len(points)<3:return points
    a,b=points[0],points[-1];dx,dy=b[0]-a[0],b[1]-a[1]
    distances=[abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/math.hypot(dx,dy) for p in points[1:-1]]
    d=max(distances);i=distances.index(d)+1
    return rdp(points[:i+1],tolerance)[:-1]+rdp(points[i:],tolerance) if d>tolerance else [a,b]
def silhouette(f,s):
    segments=[(list(map(float,one(n,'start')[1:])),list(map(float,one(n,'end')[1:])))
              for n in nodes(f,'fp_line') if one(n,'layer')[1]=='F.Fab']
    def width(y):
        xs=[]
        for a,b in segments:
            if min(a[1],b[1])-1e-6<=y<=max(a[1],b[1])+1e-6:
                if abs(b[1]-a[1])<1e-8:xs.extend([a[0],b[0]])
                else:xs.append(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
        assert xs, y
        return max(xs)
    # Ignore thread helices for the clean envelope; retain washer, nut lip,
    # body/neck steps, and the CAD-derived rounded cap profile.
    right=[(s['thread'],-12.9794),(s['thread'],-8.4836),
           (s['nut'],-8.4836),(s['nut'],-3.4036),(s['lip'],-3.4036),
           (s['lip'],-1.8796),(s['thread'],-1.8796),(s['thread'],0),
           (s['washer'],0),(s['washer'],2.0066),(s['body'],2.0066),
           (s['body'],8.3566),(s['neck'],8.3566),(s['neck'],s['cap_start']),
           (s['body'],s['cap_start'])]
    start=s['cap_round_start']
    ys=[start+(s['end']-start)*i/32 for i in range(33)]
    right+=rdp([(width(y),y) for y in ys])
    return [(-x,y) for x,y in right]+list(reversed(right))
def drawings(f,s):
    pts=silhouette(f,s);out=[]
    for layer,fill in [('F.SilkS','none'),('F.Adhes','solid')]:
        out.append('(fp_poly (pts '+' '.join('(xy '+point(p)+')' for p in pts)+
                   f') (stroke (width 0.25) (type solid)) (fill {fill}) (layer "{layer}"))')
    for y,w,stroke in [(0,s['washer'],.15),(-8.4836,s['nut'],.1),
                       (-3.4036,s['lip'],.1),(2.0066,s['body'],.1),
                       (8.3566,s['body'],.1),(s['cap_start'],s['body'],.1),
                       (s['cap_seam'],s['seam_width'],.1)]:
        spans=[(-w,w)]
        for pad in nodes(f,'pad'):
            px,py=map(float,one(pad,'at')[1:3]);radius=float(one(pad,'size')[1])/2+.15+stroke/2
            if abs(y-py)>=radius:continue
            dx=math.sqrt(radius**2-(y-py)**2);left,right=px-dx,px+dx
            spans=[segment for a,b in spans for segment in [(a,min(b,left)),(max(a,right),b)] if segment[1]-segment[0]>.02]
        for a,b in spans:
            out.append(f'(fp_line (start {point((a,y))}) (end {point((b,y))}) (stroke (width {stroke}) (type default)) (layer "F.SilkS"))')
    return out,pts

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--library-dir',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--board',type=Path)
    args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True);report=[];art={}
    for name,s in SPECS.items():
        p=args.library_dir/(name+'_BottomWall.kicad_mod');text=p.read_text();f=parse(text);art[name],pts=drawings(f,s)
        edits=[]
        for a,b,n in children(text):
            parsed=parse(n)
            if key(n).startswith('fp_') and one(parsed,'layer')[1] in ['F.SilkS','F.Adhes']:edits.append((a,b,''))
            elif key(n)=='property' and parsed[1]=='Reference':edits.append((a,b,re.sub(r'\(at [^)]*\)','(at 0 -17.145 0)',n,count=1)))
        result=replace(text,edits);result=re.sub(r'\n[ \t]*\n','\n',result)
        result=result.rstrip()[:-1].rstrip()+'\n '+'\n '.join(art[name])+'\n)\n'
        result=re.sub(r'(?m)^[ \t]+$', '', result)
        # Assert every non-artwork physical record survives exactly.
        for a,b,n in children(text):
            if key(n) in ['pad','model'] or (key(n).startswith('fp_') and one(parse(n),'layer')[1]=='F.Fab'):assert n in result
        (args.output_dir/p.name).write_text(result)
        report.append(dict(part=name,polygon_vertices=len(pts),bounds_mm=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)],input_sha256=hashlib.sha256(text.encode()).hexdigest(),output_sha256=hashlib.sha256(result.encode()).hexdigest(),pads_models_fab_preserved=True))
    if args.board:
        text=args.board.read_text();edits=[];seen=[]
        for a,b,n in children(text):
            if key(n)!='footprint':continue
            part=field(n,'Value')
            if part not in SPECS:continue
            nn=[];offset=list(map(float,one(parse(n),'at')[1:3]))
            for aa,bb,c in children(n):
                if key(c).startswith('fp_') and one(parse(c),'layer')[1] in ['F.SilkS','F.Adhes']:nn.append((aa,bb,''))
                elif key(c)=='property' and field(n,'Reference') in ['J4','J5'] and parse(c)[1]=='Reference':
                    nn.append((aa,bb,re.sub(r'\(at [^)]*\)','(at 0 -17.145 0)',c,count=1)))
            updated=replace(n,nn);updated=re.sub(r'\n[ \t]*\n','\n',updated)
            updated=updated.rstrip()[:-1].rstrip()+'\n '+'\n '.join(art[part])+'\n)'
            updated=re.sub(r'(?m)^[ \t]+$', '', updated)
            for _,_,c in children(n):
                if key(c) in ['pad','model','at','path','uuid']:assert c in updated
            edits.append((a,b,updated));seen.append(field(n,'Reference'))
        assert sorted(seen)==['J4','J5'],seen
        out=replace(text,edits);(args.output_dir/args.board.name).write_text(out)
        report.append(dict(board_input_sha256=hashlib.sha256(text.encode()).hexdigest(),board_output_sha256=hashlib.sha256(out.encode()).hexdigest(),modified_references=seen,pads_models_placements_and_connectivity_preserved=True))
    (args.output_dir/'artwork_review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
