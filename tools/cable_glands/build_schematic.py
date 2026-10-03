#!/usr/bin/env python3
"""Stage catalog symbols and a labelled cable-entry interface, preserving wiring."""
from pathlib import Path
import sys,json,re,uuid,csv,io,hashlib,copy
from sexpr import parse,nodes,one,prop
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'controls_footprints/left_wall'))
from install import children,key,replace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];WORK=Path(sys.argv[1]);STAGE=WORK/'stage';CFG=json.loads((HERE/'config.json').read_text());PARTS=Path.home()/'Projects/_parts'
SCH=ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_sch'
q=json.dumps
uid=lambda:str(uuid.uuid4())
def effects(size=1.27,hide=False):return f'(effects (font (size {size} {size}))'+(' (hide yes)' if hide else '')+')'
def property_(name,value,x=0,y=0,hide=True):return f'(property {q(name)} {q(value)} (at {x} {y} 0) {effects(hide=hide)})'
def props(p):return {'Reference':'J','Value':p['part'],'Footprint':'Controls:'+p['part']+'_BottomWall','Datasheet':'${PARTS_LIB}/datasheets/'+p['part']+'_Drawing.pdf','Description':f"Bimed {p['thread']} cable gland, cable OD {p['range_mm'][0]}-{p['range_mm'][1]} mm. Logical cable-core interface, not separable contacts.",'Part Name':p['role']+'\nCable Gland','MPN':p['part'],'Manufacturer':'Bimed','Supplier':'AD','SupplierPartNumber':p['part'],'Category':'connector','Type':'Passive','Package':p['thread']+' bottom wall','Cable MPN':p['cable'],'Cable cores':str(p['cores']),'Cable OD mm':str(p['od_mm'])}
def library(p,templates):
 part=p['part'];fields=props(p)
 if 'template' in p:
  source=templates[p['template']]
  nested=[c.replace(p['template'],part) for _,_,c in children(source) if key(c)=='symbol']
  meta=[c for _,_,c in children(source) if key(c) in ['pin_names','pin_numbers']]
 else:
  meta=['(pin_names (offset 0.508))'];nested=[]
  graphics='(rectangle (start -12.7 10.16) (end 12.7 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))'
  pins=[]
  for i,n in enumerate(p['pins']):
   y=(p['cores']-1)*1.27-i*2.54;name=p['signals'][i] or 'SPARE'
   pins.append(f'(pin passive line (at -17.78 {y:.2f} 0) (length 5.08) (name {q(name)} {effects(.9)}) (number {q(n)} {effects(.9)}))')
  nested=[f'(symbol "{part}_0_1" {graphics})',f'(symbol "{part}_1_1" '+ '\n'.join(pins)+')']
 items=[f'(symbol {q(part)}','(exclude_from_sim no) (in_bom yes) (on_board yes)',*meta]
 for k,v in fields.items():
  if k=='Reference':items.append(property_(k,v,0,18,False))
  elif k=='Value':items.append(property_(k,v,0,15.5,False))
  elif k=='Part Name':items.append(property_(k,v,0,-18,False))
  else:items.append(property_(k,v))
 items+=nested;return '\n '.join(items)+'\n)'
def label(name,x,y):
 if name.startswith('M1_T') or name in ['+24V_CTRL','+24V_RUN']:return f'(global_label {q(name)} (shape input) (at {x} {y} 180) (effects (font (size .9 .9)) (justify right)) (uuid "{uid()}"))'
 return f'(label {q(name)} (at {x} {y} 0) {effects(.9)} (uuid "{uid()}"))'
def wire(a,b):return f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{uid()}"))'
def text(value,x,y,size=1.27):return f'(text {q(value)} (at {x} {y} 0) {effects(size)} (uuid "{uid()}"))'
original=SCH.read_text();r=parse(original);lib_node=next((a,b,c) for a,b,c in children(original) if key(c)=='lib_symbols');templates={parse(c)[1].split(':',1)[-1]:c for _,_,c in children(lib_node[2]) if key(c)=='symbol'}
assert not any(prop(n,'Reference') in ['J3','J4','J5'] for n in nodes(r,'symbol'))
libs=[library(p,templates) for p in CFG['parts']]
lib=PARTS/'symbols/Controls.kicad_sym';original_lib=lib.read_text();(WORK/'library_before.sha256').write_text(hashlib.sha256(original_lib.encode()).hexdigest());(WORK/'sch_before.sha256').write_text(hashlib.sha256(original.encode()).hexdigest());(WORK/'before.kicad_sch').write_text(original)
(STAGE/'symbols').mkdir(exist_ok=True);(STAGE/'symbols/Controls.kicad_sym').write_text(original_lib[:original_lib.rfind(')')]+ '\n'+ '\n'.join(libs)+'\n)\n')
cache=[s.replace('(symbol '+q(p['part']), '(symbol '+q('Controls:'+p['part']),1) for s,p in zip(libs,CFG['parts'])]
new_lib_node=lib_node[2][:-1]+'\n'+ '\n'.join(cache)+'\n)';updated=replace(original,[(lib_node[0],lib_node[1],new_lib_node)])
items=[];mapping=[]
# Aliases on existing, unchanged conductor endpoints. Seven wires cross the
# panel-to-pendant boundary; remaining S2/S3 connections stay pendant-internal.
aliases=[('FWD_CMD','S2','1','R1'),('REV_CMD','S2','2','R3'),('STOP_CHAIN','S2','3','L5'),('LOW_CMD','S3','1','1.U'),('HIGH_CMD','S3','1','2.U')]
for name,ref,unit,pin in aliases:
 inst=next(n for n in nodes(r,'symbol') if prop(n,'Reference')==ref and one(n,'unit')[1]==unit);libid=one(inst,'lib_id')[1];definition=parse(next(c for _,_,c in children(lib_node[2]) if key(c)=='symbol' and parse(c)[1]==libid))
 ps=[n for sub in nodes(definition,'symbol') if sub[1].endswith('_'+unit+'_1') for n in nodes(sub,'pin') if one(n,'number')[1]==pin];assert len(ps)==1,(name,libid,pin)
 at=one(inst,'at');pa=one(ps[0],'at');assert at[3]=='0' and not one(inst,'mirror')
 x=float(at[1])+float(pa[1]);y=float(at[2])-float(pa[2]);items.append(label(name,x,y))
for index,(p,libtext) in enumerate(zip(CFG['parts'],libs)):
 x=[205.74,303.53,415.29][index];y=180.34;part=p['part'];u=uid();fields=props(p);fields['Reference']=p['ref'];definition=parse(libtext)
 instance=[f'(symbol (lib_id "Controls:{part}") (at {x} {y} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{u}")']
 for k,v in fields.items():
  py=y-18 if k=='Reference' else y-15.5 if k=='Value' else y+18 if k=='Part Name' else y
  instance.append(property_(k,v,x,py,k not in ['Reference','Value','Part Name']))
 pins=[n for sub in nodes(definition,'symbol') for n in nodes(sub,'pin')]
 for pin in pins:instance.append(f'(pin {q(one(pin,"number")[1])} (uuid "{uid()}"))')
 instance.append(f'(instances (project "" (path "/{one(r,"uuid")[1]}" (reference "{p["ref"]}") (unit 1))))');items.append('\n'.join(instance)+')')
 for pin in pins:
  num=one(pin,'number')[1];i=p['pins'].index(num);sig=p['signals'][i];pa=one(pin,'at');px=x+float(pa[1]);py=y-float(pa[2]);lx=px-20.32
  if sig is None:items.append(f'(no_connect (at {px} {py}) (uuid "{uid()}"))')
  else:items.extend([wire([lx,py],[px,py]),label(sig,lx,py)])
  mapping.append({'reference':p['ref'],'pin':num,'signal':sig})
 caption=['Panel -- J3 -- J2 power plug','Panel -- J4 -- M1 motor','Panel -- J5 -- S2 / S3 pendant'][index]
 items.append(text(caption,x,y+27.94,1));items.append(text('Cable '+p['cable']+' / '+str(p['cores'])+' cores',x,y+32,1))
items.append(text('ENCLOSURE BOTTOM CABLE ENTRIES - logical conductor interfaces',307.34,151.13,1.8));items.append(text('J5 uses all seven cable cores. Core numbers are project assignments; glands have no electrical contacts.',307.34,220.98,1.1))
updated=updated[:updated.rfind(')')]+ '\n'+ '\n'.join(items)+'\n)\n';parse(updated);(WORK/'candidate.kicad_sch').write_text(updated);(HERE/'pin_map.json').write_text(json.dumps(mapping,indent=2)+'\n')
# Append authoritative catalog rows without rewriting prior CSV records.
cat=PARTS/'database/non_lcsc_parts.csv';content=cat.read_bytes();(WORK/'csv_before.sha256').write_text(hashlib.sha256(content).hexdigest());rows=list(csv.DictReader(io.StringIO(content.decode())));assert not set(p['part'] for p in CFG['parts']) & set(row['PartID'] for row in rows)
fields=list(rows[0]);buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n')
for p in CFG['parts']:
 vals=props(p);row={k:'' for k in fields};row.update({k:vals[k] for k in fields if k in vals});row.update(PartID=p['part'],Symbol='Controls:'+p['part'],Keywords='Bimed cable gland '+p['role']+' bottom enclosure',inventory='0');w.writerow(row)
(STAGE/'database').mkdir(exist_ok=True);(STAGE/'database/non_lcsc_parts.csv').write_bytes(content+buf.getvalue().encode());print('Staged 3 symbols, catalog rows and schematic interfaces')
