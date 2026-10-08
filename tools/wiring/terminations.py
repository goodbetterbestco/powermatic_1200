#!/usr/bin/env python3
"""Populate or review one custom Termination.<pin> symbol field per physical pin."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import re

from generate import DEFAULT_SCH, PROJECT
from model import Schematic, change_fields, digest
from source import nodes, one, prop

PREFIX = 'Termination.'
ALIASES = {
    'Mains Plug': 'J2', 'DC Supply': 'PS1', '24V Breaker': 'Q1',
    'Circuit Breaker': 'Q1', 'Fuse Holder': 'FH1', 'Disconnect': 'SW1',
    'Coil Enable Relay': 'K3', 'Indicator Lamp': 'H1', 'Button Station': 'S2',
    'Drum Switch': 'S3', 'M12 Socket': 'J1', 'Motor': 'M1',
    'Overload OL1': 'OL4', 'Overload OL2': 'OL6',
}


def legacy_endpoint(name, pin):
    ref = ALIASES.get(name, name.removeprefix('Contactor '))
    pin = pin.strip()
    first = pin.split()[0]
    if ref == 'J2':
        return ref, {'L1': 'X', 'L2': 'Y', 'L3': 'Z', 'PE': 'G'}.get(first, first)
    if ref.startswith('K') and pin.startswith('COIL '):
        words = pin.split()
        return ref, words[1] + '.' + words[2] if ref != 'K3' else words[1]
    if ref.startswith('K'):
        match = re.search(r'\((\d+)\)', pin) or re.match(r'(?:NO|NC)(\d+)', pin)
        if match:
            return ref, match[1]
    if ref == 'S3':
        first = re.sub(r'^(\d+)([UL])$', r'\1.\2', first)
    if ref == 'S2':
        first = {'L1': '2T', 'R2': '1T', 'L2': '2B', 'R1': '1B',
                 'L3': '4T', 'R4': '3T', 'L4': '4B', 'R3': '3B',
                 'L5': '6T', 'R5': '5T'}.get(first, first)
    return ref, first


def pin_numbers(schematic, symbol):
    library = schematic.library_for(symbol)
    unit = one(symbol, 'unit')[1]
    result = set()
    for body in nodes(library, 'symbol'):
        suffix = body[1].rsplit('_', 2)
        if len(suffix) == 3 and suffix[-2].isdigit() and suffix[-2] not in ['0', unit]:
            continue
        result.update(one(p, 'number')[1] for p in nodes(body, 'pin'))
    return sorted(result)


def regauge(description, awg):
    return re.sub(r'\b\d+\s*AWG\b', f'{awg} AWG', description)


def records(schematic, schedule):
    by_pin, profiles = defaultdict(set), defaultdict(set)
    with schedule.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    for line, row in enumerate(rows, 2):
        for side, endpoint in [('1', 'FROM'), ('2', 'TO')]:
            ref, pin = legacy_endpoint(row[endpoint], row[endpoint + ' PIN'])
            if ref not in schematic.by_ref:
                continue  # PCB-only clamps/studs are not schematic symbol pins.
            term = row['TERM ' + side].strip()
            by_pin[ref, pin].add((term, line, side))
            if term.startswith('Ferrule '):
                profiles[prop(schematic.by_ref[ref][0], 'Value')].add(term)
    for record in schematic.records():
        ref = prop(schematic.by_uuid[record['from_endpoint']['symbol_uuid']], 'Reference')
        by_pin[ref, record['from_pin']] = {(record['term1'], record['id'], '1')}
        # The existing three destinations are deleted symbol UUIDs. Never bind
        # them to a guessed PCB-only clamp or another same-named symbol.
    return by_pin, profiles


def populate(text, schedule):
    schematic = Schematic(text)
    by_pin, profiles = records(schematic, schedule)
    updates, provenance = {}, []
    for symbol in schematic.symbols:
        ref = prop(symbol, 'Reference')
        if ref.startswith('#'):
            continue
        sid = one(symbol, 'uuid')[1]
        size_field = prop(symbol, 'Wire.Sizes')
        sizes = {e['pin']: e for e in json.loads(size_field)['entries']} if size_field else {}
        for pin in pin_numbers(schematic, symbol):
            field = PREFIX + pin
            existing = prop(symbol, field)
            size = sizes.get(pin)
            scope = size['scope'] if size else None
            awg = size.get('awg') if size else None
            raw = sorted(by_pin.get((ref, pin), set()), key=lambda item: str(item[1]))
            source = []
            if existing is not None:
                value, source = existing, ['Existing custom symbol field']
            elif size is None:
                value = 'N/A — unused pin'
                source = ['Saved connected-pin inventory']
            elif scope == 'retained_link':
                value = 'Retained jumper'
                source = ['Saved connection classification; jumpers are separate from wire']
            elif scope == 'direct_mount':
                value = 'N/A — direct-mounted connection'
                source = ['Saved connection classification']
            elif scope == 'suppressor_lead':
                value = 'Supplied fork-ended lead (retained)'
                source = ['Existing Controls:HMX1-SSVRC-DC part description']
            elif scope == 'connector_interface':
                value = 'M12 mating contact (retained)'
                source = ['Saved connection classification']
            elif scope == 'estop_assembly':
                value = 'Supplied assembly connection (retained)'
                source = ['Saved connection classification']
            elif scope == 'factory_pigtail':
                value = f'Factory pigtail, {awg} AWG (retained)'
                source = ['Saved factory-lead declaration']
            elif ref == 'M1':
                value = f'Wire-splice connector, {awg} AWG'
                source = ['Current motor-end Wago plan in WIRING_STANDARD.md',
                          *[f'Legacy schedule row {line}, TERM {side}: {term}'
                            for term, line, side in raw]]
            elif raw:
                choices = {regauge(term, awg) for term, line, side in raw if term != '-'}
                if len(choices) != 1:
                    raise ValueError(f'{ref}.{pin}: conflicting existing termination records {choices}')
                value = choices.pop()
                if value == 'remote terminal TBD':
                    value = f'Remote terminal TBD; {awg} AWG'
                elif value == 'plug clamp':
                    value = f'Plug clamp, {awg} AWG'
                source = [f'Legacy schedule row {line}, TERM {side}: {term}'
                          for term, line, side in raw]
            else:
                profile = profiles.get(prop(symbol, 'Value'), set())
                if not profile:
                    value = f'Termination type TBD; {awg} AWG'
                    source = ['No termination description in the existing records']
                else:
                    descriptions = {regauge(term, awg) for term in profile}
                    if len(descriptions) != 1:
                        raise ValueError(f'{ref}.{pin}: per-part termination profile conflicts')
                    value = descriptions.pop()
                    source = ['Ferrule description already recorded on this part type; draft inheritance']
            updates.setdefault(sid, {})[field] = value
            provenance.append({'reference': ref, 'pin': pin, 'symbol_uuid': sid,
                               'field': field, 'termination': value, 'scope': scope,
                               'awg': awg, 'source': source})
    return change_fields(text, updates), provenance


def review(text):
    schematic = Schematic(text)
    entries = []
    for symbol in schematic.symbols:
        ref = prop(symbol, 'Reference')
        if ref.startswith('#'):
            continue
        pins = pin_numbers(schematic, symbol)
        fields = {p[1][len(PREFIX):]: p[2] for p in nodes(symbol, 'property')
                  if p[1].startswith(PREFIX)}
        if set(fields) != set(pins):
            raise ValueError(f'{ref}: termination fields do not match its actual pin inventory')
        for pin in pins:
            if not fields[pin].strip():
                raise ValueError(f'{ref}.{pin}: empty termination field')
            entries.append({'reference': ref, 'pin': pin, 'field': PREFIX + pin,
                            'termination': fields[pin]})
    return {'source_sha256': digest(text.encode()), 'pin_fields': len(entries),
            'symbols': len({e['reference'] for e in entries}), 'entries': entries,
            'description_counts': dict(sorted(Counter(e['termination'] for e in entries).items()))}


def markdown(report):
    lines = ['# Pin termination draft', '',
             'One custom `Termination.<pin>` field is stored on each physical schematic symbol.',
             'Descriptions come from existing records, using the current conductor AWG.',
             'Recorded TBD lengths and dimensions remain unchanged for review.', '',
             f'Fields: **{report["pin_fields"]}** on **{report["symbols"]}** symbols.', '',
             '## Description inventory', '', '| Description | Pin fields |', '|---|---:|']
    lines += [f'| {term} | {count} |' for term, count in report['description_counts'].items()]
    lines += ['', 'These are pin-field counts, not purchasing quantities. Internally common pins,',
              'retained/supplied connections and unused pins are included in the field inventory.',
              'PCB-only terminal blocks and enclosure studs have no schematic symbols and are',
              'outside this symbol-field population. No terminal allocation or wire route is inferred.',
              '', '## All pin fields', '', '| Component | Pin | Field | Termination |', '|---|---|---|---|']
    lines += [f'| {e["reference"]} | {e["pin"]} | `{e["field"]}` | {e["termination"]} |'
              for e in sorted(report['entries'], key=lambda e: (e['reference'], e['pin']))]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    parser.add_argument('--legacy', type=Path, default=PROJECT / 'Wire_schedule.csv')
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        text = args.schematic.read_text()
        if args.stage:
            if args.stage.resolve() == args.schematic.resolve():
                raise ValueError('Staging cannot overwrite the source schematic')
            text, provenance = populate(text, args.legacy)
        report = review(text)
        if args.stage:
            args.stage.parent.mkdir(parents=True, exist_ok=True)
            args.stage.write_text(text)
            args.stage.with_suffix('.termination-provenance.json').write_text(
                json.dumps({'source_sha256': report['source_sha256'],
                            'legacy_sha256': digest(args.legacy.read_bytes()),
                            'entries': provenance}, indent=2) + '\n')
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(markdown(report))
            args.report.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
        print(f'Populated/reviewed {report["pin_fields"]} pin fields on {report["symbols"]} symbols.')
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'Termination population failed: {error}\n')


if __name__ == '__main__':
    main()
