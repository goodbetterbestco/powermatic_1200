#!/usr/bin/env python3
"""Stage S2 physical terminal IDs and standard symbol geometry without rewiring."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, replace, nodes, TOKEN

PIN_MAP = {'L1': '2T', 'R2': '1T', 'L2': '2B', 'R1': '1B',
           'L3': '4T', 'R4': '3T', 'L4': '4B', 'R3': '3B',
           'L5': '6T', 'R5': '5T'}
FUNCTIONS = {'1T': 'FWD_NC_1', '2T': 'FWD_NC_2', '1B': 'FWD_NO_1', '2B': 'FWD_NO_2',
             '3T': 'REV_NC_1', '4T': 'REV_NC_2', '3B': 'REV_NO_1', '4B': 'REV_NO_2',
             '5T': 'STOP_NC_1', '6T': 'STOP_NC_2'}


def scalar(raw, index, value):
    tokens = list(TOKEN.finditer(raw))
    start, end = tokens[index].span()
    return raw[:start] + json.dumps(value) + raw[end:]


def child_at(raw, position):
    edits = [(a, b, '(at ' + ' '.join(str(v) for v in position) + ')')
             for a, b, entry in children(raw) if key(entry) == 'at']
    assert len(edits) == 1
    return replace(raw, edits)


def definition(raw):
    edits = []
    for a, b, entry in children(raw):
        kind, tree = key(entry), parse(entry)
        if kind == 'property' and tree[1] == 'Reference':
            edits.append((a, b, child_at(entry, [0, 22.86, 0])))
        elif kind == 'symbol':
            inner = []
            for x, y, element in children(entry):
                typ, node = key(element), parse(element)
                if typ == 'rectangle':
                    sub = [(i, j, f'({key(part)} {"-7.62 19.05" if key(part) == "start" else "7.62 -19.05"})')
                           for i, j, part in children(element) if key(part) in ['start', 'end']]
                    inner.append((x, y, replace(element, sub)))
                elif typ == 'pin':
                    old = one(node, 'number')[1]
                    number = PIN_MAP.get(old, old)
                    assert number in FUNCTIONS
                    sub = []
                    for i, j, part in children(element):
                        if key(part) == 'number':
                            sub.append((i, j, scalar(part, 2, number)))
                        elif key(part) == 'name':
                            sub.append((i, j, scalar(part, 2, FUNCTIONS[number])))
                        elif key(part) == 'at':
                            pos = parse(part)
                            sub.append((i, j, f'(at -10.16 {pos[2]} {pos[3]})'))
                    inner.append((x, y, replace(element, sub)))
            edits.append((a, b, replace(entry, inner)))
    return replace(raw, edits)


def instance(raw):
    tree = parse(raw)
    pos = one(tree, 'at')
    legacy = any(pin[1] in PIN_MAP for pin in nodes(tree, 'pin'))
    new_x, cy = round(float(pos[1]) + (1.27 if legacy else 0), 6), float(pos[2])
    edits = []
    for a, b, entry in children(raw):
        kind, node = key(entry), parse(entry)
        if kind == 'at':
            edits.append((a, b, f'(at {new_x} {cy} {pos[3]})'))
        elif kind == 'pin' and node[1] in PIN_MAP:
            edits.append((a, b, scalar(entry, 2, PIN_MAP[node[1]])))
        elif kind == 'property':
            name, value = node[1:3]
            if name.startswith('Termination.'):
                old = name.removeprefix('Termination.')
                if old in PIN_MAP:
                    entry = scalar(entry, 2, 'Termination.' + PIN_MAP[old])
            elif name == 'Wire.Sizes':
                payload = json.loads(value)
                for item in payload['entries']:
                    item['pin'] = PIN_MAP.get(item['pin'], item['pin'])
                entry = scalar(entry, 3, json.dumps(payload, separators=(',', ':')))
            old_at = one(node, 'at')
            if old_at:
                py = cy - 22.86 if name == 'Reference' else float(old_at[2])
                entry = child_at(entry, [new_x, py, old_at[3]])
            edits.append((a, b, entry))
    return replace(raw, edits)


def rename_pads(raw):
    return replace(raw, [(a, b, scalar(entry, 2, PIN_MAP[parse(entry)[1]]))
                        for a, b, entry in children(raw)
                        if key(entry) == 'pad' and parse(entry)[1] in PIN_MAP])


def finish_board(work, netlist):
    xml = ET.parse(netlist).getroot()
    before = ET.parse(work / 'before-netlist.xml').getroot()
    pins = {p.get('pin'): (n.get('name'), p.get('pinfunction'), p.get('pintype'))
            for n in xml.findall('nets/net') for p in n.findall('node') if p.get('ref') == 'S2'}
    old = {p.get('pin'): n.get('name') for n in before.findall('nets/net')
           for p in n.findall('node') if p.get('ref') == 'S2'}
    netmap = {old[p]: pins[q][0] for p, q in PIN_MAP.items() if old[p] != pins[q][0]}
    path = work / 'after/powermatic_1200.kicad_pcb'
    original = path.read_text()
    edits = []
    for a, b, raw in children(original):
        if key(raw) == 'net' and parse(raw)[2] in netmap:
            node = parse(raw)
            edits.append((a, b, f'(net {node[1]} {json.dumps(netmap[node[2]])})'))
        elif key(raw) == 'footprint' and prop(parse(raw), 'Reference') == 'S2':
            inner = []
            for x, y, pad in children(raw):
                if key(pad) != 'pad':
                    continue
                net, function, typ = pins[parse(pad)[1]]
                sub = []
                for i, j, field in children(pad):
                    kind, node = key(field), parse(field)
                    if kind == 'pinfunction':
                        sub.append((i, j, f'(pinfunction {json.dumps(function)})'))
                    elif kind == 'pintype':
                        sub.append((i, j, f'(pintype {json.dumps(typ)})'))
                    elif kind == 'net':
                        sub.append((i, j, '(net ' + (str(node[1]) + ' ' if len(node) == 3 else '') + json.dumps(net) + ')'))
                inner.append((x, y, replace(pad, sub)))
            edits.append((a, b, replace(raw, inner)))
    path.write_text(replace(original, edits))
    print('Updated S2 pad functions and its two generated unconnected-net names from the native netlist.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--netlist', type=Path, help='Finish the already staged board using the candidate native netlist')
    parser.add_argument('--install', action='store_true', help='Install validated candidates with concurrent-edit checks')
    args = parser.parse_args()
    work = args.work
    if args.install:
        report = json.loads((work / 'staging.json').read_text())
        assert (work / 'validation.json').exists()
        review = ROOT / 'reviews/S2_model_2026-10-08/pin_numbering'
        for item in report['files'].values():
            source = Path(item['source'])
            assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sha256_before'], 'Concurrent file edit: ' + str(source)
        review.mkdir(parents=True, exist_ok=True)
        shutil.copytree(work / 'before', review / 'before', dirs_exist_ok=True)
        for item in report['files'].values():
            source, candidate = Path(item['source']), Path(item['candidate'])
            shutil.copy2(candidate, source)
            item['sha256_after'] = hashlib.sha256(source.read_bytes()).hexdigest()
            assert source.read_bytes() == candidate.read_bytes()
        for name in ['staging.json', 'validation.json', 'before-netlist.xml', 'candidate-netlist.xml', 'S2-symbol.svg', 'S2-symbol.png']:
            shutil.copy2(work / name, review / name)
        (review / 'installed.json').write_text(json.dumps(report, indent=2) + '\n')
        print('Installed physical S2 terminal IDs, standard symbol geometry and associated wiring metadata.')
        return
    if args.netlist:
        finish_board(work, args.netlist)
        return
    before, after = work / 'before', work / 'after'
    before.mkdir(parents=True, exist_ok=True)
    after.mkdir(exist_ok=True)
    parts = Path.home() / 'Projects/_parts'
    project = ROOT / 'kicad/powermatic_1200'
    paths = {'library': parts / 'symbols/Controls.kicad_sym',
             'footprint': parts / 'footprints/Controls.pretty/50MA3KLE_Top.kicad_mod',
             'schematic': project / 'powermatic_1200.kicad_sch',
             'board': project / 'powermatic_1200.kicad_pcb'}
    report = {'pin_map': PIN_MAP, 'files': {}}
    for tag, path in paths.items():
        shutil.copy2(path, before / path.name)
        original = path.read_text()
        if tag == 'library':
            edits = [(a, b, definition(raw)) for a, b, raw in children(original)
                     if key(raw) == 'symbol' and parse(raw)[1] == '50MA3KLE']
            assert len(edits) == 1
            updated = replace(original, edits)
        elif tag == 'footprint':
            updated = rename_pads(original)
        elif tag == 'schematic':
            edits = []
            for a, b, raw in children(original):
                if key(raw) == 'symbol' and prop(parse(raw), 'Reference') == 'S2':
                    edits.append((a, b, instance(raw)))
                elif key(raw) == 'lib_symbols':
                    sub = [(x, y, definition(entry)) for x, y, entry in children(raw)
                           if key(entry) == 'symbol' and parse(entry)[1] == 'Controls:50MA3KLE']
                    assert len(sub) == 1
                    edits.append((a, b, replace(raw, sub)))
            assert len(edits) == 2
            updated = replace(original, edits)
        else:
            edits = [(a, b, rename_pads(raw)) for a, b, raw in children(original)
                     if key(raw) == 'footprint' and prop(parse(raw), 'Reference') == 'S2']
            assert len(edits) == 1
            updated = replace(original, edits)
        candidate = after / path.name
        candidate.write_text(updated)
        report['files'][tag] = {'source': str(path), 'candidate': str(candidate),
                               'sha256_before': hashlib.sha256(path.read_bytes()).hexdigest()}
    (work / 'staging.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Staged ten physical terminal IDs and standard-grid symbol geometry; connection points preserved.')


if __name__ == '__main__':
    main()
