#!/usr/bin/env python3
"""Validate schematic connection sizes independently of unfinished physical routes.

Wire.Sizes is a custom symbol field. It assigns sizes to terminal connections,
not to KiCad's graphical wire segments or a fabricated conductor graph.
The physical Wire.Wxxx records remain a separate, more detailed data type.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import tempfile

from generate import DEFAULT_SCH
from model import Schematic, change_fields, digest, export_netlist
from source import nodes, one, prop

FIELD = 'Wire.Sizes'
PLAN_FIELD = 'Wire.SizePlan'
SCOPES = {
    'panel_power', 'panel_control', 'panel_pe', 'incoming_cable',
    'motor_conduit', 'controls_conduit', 'factory_pigtail',
    'retained_link', 'suppressor_lead', 'connector_interface',
    'estop_assembly', 'direct_mount',
}
FIXED = {'retained_link', 'suppressor_lead', 'connector_interface',
         'estop_assembly', 'direct_mount'}
WIRE_COLORS = {
    'panel_power': 'Black', 'panel_control': 'Blue', 'panel_pe': 'Green/Yellow',
    'motor_conduit': 'Black', 'controls_conduit': 'Blue',
}
J1_COLORS = {'1': 'Brown', '2': 'White', '3': 'Blue', '4': 'Black'}


def color_for(scope, pin):
    if scope == 'factory_pigtail':
        return J1_COLORS[pin]
    if scope == 'motor_conduit' and pin == 'PE':
        return 'Green/Yellow'
    return WIRE_COLORS.get(scope)


def endpoint_map(schematic, pin_nets):
    result = {}
    for (ref, pin), net in pin_nets.items():
        if net.startswith('unconnected-') or ref.startswith('#'):
            continue
        endpoint = schematic.endpoint(ref, pin)
        result[endpoint['symbol_uuid'], pin] = (ref, net)
    return result


def inspect(text):
    schematic = Schematic(text)
    with tempfile.TemporaryDirectory(prefix='powermatic-wire-sizes-') as work:
        snapshot = Path(work) / DEFAULT_SCH.name
        snapshot.write_text(text)
        nets, pin_nets = export_netlist(snapshot, work)
    expected = endpoint_map(schematic, pin_nets)
    assigned, rows, plans = {}, [], []
    for symbol in schematic.symbols:
        sid, ref = one(symbol, 'uuid')[1], prop(symbol, 'Reference')
        value = prop(symbol, FIELD)
        if value:
            payload = json.loads(value)
            if payload.get('schema') != 1 or payload.get('owner_uuid') != sid:
                raise ValueError(f'{ref}: invalid or copied Wire.Sizes owner/schema')
            for entry in payload.get('entries', []):
                pin, scope = entry['pin'], entry['scope']
                key = sid, pin
                if key not in expected:
                    raise ValueError(f'{ref}.{pin}: missing, disconnected or replaced endpoint')
                if key in assigned:
                    raise ValueError(f'{ref}.{pin}: duplicate size declaration')
                if entry['net'] != expected[key][1]:
                    raise ValueError(f'{ref}.{pin}: declared net differs from native netlist')
                if scope not in SCOPES:
                    raise ValueError(f'{ref}.{pin}: unknown sizing scope {scope}')
                awg = entry.get('awg')
                if scope in FIXED:
                    if awg is not None:
                        raise ValueError(f'{ref}.{pin}: fixed/interface connection has an invented gauge')
                elif not isinstance(awg, int) or not 1 <= awg <= 40:
                    raise ValueError(f'{ref}.{pin}: expected an integer AWG from 1 to 40')
                assigned[key] = entry
                rows.append(dict(entry, reference=ref, symbol_uuid=sid))
        value = prop(symbol, PLAN_FIELD)
        if value:
            payload = json.loads(value)
            if payload.get('schema') != 1 or payload.get('owner_uuid') != sid:
                raise ValueError(f'{ref}: invalid or copied Wire.SizePlan owner/schema')
            for entry in payload.get('entries', []):
                if not isinstance(entry.get('awg'), int) or not 1 <= entry['awg'] <= 40:
                    raise ValueError(f'{ref}: invalid planned conductor AWG')
                if 'pin' in entry:
                    raise ValueError(f'{ref}: a mechanical size plan must not invent a symbol pin')
                plans.append(dict(entry, reference=ref, symbol_uuid=sid))
    missing = [f'{ref}.{pin}' for (sid, pin), (ref, net) in expected.items()
               if (sid, pin) not in assigned]
    return {
        'schema': 1, 'source_sha256': digest(text.encode()),
        'connected_pins': len(expected), 'sized_pins': len(rows),
        'complete_connection_sizing': not missing, 'missing': sorted(missing),
        'scopes': dict(Counter(r['scope'] for r in rows)),
        'entries': sorted(rows, key=lambda r: (r['reference'], r['pin'])),
        'planned_conductors': plans,
        'physical_wire_schedule_complete': False,
    }


def populate(text):
    """Apply the owner's approved sizes to this exact saved circuit inventory."""
    schematic = Schematic(text)
    with tempfile.TemporaryDirectory(prefix='powermatic-sizing-plan-') as work:
        snapshot = Path(work) / DEFAULT_SCH.name
        snapshot.write_text(text)
        _, pin_nets = export_netlist(snapshot, work)
    external = {
        'S2': {'5T', '6T', '2B', '1B', '3B'},
        'S3': {'1B', '1T', '2T'},
    }
    direct = {
        ('K4', '2'), ('K4', '4'), ('K4', '6'),
        ('K6', '2'), ('K6', '4'), ('K6', '6'),
        ('OL4', 'IN1'), ('OL4', 'IN2'), ('OL4', 'IN3'),
        ('OL6', 'IN1'), ('OL6', 'IN2'), ('OL6', 'IN3'),
    }
    # These are device identities, not guesses based on net-name patterns.
    power_values = {'RM25030-3SR', '222102', 'FAZ-D4/2-NA-L'}
    updates, chosen_external = {}, {'S2': set(), 'S3': set()}
    by_owner = {}
    for (sid, pin), (ref, net) in sorted(endpoint_map(schematic, pin_nets).items()):
        symbol = schematic.by_uuid[sid]
        value = prop(symbol, 'Value')
        scope, awg, note = None, None, ''
        if ref == 'J2':
            scope, awg = 'incoming_cable', 12
            note = 'Selected 12/4 incoming cable; panel-tail routing remains pending.'
        elif ref == 'M1':
            if pin == 'PE' and net == 'PE':
                scope, awg = 'motor_conduit', 12
                note = 'Motor-conduit PE to the bonding junction; attachment hardware remains installation work.'
            elif pin in {f'T{i}' for i in range(1, 7)}:
                scope, awg = 'motor_conduit', 14
                note = 'One external 14 AWG conductor per motor lead; factory motor lead size is separate.'
            else:
                raise ValueError('Motor pin inventory changed; review its conductor plan.')
        elif ref in external:
            if pin in external[ref]:
                scope, awg = 'controls_conduit', 16
                chosen_external[ref].add(pin)
                note = 'Individual external control wire; panel-side extensions use 18 AWG.'
            else:
                scope = 'retained_link'
                note = 'Retained switch jumper/strap; preserve the existing assembly.'
                if ref == 'S2':
                    note = ('Required station jumper 2B-4B; physical installation unconfirmed.'
                            if pin == '4B' else
                            'Installed station jumpers 1T-3T and 3T-5T; no external conductor.')
        elif ref == 'J1':
            scope, awg = 'factory_pigtail', 22
            note = 'T4171310004-001 factory 0.34 mm² / 22 AWG lead; any extension is a separate wire.'
        elif ref == 'J6':
            scope = 'connector_interface'
            note = 'M12 mating interface; retain the supplied assembly.'
        elif ref == 'S1':
            scope = 'estop_assembly'
            note = 'Retained E-stop assembly; supplied wiring stays as-is.'
        elif value == 'HMX1-SSVRC-DC':
            scope = 'suppressor_lead'
            note = 'Device-supplied suppressor connection; do not create a loose-wire purchase.'
        elif (ref, pin) in direct:
            scope = 'direct_mount'
            note = 'Direct-mounted overload power connection; no separate assembly wire.'
        elif value == 'NDR-240-24':
            if pin == '1_BOT':
                scope, awg = 'panel_pe', 14
            elif pin in {'2_BOT', '3_BOT'}:
                scope, awg = 'panel_power', 14
            else:
                scope, awg = 'panel_control', 18
                note = 'PSU duplicate output terminals are internally common; no jumper is implied.'
        elif value in power_values:
            scope, awg = 'panel_power', 14
        elif value == 'HTOR32-6-S' and pin in {'2', '4', '6'}:
            scope, awg = 'panel_power', 14
        elif value == 'HMC-9B30-11-DS' and pin in {'1', '2', '3', '4', '5', '6'}:
            scope, awg = 'panel_power', 14
            note = 'Gauge for discrete panel wire; reversing connection-kit bars retain their supplied form.'
        elif value in {'HMC-9B30-11-DS', 'HC3096N-52-900-24', 'HTOR32-6-S', 'XB4BVB1'}:
            scope, awg = 'panel_control', 18
            if pin.startswith(('A1.', 'A2.')):
                note = 'Duplicate coil terminals are internally common; this size does not imply a jumper.'
        else:
            raise ValueError(f'Unclassified connected component {ref} ({value}), pin {pin}.')
        entry = {'pin': pin, 'net': net, 'scope': scope, 'awg': awg}
        color = color_for(scope, pin)
        if color:
            entry['color'] = color
        if note:
            entry['note'] = note
        by_owner.setdefault(sid, []).append(entry)
    if chosen_external != external:
        raise ValueError('External control terminal inventory changed; review the 5+3 conductor plan.')
    for sid, entries in by_owner.items():
        updates[sid] = {FIELD: json.dumps({'schema': 1, 'owner_uuid': sid, 'entries': entries},
                                         ensure_ascii=False, separators=(',', ':'))}
    motor = schematic.endpoint('M1', 'T1')['symbol_uuid']
    motor_pe_plan = [] if (motor, 'PE') in endpoint_map(schematic, pin_nets) else [
        {'id': 'motor-conduit-pe', 'awg': 12, 'net': 'PE', 'scope': 'motor_conduit',
         'from': 'panel PE terminal', 'to': 'motor-end PE splice',
         'status': 'planned', 'note': 'Mechanical PE plan; M1 has no connected PE pin.'},
    ]
    updates[motor][PLAN_FIELD] = json.dumps({
        'schema': 1, 'owner_uuid': motor,
        'entries': motor_pe_plan + [
            {'id': 'motor-body-bond', 'awg': 10, 'net': 'PE', 'scope': 'prefab_bond',
             'from': 'motor-end PE splice', 'to': 'motor body', 'status': 'proposed',
             'note': 'GRDKIT01 supplied assembly if selected; attachment hardware remains open.'},
            {'id': 'machine-frame-bond', 'awg': 10, 'net': 'PE', 'scope': 'prefab_bond',
             'from': 'motor-end PE splice', 'to': 'machine frame', 'status': 'proposed',
             'note': 'GRDKIT01 supplied assembly if selected; attachment hardware remains open.'},
        ]}, separators=(',', ':'))
    psu = schematic.endpoint('PS1', '1_BOT')['symbol_uuid']
    updates[psu][PLAN_FIELD] = json.dumps({
        'schema': 1, 'owner_uuid': psu,
        'entries': [{'id': 'enclosure-door-bond', 'awg': 10, 'net': 'PE', 'scope': 'prefab_bond',
                     'from': 'enclosure stud', 'to': 'door stud', 'status': 'proposed',
                     'note': 'GRDKIT01 supplied assembly if selected; stud fit/length remain open.'}]},
        separators=(',', ':'))
    result = change_fields(text, updates)
    # Remove only these sizing fields from the candidate: the drawing, other
    # metadata and existing wire records must be byte-for-byte preserved.
    candidate = Schematic(result)
    if nodes(candidate.tree, 'wire') != nodes(schematic.tree, 'wire'):
        raise ValueError('Unexpected wire geometry change.')
    clean = lambda s: [p for p in s if not (isinstance(p, list) and
                        p[0] == 'property' and p[1] in {FIELD, PLAN_FIELD})]
    if [clean(s) for s in candidate.symbols] != [clean(s) for s in schematic.symbols]:
        raise ValueError('Unexpected existing symbol change.')
    return result


def markdown(report):
    lines = ['# Schematic connection sizing', '',
             'Sizes are custom Wire.Sizes symbol fields in the schematic. These declarations',
             'classify connected terminals; they do not choose physical terminal routes,',
             'create jumpers between internally common pins or define cut lengths.', '',
             f'Connected terminals classified: {report["sized_pins"]}/{report["connected_pins"]}.',
             f'Connection sizing complete: {report["complete_connection_sizing"]}.',
             'Physical conductor schedule and terminal allocation remain pending.', '',
             '| Terminal | Net | Scope | AWG | Color |', '|---|---|---|---|---|']
    for r in report['entries']:
        lines.append(f'| {r["reference"]}.{r["pin"]} | {r["net"]} | {r["scope"]} | '
                     f'{r["awg"] if r["awg"] is not None else "—"} | '
                     f'{r.get("color", "")} |')
    lines += ['', '## Planned PE conductors', '', '| Plan | AWG | Status |', '|---|---|---|']
    lines += [f'| {r["id"]} | {r["awg"]} | {r["status"]} |' for r in report['planned_conductors']]
    lines += ['', 'The existing Wire.Wxxx physical-wire records still require reconciliation',
              'with the PCB-only terminal model. Fixed lead sizes and conductor protection',
              'must be checked against the actual component and installation.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schematic', type=Path, default=DEFAULT_SCH)
    parser.add_argument('--stage', type=Path, help='write a candidate copy; never overwrites the source')
    parser.add_argument('--report', type=Path, help='write derived Markdown and JSON reports')
    args = parser.parse_args()
    try:
        text = args.schematic.read_text()
        if args.stage:
            if args.stage.resolve() == args.schematic.resolve():
                raise ValueError('Staging must not overwrite the source schematic.')
            result = populate(text)
        else:
            result = text
        report = inspect(result)
        if not report['complete_connection_sizing']:
            raise ValueError('Unclassified connected terminals: ' + ', '.join(report['missing']))
        if args.stage:
            args.stage.parent.mkdir(parents=True, exist_ok=True)
            args.stage.write_text(result)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(markdown(report))
            args.report.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
        print(f'Classified {report["sized_pins"]} connected terminals; '
              f'{report["scopes"]["controls_conduit"]} external control wires. '
              'Physical routes remain pending.')
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, f'Wire sizing failed: {error}\n')


if __name__ == '__main__':
    main()
