#!/usr/bin/env python3
"""Verify the installed STEP registration and assembly settings with KiCad Python."""
import hashlib,json,re,sys
from pathlib import Path
import pcbnew
ROOT=Path(__file__).resolve().parents[3]
PARTS=Path.home()/'Projects/_parts'
HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/'settings.json').read_text())
b=pcbnew.LoadBoard(str(ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_pcb'))
byref={f.GetReference():f for f in b.GetFootprints()}
checks=[]
for f in b.GetFootprints():
 name=str(f.GetFPID().GetLibItemName());models=list(f.Models());assert len(models)==1
 m=models[0];file=Path(m.m_Filename.replace('${PARTS_LIB}',str(PARTS)));assert file.is_file(),file
 values=dict(file=file.name,offset=[m.m_Offset.x,m.m_Offset.y,m.m_Offset.z],rotate=[m.m_Rotation.x,m.m_Rotation.y,m.m_Rotation.z],scale=[m.m_Scale.x,m.m_Scale.y,m.m_Scale.z])
 assert values['scale']==[1,1,1]
 if name in CONFIG['board_models']:
  target=CONFIG['board_models'][name];assert values['file']==target['file']
  for k in ['offset','rotate']:assert max(abs(x-y) for x,y in zip(values[k],target[k]))<1e-6,(f.GetReference(),k)
 checks.append(dict(ref=f.GetReference(),footprint=name,model=values,model_sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
for r in CONFIG['assemblies']:
 p,c=byref[r['parent']],byref[r['ref']];dx=(c.GetPosition().x-p.GetPosition().x)/1e6;dy=(c.GetPosition().y-p.GetPosition().y)/1e6
 assert max(abs(a-b) for a,b in zip([dx,dy],r['relative_mm']))<1e-6,r
for name in CONFIG['library_models']:
 f=pcbnew.FootprintLoad(str(PARTS/'footprints/Controls.pretty'),name);assert f
 m=list(f.Models())[0];s=CONFIG['library_models'][name]
 assert Path(m.m_Filename).name==s['file']
 assert max(abs(x-y) for x,y in zip([m.m_Offset.x,m.m_Offset.y,m.m_Offset.z],s['offset']))<1e-6
 assert max(abs(x-y) for x,y in zip([m.m_Rotation.x,m.m_Rotation.y,m.m_Rotation.z],s['rotate']))<1e-6
for name,digest in CONFIG['updated_step_sha256'].items():
 assert hashlib.sha256((PARTS/'3dmodels/Controls'/name).read_bytes()).hexdigest()==digest
report=dict(footprint_count=len(checks),unique_types=len({r['footprint'] for r in checks}),all_models_resolved=True,all_model_scales_unity=True,updated_step_files_preserved=True,assembly_instances_checked=len(CONFIG['assemblies']),tracks=len(list(b.GetTracks())),zones=len(list(b.Zones())),instances=checks)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='instances'}))
