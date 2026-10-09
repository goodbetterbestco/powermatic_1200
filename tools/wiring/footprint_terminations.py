#!/usr/bin/env python3
"""Stage/review footprint-owned terminations without changing physical layout."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import tempfile
import uuid

from generate import DEFAULT_PCB, DEFAULT_SCH, PROJECT
from model import Schematic, change_fields, digest, export_netlist
from source import children, key, nodes, one, parse, prop, replace
from terminations import legacy_endpoint, pin_numbers

PREFIX = 'Termination.'
EXTERNAL = {'M1', 'J2', 'S1', 'J6'}
BLOCK_POLICY = 'One conductor per clamp: ferrule; two conductors per clamp: twin ferrule. Size for the actual conductor(s).'
BLOCK_TERMINATION = 'Ferrule or twin ferrule as required'


def field(name, value, at):
    return (f'(property {json.dumps(name)} {json.dumps(value, ensure_ascii=False)} '
            f'(at {at[1]} {at[2]} 0) (layer "F.Fab") (hide yes) '
            '(effects (font (size 1 1) (thickness 0.15))))')


def patch_footprints(text, updates):
    edits, seen = [], set()
    for a, b, raw in children(text):
        if key(raw) != 'footprint':
            continue
        f = parse(raw)
        fid = one(f, 'uuid')[1]
        if fid not in updates:
            continue
        seen.add(fid)
        pending = dict(updates[fid])
        sub = []
        for aa, bb, child in children(raw):
            if key(child) == 'property':
                p = parse(child)
                if p[1] in pending:
                    sub.append((aa, bb, child.replace(json.dumps(p[2], ensure_ascii=False),
                                                     json.dumps(pending.pop(p[1]), ensure_ascii=False), 1)))
        out = replace(raw, sub)
        end = out.rfind(')')
        start = end
        while start and out[start - 1] in ' \t':
            start -= 1
        extra = '\n'.join(field(n, v, one(f, 'at')) for n, v in pending.items())
        if extra:
            out = out[:start] + extra + '\n' + out[start:]
        edits.append((a, b, out))
    if seen != set(updates):
        raise ValueError('A footprint changed before its terminations could be staged.')
    return replace(text, edits)


def external_footprint(symbol, schematic):
    ref = prop(symbol, 'Reference')
    at = ['at', '0', '0']
    sid = one(symbol, 'uuid')[1]
    data = {'Reference': ref, 'Value': prop(symbol, 'Value') or ref,
            'Part Name': prop(symbol, 'Part Name') or ref,
            'Wire.MetadataOnly': 'yes',
            'Wire.TerminalPins': json.dumps(pin_numbers(schematic, symbol), separators=(',', ':'))}
    return (f'(footprint "{ref}_Termination_Metadata" (layer "F.Cu") '
            f'(uuid "{uuid.uuid4()}") (at 0 0) (path "/{sid}") '
            '(attr board_only exclude_from_pos_files exclude_from_bom allow_missing_courtyard)\n'
            + '\n'.join(field(n, v, at) for n, v in data.items()) + '\n)')


def stage(schematic_text, pcb_text, legacy_path):
    schematic = Schematic(schematic_text)
    tree = parse(pcb_text)
    footprints = nodes(tree, 'footprint')
    by_ref = {prop(f, 'Reference'): f for f in footprints if prop(f, 'Reference') != 'REF**'}
    added = []
    for symbol in schematic.symbols:
        ref = prop(symbol, 'Reference')
        if ref in EXTERNAL and ref not in by_ref:
            raw = external_footprint(symbol, schematic)
            added.append(raw)
            by_ref[ref] = parse(raw)
    if added:
        end = pcb_text.rfind(')')
        pcb_text = pcb_text[:end] + '\n' + '\n'.join(added) + '\n' + pcb_text[end:]
    footprints = nodes(parse(pcb_text), 'footprint')
    legacy = defaultdict(set)
    with legacy_path.open(newline='', encoding='utf-8-sig') as stream:
        for row in csv.DictReader(stream):
            for side, col in [('1', 'FROM'), ('2', 'TO')]:
                ref, pin = legacy_endpoint(row[col], row[col + ' PIN'])
                if row['TERM ' + side].strip() not in ['', '-']:
                    legacy[ref, pin].add(row['TERM ' + side].strip())
    updates, sch_updates, provenance = {}, {}, []
    pin_nets = None
    for f in footprints:
        ref, fid = prop(f, 'Reference'), one(f, 'uuid')[1]
        terminal_block = any(name in f[1] for name in ['KN-T12GRY-25', 'KN-G12SP-10'])
        if terminal_block:
            updates.setdefault(fid, {})['Wire.TerminationPolicy'] = BLOCK_POLICY
        pads = {p[1] for p in nodes(f, 'pad') if p[1]}
        metadata_only = prop(f, 'Wire.MetadataOnly') == 'yes'
        pins = set(json.loads(prop(f, 'Wire.TerminalPins'))) if metadata_only else pads
        symbols = schematic.by_ref.get(ref, [])
        if symbols:
            linked = one(f, 'path')
            if linked is None or linked[1].split('/')[-1] not in {one(s, 'uuid')[1] for s in symbols}:
                if (len(symbols) != 1 or not prop(f, 'MPN')
                        or prop(f, 'MPN') != prop(symbols[0], 'MPN')
                        or pins != set(pin_numbers(schematic, symbols[0]))):
                    raise ValueError(f'{ref}: footprint/symbol identity differs; do not guess ownership.')
                if pin_nets is None:
                    with tempfile.TemporaryDirectory(prefix='termination-identity-') as work:
                        snapshot = Path(work) / DEFAULT_SCH.name
                        snapshot.write_text(schematic_text)
                        _, pin_nets = export_netlist(snapshot, work)
                for pad in nodes(f, 'pad'):
                    net = one(pad, 'net')
                    if net is None or net[-1] != pin_nets.get((ref, pad[1])):
                        raise ValueError(f'{ref}.{pad[1]}: stale UUID and differing nets; reconcile before migration.')
        old = {p[1][len(PREFIX):]: p[2] for s in symbols for p in nodes(s, 'property')
               if p[1].startswith(PREFIX)}
        existing = {p[1][len(PREFIX):]: p[2] for p in nodes(f, 'property') if p[1].startswith(PREFIX)}
        if set(old) - pins:
            raise ValueError(f'{ref}: symbol termination pins absent from footprint: {sorted(set(old) - pins)}')
        for pin in sorted(pins):
            legacy_pin = {'1': 'TOP', '2': 'BOT'}.get(pin, pin) if 'KN-G12SP' in f[1] else pin
            source = 'Existing footprint field'
            if pin in existing:
                value = existing[pin]
                if pin in old and value != old[pin]:
                    raise ValueError(f'{ref}.{pin}: footprint and symbol termination selections conflict.')
            elif terminal_block and pin != 'PE':
                value, source = BLOCK_TERMINATION, 'Owner block termination capability; allocation occurs during routing'
            elif pin in old:
                value, source = old[pin], 'Moved from existing symbol field'
            elif ref in ['H1', 'H2']:
                value, source = 'Ferrule 18 AWG; L=TBD mm', 'Existing indicator wiring selection'
            elif 'BottomWall' in f[1] and 'Cable Gland' in (prop(f, 'Part Name') or ''):
                value, source = 'N/A — cable pass-through; no electrical termination', 'Gland routing marker'
            elif 'HMX1-MI' in f[1]:
                value, source = 'N/A — mechanical interlock; no wire termination', 'Mechanical interlock marker'
            elif 'KN-G12SP' in f[1] and pin == 'PE':
                value, source = 'Conductive DIN-rail foot (retained)', 'Ground terminal rail contact'
            elif legacy[ref, legacy_pin]:
                choices = legacy[ref, legacy_pin]
                if len(choices) != 1:
                    raise ValueError(f'{ref}.{pin}: conflicting legacy termination descriptions {sorted(choices)}')
                value, source = next(iter(choices)), 'Legacy schedule draft, pending wiring reconciliation'
                if ref == 'TB52' and pin == '2':
                    value = 'Ferrule 12 AWG; L=TBD mm'
                    source = 'Owner motor-conduit PE correction to 12 AWG'
            else:
                value, source = 'Termination type TBD; conductor size TBD', 'No recorded selection; left explicit'
            updates.setdefault(fid, {})[PREFIX + pin] = value
            provenance.append({'reference': ref, 'footprint_uuid': fid, 'pin': pin,
                               'termination': value, 'source': source})
        for symbol in symbols:
            sid = one(symbol, 'uuid')[1]
            for p in nodes(symbol, 'property'):
                if p[1].startswith(PREFIX):
                    sch_updates.setdefault(sid, {})[p[1]] = None
    # Mechanical termination descriptions belong to the existing mechanical footprint.
    enclosures = [f for f in footprints if 'EN4SD20208GY' in f[1]]
    rails = sorted([f for f in footprints if 'DN-R35S1_' in f[1]], key=lambda f: float(one(f, 'at')[2]))
    mechanical = []
    if len(enclosures) == 1:
        mechanical += [(enclosures[0], 'Enclosure', 'STUD', 'STUD'),
                       (enclosures[0], 'Enclosure Door', 'STUD', 'DOOR_STUD'),
                       (enclosures[0], 'Backplate', 'STUD', 'BACKPLATE_STUD')]
    if len(rails) == 2:
        mechanical += [(rails[0], 'Din Rail Top', 'LUG', 'LUG'), (rails[1], 'Din Rail Bottom', 'LUG', 'LUG')]
    for f, name, legacy_pin, pin in mechanical:
        choices = legacy[name, legacy_pin]
        if not choices:
            continue
        if len(choices) != 1:
            raise ValueError(f'{name}: conflicting legacy mechanical terminations')
        value = prop(f, PREFIX + pin) or next(iter(choices))
        fid = one(f, 'uuid')[1]
        updates.setdefault(fid, {})[PREFIX + pin] = value
        provenance.append({'reference': name, 'footprint_uuid': fid, 'pin': pin,
                           'termination': value, 'source': 'Legacy mechanical bond draft; topology remains pending'})
    # Physical wire records no longer own duplicate TERM 1/TERM 2 values.
    for s in schematic.symbols:
        sid = one(s, 'uuid')[1]
        for p in nodes(s, 'property'):
            if p[1].startswith('Wire.W') and p[1][6:].isdigit():
                record = json.loads(p[2])
                record.pop('term1', None)
                record.pop('term2', None)
                sch_updates.setdefault(sid, {})[p[1]] = json.dumps(record, separators=(',', ':'))
    return change_fields(schematic_text, sch_updates), patch_footprints(pcb_text, updates), provenance


def review(pcb_text):
    entries, owners, missing = [], set(), []
    for f in nodes(parse(pcb_text), 'footprint'):
        fid, ref = one(f, 'uuid')[1], prop(f, 'Reference')
        pins = {p[1] for p in nodes(f, 'pad') if p[1]}
        if prop(f, 'Wire.MetadataOnly') == 'yes':
            pins = set(json.loads(prop(f, 'Wire.TerminalPins')))
        fields = {p[1][len(PREFIX):]: p[2] for p in nodes(f, 'property') if p[1].startswith(PREFIX)}
        for pin in pins:
            if not fields.get(pin, '').strip():
                missing.append(f'{ref}.{pin}')
        for pin, value in fields.items():
            if not value.strip():
                missing.append(f'{ref}.{pin}')
            entries.append({'reference': ref, 'footprint_uuid': fid, 'pin': pin,
                            'field': PREFIX + pin, 'termination': value})
            owners.add(fid)
    if missing:
        raise ValueError('Missing footprint termination fields: ' + ', '.join(sorted(set(missing))))
    return {'pcb_sha256': digest(pcb_text.encode()), 'footprints': len(owners),
            'pin_fields': len(entries), 'entries': entries,
            'description_counts': dict(Counter(e['termination'] for e in entries))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    parser.add_argument('--pcb', type=Path, default=DEFAULT_PCB)
    parser.add_argument('--legacy', type=Path, default=PROJECT / 'Wire_schedule.csv')
    parser.add_argument('--stage-dir', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        schematic_text, pcb_text = args.schematic.read_text(), args.pcb.read_text()
        if args.stage_dir:
            if args.stage_dir.resolve() in [args.schematic.parent.resolve(), args.pcb.parent.resolve()]:
                raise ValueError('Staging must use a separate directory.')
            schematic_text, pcb_text, provenance = stage(schematic_text, pcb_text, args.legacy)
            args.stage_dir.mkdir(parents=True, exist_ok=True)
            (args.stage_dir / args.schematic.name).write_text(schematic_text)
            (args.stage_dir / args.pcb.name).write_text(pcb_text)
            (args.stage_dir / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
        report = review(pcb_text)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + '\n')
        print(f'Reviewed {report["pin_fields"]} termination fields on {report["footprints"]} footprints.')
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'Footprint terminations failed: {error}\n')


if __name__ == '__main__':
    main()
