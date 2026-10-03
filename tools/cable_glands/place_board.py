#!/usr/bin/env python3
"""Add only the three gland footprints. Use KiCad's bundled Python.
Preserves all existing board records verbatim, assigns logical core target nets.
"""
from pathlib import Path
import sys,json,hashlib,re
import pcbnew
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'controls_footprints/left_wall'))
from install import children,key
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];WORK=Path(sys.argv[1]);CFG=json.loads((HERE/'config.json').read_text());BOARD=ROOT/'kicad/powermatic_1200/powermatic_1200.kicad_pcb';PARTS=Path.home()/'Projects/_parts'
source=BOARD.read_text();b=pcbnew.LoadBoard(str(BOARD));netinfo={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
alias={'FWD_CMD':'Net-(K1A-AUX_NO_2)','REV_CMD':'Net-(K1A-AUX_NC_1)','STOP_CHAIN':'Net-(OL2B-TRIP_NC_2)','LOW_CMD':'Net-(K6A-AUX_NC_1)','HIGH_CMD':'Net-(K4A-AUX_NC_1)'}
assert not any(f.GetReference() in {'J3','J4','J5'} for f in b.GetFootprints())
# Isolate native serialization to only the new footprints; all existing records
# and net names are retained, including names aliased in the schematic.
review=pcbnew.BOARD();report=[];r=__import__('xml.etree.ElementTree',fromlist=['']).parse(WORK/'candidate.xml')
for p in CFG['parts']:
 name=p['part']+'_BottomWall';f=pcbnew.FootprintLoad(str(PARTS/'footprints/Controls.pretty'),name);assert f
 f.SetFPID(pcbnew.LIB_ID('Controls',name));f.SetReference(p['ref']);f.SetValue(p['part']);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(p['x_mm']),pcbnew.FromMM(CFG['bottom_wall_pcb_y_mm'])))
 f.SetPath(pcbnew.KIID_PATH('/e44f68e1-a298-4b0d-a2e0-68bc2c75ea41/'+r.find('./components/comp[@ref="'+p['ref']+'"]/tstamps').text))
 assert {pad.GetNumber() for pad in f.Pads()}==set(p['pins'])
 for pad in f.Pads():
  sig=p['signals'][p['pins'].index(pad.GetNumber())]
  if sig:
   name=alias.get(sig,sig);net=netinfo.get(name) or netinfo.get('/'+name);assert net,(p,sig,list(netinfo));pad.SetNet(net)
 review.Add(f);report.append({'reference':p['ref'],'part':p['part'],'position_mm':[p['x_mm'],CFG['bottom_wall_pcb_y_mm']],'distance_from_left_mm':p['x_mm']-CFG['enclosure_left_pcb_x_mm'],'distance_from_right_mm':CFG['enclosure_right_pcb_x_mm']-p['x_mm'],'centerline_from_back_mm':75,'symbol_uuid_path':f.GetPath().AsString(),'pads_are_logical_core_targets':True})
pcbnew.SaveBoard(str(WORK/'glands-only.kicad_pcb'),review)
new=[n for _,_,n in children((WORK/'glands-only.kicad_pcb').read_text()) if key(n)=='footprint'];assert len(new)==3
codes={json.loads(name):int(code) for code,name in re.findall(r'^\s*\(net (\d+) ("(?:\\.|[^"\\])*")\)',source,re.M)}
new=[re.sub(r'\(net (\d+) ("(?:\\.|[^"\\])*")\)',lambda m:'(net '+str(codes[json.loads(m[2])])+' '+m[2]+')',n) for n in new]
updated=source[:source.rfind(')')].rstrip()+'\n'+ '\n'.join(new)+'\n)\n';oldnodes=[n for _,_,n in children(source)];newnodes=[n for _,_,n in children(updated)];assert oldnodes==newnodes[:-3]
for label,oldname in alias.items():updated=updated.replace(json.dumps(oldname),json.dumps('/'+label))
(WORK/'board-before.kicad_pcb').write_text(source);(WORK/'board-candidate.kicad_pcb').write_text(updated);test=pcbnew.LoadBoard(str(WORK/'board-candidate.kicad_pcb'));assert len(list(test.GetFootprints()))==len(list(b.GetFootprints()))+3
assert BOARD.read_text()==source;BOARD.write_text(updated)
(HERE/'placement.json').write_text(json.dumps({'parts':report,'other_top_level_records_unchanged':True,'before_sha256':hashlib.sha256(source.encode()).hexdigest(),'after_sha256':hashlib.sha256(updated.encode()).hexdigest()},indent=2)+'\n');print(json.dumps(report,indent=2))
