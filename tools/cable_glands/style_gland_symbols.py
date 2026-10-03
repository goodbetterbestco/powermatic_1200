#!/usr/bin/env python3
"""Stage J4/J5 schematic artwork matching the user's compact J3 connector.

Uses 50 mil (1.27 mm) coordinates, 100 mil core pitch, zero-length pins,
external names and close fields. Keeps net labels, pin identities and UUIDs.
"""
from pathlib import Path
import argparse,sys,json,re,hashlib
from sexpr import parse,one,nodes,prop
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'controls_footprints/left_wall'))
from install import children,key,field,replace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];GRID=1.27
SPECS={'BSPDX-23-W':dict(ref='J4',count=6,x=303.53,y=179.07),
       'BSPBX-22-W':dict(ref='J5',count=7,x=350.52,y=179.07)}
def fmt(x):return f'{x:.6f}'.rstrip('0').rstrip('.') if abs(x)>1e-7 else '0'
def at(x,y,angle=0):return f'(at {fmt(x)} {fmt(y)} {angle})'
def effects():return '(effects (font (size 1.27 1.27)))'
def positions(s):return [round((s['count']-1)*1.27-i*2.54,6) for i in range(s['count'])]
def fields(n,s,instance=False):
    out=[];h=s['count']*1.27
    x=s['x'] if instance else 0;y=s['y'] if instance else 0
    offsets={'Reference':h+3.81,'Value':h+1.27,'Part Name':-h-3.81}
    for a,b,c in children(n):
        if key(c)!='property':continue
        name=parse(c)[1];dy=offsets.get(name,0)
        py=y-dy if instance else dy
        inner=[(aa,bb,at(x,py)) for aa,bb,cc in children(c) if key(cc)=='at']
        out.append((a,b,replace(c,inner)))
    return out

def definition(n,s):
    d=parse(n);pins=[p for sub in nodes(d,'symbol') for p in nodes(sub,'pin')];assert len(pins)==s['count']
    h=s['count']*1.27;part=d[1].split(':')[-1]
    graphics=[f'(rectangle (start -1.27 {fmt(h)}) (end 1.27 {fmt(-h)}) (stroke (width 0) (type default)) (fill (type background)))']
    ys=positions(s)
    for a,b in zip(ys,ys[1:]):
        y=(a+b)/2;graphics.append(f'(polyline (pts (xy -1.27 {fmt(y)}) (xy 1.27 {fmt(y)})) (stroke (width 0) (type default)) (fill (type none)))')
    edited_pins=[]
    for old,y in zip(pins,ys):
        num=one(old,'number')[1];name=one(old,'name')[1]
        edited_pins.append(f'(pin passive line {at(0,y)} (length 0) (name {json.dumps(name)} {effects()}) (number {json.dumps(num)} {effects()}))')
    ed=fields(n,s)
    for a,b,c in children(n):
        if key(c) in ['symbol','pin_names','pin_numbers']:ed.append((a,b,''))
    result=replace(n,ed).rstrip()[:-1].rstrip()
    result+='\n (pin_numbers (hide yes))\n (pin_names (offset 2.54))\n'
    result+=f'(symbol "{part}_0_1" '+'\n '.join(graphics)+')\n'
    result+=f'(symbol "{part}_1_1" '+'\n '.join(edited_pins)+')\n)'
    result=re.sub(r'(?m)^[ \t]+$','',result)
    assert [(one(p,'number')[1],one(p,'name')[1]) for p in pins]==[(one(p,'number')[1],one(p,'name')[1]) for sub in nodes(parse(result),'symbol') for p in nodes(sub,'pin')]
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    sch=ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_sch';library=Path.home()/'Projects/_parts/symbols/Controls.kicad_sym'
    original=sch.read_text();r=parse(original);cache=one(r,'lib_symbols');definitions={d[1]:d for d in nodes(cache,'symbol')}
    pin_moves=[];instances={prop(n,'Reference'):n for n in nodes(r,'symbol')}
    for part,s in SPECS.items():
        inst=instances[s['ref']];ix,iy,rot=map(float,one(inst,'at')[1:]);assert rot==0 and not one(inst,'mirror')
        pins=[p for sub in nodes(definitions['Controls:'+part],'symbol') for p in nodes(sub,'pin')]
        for pin,y in zip(pins,positions(s)):
            old=(round(ix+float(one(pin,'at')[1]),6),round(iy-float(one(pin,'at')[2]),6))
            ws=[w for w in nodes(r,'wire') if old in [tuple(map(float,p[1:])) for p in one(w,'pts')[1:]]];assert len(ws)==1,(s['ref'],old,len(ws))
            wire=ws[0];ends=[tuple(map(float,p[1:])) for p in one(wire,'pts')[1:]];labelat=next(p for p in ends if p!=old)
            labels=[l for k in ['global_label','label'] for l in nodes(r,k) if tuple(map(float,one(l,'at')[1:3]))==labelat];assert len(labels)==1
            pin_moves.append(dict(ref=s['ref'],pin=one(pin,'number')[1],wire_uuid=one(wire,'uuid')[1],label_uuid=one(labels[0],'uuid')[1],net_label=labels[0][1],pin_at=[s['x'],round(s['y']-y,6)],label_at=[round(s['x']-3.81,6),round(s['y']-y,6)]))
    bywire={p['wire_uuid']:p for p in pin_moves};bylabel={p['label_uuid']:p for p in pin_moves};ed=[]
    for a,b,n in children(original):
        k=key(n);d=parse(n)
        if k=='lib_symbols':
            ee=[]
            for aa,bb,c in children(n):
                if key(c)=='symbol' and parse(c)[1] in definitions:
                    part=parse(c)[1].split(':')[-1]
                    if part in SPECS:ee.append((aa,bb,definition(c,SPECS[part])))
            ed.append((a,b,replace(n,ee)))
        elif k=='symbol' and field(n,'Reference') in ['J4','J5']:
            s=SPECS[prop(d,'Value')];ee=fields(n,s,True)
            ee += [(aa,bb,at(s['x'],s['y'])) for aa,bb,c in children(n) if key(c)=='at'];ed.append((a,b,replace(n,ee)))
        elif k=='wire' and one(d,'uuid')[1] in bywire:
            p=bywire[one(d,'uuid')[1]];new='(pts '+' '.join(f'(xy {fmt(x)} {fmt(y)})' for x,y in [p['label_at'],p['pin_at']])+')'
            ed.append((a,b,replace(n,[(aa,bb,new) for aa,bb,c in children(n) if key(c)=='pts'])))
        elif k in ['global_label','label'] and one(d,'uuid')[1] in bylabel:
            p=bylabel[one(d,'uuid')[1]];ee=[]
            for aa,bb,c in children(n):
                if key(c)=='at':ee.append((aa,bb,at(*p['label_at'],180 if k=='global_label' else 0)))
                elif key(c)=='property':
                    inn=[(aaa,bbb,at(*p['label_at'])) for aaa,bbb,cc in children(c) if key(cc)=='at'];ee.append((aa,bb,replace(c,inn)))
            ed.append((a,b,replace(n,ee)))
    result=replace(original,ed);(args.output/sch.name).write_text(result);(args.output/'before.kicad_sch').write_text(original)
    oldlib=library.read_text();le=[]
    for a,b,n in children(oldlib):
        if key(n)=='symbol' and parse(n)[1] in SPECS:le.append((a,b,definition(n,SPECS[parse(n)[1]])))
    assert len(le)==2;newlib=replace(oldlib,le);(args.output/library.name).write_text(newlib);(args.output/'Controls.before.kicad_sym').write_text(oldlib)
    # Every coordinate edited for J4/J5 is an integer multiple of 50 mil.
    for p in pin_moves:
        assert all(abs(v/GRID-round(v/GRID))<1e-7 for v in p['pin_at']+p['label_at'])
    final=parse(result)
    for ref in ['J3','J2','M1']:assert instances[ref]==next(n for n in nodes(final,'symbol') if prop(n,'Reference')==ref)
    report=dict(grid_mm=GRID,pin_length_mm=0,pin_pitch_mm=2.54,body_width_mm=2.54,pin_names_offset_mm=2.54,updated_references=['J4','J5'],j3_j2_m1_instances_preserved=True,pin_moves=pin_moves,schematic_before_sha256=hashlib.sha256(original.encode()).hexdigest(),schematic_after_sha256=hashlib.sha256(result.encode()).hexdigest(),library_before_sha256=hashlib.sha256(oldlib.encode()).hexdigest(),library_after_sha256=hashlib.sha256(newlib.encode()).hexdigest())
    (args.output/'symbol_artwork_review.json').write_text(json.dumps(report,indent=2)+'\n');print('Staged compact 50 mil-grid J4/J5 symbols and 13 preserved conductor connections.')
if __name__=='__main__':main()
