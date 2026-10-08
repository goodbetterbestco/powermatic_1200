#!/usr/bin/env python3
"""Stage S3's source association without touching unrelated project records."""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, replace, nodes, TOKEN

FP = 'Controls:365-TAV2111_Top'
PACKAGE = 'Machine-mounted drum switch 156 x 73 x 75 mm'


def patch_fields(raw, updates):
    edits = []
    found = set()
    for start, end, child in children(raw):
        if key(child) != 'property':
            continue
        value = parse(child)
        if value[1] not in updates:
            continue
        found.add(value[1])
        tokens = list(TOKEN.finditer(child))
        a, b = tokens[3].span()
        edits.append((start, end, child[:a] + json.dumps(updates[value[1]]) + child[b:]))
    assert found == set(updates), (found, updates)
    return replace(raw, edits)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    work = args.work
    parts = Path.home() / 'Projects/_parts'
    project = ROOT / 'kicad/powermatic_1200'
    (work / 'before').mkdir(exist_ok=True)
    (work / 'after').mkdir(exist_ok=True)
    (work / 'shared-before').mkdir(exist_ok=True)
    (work / 'shared-after').mkdir(exist_ok=True)
    report = {'files': {}, 'shared_files': {}, 'source': str(work)}
    for suffix in ['kicad_pcb', 'kicad_sch', 'kicad_pro']:
        source = project / ('powermatic_1200.' + suffix)
        shutil.copy2(source, work / 'before' / source.name)
        shutil.copy2(source, work / 'after' / source.name)
        report['files'][source.name] = {'source': str(source),
                                      'sha256_before': hashlib.sha256(source.read_bytes()).hexdigest()}
    schematic = work / 'after/powermatic_1200.kicad_sch'
    original = schematic.read_text()
    edits = []
    for a, b, child in children(original):
        if key(child) == 'symbol' and prop(parse(child), 'Reference') == 'S3':
            edits.append((a, b, patch_fields(child, {'Footprint': FP, 'Package': PACKAGE})))
        elif key(child) == 'lib_symbols':
            nested = []
            for x, y, raw in children(child):
                if key(raw) == 'symbol' and parse(raw)[1] == 'Controls:365-TAV2111':
                    nested.append((x, y, patch_fields(raw, {'Footprint': FP, 'Package': PACKAGE})))
            assert len(nested) == 1
            edits.append((a, b, replace(child, nested)))
    assert len(edits) == 2
    schematic.write_text(replace(original, edits))
    shared_symbol = parts / 'symbols/Controls.kicad_sym'
    source = shared_symbol.read_text()
    edits = [(a, b, patch_fields(raw, {'Footprint': FP, 'Package': PACKAGE}))
             for a, b, raw in children(source)
             if key(raw) == 'symbol' and parse(raw)[1] == '365-TAV2111']
    assert len(edits) == 1
    (work / 'shared-before/Controls.kicad_sym').write_text(source)
    (work / 'shared-after/Controls.kicad_sym').write_text(replace(source, edits))
    report['shared_files']['symbols/Controls.kicad_sym'] = {
        'source': str(shared_symbol), 'candidate': str(work / 'shared-after/Controls.kicad_sym'),
        'sha256_before': hashlib.sha256(source.encode()).hexdigest()}
    source_csv = parts / 'database/non_lcsc_parts.csv'
    raw = source_csv.read_bytes()
    text = raw.decode()
    lines = text.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(text, newline=''))
    header = next(reader)
    previous = reader.line_num
    found = 0
    for row in reader:
        end = reader.line_num
        if row[header.index('PartID')] == '365-TAV2111':
            row[header.index('Footprint')] = FP
            row[header.index('Package')] = PACKAGE
            stream = io.StringIO(newline='')
            csv.writer(stream, lineterminator='\n').writerow(row)
            after = ''.join(lines[:previous]) + stream.getvalue() + ''.join(lines[end:])
            found += 1
        previous = end
    assert found == 1
    before_rows = list(csv.DictReader(io.StringIO(text)))
    after_rows = list(csv.DictReader(io.StringIO(after)))
    expected = [dict(row, **{'Footprint': FP, 'Package': PACKAGE})
                if row['PartID'] == '365-TAV2111' else row for row in before_rows]
    assert expected == after_rows
    (work / 'shared-before/non_lcsc_parts.csv').write_bytes(raw)
    (work / 'shared-after/non_lcsc_parts.csv').write_text(after)
    report['shared_files']['database/non_lcsc_parts.csv'] = {
        'source': str(source_csv), 'candidate': str(work / 'shared-after/non_lcsc_parts.csv'),
        'sha256_before': hashlib.sha256(raw).hexdigest()}
    # Expose existing models read-only to native candidate rendering/export.
    assets = work / 'assets/3dmodels/Controls'
    for source in (parts / '3dmodels/Controls').iterdir():
        destination = assets / source.name
        if source.is_file() and not destination.exists():
            destination.symlink_to(source)
    database = work / 'database'
    database.mkdir(exist_ok=True)
    shutil.copy2(parts / 'database/rebuild_db.py', database / 'rebuild_db.py')
    shutil.copy2(parts / 'database/parts.csv', database / 'parts.csv')
    shutil.copy2(work / 'shared-after/non_lcsc_parts.csv', database / 'non_lcsc_parts.csv')
    (work / 'staging.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Staged S3 footprint association and source catalog; existing records preserved.')


if __name__ == '__main__':
    main()
