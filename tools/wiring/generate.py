#!/usr/bin/env python3
"""Generate physical wires from the saved PCB's explicit trace paths."""
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
import webbrowser

from model import HEADERS, Schematic, atomic_write, digest, export_netlist, prop
from source import footprint_metadata, nodes, one
from traces import native_board, rows_from_traces

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_SCH = PROJECT / 'kicad/powermatic_1200/powermatic_1200.kicad_sch'
DEFAULT_PCB = DEFAULT_SCH.with_suffix('.kicad_pcb')
DEFAULT_OUTPUT = PROJECT / 'Wire_schedule.csv'


def coverage(schematic, nets, details, internal_groups=()):
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
        endpoints=set(pins)|{p for pair in edges[name] for p in pair}
        parent = {p: p for p in endpoints}
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
        for group in internal_groups:
            known=[tuple(p) for p in group if tuple(p) in parent]
            for other in known[1:]:join(known[0],other)
        groups = defaultdict(list)
        for p in pins:
            groups[find(p)].append('.'.join(p))
        result.append({'net': name, 'covered': len(groups) == 1,
                       'remaining_groups': [sorted(g) for g in groups.values()]})
    return result


def generate(sch_path, pcb_path, output, section=None, check=False):
    sch_path, pcb_path, output = map(lambda p: Path(p).resolve(), [sch_path, pcb_path, output])
    source, board = sch_path.read_bytes(), pcb_path.read_bytes()
    output_before = output.read_bytes() if output.exists() else None
    schematic = Schematic(source.decode('utf-8'), allow_in_progress=True)
    if section and section != 'PCB traces':
        raise ValueError('Trace export has one PCB traces section.')
    with tempfile.TemporaryDirectory(prefix='powermatic-wires-') as work:
        # Export exactly the bytes used to read the records, even if the editor saves meanwhile.
        snapshot = Path(work) / sch_path.name
        export_text, unfinished = schematic.export_snapshot()
        snapshot.write_text(export_text)
        nets, pin_nets = export_netlist(snapshot, work)
        board_snapshot = Path(work)/pcb_path.name
        board_snapshot.write_bytes(board)
        geometry = native_board(board_snapshot,work)
        geometry['internal_groups']=[];geometry['pass_through_pairs']=[]
        pad_ids={(p['footprint_id'],p['pin']):p['id'] for p in geometry['pads']}
        for footprint in footprint_metadata(board.decode()):
            fid=one(footprint,'uuid')[1];ref=prop(footprint,'Reference')
            group_node=one(footprint,'jumper_pad_groups')
            if group_node:
                for group in group_node[1:]:
                    geometry['internal_groups'].append([[ref,pin] for pin in group])
                    ids=[pad_ids.get((fid,pin)) for pin in group]
                    if len(ids)==2 and all(ids) and all(next(p for p in geometry['pads'] if p['id']==pid).get('pass_through') for pid in ids):
                        geometry['pass_through_pairs'].append(ids)
        rows,details,warnings = rows_from_traces(geometry,schematic,pin_nets)
        for d in details:
            if any(ref in unfinished for ref, pin in nets.get(d['net'], ())):
                raise ValueError(f"{d['id']}: an unfinished symbol shares recorded net {d['net']}; annotate/reconcile it first.")
    audit = coverage(schematic, nets, details,geometry['internal_groups'])
    report = {'schema': 2, 'source_schematic': str(sch_path), 'source_pcb': str(pcb_path),
              'schematic_sha256': digest(source), 'pcb_sha256': digest(board),
              'generated_rows': len(rows), 'omitted_records': sum(not d['exported'] for d in details),
              'sections': dict(Counter(d['section'] for d in details if d['exported'])),
              'review_states': dict(Counter(d['review'] for d in details if d['exported'])),
              'complete': all(n['covered'] for n in audit) and not unfinished and not warnings, 'net_coverage': audit,
              'unfinished_symbols_outside_recorded_nets': list(unfinished.values()),
              'records': details, 'csv_is_generated': True,'wire_source':'PCB traces',
              'trace_objects':len(geometry['tracks']),'warnings':warnings,
              'route_sections':sum(d['kind']=='route-section' for d in details),
              'legacy_wire_fields_used':False,
              'unrouted_nets': [n['net'] for n in audit if not n['covered']]}
    if digest(sch_path.read_bytes()) != digest(source) or digest(pcb_path.read_bytes()) != digest(board):
        raise ValueError('The schematic or PCB changed during generation. Save and generate again.')
    if not check:
        current_output = output.read_bytes() if output.exists() else None
        if current_output != output_before:
            raise ValueError('The CSV changed during extraction; its newer edits were preserved.')
        stream = io.StringIO(newline='')
        csv.writer(stream, lineterminator='\r\n').writerows([HEADERS, *rows])
        atomic_write(output, stream.getvalue().encode('utf-8'),
                     expected=digest(output_before) if output_before is not None else None)
    return report


def open_review(output, no_browser=False):
    """Fresh extraction into the live CSV, then an editable browser review."""
    if Path(output).resolve() != DEFAULT_OUTPUT.resolve():
        raise ValueError("The Finder review uses the project live Wire_schedule.csv.")
    helper = PROJECT.parents[1] / "bom_review/finder_launch.py"
    result = subprocess.run([sys.executable, str(helper), str(PROJECT), "--mode", "wire"],
                            capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "Could not extract fresh wiring data.")
    url = result.stdout.strip()
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
    parser.add_argument('--open', action='store_true', help='extract fresh data and open the editable live CSV')
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        if args.open and not args.check:
            if (args.schematic.resolve() != DEFAULT_SCH.resolve()
                    or args.pcb.resolve() != DEFAULT_PCB.resolve() or args.section):
                raise ValueError('The Finder editor refreshes the configured project files and all recorded wires. Use export without --open for custom inputs or sections.')
            print('Review: ' + open_review(args.output, args.no_browser))
            return
        report = generate(args.schematic, args.pcb, args.output, args.section, args.check)
        print(f"Generated {report['generated_rows']} assembly wires; full-schematic coverage: {'complete' if report['complete'] else 'partial'}.")
        if not args.check:
            print(args.output.resolve())
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f'Wire generation failed: {error}\n')


if __name__ == '__main__':
    main()
