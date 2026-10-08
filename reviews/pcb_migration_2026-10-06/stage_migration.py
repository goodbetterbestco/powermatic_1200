import hashlib, json, re, shutil, sys
from pathlib import Path
import xml.etree.ElementTree as ET
sys.path.insert(0, '/Users/evanthayer/Projects/_hardware/powermatic_1200/tools/wiring')
from source import children, key, nodes, one, parse, prop, replace

ROOT=Path('/Users/evanthayer/Projects/_hardware/powermatic_1200')
PARTS=Path('/Users/evanthayer/Projects/_parts/footprints/Controls.pretty')
W=Path('/private/tmp/powermatic-pcb-migration-20261006')
G=Path('/private/tmp/powermatic-gland-jumpers')
N='powermatic_1200'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
state=json.loads((W/'checkpoint.json').read_text())
for name,h in state['project_hashes'].items():
 assert digest(ROOT/'kicad'/N/name)==h, f'Project changed: {name}'
for name,h in state['library_hashes'].items():assert digest(PARTS/name)==h,name
original=(W/'before'/(N+'.kicad_pcb')).read_text()
source=(G/'after'/(N+'.kicad_pcb')).read_text()
assert (G/'before'/(N+'.kicad_pcb')).read_text()==original
assert (G/'before'/(N+'.kicad_sch')).read_bytes()==(W/'before'/(N+'.kicad_sch')).read_bytes()
sch=parse((W/'before'/(N+'.kicad_sch')).read_text())
symbols={prop(s,'Reference'):s for s in nodes(sch,'symbol') if one(s,'on_board')==['on_board','yes'] and not prop(s,'Reference').startswith('#')}
xml=ET.parse(W/'netlist.xml').getroot()
comps={c.get('ref'):c for c in xml.findall('./components/comp')}
pin_net={};pin_data={}
for n in xml.findall('./nets/net'):
 for p in n.findall('node'):
  k=(p.get('ref'),p.get('pin'));assert k not in pin_net
  pin_net[k]=n.get('name');pin_data[k]=p.attrib
rename={'OL1':'OL4','OL2':'OL6','SP3':'SP4','SP4':'SP5','SP5':'SP6'}
psmap={'TB1.1':'1_BOT','TB1.2':'2_BOT','TB1.3':'3_BOT','TB2.1':'1_TOP','TB2.2':'2_TOP','TB2.3':'3_TOP','TB2.4':'4_TOP'}
before=parse(original);aliases={};current_names=set(pin_net.values())
for f in nodes(before,'footprint'):
 ref=rename.get(prop(f,'Reference'),prop(f,'Reference'))
 if ref not in symbols:continue
 for pad in nodes(f,'pad'):
  number=psmap.get(pad[1],pad[1]) if ref=='PS1' else pad[1]
  old=one(pad,'net')
  if old and (ref,number) in pin_net:aliases.setdefault(old[2],set()).add(pin_net[ref,number])
aliases={old:next(iter(ns)) for old,ns in aliases.items() if old not in current_names and len(ns)==1}

# Stable codes for retained or renamed nets; allocate only genuinely new names.
codes={};code_names={};oldnets=nodes(before,'net')
for n in oldnets:
 if not n[2]:continue
 name=n[2] if n[2] in current_names else aliases.get(n[2])
 if name and name not in codes:codes[name]=n[1];code_names[n[1]]=name
next_code=max(int(n[1]) for n in oldnets)+1
def net_entry(name):
 global next_code
 if name not in codes:
  codes[name]=str(next_code);code_names[str(next_code)]=name;next_code+=1
 return f'(net {codes[name]} {json.dumps(name)})'

def board_only_net(old):
 if old in current_names:return old
 assert old in aliases, f'Unresolved PCB-only net: {old}'
 return aliases[old]

edits=[];pad_assignments={};ref_map={};field_updates=[]
for a,b,raw in children(source):
 if key(raw)!='footprint':continue
 f=parse(raw);oldref=prop(f,'Reference');ref=rename.get(oldref,oldref)
 se=symbols.get(ref);comp=comps.get(ref) if se else None
 ed=[];seen_fields=set();seen_pads=set()
 desired={p[1]:p[2] for p in nodes(se,'property') if p[1]!='Footprint'} if se else {}
 if se:
  assert f[1]==prop(se,'Footprint'),f'Footprint substitution would be needed: {ref}'
  desired.update(Sheetname=N,Sheetfile=N+'.kicad_sch')
  ref_map[oldref]=ref
 for x,y,child in children(raw):
  k=key(child);obj=parse(child)
  if k=='property':
   name=obj[1];seen_fields.add(name)
   if se and name in desired and obj[2]!=desired[name]:
    m=list(__import__('source').TOKEN.finditer(child));t=m[3]
    ed.append((x,y,child[:t.start()]+json.dumps(desired[name])+child[t.end():]))
    field_updates.append([ref,name])
   elif not se and name in ['Sheetname','Sheetfile']:ed.append((x,y,''))
  elif k=='path':
   ed.append((x,y,'(path '+json.dumps(comp.find('sheetpath').get('tstamps')+comp.findtext('tstamps'))+')' if se else ''))
  elif k=='attr' and not se:
   ed.append((x,y,'(attr board_only '+' '.join(v for v in obj[1:] if v!='board_only')+')'))
  elif k=='pad':
   number=psmap.get(obj[1],obj[1]) if ref=='PS1' else obj[1]
   seen_pads.add(number);pe=[]
   if number!=obj[1]:
    m=list(__import__('source').TOKEN.finditer(child));t=m[2]
    pe.append((t.start(),t.end(),json.dumps(number)))
   pd=pin_data.get((ref,number)) if se else None
   if se:
    assert pd is not None,f'Unmatched physical pad {ref}.{number}'
    name=pin_net[ref,number]
   else:
    oldnet=one(obj,'net')
    name=None if f[1]=='Controls:KN-T12GRY-25_Front' else board_only_net(oldnet[2]) if oldnet and oldnet[2] else None
   seen=set()
   for aa,bb,sub in children(child):
    kk=key(sub);seen.add(kk)
    if kk=='net':pe.append((aa,bb,net_entry(name) if name else ''))
    elif kk in ['pinfunction','pintype']:
     pe.append((aa,bb,f'({kk} {json.dumps(pd.get(kk,"passive"))})' if se else ''))
   insert=[]
   if name and 'net' not in seen:insert.append(net_entry(name))
   if se:
    for kk in ['pinfunction','pintype']:
     if kk not in seen:insert.append(f'({kk} {json.dumps(pd.get(kk,"passive"))})')
   if insert:pe.append((len(child)-1,len(child)-1,'\n\t\t\t'+'\n\t\t\t'.join(insert)+'\n\t\t'))
   ed.append((x,y,replace(child,pe)))
   pad_assignments[f'{ref}.{number}']=name
 if se:
  expected={p for r,p in pin_net if r==ref};assert seen_pads==expected,(ref,seen_pads,expected)
  if not one(f,'path'):ed.append((len(raw)-1,len(raw)-1,'\n(path '+json.dumps(comp.find('sheetpath').get('tstamps')+comp.findtext('tstamps'))+')\n'))
  for name,value in desired.items():
   if name in seen_fields:continue
   # Metadata stays hidden; retain all existing user field placement and styling.
   at=one(f,'at')[1:3]
   ed.append((len(raw)-1,len(raw)-1,f'\n(property {json.dumps(name)} {json.dumps(value)} (at {at[0]} {at[1]}) (layer "Dwgs.User") (hide yes) (effects (font (size 1 1) (thickness 0.15))))\n'))
 else:
  if not one(f,'attr'):ed.append((len(raw)-1,len(raw)-1,'\n(attr board_only)\n'))
  # Routing terminal groups are electrically common physical parts.
  if oldref and oldref.startswith('TB') and not one(f,'jumper_pad_groups'):
   groups='("TOP" "BOT")' if {p[1] for p in nodes(f,'pad')}=={'TOP','BOT'} else '("1" "2" "PE")'
   ed.append((len(raw)-1,len(raw)-1,'\n(duplicate_pad_numbers_are_jumpers no)\n(jumper_pad_groups '+groups+')\n'))
 edits.append((a,b,replace(raw,ed)))
assert len(ref_map)==len(symbols)==19
after=replace(source,edits)
net_ed=[];first=True
for a,b,raw in children(after):
 if key(raw)=='net':
  net_ed.append((a,b,'(net 0 "")\n\t'+'\n\t'.join(f'(net {c} {json.dumps(n)})' for c,n in sorted(code_names.items(),key=lambda x:int(x[0]))) if first else ''));first=False
after=replace(after,net_ed)
new=parse(after)

def placements(tree):
 return {one(f,'uuid')[1]:(one(f,'at'),one(f,'layer')) for f in nodes(tree,'footprint')}
assert placements(before)==placements(new),'A footprint was added, removed or moved'
for k in ['segment','via','zone','group','gr_line','gr_rect','gr_poly','gr_arc','gr_circle','gr_text','model']:
 assert nodes(before,k)==nodes(new,k),f'Changed board object: {k}'
# Mechanical footprint contents and every unaffected pad's geometry stay exact.
old_by={one(f,'uuid')[1]:f for f in nodes(before,'footprint')}
for f in nodes(new,'footprint'):
 old=old_by[one(f,'uuid')[1]]
 ignore={'pad','path','sheetname','sheetfile','property','attr','jumper_pad_groups','duplicate_pad_numbers_are_jumpers'}
 filt=lambda v:[x for x in v if not(isinstance(x,list) and x[0] in ignore)]
 assert filt(f)==filt(old),prop(f,'Reference')
 if prop(old,'Reference') not in ['J3','J4','J5']:
  pd=lambda p:[x for x in p[2:] if not(isinstance(x,list) and x[0] in ['net','pinfunction','pintype'])]
  assert [pd(p) for p in nodes(f,'pad')]==[pd(p) for p in nodes(old,'pad')],prop(f,'Reference')
(W/'after'/(N+'.kicad_pcb')).write_text(after)

# Shared assets: native gland groups, PSU terminal IDs, and PCB-only defaults.
for name in state['library_hashes']:
 raw=(W/'library-before'/name).read_text()
 if name.startswith(('BNSPDX','BSPDX','BSPBX')):result=(G/'Controls.pretty'/name).read_text()
 else:
  ed=[]
  for a,b,child in children(raw):
   k=key(child);obj=parse(child)
   if name=='NDR-240-24_Front.kicad_mod' and k=='pad':
    m=list(__import__('source').TOKEN.finditer(child));t=m[2]
    ed.append((a,b,child[:t.start()]+json.dumps(psmap[obj[1]])+child[t.end():]))
   elif name in ['HMX1-MI_Front.kicad_mod','KN-G12SP-10_Front.kicad_mod'] and k=='attr':
    ed.append((a,b,'(attr board_only '+' '.join(v for v in obj[1:] if v!='board_only')+')'))
  if name=='KN-G12SP-10_Front.kicad_mod':
   ed.append((len(raw)-1,len(raw)-1,'\n(duplicate_pad_numbers_are_jumpers no)\n(jumper_pad_groups ("1" "2" "PE"))\n'))
  ed.append(next((a,b,'(version 20260206)') for a,b,c in children(raw) if key(c)=='version'))
  result=replace(raw,ed)
 (W/'library-after'/name).write_text(result)
for p in PARTS.glob('*.kicad_mod'):
 target=(W/'library-after'/p.name) if (W/'library-after'/p.name).exists() else p
 link=W/'Controls.pretty'/p.name
 if link.is_symlink() or link.exists():link.unlink()
 link.symlink_to(target)
(W/'after'/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Controls") (type "KiCad") (uri '+json.dumps(str(W/'Controls.pretty'))+') (options "") (descr "Migration validation overlay")))\n')
state.update(reference_map=ref_map,net_aliases=aliases,pad_assignments=pad_assignments,footprints_retained=len(placements(new)),positions_angles_layers_unchanged=True,board_artwork_groups_unchanged=True,shared_library_changes=list(state['library_hashes']),board_after_sha256=digest(W/'after'/(N+'.kicad_pcb')))
(W/'staged.json').write_text(json.dumps(state,indent=2)+'\n')
print(f'Staged {len(placements(new))} retained footprints, 19 current symbol links, {len(aliases)} net renames and 6 shared footprint updates. Placement and geometry checks pass.')
