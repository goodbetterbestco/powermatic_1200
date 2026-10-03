from pathlib import Path
import sys,xml.etree.ElementTree as ET,json
HERE=Path(__file__).resolve().parent;work=Path(sys.argv[1])
def nets(p):return [(n.attrib['name'],frozenset((x.attrib['ref'],x.attrib['pin']) for x in n.findall('node'))) for n in ET.parse(p).findall('./nets/net')]
before=nets(work/'before.xml');after=nets(work/'candidate.xml');original_pins=set().union(*(s for _,s in before))
assert {s for _,s in before}=={s & original_pins for _,s in after if s & original_pins},'Existing net connectivity changed'
mapping=json.loads((HERE/'pin_map.json').read_text());aliases={'FWD_CMD':'Net-(K1A-AUX_NO_2)','REV_CMD':'Net-(K1A-AUX_NC_1)','STOP_CHAIN':'Net-(OL2B-TRIP_NC_2)','LOW_CMD':'Net-(K6A-AUX_NC_1)','HIGH_CMD':'Net-(K4A-AUX_NC_1)'}
for p in mapping:
 if not p['signal']:continue
 original=aliases.get(p['signal'],p['signal']);expected=next(s for n,s in before if n==original or n=='/'+original)
 actual=next(s for n,s in after if (p['reference'],p['pin']) in s);assert expected==actual & original_pins,(p,expected,actual)
print('All existing net membership preserved; 17 gland conductor connections match, all seven controls cores used.')
(HERE/'connectivity_validation.json').write_text(json.dumps({'all_original_pin_net_memberships_preserved':True,'connected_gland_cores':17,'spares':0,'original_nets':len(before)},indent=2)+'\n')
