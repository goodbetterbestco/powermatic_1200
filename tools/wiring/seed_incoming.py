#!/usr/bin/env python3
"""Reconcile only incoming phases, then seed their six schematic wire records."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import tempfile
import uuid

from model import Schematic, Panel, atomic_write, change_fields, digest, export_netlist, make_rows
from model import children, key, replace, parse, nodes, one, prop
from generate import PROJECT, DEFAULT_SCH, DEFAULT_PCB


def identity(raw, newref, newuuid):
    s = parse(raw)
    oldref = prop(s, 'Reference')
    edits = []
    for a, b, child in children(raw):
        k = key(child)
        if k == 'property' and parse(child)[1] == 'Reference':
            edits.append((a, b, child.replace(json.dumps(oldref), json.dumps(newref), 1)))
        elif k == 'instances':
            edits.append((a, b, child.replace(f'(reference "{oldref}")', f'(reference "{newref}")')))
        elif k == 'uuid':
            edits.append((a, b, f'(uuid "{newuuid}")'))
    return replace(raw, edits)


def seed(sch_path, pcb_path, legacy_path, apply=False):
    sch_path, pcb_path, legacy_path = map(Path, [sch_path, pcb_path, legacy_path])
    source, board, legacy = sch_path.read_bytes(), pcb_path.read_bytes(), legacy_path.read_bytes()
    text = source.decode('utf-8')
    original = parse(text)
    bodies = nodes(original, 'symbol')
    mains = [s for s in bodies if one(s, 'lib_id')[1] == 'Controls:3PH-4W-PLUG']
    if len(mains) != 1:
        raise ValueError('Expected one mains plug; choose the incoming section explicitly.')
    mi = one(mains[0], 'uuid')[1]
    if any(prop(s, 'Reference') == 'J2' and one(s, 'uuid')[1] != mi for s in bodies):
        raise ValueError('J2 is occupied by another device; resolve that reference first.')
    edits = [(a, b, identity(raw, 'J2', mi)) for a, b, raw in children(text)
             if key(raw) == 'symbol' and one(parse(raw), 'uuid')[1] == mi]
    text = replace(text, edits)
    # Use a native snapshot to identify which block currently carries each phase.
    with tempfile.TemporaryDirectory(prefix='incoming-wires-') as work:
        snapshot = Path(work) / sch_path.name
        snapshot.write_text(text)
        _, pin_nets = export_netlist(snapshot, work)
    index = Schematic(text)
    board_tree = parse(board.decode('utf-8'))
    fps = {prop(f, 'Reference'): f for f in nodes(board_tree, 'footprint')
           if prop(f, 'Reference') in ['TB40', 'TB41', 'TB42']}
    targets = {}
    for phase, correct in [('L1_IN', 'TB40'), ('L2_IN', 'TB41'), ('L3_IN', 'TB42')]:
        candidates = [ref for ref in ['TB40', 'TB41', 'TB42'] if pin_nets.get((ref, '1')) == phase]
        if len(candidates) != 1:
            raise ValueError(f'Cannot identify the incoming feedthrough for {phase}.')
        old = index.by_ref[candidates[0]][0]
        if one(old, 'at')[3] != '0':
            raise ValueError('Keep the incoming terminal symbols vertical with pin 1 above pin 2.')
        targets[one(old, 'uuid')[1]] = (correct, one(fps[correct], 'path')[1].split('/')[-1])
    edits = []
    for a, b, raw in children(text):
        if key(raw) == 'symbol' and one(parse(raw), 'uuid')[1] in targets:
            edits.append((a, b, identity(raw, *targets[one(parse(raw), 'uuid')[1]])))
    text = replace(text, edits)
    tree = parse(text)
    wires = nodes(tree, 'wire')
    extra = []
    for ref in ['TB40', 'TB41', 'TB42']:
        s = next(s for s in nodes(tree, 'symbol') if prop(s, 'Reference') == ref)
        at = one(s, 'at')
        x, y = map(float, at[1:3])
        a, b = (x, round(y - 10.16, 5)), (x, round(y + 10.16, 5))
        if not any({tuple(map(float, p[1:3])) for p in nodes(one(w, 'pts'), 'xy')} == {a, b} for w in wires):
            extra.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) '
                         f'(stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))')
    if extra:
        text = text[:text.rfind(')')] + '\n' + '\n'.join(extra) + '\n)\n'
    index = Schematic(text)
    records = index.records()
    if records:
        if {r['id'] for r in records if r.get('section') == '01 Incoming phases'} >= {f'W{i:03}' for i in range(1, 7)}:
            print('Incoming phase records already exist; their current metadata was preserved.')
            return False
        raise ValueError('Wire records already exist. Add/reconcile new records individually instead of reseeding.')
    legacy_rows = list(csv.DictReader(legacy.decode('utf-8-sig').splitlines()))
    plan = [('J2', 'X', 'TB40', '2', 0), ('TB40', '1', 'FH1', 'P1.A', 1),
            ('J2', 'Y', 'TB41', '2', 4), ('TB41', '1', 'FH1', 'P2.A', 5),
            ('J2', 'Z', 'TB42', '2', 8), ('TB42', '1', 'FH1', 'P3.A', 9)]
    updates = {}
    migration = []
    for number, (fr, fp, tr, tp, old_index) in enumerate(plan, 1):
        old = legacy_rows[old_index]
        expected_from = 'Mains Plug' if fr == 'J2' else fr
        expected_to = tr if tr.startswith('TB') else 'Fuse Holder'
        if old['FROM'] != expected_from or old['TO'] != expected_to:
            raise ValueError('The legacy schedule was reordered/edited. Reconcile its rows before seeding.')
        source_ep, target_ep = index.endpoint(fr, fp), index.endpoint(tr, tp)
        record = {'schema': 1, 'from_symbol_uuid': source_ep['symbol_uuid'], 'from_pin': fp, 'to': target_ep, 'section': '01 Incoming phases',
                  'kind': 'panel_cable_core' if fr == 'J2' else 'wire', 'review': 'pending',
                  'awg': old['AWG'], 'term1': old['TERM 1'], 'term2': old['TERM 2'],
                  'length': {'mode': 'auto', 'slack_mm': '200', 'round_mm': '50',
                             'minimum_mm': old['LENGTH']},
                  'migration_note': 'The legacy cut estimate is retained as a minimum until this section is reviewed.'}
        if fr == 'J2':
            record['route_from'] = index.endpoint('J3', fp)
            record['migration_note'] += ' Length covers the panel tail; external cable allowance remains in the BOM.'
        wid = f'W{number:03}'
        updates.setdefault(source_ep['symbol_uuid'], {})['Wire.' + wid] = json.dumps(record, separators=(',', ':'))
        migration.append({'id': wid, 'legacy_row': old_index + 2, 'legacy_values': old})
    for ref, name in [('J2', 'Mains Plug'), ('FH1', 'Fuse Holder')]:
        s = index.by_ref[ref][0]
        if prop(s, 'WireName') is None:
            updates.setdefault(one(s, 'uuid')[1], {})['WireName'] = name
    for pin, label in [('X', 'L1'), ('Y', 'L2'), ('Z', 'L3'), ('G', 'PE')]:
        if prop(index.by_ref['J2'][0], 'WirePin.' + pin) is None:
            updates.setdefault(mi, {})['WirePin.' + pin] = label
    text = change_fields(text, updates)
    candidate = Schematic(text)
    with tempfile.TemporaryDirectory(prefix='incoming-wire-proof-') as work:
        snapshot = Path(work) / sch_path.name
        snapshot.write_text(text)
        _, pin_nets = export_netlist(snapshot, work)
        rows, details = make_rows(candidate, Panel(board.decode('utf-8')), candidate.records(), pin_nets)
    if len(rows) != 6:
        raise ValueError('Expected six incoming phase wire records.')
    for name in ['lib_symbols', 'label', 'global_label', 'junction', 'no_connect']:
        if nodes(original, name) != nodes(parse(text), name):
            raise ValueError(f'Unexpected change outside the incoming section: {name}')
    out = PROJECT / 'reviews/wiring_migration'
    out.mkdir(parents=True, exist_ok=True)
    atomic_write(out / 'schematic_before_setup.kicad_sch', source)
    atomic_write(out / 'legacy_schedule_before_setup.csv', legacy)
    atomic_write(out / 'setup.json', (json.dumps({'legacy_rows': len(legacy_rows), 'migrated_rows': 6,
                 'remaining_legacy_rows': len(legacy_rows) - 6, 'records': migration,
                 'source_sha256': digest(source), 'pcb_sha256': digest(board),
                 'phase_through_wires_restored': len(extra), 'generated_preview': details}, indent=2) + '\n').encode())
    if apply:
        if digest(pcb_path.read_bytes()) != digest(board) or digest(legacy_path.read_bytes()) != digest(legacy):
            raise ValueError('The PCB or legacy schedule changed; retry from the current saved files.')
        atomic_write(sch_path, text.encode(), expected=digest(source))
    else:
        atomic_write(out / 'schematic_with_incoming_records.kicad_sch', text.encode())
    print(('Saved' if apply else 'Staged') + ' six schematic wire records; legacy CSV and PCB preserved.')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    parser.add_argument('--pcb', type=Path, default=DEFAULT_PCB)
    parser.add_argument('--legacy', type=Path, default=PROJECT / 'Wire_schedule.csv')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        seed(args.schematic, args.pcb, args.legacy, args.apply)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'Incoming phase setup failed: {error}\n')


if __name__ == '__main__':
    main()
