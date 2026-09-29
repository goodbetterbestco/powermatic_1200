#!/usr/bin/env python3
"""Install the BACO project view on SW1, preserving all unrelated records."""
from pathlib import Path
import hashlib, importlib.util, json, re, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]/'kicad/powermatic_1200'
spec=importlib.util.spec_from_file_location('left_wall_install',HERE.parent/'left_wall/install.py')
helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
children,key,field,replace=helpers.children,helpers.key,helpers.field,helpers.replace
NAME='Controls:222102_LeftWall'
BACKUP=Path('/tmp/baco-leftwall/before-install');BACKUP.mkdir(parents=True,exist_ok=True)

def target(text,kind):
    matches=[(a,b,n) for a,b,n in children(text) if key(n)==kind and field(n,'Reference')=='SW1']
    assert len(matches)==1
    return matches[0]

def props(node):
    result={}
    for _,_,n in children(node):
        if key(n)=='property':
            tokens=list(helpers.TOKEN.finditer(n))
            result[json.loads(tokens[2][0])]=tokens[3][0]
    return result

def geometry(node):
    return {key(n):n for _,_,n in children(node) if key(n) in ('at','uuid','path')}

def pads(node):
    return {re.match(r'\(pad "([^"]+)"',n)[1]:n for _,_,n in children(node) if key(n)=='pad'}

def main():
    assert json.loads((HERE/'validation.json').read_text())['render']
    assert json.loads((HERE/'alignment_validation.json').read_text())['model_solid_count']==80
    sch=PROJECT/'powermatic_1200.kicad_sch';pcb=PROJECT/'powermatic_1200.kicad_pcb'
    originals={sch:sch.read_text(),pcb:pcb.read_text()}
    a,b,symbol=target(originals[sch],'symbol');assert field(symbol,'Value')=='222102'
    new_symbol,count=re.subn(r'(\(property "Footprint" ")[^"]*(")',lambda m:m[1]+NAME+m[2],symbol)
    assert count==1
    outputs={sch:replace(originals[sch],[(a,b,new_symbol)])}
    a,b,old=target(originals[pcb],'footprint')
    assert field(old,'Value') in ('22013003','222102')
    fresh=helpers.footprint(old,{'name':'222102_LeftWall'})
    schematic_props=props(new_symbol);edits=[]
    for x,y,n in children(fresh):
        if key(n)!='property':continue
        tokens=list(helpers.TOKEN.finditer(n));name=json.loads(tokens[2][0])
        if name in schematic_props:
            start,end=tokens[3].span()
            edits.append((x,y,n[:start]+schematic_props[name]+n[end:]))
    fresh=replace(fresh,edits)
    assert geometry(fresh)==geometry(old)
    # Only pad positions change. Numbers, UUIDs, nets, functions and sizes stay.
    before,after=pads(old),pads(fresh);assert before.keys()==after.keys()
    for number in before:
        strip=lambda n:re.sub(r'\(at [^)]*\)','',n,count=1)
        assert strip(before[number])==strip(after[number])
    outputs[pcb]=replace(originals[pcb],[(a,b,fresh)])
    result=[]
    for path,updated in outputs.items():
        old=originals[path];kind='symbol' if path==sch else 'footprint'
        pairs=list(zip(children(old),children(updated)))
        assert len(pairs)==len(list(children(old)))==len(list(children(updated)))
        for (_,_,before),(_,_,after) in pairs:
            if key(before)==kind and field(before,'Reference')=='SW1':continue
            assert before==after
        backup=BACKUP/path.name
        if not backup.exists():backup.write_text(old)
        assert path.read_text()==old, 'Concurrent file save detected'
        path.write_text(updated)
        result.append({'file':path.name,'reference':'SW1','footprint':NAME,
                       'before_sha256':hashlib.sha256(old.encode()).hexdigest(),
                       'after_sha256':hashlib.sha256(updated.encode()).hexdigest(),
                       'unrelated_top_level_records_unchanged':True})
    (HERE/'installation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Installed SW1 schematic association and PCB footprint; other objects unchanged.')

if __name__=='__main__':main()
