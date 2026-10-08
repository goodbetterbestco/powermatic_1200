import json, sys
from pathlib import Path
import pcbnew as k
sys.path.insert(0,'/Users/evanthayer/Projects/_hardware/powermatic_1200/tools/wiring')
from source import parse,nodes,one,prop
W=Path('/private/tmp/powermatic-pcb-migration-20261006')
s=json.loads((W/'staged.json').read_text())
b=k.LoadBoard(str(W/'after/powermatic_1200.kicad_pcb'))
assert len(list(b.GetFootprints()))==87
refs={f.GetReference():f for f in b.GetFootprints() if f.GetReference()!='REF**'}
links=0;gray=0
for f in b.GetFootprints():
 ref=f.GetReference()
 if ref in s['reference_map'].values():
  assert f.GetPath().AsString()
  assert not f.GetAttributes()&k.FP_BOARD_ONLY
  links+=1
 else:
  assert f.GetAttributes()&k.FP_BOARD_ONLY
 for p in f.Pads():
  if ref=='REF**':continue
  wanted=s['pad_assignments'][ref+'.'+p.GetNumber()]
  assert str(p.GetNetname())==(wanted or ''),(ref,p.GetNumber(),p.GetNetname(),wanted)
 if f.GetFPID().GetLibItemName()=='KN-T12GRY-25_Front':
  gray+=1
  assert not f.GetPath().AsString()
  assert all(not p.GetNetname() for p in f.Pads())
assert links==19 and gray==29
for ref,count in [('J3',8),('J4',12),('J5',16)]:assert len(list(refs[ref].Pads()))==count
for file in s['shared_library_changes']:
 fp=k.FootprintLoad(str(W/'library-after'),file.removesuffix('.kicad_mod'))
 assert fp,file
 if file=='NDR-240-24_Front.kicad_mod':
  assert {p.GetNumber() for p in fp.Pads()}=={'1_BOT','2_BOT','3_BOT','1_TOP','2_TOP','3_TOP','4_TOP'}
b.BuildConnectivity()
k.SaveBoard(str(W/'native-roundtrip.kicad_pcb'),b)
rt=parse((W/'native-roundtrip.kicad_pcb').read_text())
raw=parse((W/'after/powermatic_1200.kicad_pcb').read_text())
groups=lambda t:{one(f,'uuid')[1]:set(frozenset(g) for g in (one(f,'jumper_pad_groups') or [])[1:]) for f in nodes(t,'footprint')}
assert groups(rt)==groups(raw)
result={'kicad_version':k.Version(),'footprints':87,'linked_footprints':19,'pcb_only':68,'unassigned_gray_feedthroughs':29,'gland_pad_counts':{'J3':8,'J4':12,'J5':16},'native_roundtrip_preserves_jumper_groups':True,'all_physical_pad_nets_match_current_schematic':True,'all_shared_library_files_load':True}
(W/'native-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
