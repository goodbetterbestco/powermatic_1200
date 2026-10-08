#!/usr/bin/env python3
"""Check S2 renumbering against native nets, terminal geometry and symbol rules."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, nodes
from renumber import PIN_MAP, FUNCTIONS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    work = args.work
    before, after = work / 'before', work / 'after'
    def graph(path, old=False):
        result = []
        for net in ET.parse(path).findall('nets/net'):
            endpoints = sorted((p.get('ref'), PIN_MAP.get(p.get('pin'), p.get('pin'))
                                if old and p.get('ref') == 'S2' else p.get('pin'))
                               for p in net.findall('node'))
            name = '<unconnected>' if net.get('name').startswith('unconnected-') else net.get('name')
            result.append((name, endpoints))
        return sorted(result)
    assert graph(work / 'before-netlist.xml', True) == graph(work / 'candidate-netlist.xml')
    old = parse((before / 'powermatic_1200.kicad_sch').read_text())
    new = parse((after / 'powermatic_1200.kicad_sch').read_text())
    def other_schematic_records(text):
        return [raw for a, b, raw in children(text) if key(raw) != 'lib_symbols'
                and not (key(raw) == 'symbol' and prop(parse(raw), 'Reference') == 'S2')]
    assert other_schematic_records((before / 'powermatic_1200.kicad_sch').read_text()) == other_schematic_records((after / 'powermatic_1200.kicad_sch').read_text())
    old_library, new_library = one(old, 'lib_symbols'), one(new, 'lib_symbols')
    assert [s for s in nodes(old_library, 'symbol') if s[1] != 'Controls:50MA3KLE'] == [s for s in nodes(new_library, 'symbol') if s[1] != 'Controls:50MA3KLE']
    old_instance = next(s for s in nodes(old, 'symbol') if prop(s, 'Reference') == 'S2')
    new_instance = next(s for s in nodes(new, 'symbol') if prop(s, 'Reference') == 'S2')
    assert one(old_instance, 'uuid') == one(new_instance, 'uuid')
    old_def = next(s for s in nodes(old_library, 'symbol') if s[1] == 'Controls:50MA3KLE')
    new_def = next(s for s in nodes(new_library, 'symbol') if s[1] == 'Controls:50MA3KLE')
    def pin_map(definition):
        return {one(p, 'number')[1]: p for u in nodes(definition, 'symbol') for p in nodes(u, 'pin')}
    old_pins, new_pins = pin_map(old_def), pin_map(new_def)
    assert set(new_pins) == set(FUNCTIONS)
    def world(instance, pin):
        i, p = one(instance, 'at'), one(pin, 'at')
        return [round(float(i[1]) + float(p[1]), 6), round(float(i[2]) - float(p[2]), 6)]
    for previous, physical in PIN_MAP.items():
        assert world(old_instance, old_pins[previous]) == world(new_instance, new_pins[physical])
        pin = new_pins[physical]
        assert pin[1:3] == ['passive', 'line']
        assert one(pin, 'name')[1] == FUNCTIONS[physical]
        assert abs(float(one(pin, 'length')[1]) - 2.54) < 1e-6
        assert abs(float(one(pin, 'at')[1]) / 2.54 - round(float(one(pin, 'at')[1]) / 2.54)) < 1e-6
        assert abs(float(one(pin, 'at')[2]) / 1.27 - round(float(one(pin, 'at')[2]) / 1.27)) < 1e-6
    for field in ['Reference', 'Value', 'Part Name', 'MPN']:
        p = next(p for p in nodes(new_def, 'property') if p[1] == field)
        for value in one(p, 'at')[1:3]:
            assert abs(float(value) / 1.27 - round(float(value) / 1.27)) < 1e-6
    sizes = json.loads(prop(old_instance, 'Wire.Sizes'))
    for entry in sizes['entries']:
        entry['pin'] = PIN_MAP[entry['pin']]
    assert sizes == json.loads(prop(new_instance, 'Wire.Sizes'))
    for previous, physical in PIN_MAP.items():
        assert prop(old_instance, 'Termination.' + previous) == prop(new_instance, 'Termination.' + physical)
    assert {p[1] for p in nodes(new_instance, 'property') if p[1].startswith('Termination.')} == {'Termination.' + p for p in FUNCTIONS}
    old_shared = parse((before / 'Controls.kicad_sym').read_text())
    new_shared = parse((after / 'Controls.kicad_sym').read_text())
    assert [s for s in nodes(old_shared, 'symbol') if s[1] != '50MA3KLE'] == [s for s in nodes(new_shared, 'symbol') if s[1] != '50MA3KLE']
    # Footprint/library geometry and the board's other records are immutable.
    def geometry(node):
        return [n for n in node if not (isinstance(n, list) and n[0] == 'pad')]
    for filename, library in [('50MA3KLE_Top.kicad_mod', True), ('powermatic_1200.kicad_pcb', False)]:
        a, b = parse((before / filename).read_text()), parse((after / filename).read_text())
        if not library:
            def others(board):
                return [n for n in board if not (isinstance(n, list) and
                        (n[0] == 'footprint' and prop(n, 'Reference') == 'S2' or
                         n[0] == 'net' and str(n[-1]).startswith('unconnected-(S2-')))]
            assert others(a) == others(b)
            a = next(f for f in nodes(a, 'footprint') if prop(f, 'Reference') == 'S2')
            b = next(f for f in nodes(b, 'footprint') if prop(f, 'Reference') == 'S2')
        assert geometry(a) == geometry(b)
        pa, pb = {p[1]: p for p in nodes(a, 'pad')}, {p[1]: p for p in nodes(b, 'pad')}
        assert set(pb) == set(FUNCTIONS)
        for previous, physical in PIN_MAP.items():
            def physical_pad(p):
                return [n for n in p[2:] if not (isinstance(n, list) and n[0] in ['net', 'pinfunction', 'pintype'])]
            assert physical_pad(pa[previous]) == physical_pad(pb[physical])
    report = {'terminal_ids': sorted(FUNCTIONS), 'pin_names_match_physical_contact_ends': True,
              'all_contact_pins_passive_and_visible': True, 'pin_and_field_grids_correct': True,
              'all_ten_absolute_schematic_connection_points_unchanged': True,
              'electrical_connectivity_unchanged': True, 'wire_sizes_and_terminations_follow_physical_IDs': True,
              'all_other_symbols_and_board_records_preserved': True,
              'footprint_pad_geometry_and_model_transform_unchanged': True,
              'live_symbol_editor_inspection': 'pending'}
    (work / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('S2 native-net, grid, pin/function, metadata and preservation checks passed.')


if __name__ == '__main__':
    main()
