#!/usr/bin/env python3
"""Stage TOP/BOT feedthrough pins without changing their physical PCB placement."""
import argparse
import json
import math
from pathlib import Path
import tempfile

from model import Schematic, atomic_write, digest, export_netlist
from source import parse, nodes, one, prop, children, key, replace
from generate import PROJECT, DEFAULT_SCH, DEFAULT_PCB

PARTS = PROJECT.parents[1] / '_parts'


def position(local, at):
    x, y = map(float, local[1:3]); t = math.radians(float(at[3]))
    return round(float(at[1]) + x * math.cos(t) - y * math.sin(t), 5), round(float(at[2]) - x * math.sin(t) - y * math.cos(t), 5)


def pins(symbol):
    return {one(p, 'number')[1]: one(p, 'at') for b in nodes(symbol, 'symbol') for p in nodes(b, 'pin')}


def stage():
    sch_raw, pcb_raw = DEFAULT_SCH.read_bytes(), DEFAULT_PCB.read_bytes()
    text = sch_raw.decode(); tree = parse(text)
    library = (PARTS / 'symbols/Controls.kicad_sym').read_text()
    fresh_raw = next(raw for _, _, raw in children(library) if key(raw) == 'symbol' and parse(raw)[1] == 'KN-T12GRY-25')
    fresh = parse(fresh_raw)
    if set(pins(fresh)) != {'TOP', 'BOT'}:
        raise ValueError('The chosen shared symbol must have TOP/BOT pin numbers.')
    caches = {n[1]: n for n in nodes(one(tree, 'lib_symbols'), 'symbol')}
    converted, movements, edits, terminal_ids, cache_names = {}, {}, [], set(), set()
    for symbol in nodes(tree, 'symbol'):
        override = one(symbol, 'lib_name')
        libid = override[1] if override else one(symbol, 'lib_id')[1]
        if prop(symbol, 'Value') != 'KN-T12GRY-25' or libid not in caches:
            continue
        old = caches[libid]
        terminal_ids.add(one(symbol, 'uuid')[1])
        if set(pins(old)) != {'1', '2'}:
            continue
        sid = one(symbol, 'uuid')[1]
        converted[sid] = prop(symbol, 'Reference')
        cache_names.add(libid)
        for before, after in [('1', 'TOP'), ('2', 'BOT')]:
            a, b = position(pins(old)[before], one(symbol, 'at')), position(pins(fresh)[after], one(symbol, 'at'))
            if a in movements and movements[a] != b:
                raise ValueError('Two terminal anchors overlap; review that group manually.')
            movements[a] = b
    # The first setup snapshot identifies original owners, not later symbol copies.
    originals, original_parts, relinked = {}, {}, []
    snapshot = PROJECT / 'reviews/wiring_migration/schematic_with_incoming_records.kicad_sch'
    if snapshot.exists():
        for s in nodes(parse(snapshot.read_text()), 'symbol'):
            for p in nodes(s, 'property'):
                if p[1].startswith('Wire.W'):
                    originals[p[1]] = one(s, 'uuid')[1]
                    original_parts[p[1]] = (prop(s, 'Reference'), one(s, 'lib_id')[1], prop(s, 'Value'))
    def move_child(child):
        p = parse(child)
        values = tuple(map(float, p[1:3]))
        target = movements.get(values)
        return f'({p[0]} {target[0]} {target[1]}' + (' ' + ' '.join(p[3:]) if len(p) > 3 else '') + ')' if target else child
    for a, b, raw in children(text):
        kind = key(raw)
        if kind == 'lib_symbols':
            sub = []
            for aa, bb, child in children(raw):
                if key(child) == 'symbol' and parse(child)[1] in caches:
                    name = parse(child)[1]
                    if name in cache_names:
                        base = name.split(':')[-1]
                        replacement = fresh_raw.replace('(symbol "KN-T12GRY-25_', '(symbol "' + base + '_')
                        replacement = replacement.replace('(symbol "KN-T12GRY-25"', '(symbol ' + json.dumps(name), 1)
                        sub.append((aa, bb, replacement))
            edits.append((a, b, replace(raw, sub)))
        elif kind == 'wire':
            sub = []
            for aa, bb, child in children(raw):
                if key(child) == 'pts':
                    points = [(x, y, move_child(pt)) for x, y, pt in children(child) if key(pt) == 'xy']
                    sub.append((aa, bb, replace(child, points)))
            edits.append((a, b, replace(raw, sub)))
        elif kind in ['junction', 'label', 'global_label', 'no_connect']:
            sub = [(aa, bb, move_child(child)) for aa, bb, child in children(raw) if key(child) == 'at']
            edits.append((a, b, replace(raw, sub)))
        elif kind == 'symbol':
            s = parse(raw); sid = one(s, 'uuid')[1]; sub = []
            for aa, bb, child in children(raw):
                if key(child) == 'pin' and sid in converted:
                    value = parse(child)[1]
                    if value in ['1', '2']:
                        sub.append((aa, bb, child.replace(json.dumps(value), json.dumps({'1': 'TOP', '2': 'BOT'}[value]), 1)))
                elif key(child) == 'property' and parse(child)[1].startswith('Wire.W'):
                    field = parse(child); record = json.loads(field[2])
                    record['from_symbol_uuid'] = record.get('from_symbol_uuid', originals.get(field[1], sid))
                    live_ids = {one(n, 'uuid')[1] for n in nodes(tree, 'symbol')}
                    same_part = original_parts.get(field[1]) == (prop(s, 'Reference'), one(s, 'lib_id')[1], prop(s, 'Value'))
                    if record['from_symbol_uuid'] not in live_ids and same_part:
                        relinked.append({'id': field[1], 'old_owner': record['from_symbol_uuid'], 'new_owner': sid})
                        record['from_symbol_uuid'] = sid
                    if record['from_symbol_uuid'] in terminal_ids and record.get('from_pin') in ['1', '2']:
                        record['from_pin'] = {'1': 'TOP', '2': 'BOT'}[record['from_pin']]
                    for name in ['to', 'route_from', 'route_to']:
                        ep = record.get(name, {})
                        if ep.get('symbol_uuid') in terminal_ids and ep.get('pin') in ['1', '2']:
                            ep['pin'] = {'1': 'TOP', '2': 'BOT'}[ep['pin']]
                    value = json.dumps(record, separators=(',', ':'))
                    sub.append((aa, bb, child.replace(json.dumps(field[2], ensure_ascii=False), json.dumps(value), 1)))
            edits.append((a, b, replace(raw, sub)))
    new_sch = replace(text, edits)
    board_text = pcb_raw.decode(); board_edits = []
    for a, b, raw in children(board_text):
        if key(raw) != 'footprint' or prop(parse(raw), 'Value') != 'KN-T12GRY-25':
            continue
        sub = []
        for aa, bb, child in children(raw):
            if key(child) == 'pad' and parse(child)[1] in ['1', '2']:
                old = parse(child)[1]
                sub.append((aa, bb, child.replace(json.dumps(old), json.dumps({'1': 'TOP', '2': 'BOT'}[old]), 1)))
        board_edits.append((a, b, replace(raw, sub)))
    new_pcb = replace(board_text, board_edits)
    footprint_path = PARTS / 'footprints/Controls.pretty/KN-T12GRY-25_Front.kicad_mod'
    footprint = footprint_path.read_text()
    new_footprint = footprint.replace('(pad "1" ', '(pad "TOP" ').replace('(pad "2" ', '(pad "BOT" ')
    work = PROJECT / 'reviews/wiring_migration/top_bot_transition'
    work.mkdir(parents=True, exist_ok=True)
    for filename, content in [('before.kicad_sch', text), ('after.kicad_sch', new_sch),
                              ('before.kicad_pcb', board_text), ('after.kicad_pcb', new_pcb),
                              ('KN-T12GRY-25_Front.kicad_mod', new_footprint)]:
        atomic_write(work / filename, content.encode())
    # Prove endpoint net groups are identical after renaming 1/2 to TOP/BOT.
    def native(content, destination):
        sc = Schematic(content, allow_in_progress=True)
        export, aliases = sc.export_snapshot()
        p = Path(destination) / 'test.kicad_sch'; p.write_text(export)
        nets, _ = export_netlist(p, destination)
        return {frozenset(p for p in group) for group in nets.values()}
    with tempfile.TemporaryDirectory() as w1, tempfile.TemporaryDirectory() as w2:
        old_groups = native(text, w1); new_groups = native(new_sch, w2)
    refs = set(converted.values())
    expected = {frozenset((ref, {'1': 'TOP', '2': 'BOT'}.get(pin, pin) if ref in refs else pin)
                          for ref, pin in group) for group in old_groups}
    if expected != new_groups:
        raise ValueError('TOP/BOT transition changes electrical connections; staged files were not applied.')
    report = {'source_sha256': digest(sch_raw), 'pcb_sha256': digest(pcb_raw),
              'footprint_sha256': digest(footprint.encode()), 'converted_symbols': converted,
              'converted_footprints': len(board_edits), 'electrical_connections_preserved': True,
              'pcb_positions_and_graphics_preserved': True, 'relinked_same_named_replacements': relinked}
    atomic_write(work / 'transition.json', (json.dumps(report, indent=2) + '\n').encode())
    print(f'Staged {len(converted)} symbol updates and {len(board_edits)} TOP/BOT footprints; native connections preserved.')
    return work


if __name__ == '__main__':
    try:
        stage()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit('Terminal transition failed: ' + str(error))
