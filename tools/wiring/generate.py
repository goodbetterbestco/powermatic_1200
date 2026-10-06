#!/usr/bin/env python3
"""Generate a partial or complete wire schedule from saved schematic wire records."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request
import webbrowser

from model import HEADERS, Schematic, Panel, atomic_write, digest, export_netlist, make_rows, prop

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_SCH = PROJECT / 'kicad/powermatic_1200/powermatic_1200.kicad_sch'
DEFAULT_PCB = DEFAULT_SCH.with_suffix('.kicad_pcb')
DEFAULT_OUTPUT = PROJECT / 'reviews/wiring_generated/Wire_schedule_generated.csv'


def coverage(schematic, nets, details):
    edges = defaultdict(list)
    for detail in details:
        a = tuple(detail['from'].split('.', 1))
        b = tuple(detail['to'].split('.', 1))
        edges[detail['net']].append((a, b))
        for name in ['route_from', 'route_to']:
            if name in detail:
                edges[detail['net']].append((a if name == 'route_from' else b,
                                             tuple(detail[name].split('.', 1))))
    result = []
    for name, pins in sorted(nets.items()):
        if name.startswith('unconnected-') or len(pins) < 2:
            continue
        parent = {p: p for p in pins}
        def find(p):
            if parent[p] != p:
                parent[p] = find(parent[p])
            return parent[p]
        def join(a, b):
            if a in parent and b in parent:
                parent[find(a)] = find(b)
        # These terminal models are actual internally common feedthrough/PE blocks.
        # This does not infer bridges between different blocks or contacts in relays.
        for ref, instances in schematic.by_ref.items():
            value = prop(instances[0], 'Value')
            if value in ['KN-T12GRY-25', 'KN-G12SP-10']:
                pair = ('1', '2') if (ref, '1') in parent else ('TOP', 'BOT')
                join((ref, pair[0]), (ref, pair[1]))
                if value == 'KN-G12SP-10':
                    join((ref, pair[0]), (ref, 'PE'))
        for a, b in edges[name]:
            join(a, b)
        groups = defaultdict(list)
        for p in pins:
            groups[find(p)].append('.'.join(p))
        result.append({'net': name, 'covered': len(groups) == 1,
                       'remaining_groups': [sorted(g) for g in groups.values()]})
    return result


def generate(sch_path, pcb_path, output, section=None, check=False):
    sch_path, pcb_path, output = map(lambda p: Path(p).resolve(), [sch_path, pcb_path, output])
    if output == (PROJECT / 'Wire_schedule.csv').resolve():
        raise ValueError('The legacy schedule is preserved during migration. Use the generated review path.')
    source, board = sch_path.read_bytes(), pcb_path.read_bytes()
    schematic, panel = Schematic(source.decode('utf-8'), allow_in_progress=True), Panel(board.decode('utf-8'))
    records = schematic.records()
    if not records:
        raise ValueError('No schematic wire records exist yet; add the first reviewed section.')
    if section:
        records = [r for r in records if r.get('section') == section]
        if not records:
            raise ValueError(f'No wire records in section {section!r}.')
    with tempfile.TemporaryDirectory(prefix='powermatic-wires-') as work:
        # Export exactly the bytes used to read the records, even if the editor saves meanwhile.
        snapshot = Path(work) / sch_path.name
        export_text, unfinished = schematic.export_snapshot()
        snapshot.write_text(export_text)
        nets, pin_nets = export_netlist(snapshot, work)
        rows, details = make_rows(schematic, panel, records, pin_nets)
        for d in details:
            if any(ref in unfinished for ref, pin in nets[d['net']]):
                raise ValueError(f"{d['id']}: an unfinished symbol shares recorded net {d['net']}; annotate/reconcile it first.")
    audit = coverage(schematic, nets, details)
    report = {'schema': 1, 'source_schematic': str(sch_path), 'source_pcb': str(pcb_path),
              'schematic_sha256': digest(source), 'pcb_sha256': digest(board),
              'generated_rows': len(rows), 'omitted_records': sum(not d['exported'] for d in details),
              'sections': dict(Counter(d['section'] for d in details if d['exported'])),
              'review_states': dict(Counter(d['review'] for d in details if d['exported'])),
              'complete': all(n['covered'] for n in audit) and not unfinished, 'net_coverage': audit,
              'unfinished_symbols_outside_recorded_nets': list(unfinished.values()),
              'inherited_wire_fields_on_copied_symbols': schematic.copied_wire_fields,
              'records': details, 'csv_is_generated': True}
    if digest(sch_path.read_bytes()) != digest(source) or digest(pcb_path.read_bytes()) != digest(board):
        raise ValueError('The schematic or PCB changed during generation. Save and generate again.')
    if not check:
        stream = io.StringIO(newline='')
        csv.writer(stream, lineterminator='\r\n').writerows([HEADERS, *rows])
        atomic_write(output, stream.getvalue().encode('utf-8'))
        atomic_write(output.with_suffix('.source.json'), (json.dumps(report, indent=2) + '\n').encode())
        markdown = ['# Generated wire schedule', '',
                    'This is a generated section review. Wire records in the saved schematic are authoritative.',
                    'Only recorded assembly wires are included; unrecorded sections are not inferred from global net names.',
                    '', f'Assembly wires: **{len(rows)}**. Full-schematic coverage: **{"complete" if report["complete"] else "partial"}**.',
                    '', '## Sections', '', '| Section | Wires |', '|---|---:|']
        markdown += [f'| {name} | {count} |' for name, count in report['sections'].items()]
        markdown += ['', '## Current review', '', '| ID | From | To | AWG | Cut estimate, mm | Route, mm | State |',
                     '|---|---|---|---:|---:|---:|---|']
        for d in details:
            if d['exported']:
                markdown.append(f"| {d['id']} | {d['from']} | {d['to']} | {d['row'][4]} | {d['row'][5]} | {d.get('route_mm', 'manual')} | {d['review']} |")
        markdown += ['', 'Panel-cable-core lengths cover the panel tail only. Overall external cable allowances remain in the project BOM.',
                     'Automatic lengths use modeled duct routing, a cut allowance and rounding; they are estimates for review.',
                     '', '## Coverage', '', '| Net | Physical connection records complete |', '|---|---|']
        markdown += [f"| {n['net']} | {'Yes' if n['covered'] else 'Not yet recorded'} |" for n in audit]
        if unfinished:
            markdown += ['', '## Unfinished sections', '',
                         f'{len(unfinished)} unannotated symbols are outside the recorded wire nets. Their saved names and drawing were preserved.']
        markdown += ['', 'Edit schematic wire records with `tools/wiring/records.py`, then regenerate. The generated CSV is a read-only review.', '']
        atomic_write(output.parent / 'review.md', '\n'.join(markdown).encode())
    return report


def open_review(output, no_browser=False):
    """Reuse one localhost read-only reviewer for this generated file."""
    output = Path(output).resolve()
    review = PROJECT.parents[1] / 'bom_review/review.py'
    if not review.exists():
        raise ValueError('bom_review/review.py was not found alongside the project repositories.')
    registry = output.parent / '.review-server.json'
    url = None
    if registry.exists():
        try:
            state = json.loads(registry.read_text())
            port = int(state['port'])
            if not 1 <= port <= 65535:
                raise ValueError('Invalid reviewer port')
            base = f'http://127.0.0.1:{port}/'
            with urllib.request.urlopen(base + 'initial-bom', timeout=1) as response:
                info = json.load(response)
            if info.get('path') == str(output) and info.get('readOnly'):
                url = base + '?initial=1&mode=wire'
        except (OSError, ValueError, KeyError):
            pass
    if url is None:
        process = subprocess.Popen([sys.executable, str(review), str(output), '--mode', 'wire',
                                    '--read-only', '--port', '0', '--no-browser'],
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                                   start_new_session=True)
        line = process.stdout.readline().strip()
        if not line.startswith('BOM review: '):
            process.wait(timeout=5)
            raise ValueError('The BOM reviewer must support --read-only before opening generated schedules.')
        url = line.split('BOM review: ', 1)[1]
        port = int(url.split('127.0.0.1:', 1)[1].split('/', 1)[0])
        process.stdout.close()
        atomic_write(registry, json.dumps({'port': port}).encode())
    if not no_browser:
        webbrowser.open(url, new=0)
    return url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    parser.add_argument('--pcb', type=Path, default=DEFAULT_PCB)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--section')
    parser.add_argument('--check', action='store_true', help='validate without writing output')
    parser.add_argument('--open', action='store_true', help='open the generated read-only reviewer')
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        report = generate(args.schematic, args.pcb, args.output, args.section, args.check)
        print(f"Generated {report['generated_rows']} assembly wires; full-schematic coverage: {'complete' if report['complete'] else 'partial'}.")
        if not args.check:
            print(args.output.resolve())
        if args.open and not args.check:
            print('Review: ' + open_review(args.output, args.no_browser))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f'Wire generation failed: {error}\n')


if __name__ == '__main__':
    main()
