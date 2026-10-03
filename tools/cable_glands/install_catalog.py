#!/usr/bin/env python3
"""Install staged gland assets, append-only catalog and symbols; rebuild databases."""
from pathlib import Path
from collections import Counter
import sys,hashlib,shutil,csv,sqlite3,subprocess
work=Path(sys.argv[1]);stage=work/'stage';root=Path.home()/'Projects/_parts'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root/'database/non_lcsc_parts.csv')==(work/'csv_before.sha256').read_text()
assert sha(root/'symbols/Controls.kicad_sym')==(work/'library_before.sha256').read_text()
assert (stage/'reviews/Controls/CableGlands/geometry.json').exists(),'CAD generation incomplete'
for folder in ['3dmodels/Controls','footprints/Controls.pretty','datasheets','reviews/Controls/CableGlands']:
 for p in (stage/folder).iterdir():
  target=root/folder/p.name;assert not target.exists(),target;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ['database/non_lcsc_parts.csv','symbols/Controls.kicad_sym']:
 shutil.copy2(root/name,work/(Path(name).name+'.before'));shutil.copy2(stage/name,root/name)
subprocess.run(['python3','database/rebuild_db.py'],cwd=root,check=True)
for stem,key in [('parts','LCSC'),('non_lcsc_parts','PartID')]:
 with (root/f'database/{stem}.csv').open(newline='') as f:r=csv.DictReader(f);cols=r.fieldnames;rows=list(r)
 with sqlite3.connect(f'file:{root}/database/{stem}.db?mode=ro',uri=True) as db:
  assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
  assert Counter(tuple(r[c] for c in cols) for r in rows)==Counter(db.execute('select * from parts').fetchall())
 assert all(r[key] for r in rows) and len({r[key] for r in rows})==len(rows);print(stem,len(rows),'CSV/database parity, unique keys and integrity passed')
