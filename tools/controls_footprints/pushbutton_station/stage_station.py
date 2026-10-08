#!/usr/bin/env python3
"""Stage the new Furnas catalog symbol and S2 association; retain wire records."""
from pathlib import Path
import csv
import hashlib
import io
import json
import shutil
import sys
import uuid

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
sys.path.insert(0, str(ROOT / 'tools/controls_footprints/drum_switch'))
from source import children, key, parse, prop, replace
from stage import patch_fields
from renumber import definition, instance

WORK = Path('/private/tmp/powermatic-s2-model')
PARTS = Path.home() / 'Projects/_parts'
FP = 'Controls:50MA3KLE_Top'
UPDATES = {'Value': '50MA3KLE', 'MPN': '50MA3KLE', 'Manufacturer': 'Furnas',
           'Footprint': FP, 'Datasheet': '',
           'Package': 'Machine-mounted pushbutton station 52 x 116 x 44.7 mm',
           'Part Name': 'Button\nStation'}


def symbol_patch(raw, library=False):
    updates = dict(UPDATES)
    if library:
        updates['ki_keywords'] = 'Furnas 50MA3KLE vintage forward reverse stop pushbutton station'
    result = patch_fields(raw, updates).replace('(on_board no)', '(on_board yes)')
    result = result.replace('800S-3SA', '50MA3KLE')
    return definition(result) if library else instance(result)


def main():
    shared_before = WORK / 'shared-before'
    shared_after = WORK / 'shared-after'
    shared_before.mkdir(exist_ok=True)
    shared_after.mkdir(exist_ok=True)
    library = PARTS / 'symbols/Controls.kicad_sym'
    original = library.read_text()
    raw = next(raw for a, b, raw in children(original)
               if key(raw) == 'symbol' and parse(raw)[1] == '800S-3SA')
    new = symbol_patch(raw, True)
    # Keep the old Allen-Bradley library device available to other projects.
    candidate = original[:original.rfind(')')] + '\n' + new + '\n)\n'
    assert parse(candidate)[:-1] == parse(original)
    (shared_before / library.name).write_text(original)
    (shared_after / library.name).write_text(candidate)
    path = WORK / 'after/powermatic_1200.kicad_sch'
    original = (ROOT / 'reviews/S2_model_2026-10-08/before' / path.name).read_text()
    edits = []
    for a, b, raw in children(original):
        if key(raw) == 'symbol' and prop(parse(raw), 'Reference') == 'S2':
            candidate_symbol = symbol_patch(raw)
            sizes = json.loads(prop(parse(candidate_symbol), 'Wire.Sizes'))
            for entry in sizes['entries']:
                if entry['pin'] in ['1T', '3T']:
                    entry['net'] = 'OVERLOAD_OK'
                    entry['note'] = 'Installed station jumpers 1T-3T and 3T-5T; no external conductor.'
                elif entry['pin'] == '4B':
                    entry['note'] = 'Required station jumper 2B-4B; physical installation unconfirmed.'
            candidate_symbol = patch_fields(candidate_symbol, {'Wire.Sizes': json.dumps(sizes, separators=(',', ':')),
                                                             'Termination.4B': 'Required jumper, 2B-4B'})
            edits.append((a, b, candidate_symbol))
        elif key(raw) == 'lib_symbols':
            inner = [(x, y, symbol_patch(entry, True)) for x, y, entry in children(raw)
                     if key(entry) == 'symbol' and parse(entry)[1] == 'Controls:800S-3SA']
            assert len(inner) == 1
            edits.append((a, b, replace(raw, inner)))
    assert len(edits) == 2
    candidate = replace(original, edits)
    # The owner's installed 3T-5T link joins the existing NC common rail to
    # STOP's input. Intersections with other signal wires have no junctions.
    addition_ids = [str(uuid.uuid4()) for _ in range(3)]
    additions = [f'(wire (pts (xy 55.88 -8.89) (xy 55.88 6.35)) (stroke (width 0) (type default)) (uuid "{addition_ids[0]}"))',
                 f'(junction (at 55.88 -8.89) (diameter 0) (color 0 0 0 0) (uuid "{addition_ids[1]}"))',
                 f'(junction (at 55.88 6.35) (diameter 0) (color 0 0 0 0) (uuid "{addition_ids[2]}"))']
    candidate = candidate[:candidate.rfind(')')] + '\n' + '\n'.join(additions) + '\n)\n'
    path.write_text(candidate)
    source = PARTS / 'database/non_lcsc_parts.csv'
    raw = source.read_text()
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)
    assert not any(row['PartID'] == '50MA3KLE' for row in rows)
    row = dict(next(row for row in rows if row['PartID'] == '800S-3SA'))
    row.update({'PartID': '50MA3KLE', 'Symbol': 'Controls:50MA3KLE', **UPDATES})
    row['SupplierPartNumber'] = 'FURNAS_50MA3KLE'
    row['Keywords'] = 'Furnas 50MA3KLE vintage forward reverse stop pushbutton station'
    # Clear old supplier lookup fields rather than carrying AB search results.
    for column in reader.fieldnames:
        if column.startswith('JLC'):
            row[column] = ''
    row = {column: row.get(column, '') for column in reader.fieldnames}
    stream = io.StringIO(newline='')
    csv.DictWriter(stream, fieldnames=reader.fieldnames, lineterminator='\n').writerow(row)
    (shared_before / source.name).write_text(raw)
    (shared_after / source.name).write_text(raw.rstrip('\n') + '\n' + stream.getvalue())
    database = WORK / 'database'
    database.mkdir(exist_ok=True)
    for name in ['rebuild_db.py', 'parts.csv']:
        shutil.copy2(PARTS / 'database' / name, database / name)
    shutil.copy2(shared_after / source.name, database / source.name)
    report = {'added_schematic_uuids': addition_ids,
              'shared_files': {str(library): str(shared_after / library.name),
                              str(source): str(shared_after / source.name)},
              'before_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [library, source, PARTS / 'database/non_lcsc_parts.db']}}
    (WORK / 'staging.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Staged Furnas symbol, catalog row, and S2 metadata; old library device retained.')


if __name__ == '__main__':
    main()
