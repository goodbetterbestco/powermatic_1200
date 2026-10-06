#!/usr/bin/env python3
"""Edit wire records in the saved schematic; endpoints use persistent symbol UUIDs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
import tempfile

from model import Schematic, atomic_write, change_fields, digest, export_netlist, prop
from generate import DEFAULT_SCH


def endpoint(schematic, text):
    if '.' not in text:
        raise ValueError('Use an endpoint such as TB40.2 or FH1.P1.A.')
    ref, pin = text.split('.', 1)
    return schematic.endpoint(ref, pin)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    add = sub.add_parser('add')
    add.add_argument('id')
    add.add_argument('--from', dest='from_text', required=True)
    add.add_argument('--to', dest='to_text', required=True)
    add.add_argument('--section', required=True)
    add.add_argument('--awg', default='18')
    add.add_argument('--term1', default='TBD')
    add.add_argument('--term2', default='TBD')
    add.add_argument('--kind', default='wire')
    add.add_argument('--route-from')
    add.add_argument('--route-to')
    add.add_argument('--length', help='manual length in mm; otherwise automatic')
    edit = sub.add_parser('set')
    edit.add_argument('id')
    edit.add_argument('--from', dest='from_text')
    edit.add_argument('--to', dest='to_text')
    edit.add_argument('--route-from', help='physical endpoint such as J3.X, or direct to remove an override')
    edit.add_argument('--route-to', help='physical endpoint, or direct to remove an override')
    edit.add_argument('--awg')
    edit.add_argument('--term1')
    edit.add_argument('--term2')
    edit.add_argument('--length', help='manual mm, or auto')
    edit.add_argument('--review', choices=['pending', 'reviewed'])
    edit.add_argument('--kind')
    args = parser.parse_args()
    try:
        raw = args.schematic.read_bytes()
        sch = Schematic(raw.decode('utf-8'))
        existing = {r['id']: r for r in sch.records()}
        if args.command == 'list':
            for r in existing.values():
                _, fr, fp = sch.resolve(r['from_endpoint'])
                _, tr, tp = sch.resolve(r['to'])
                print(f"{r['id']}  {r['section']}  {fr}.{fp} -> {tr}.{tp}  {r.get('review', 'pending')}")
            return
        if not re.fullmatch(r'W\d+', args.id):
            raise ValueError('Wire IDs must be W followed by digits, such as W001.')
        if args.command == 'add':
            if args.id in existing:
                raise ValueError(f'{args.id} already exists; use set.')
            source = endpoint(sch, args.from_text)
            owner = source['symbol_uuid']
            record = {'schema': 1, 'from_symbol_uuid': owner, 'from_pin': source['pin'], 'to': endpoint(sch, args.to_text),
                      'section': args.section, 'awg': args.awg, 'term1': args.term1, 'term2': args.term2,
                      'kind': args.kind, 'review': 'pending',
                      'length': {'mode': 'manual', 'mm': args.length} if args.length else {'mode': 'auto'}}
            if args.route_from:
                record['route_from'] = endpoint(sch, args.route_from)
            if args.route_to:
                record['route_to'] = endpoint(sch, args.route_to)
        else:
            if args.id not in existing:
                raise ValueError(f'Unknown wire {args.id}')
            record = dict(existing[args.id])
            owner = record.pop('from_endpoint')['symbol_uuid']
            old_owner = owner
            record.pop('id')
            if args.from_text:
                source = endpoint(sch, args.from_text)
                owner = source['symbol_uuid']
                record['from_pin'] = source['pin']
            for field in ['awg', 'term1', 'term2', 'review', 'kind']:
                value = getattr(args, field)
                if value is not None:
                    record[field] = value
            if args.to_text:
                record['to'] = endpoint(sch, args.to_text)
            if args.length:
                record['length'] = {'mode': 'auto'} if args.length == 'auto' else {'mode': 'manual', 'mm': args.length}
            for field in ['route_from', 'route_to']:
                value = getattr(args, field)
                if value == 'direct':
                    record.pop(field, None)
                elif value:
                    record[field] = endpoint(sch, value)
        record['from_symbol_uuid'] = owner
        updates = {owner: {'Wire.' + args.id: json.dumps(record, separators=(',', ':'))}}
        if args.command == 'set' and old_owner != owner:
            updates[old_owner] = {'Wire.' + args.id: None}
        result = change_fields(sch.text, updates)
        candidate = Schematic(result)
        candidate.records()  # Schema and IDs must remain valid before any save.
        with tempfile.TemporaryDirectory(prefix='wire-record-check-') as work:
            snapshot = Path(work) / args.schematic.name
            snapshot.write_text(result)
            _, pin_nets = export_netlist(snapshot, work)
            _, fr, fp = candidate.resolve({'symbol_uuid': owner, 'pin': record['from_pin']})
            _, tr, tp = candidate.resolve(record['to'])
            if pin_nets.get((fr, fp)) != pin_nets.get((tr, tp)) or not pin_nets.get((fr, fp)):
                raise ValueError('The chosen wire endpoints are not electrically connected.')
        atomic_write(args.schematic, result.encode(), expected=digest(raw))
        print(f'Saved {args.id} in the schematic. Regenerate the review; reload KiCad before saving over external edits.')
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f'Wire record update failed: {error}\n')


if __name__ == '__main__':
    main()
