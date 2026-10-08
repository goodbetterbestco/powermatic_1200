#!/usr/bin/env python3
"""Verify staged S2 geometry, net membership, and unrelated-record preservation."""
from pathlib import Path
import csv
import hashlib
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import parse, nodes, prop
from source import one

WORK = Path('/private/tmp/powermatic-s2-model')
BEFORE = ROOT / 'reviews/S2_model_2026-10-08/before'


def nets(path):
    return {n.get('name'): {(p.get('ref'), p.get('pin')) for p in n.findall('node')}
            for n in ET.parse(path).findall('nets/net')}


def normalized(node):
    if not isinstance(node, list):
        return node.replace('800S-3SA', '50MA3KLE') if isinstance(node, str) else node
    if node and node[0] == 'symbol' and (prop(node, 'Reference') == 'S2' or
                                       node[1] in ['Controls:800S-3SA', 'Controls:50MA3KLE']):
        allowed = {'Value', 'MPN', 'Manufacturer', 'Footprint', 'Datasheet',
                   'Package', 'Part Name', 'ki_keywords', 'Wire.Sizes', 'Termination.L4'}
        node = [n for n in node if not (isinstance(n, list) and
                (n[0] == 'on_board' or (n[0] == 'property' and n[1] in allowed)))]
    return [normalized(n) for n in node]


def main():
    before = parse((BEFORE / 'powermatic_1200.kicad_sch').read_text())
    after = parse((WORK / 'after/powermatic_1200.kicad_sch').read_text())
    added = json.loads((WORK / 'staging.json').read_text())['added_schematic_uuids']
    filtered = [n for n in after if not (isinstance(n, list) and
                one(n, 'uuid') and one(n, 'uuid')[1] in added)]
    assert normalized(before) == normalized(filtered)
    old_nets, new_nets = nets(WORK / 'before-netlist.xml'), nets(WORK / 'candidate-netlist.xml')
    old_nets['OVERLOAD_OK'] |= old_nets.pop('Net-(S2-FWD_NC_2)')
    assert old_nets == new_nets
    for state in [before, after]:
        symbol = next(s for s in nodes(state, 'symbol') if prop(s, 'Reference') == 'S2')
        if state is before:
            old_sizes = json.loads(prop(symbol, 'Wire.Sizes'))
            old_terminations = [p for p in nodes(symbol, 'property') if p[1].startswith('Termination.') and p[1] != 'Termination.L4']
        else:
            new_sizes = json.loads(prop(symbol, 'Wire.Sizes'))
            assert old_terminations == [p for p in nodes(symbol, 'property') if p[1].startswith('Termination.') and p[1] != 'Termination.L4']
            assert prop(symbol, 'Termination.L4') == 'Required jumper, 2B-4B'
    for entry in old_sizes['entries']:
        if entry['pin'] in ['R2', 'R4']:
            entry['net'] = 'OVERLOAD_OK'
            entry['note'] = 'Installed station jumpers 1T-3T and 3T-5T; no external conductor.'
        elif entry['pin'] == 'L4':
            entry['note'] = 'Required station jumper 2B-4B; physical installation unconfirmed.'
    assert old_sizes == new_sizes
    for suffix in ['kicad_pro']:
        assert (BEFORE / ('powermatic_1200.' + suffix)).read_bytes() == (
            WORK / 'after' / ('powermatic_1200.' + suffix)).read_bytes()
    board_before = parse((BEFORE / 'powermatic_1200.kicad_pcb').read_text())
    board_after = parse((WORK / 'after/powermatic_1200.kicad_pcb').read_text())
    assert board_after[:-1] == board_before
    assert prop(board_after[-1], 'Reference') == 'S2'
    assert len(nodes(board_after[-1], 'pad')) == 10
    sym_before = parse((WORK / 'shared-before/Controls.kicad_sym').read_text())
    sym_after = parse((WORK / 'shared-after/Controls.kicad_sym').read_text())
    assert sym_after[:-1] == sym_before
    geom = json.loads((WORK / 'assets/geometry.json').read_text())
    assert hashlib.sha256((WORK / 'assets/3dmodels/Controls/Furnas_50MA3KLE.step').read_bytes()).hexdigest() == geom['source_sha256']
    assert {p['number'] for p in geom['pads']} == {f'{side}{i}' for side in ['L', 'R'] for i in range(1, 6)}
    mapping = {p['number']: p['model_screw'] for p in geom['pads']}
    expected = {'L1': 'screw_2T', 'R2': 'screw_1T', 'L2': 'screw_2B', 'R1': 'screw_1B',
                'L3': 'screw_4T', 'R4': 'screw_3T', 'L4': 'screw_4B', 'R3': 'screw_3B',
                'L5': 'screw_6T', 'R5': 'screw_5T'}
    assert mapping == expected
    functions = {p.get('pin'): p.get('pinfunction') for n in ET.parse(WORK / 'candidate-netlist.xml').findall('nets/net')
                 for p in n.findall('node') if p.get('ref') == 'S2'}
    for pin, screw in mapping.items():
        assert ('_NC_' in functions[pin]) == screw.endswith('T')
    for stem, identity in [('parts', 'LCSC'), ('non_lcsc_parts', 'PartID')]:
        rows = list(csv.DictReader((WORK / 'database' / (stem + '.csv')).open(newline='')))
        db = sqlite3.connect(WORK / 'database' / (stem + '.db'))
        db.row_factory = sqlite3.Row
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert [dict(r) for r in db.execute('SELECT * FROM parts')] == rows
        assert len({r[identity] for r in rows}) == len(rows)
        db.close()
    old_rows = list(csv.DictReader((WORK / 'shared-before/non_lcsc_parts.csv').open(newline='')))
    new_rows = list(csv.DictReader((WORK / 'shared-after/non_lcsc_parts.csv').open(newline='')))
    assert new_rows[:-1] == old_rows and new_rows[-1]['PartID'] == '50MA3KLE'
    report = {'schematic_only_S2_identity_and_association_changed': True,
              'only_unused_NC_common_joined_to_STOP_input_per_installed_jumpers': True,
              'all_external_conductor_nets_and_termination_records_unchanged': True,
              'additional_NO_common_jumper_explicitly_required_not_claimed_installed': True,
              'physical_contact_mapping_matches_symbol_pin_functions': True,
              'all_89_original_footprints_and_board_records_unchanged': True,
              'old_library_symbols_and_catalog_rows_retained': True,
              'ten_symbol_pins_match_ten_footprint_pads': True,
              'source_STEP_byte_identical': True, 'project_settings_unchanged': True,
              'CSV_SQLite_parity_and_integrity': True}
    (WORK / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('S2 preservation, catalog, pin inventory, and source checks passed.')


if __name__ == '__main__':
    main()
