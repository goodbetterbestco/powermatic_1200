#!/usr/bin/env python3
"""Serialize only the new S3 footprint with KiCad's bundled Python."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

import pcbnew as k

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, nodes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--netlist', type=Path, required=True)
    args = parser.parse_args()
    work = args.work
    path = work / 'after/powermatic_1200.kicad_pcb'
    original = path.read_text()
    board = k.LoadBoard(str(path))
    assert not any(f.GetReference() == 'S3' for f in board.GetFootprints())
    schematic = parse((work / 'after/powermatic_1200.kicad_sch').read_text())
    symbol = next(s for s in nodes(schematic, 'symbol') if prop(s, 'Reference') == 'S3')
    fp = k.FootprintLoad(str(work / 'assets/footprints/Controls.pretty'), '365-TAV2111_Top')
    assert fp
    fp.SetFPID(k.LIB_ID('Controls', '365-TAV2111_Top'))
    fp.SetReference('S3')
    fp.SetValue('365-TAV2111')
    fp.SetPosition(k.VECTOR2I(k.FromMM(600), k.FromMM(231.241)))
    fp.SetPath(k.KIID_PATH('/' + one(symbol, 'uuid')[1]))
    xml = ET.parse(args.netlist).getroot()
    pins = {pin.get('pin'): (net.get('name'), pin.get('pinfunction'), pin.get('pintype'))
            for net in xml.findall('nets/net') for pin in net.findall('node')
            if pin.get('ref') == 'S3'}
    assert set(pins) == {f'{section}.{tier}' for section in range(1, 9) for tier in ['U', 'L']}
    netitems = {net.GetNetname(): net for net in board.GetNetInfo().NetsByNetcode().values()}
    for pad in fp.Pads():
        netname, function, pintype = pins[pad.GetNumber()]
        if netname not in netitems:
            netitems[netname] = k.NETINFO_ITEM(board, netname)
            board.Add(netitems[netname])
        pad.SetNet(netitems[netname])
        pad.SetPinFunction(function)
        pad.SetPinType(pintype)
    # Use a temporary board for native serialization of the new footprint only.
    isolated = k.BOARD()
    isolated.Add(fp)
    k.SaveBoard(str(work / 's3-only.kicad_pcb'), isolated)
    serialized = [raw for a, b, raw in children((work / 's3-only.kicad_pcb').read_text())
                  if key(raw) == 'footprint']
    assert len(serialized) == 1
    raw = serialized[0]
    # Bring only ordinary device metadata across. Wiring/termination ownership
    # remains unchanged until the planned joint S2/S3 termination migration.
    updates = {name: prop(symbol, name) for name in ['Datasheet', 'Description', 'MPN',
               'Manufacturer', 'Category', 'Package', 'Part Name', 'Mounting']}
    from stage import patch_fields
    # Category and Package are added below if absent from the library template.
    present = {p[1] for p in nodes(parse(raw), 'property')}
    raw = patch_fields(raw, {name: value for name, value in updates.items() if name in present})
    extras = []
    for name, value in updates.items():
        if name not in present:
            extras.append(f'\n\t(property {json.dumps(name)} {json.dumps(value)} '
                          '(at 0 0 0) (layer "F.Fab") (hide yes) '
                          '(effects (font (size 1 1) (thickness 0.15))))')
    raw = raw[:raw.rfind(')')] + ''.join(extras) + '\n)'
    updated = original[:original.rfind(')')] + '\n' + raw + '\n)\n'
    assert parse(updated)[:-1] == parse(original)
    path.write_text(updated)
    loaded = k.LoadBoard(str(path))
    assert len(list(loaded.GetFootprints())) == len(list(board.GetFootprints())) + 1
    result = next(f for f in loaded.GetFootprints() if f.GetReference() == 'S3')
    assert result.GetPath().AsString().endswith(one(symbol, 'uuid')[1])
    assert {p.GetNumber(): p.GetNetname() for p in result.Pads()} == {
        number: values[0] for number, values in pins.items()}
    assert all(p.GetPinFunction() == pins[p.GetNumber()][1] for p in result.Pads())
    assert all(p.GetPinType() == pins[p.GetNumber()][2] for p in result.Pads())
    report = {'reference': 'S3', 'footprint_uuid': result.m_Uuid.AsString(),
              'symbol_uuid': one(symbol, 'uuid')[1], 'position_mm': [600, 231.241],
              'pad_count': 16, 'all_pad_nets_functions_and_types_match_schematic': True,
              'all_original_top_level_board_records_unchanged': True,
              'board_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (work / 'placement.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
