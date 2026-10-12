"""Stage native S3 jumper groups while preserving all saved artwork and routes."""
from pathlib import Path
import json
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / 'tools/wiring'))
from source import children, key, nodes, one, parse, prop, replace, FOOTPRINT_BLOCK

WORK = Path('/private/tmp/powermatic-s3-jumpers-20261010')
GROUPS = [('1B', '2B'), ('1T', '3T'), ('3B', '4B', '5B'),
          ('4T', '6T'), ('5T', '7T'), ('7B', '8B')]
STRAPS = {'long': [('1B', '2B'), ('3B', '4B'), ('7B', '8B')],
          'short': [('1T', '3T'), ('3B', '5B'), ('5T', '7T'), ('4T', '6T')]}


def configure(raw, kind):
    name = 'jumper_' + kind + '_groups'
    n = parse(raw)
    assert one(n, name) is None, 'Unexpected pre-existing jumper groups'
    assert one(n, 'duplicate_' + kind + '_numbers_are_jumpers') == [
        'duplicate_' + kind + '_numbers_are_jumpers', 'no']
    matches = [(a,b,c) for a,b,c in children(raw)
               if key(c) == 'duplicate_' + kind + '_numbers_are_jumpers']
    assert len(matches) == 1
    a,b,c = matches[0]
    indent = raw[raw.rfind('\n', 0, a)+1:a]
    group = '(' + name + '\n' + ''.join(
        indent + '\t(' + ' '.join(json.dumps(pin) for pin in pins) + ')\n'
        for pins in GROUPS) + indent + ')'
    return raw[:b] + '\n' + indent + group + raw[b:]


def patch_symbol_library(text):
    edits = []
    for a,b,c in children(text):
        if key(c) == 'symbol' and parse(c)[1] == '365-TAV2111':
            edits.append((a,b,configure(c,'pin')))
    assert len(edits) == 1
    return replace(text,edits)


symbols = (WORK/'before/Controls.kicad_sym').read_text()
(WORK/'after/Controls.kicad_sym').write_text(patch_symbol_library(symbols))

fp = (WORK/'before/365-TAV2111_Top.kicad_mod').read_text()
(WORK/'after/365-TAV2111_Top.kicad_mod').write_text(configure(fp,'pad'))

sch = (WORK/'before/powermatic_1200.kicad_sch').read_text()
edits = []
for a,b,c in children(sch):
    if key(c) != 'lib_symbols': continue
    subedits = []
    for sa,sb,sc in children(c):
        if parse(sc)[1] == 'Controls:365-TAV2111':
            subedits.append((sa,sb,configure(sc,'pin')))
    assert len(subedits) == 1
    edits.append((a,b,replace(c,subedits)))
assert len(edits) == 1
(WORK/'after/powermatic_1200.kicad_sch').write_text(replace(sch,edits))

board = (WORK/'before/powermatic_1200.kicad_pcb').read_text()
edits = []
for m in FOOTPRINT_BLOCK.finditer(board):
    if '\n\t\t(property "Reference" "S3"' not in m[0]: continue
    n = parse(m[0])
    pads = {p[1]:one(p,'net')[1] for p in nodes(n,'pad')}
    assert len(pads) == 16
    for pins in GROUPS:
        assert len({pads[p] for p in pins}) == 1, 'Jumper joins different saved nets'
    edits.append((m.start(),m.end(),configure(m[0],'pad')))
assert len(edits) == 1
(WORK/'after/powermatic_1200.kicad_pcb').write_text(replace(board,edits))

manifest = {'groups':GROUPS,'straps':STRAPS,'physical_strap_count':7,
            'electrical_group_count':6,'pin_ids_preserved':True,
            'artwork_preserved':True,'placement_preserved':True,
            'routes_preserved':True,'native_settings':[
                'Shared symbol jumper_pin_groups','Schematic cache jumper_pin_groups',
                'Shared footprint jumper_pad_groups','Placed S3 jumper_pad_groups']}
(WORK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Staged six S3 jumper groups for three long and four short retained straps.')
