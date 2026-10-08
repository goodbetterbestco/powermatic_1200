#!/usr/bin/env python3
"""Check the staged S3 edit, including exact preservation outside its association."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import parse, nodes, prop


def normalized(node):
    if not isinstance(node, list):
        return node
    if node and node[0] == 'symbol':
        identity = node[1] if len(node) > 1 and isinstance(node[1], str) else None
        if prop(node, 'Reference') == 'S3' or identity in {'Controls:365-TAV2111', '365-TAV2111'}:
            node = [child for child in node if not (isinstance(child, list)
                    and len(child) > 1 and child[0] == 'property'
                    and child[1] in {'Footprint', 'Package'})]
    return [normalized(child) for child in node]


def nets(path):
    return {net.get('name'): {(pin.get('ref'), pin.get('pin')) for pin in net.findall('node')}
            for net in ET.parse(path).getroot().findall('nets/net')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    work = args.work
    report = json.loads((work / 'staging.json').read_text())
    schematic_before = parse((work / 'before/powermatic_1200.kicad_sch').read_text())
    schematic_after = parse((work / 'after/powermatic_1200.kicad_sch').read_text())
    assert normalized(schematic_before) == normalized(schematic_after)
    assert normalized(parse((work / 'shared-before/Controls.kicad_sym').read_text())) == normalized(
        parse((work / 'shared-after/Controls.kicad_sym').read_text()))
    assert (work / 'before/powermatic_1200.kicad_pro').read_bytes() == (
        work / 'after/powermatic_1200.kicad_pro').read_bytes()
    before = parse((work / 'before/powermatic_1200.kicad_pcb').read_text())
    after = parse((work / 'after/powermatic_1200.kicad_pcb').read_text())
    assert after[:-1] == before
    assert prop(after[-1], 'Reference') == 'S3'
    assert nets('/private/tmp/ab365-current-netlist.xml') == nets(work / 'candidate-netlist.xml')
    assert sum(sum(p[1].startswith('Termination.') for p in nodes(s, 'property'))
               for s in nodes(schematic_after, 'symbol')) == 184
    for stem, key in [('parts', 'LCSC'), ('non_lcsc_parts', 'PartID')]:
        with (work / 'database' / (stem + '.csv')).open(newline='') as stream:
            reader = csv.DictReader(stream)
            columns, rows = reader.fieldnames, list(reader)
        connection = sqlite3.connect(work / 'database' / (stem + '.db'))
        assert connection.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert [dict(zip(columns, row)) for row in connection.execute('SELECT * FROM parts')] == rows
        assert len({row[key] for row in rows}) == len(rows)
        connection.close()
        print(stem, len(rows), 'validated')
    for name, item in report['files'].items():
        item['candidate'] = str(work / 'after' / name)
        item['sha256_after'] = hashlib.sha256(Path(item['candidate']).read_bytes()).hexdigest()
    for item in report['shared_files'].values():
        item['sha256_after'] = hashlib.sha256(Path(item['candidate']).read_bytes()).hexdigest()
    source = Path.home() / 'Projects/_parts/database/non_lcsc_parts.db'
    report['shared_files']['database/non_lcsc_parts.db'] = {
        'source': str(source), 'candidate': str(work / 'database/non_lcsc_parts.db'),
        'sha256_before': hashlib.sha256(source.read_bytes()).hexdigest(),
        'sha256_after': hashlib.sha256((work / 'database/non_lcsc_parts.db').read_bytes()).hexdigest()}
    new_files = {'footprints/Controls.pretty/365-TAV2111_Top.kicad_mod':
                 work / 'assets/footprints/Controls.pretty/365-TAV2111_Top.kicad_mod',
                 '3dmodels/Controls/AB_365-TAV2111.step':
                 work / 'assets/3dmodels/Controls/AB_365-TAV2111.step'}
    for relative, path in new_files.items():
        target = Path.home() / 'Projects/_parts' / relative
        assert not target.exists()
        report['shared_files'][relative] = {
            'source': str(target), 'candidate': str(path), 'sha256_before': None,
            'sha256_after': hashlib.sha256(path.read_bytes()).hexdigest()}
    report['checks'] = {'original_88_footprints_unchanged': True,
                        'schematic_net_membership_unchanged': True,
                        'shared_symbol_only_association_fields_changed': True,
                        'project_settings_unchanged': True,
                        'all_184_schematic_termination_fields_retained': True,
                        'catalog_CSV_SQLite_parity': True, 'catalog_unique_keys': True,
                        'catalog_integrity': 'ok'}
    (work / 'staging.json').write_text(json.dumps(report, indent=2) + '\n')
    print('All staged preservation and catalog checks passed.')


if __name__ == '__main__':
    main()
