#!/usr/bin/env python3
"""Check catalog parity and native symbol-to-footprint export without editing the project."""
from pathlib import Path
import csv,hashlib,json,re,sqlite3,subprocess,xml.etree.ElementTree as ET
H=Path(__file__).resolve().parent;R=H.parents[2];P=Path.home()/'Projects/_parts';W=Path('/tmp/powermatic-aligned-controls');W.mkdir(exist_ok=True)
CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
results={'databases':[],'parts':[]}
for stem in ['parts','non_lcsc_parts']:
 cp=P/'database'/(stem+'.csv');db=P/'database'/(stem+'.db')
 rows=list(csv.DictReader(cp.open()));con=sqlite3.connect(f'file:{db}?mode=ro',uri=True);con.row_factory=sqlite3.Row
 assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 actual=[dict(r) for r in con.execute('SELECT * FROM parts')]
 key='LCSC' if stem=='parts' else 'PartID'
 if key not in rows[0]:key=next(iter(rows[0]))
 assert len(rows)==len(actual)==len({r[key] for r in rows})
 aa={r[key]:r for r in actual}
 for r in rows:
  assert set(r)==set(aa[r[key]])
  assert all((v or '')==str(aa[r[key]][k] or '') for k,v in r.items()),r[key]
 results['databases'].append({'file':db.name,'rows':len(rows),'csv_matches':True,'integrity_check':'ok'})
 con.close()

def nodes(text):
 stack=[]
 for m in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',text):
  if m.group()=='(':stack.append(m.start())
  elif m.group()==')':yield stack.pop(),m.end()
text=(R/'kicad/powermatic_1200/powermatic_1200.kicad_sch').read_text()
config=json.loads((H/'geometry_review.json').read_text())
parts={s['part']:s for s in config}
# Include the earlier three completed parts in the final link consistency check.
parts.update({s['part']:s for s in json.loads((H.parent/'additions/geometry_review.json').read_text())})
libs={};instances={p:[] for p in parts}
for a,b in nodes(text):
 s=text[a:b]
 for p in parts:
  ids=['Controls:'+p,'non_lcsc_parts:Non-LCSC/'+p]
  if any(s.startswith('(symbol "'+i+'"') for i in ids):libs[p]=s
  elif any(re.match(r'\(symbol\s+\(lib_id "'+re.escape(i)+r'"\)',s) for i in ids):instances[p].append(s)
catalog={r['PartID']:r for r in csv.DictReader((P/'database/non_lcsc_parts.csv').open())}
library_text=(P/'symbols/Controls.kicad_sym').read_text()
library_blocks={}
for a,b in nodes(library_text):
 block=library_text[a:b]
 for p in parts:
  if block.startswith('(symbol "'+p+'"'): library_blocks[p]=block
for p in parts:
 assert catalog[p]['Footprint']=='Controls:'+p+'_Front' and catalog[p]['Package']
 assert '(property "Footprint" "Controls:'+p+'_Front"' in library_blocks[p]
 assert '(on_board yes)' in library_blocks[p]
 assert p in libs and instances[p]
 for s in [libs[p]]+instances[p]:
  assert '(property "Footprint" "Controls:'+p+'_Front"' in s
  assert '(on_board yes)' in s
 fp=P/'footprints/Controls.pretty'/(p+'_Front.kicad_mod')
 assert fp.read_bytes()==(R/'kicad/powermatic_1200/Controls_Review.pretty'/fp.name).read_bytes()
 assert hashlib.sha256(fp.read_bytes()).hexdigest()==parts[p]['footprint_sha256']
 model=P/'3dmodels/Controls'/parts[p]['model']
 assert hashlib.sha256(model.read_bytes()).hexdigest()==parts[p]['model_sha256']
 # One isolated component per type, with all placed units represented.
 result=[];seen=set();ref='TEST'+str(len(results['parts'])+1)
 for s in instances[p]:
  unit=re.search(r'\(unit (\d+)\)',s)[1]
  if unit in seen:continue
  seen.add(unit)
  s=re.sub(r'(\(property "Reference" )"[^"]*"',lambda m:m[1]+json.dumps(ref),s,count=1)
  s=re.sub(r'\(reference "[^"]*"\)','(reference "'+ref+'")',s)
  result.append(s)
 parts[p]['test_instances']=result
 results['parts'].append({'part':p,'reference':ref,'footprint':'Controls:'+p+'_Front','placed_units':len(instances[p]),'tested_units':sorted(seen),'catalog_review_copy_match':True,'manufacturer_model_unchanged':True})
uuid=re.search(r'\(uuid "([^"]+)"\)',text)[1]
schematic='(kicad_sch (version 20250114) (generator "eeschema") (uuid "'+uuid+'") (paper "A4") (lib_symbols '+'\n'.join(libs.values())+')\n'+'\n'.join(s for p in parts.values() for s in p['test_instances'])+')\n'
sp=W/'catalog-link-check.kicad_sch';sp.write_text(schematic);xp=W/'catalog-link-check.xml'
proc=subprocess.run([CLI,'sch','export','netlist','--format','kicadxml','--output',str(xp),str(sp)],capture_output=True,text=True)
assert proc.returncode==0,proc.stdout+proc.stderr
comps=ET.parse(xp).getroot().find('components').findall('comp');assert len(comps)==len(parts)
refs={r['reference']:r for r in results['parts']}
for c in comps:assert c.findtext('footprint')==refs[c.attrib['ref']]['footprint']
results['native_export_component_count']=len(comps)
(H/'catalog_validation.json').write_text(json.dumps(results,indent=2)+'\n')
print('CSV/SQLite parity and integrity passed:',results['databases'])
print('Native schematic export:',len(comps),'distinct types, all matching footprint links; all original model hashes preserved.')
