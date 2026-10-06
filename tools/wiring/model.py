"""Schematic-owned wire records and panel routing, using only the standard library."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from source import parse, nodes, one, prop, children, key, replace

HEADERS = ['FROM', 'FROM PIN', 'TO', 'TO PIN', 'AWG', 'LENGTH', 'TERM 1', 'TERM 2']
KINDS = {'wire', 'panel_cable_core', 'factory', 'internal', 'bridge', 'plug_cable'}
OMITTED = {'factory', 'internal', 'bridge', 'plug_cable'}
PREFIX = 'Wire.'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def kicad_cli():
    found = shutil.which('kicad-cli')
    mac = Path('/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
    if found:
        return found
    if mac.exists():
        return str(mac)
    raise ValueError('kicad-cli is required to check the saved schematic connectivity.')


def export_netlist(path, directory):
    target = Path(directory) / 'netlist.xml'
    result = subprocess.run([kicad_cli(), 'sch', 'export', 'netlist', '--format', 'kicadxml',
                             '--output', str(target), str(path)], capture_output=True, text=True)
    if result.returncode or not target.exists():
        message = result.stdout.strip() or result.stderr.strip()[-600:]
        raise ValueError(f'KiCad could not export the saved netlist (exit {result.returncode}): ' + message)
    if 'annotation errors' in result.stdout.lower():
        raise ValueError('Fix duplicate or unannotated schematic references before generating wires.')
    root = ET.parse(target).getroot()
    nets, pin_nets = {}, {}
    for n in root.findall('nets/net'):
        name = n.get('name')
        pins = {(p.get('ref'), p.get('pin')) for p in n.findall('node')}
        nets[name] = pins
        for pin in pins:
            pin_nets[pin] = name
    return nets, pin_nets


class Schematic:
    def __init__(self, text, allow_in_progress=False):
        self.text = text
        self.tree = parse(text)
        if not self.tree or self.tree[0] != 'kicad_sch':
            raise ValueError('Expected a KiCad schematic.')
        self.symbols = nodes(self.tree, 'symbol')
        self.by_uuid = {one(s, 'uuid')[1]: s for s in self.symbols}
        self.by_ref = {}
        self.unannotated = {}
        for s in self.symbols:
            ref = prop(s, 'Reference')
            if not ref or '?' in ref:
                if not allow_in_progress:
                    raise ValueError(f'Unannotated schematic symbol: {ref!r}')
                self.unannotated[one(s, 'uuid')[1]] = s
                continue
            previous = self.by_ref.setdefault(ref, [])
            if any(one(p, 'unit')[1] == one(s, 'unit')[1] for p in previous):
                raise ValueError(f'Duplicate schematic reference/unit: {ref}')
            previous.append(s)
        self.libs = {s[1]: s for s in nodes(one(self.tree, 'lib_symbols'), 'symbol')}
        self.copied_wire_fields = []

    def library_for(self, symbol):
        override = one(symbol, 'lib_name')
        return self.libs.get(override[1] if override else one(symbol, 'lib_id')[1])

    def export_snapshot(self):
        """Give unfinished, unrecorded symbols temporary names only in the export copy."""
        edits, aliases = [], {}
        for a, b, raw in children(self.text):
            if key(raw) != 'symbol':
                continue
            s = parse(raw)
            sid = one(s, 'uuid')[1]
            if sid not in self.unannotated:
                continue
            number = len(aliases) + 1
            alias = f'ZZUNFINISHED{number}'
            while alias in self.by_ref:
                number += 1
                alias = f'ZZUNFINISHED{number}'
            old = prop(s, 'Reference')
            sub = []
            for aa, bb, child in children(raw):
                if key(child) == 'property' and parse(child)[1] == 'Reference':
                    sub.append((aa, bb, child.replace(json.dumps(old), json.dumps(alias), 1)))
                elif key(child) == 'instances':
                    sub.append((aa, bb, child.replace(f'(reference "{old}")', f'(reference "{alias}")')))
            edits.append((a, b, replace(raw, sub)))
            aliases[alias] = {'symbol_uuid': sid, 'reference': old, 'value': prop(s, 'Value')}
        return replace(self.text, edits), aliases

    def resolve(self, endpoint):
        s = self.by_uuid.get(endpoint.get('symbol_uuid'))
        if s is None:
            raise ValueError(f'Destination symbol was deleted/replaced: {endpoint.get("symbol_uuid")}')
        pin = str(endpoint.get('pin', ''))
        ref = prop(s, 'Reference')
        if not ref or '?' in ref:
            raise ValueError('Annotate a symbol before assigning an assembly wire to it.')
        definitions = []
        for instance in self.by_ref[ref]:
            library = self.library_for(instance)
            if library is None:
                raise ValueError(f'{ref}: cached symbol definition is missing.')
            definitions.extend(p for u in nodes(library, 'symbol') for p in nodes(u, 'pin'))
        if pin not in {one(p, 'number')[1] for p in definitions}:
            raise ValueError(f'{ref} has no pin {pin}; update the wire record.')
        return s, ref, pin

    def endpoint(self, reference, pin):
        candidates = self.by_ref.get(reference, [])
        for s in candidates:
            endpoint = {'symbol_uuid': one(s, 'uuid')[1], 'pin': str(pin)}
            try:
                self.resolve(endpoint)
                return endpoint
            except ValueError:
                pass
        raise ValueError(f'No schematic endpoint {reference}.{pin}')

    def records(self):
        result, ids = [], set()
        self.copied_wire_fields = []
        for s in self.symbols:
            for p in nodes(s, 'property'):
                if not p[1].startswith(PREFIX):
                    continue
                wire_id = p[1][len(PREFIX):]
                if not re.fullmatch(r'W\d+', wire_id):
                    continue
                try:
                    record = json.loads(p[2])
                except json.JSONDecodeError as error:
                    raise ValueError(f'{wire_id}: malformed wire metadata') from error
                if not isinstance(record, dict):
                    raise ValueError(f'{wire_id}: a wire record must be a JSON object')
                owner = record.get('from_symbol_uuid', one(s, 'uuid')[1])
                if owner != one(s, 'uuid')[1]:
                    self.copied_wire_fields.append({'id': wire_id, 'copied_symbol_uuid': one(s, 'uuid')[1],
                                                    'original_owner_uuid': owner})
                    continue
                if wire_id in ids:
                    raise ValueError(f'Duplicate wire record {wire_id}')
                ids.add(wire_id)
                if record.get('schema') != 1:
                    raise ValueError(f'{wire_id}: unsupported record schema')
                if not record.get('from_pin') or not isinstance(record.get('to'), dict):
                    raise ValueError(f'{wire_id}: missing from_pin or destination endpoint')
                record = dict(record, id=wire_id,
                              from_endpoint={'symbol_uuid': one(s, 'uuid')[1], 'pin': record['from_pin']})
                result.append(record)
        return sorted(result, key=lambda r: (r.get('section', ''), int(r['id'][1:])))

    def direct_endpoints(self):
        """Local drawn wire paths, with terminal internals cut and global labels unmerged."""
        pins = {}
        for s in self.symbols:
            if one(s, 'uuid')[1] in self.unannotated:
                continue
            library = self.library_for(s)
            if library is None:
                continue
            at, unit = one(s, 'at'), one(s, 'unit')[1]
            theta = math.radians(float(at[3]))
            for body in nodes(library, 'symbol'):
                suffix = body[1].rsplit('_', 2)
                if len(suffix) == 3 and suffix[-2].isdigit() and suffix[-2] not in ['0', unit]:
                    continue
                for p in nodes(body, 'pin'):
                    x, y = map(float, one(p, 'at')[1:3])
                    xy = (round(float(at[1]) + x * math.cos(theta) - y * math.sin(theta), 5),
                          round(float(at[2]) - x * math.sin(theta) - y * math.cos(theta), 5))
                    pins[(prop(s, 'Reference'), one(p, 'number')[1])] = xy
        def on(p, a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ll = dx * dx + dy * dy
            if ll < 1e-12:
                return math.dist(p, a) < 1e-5
            t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / ll
            return -1e-6 <= t <= 1 + 1e-6 and math.dist(p, (a[0] + t * dx, a[1] + t * dy)) < 1e-5
        internal = []
        for ref in self.by_ref:
            if not ref.startswith('TB'):
                continue
            for a, b in [('1', '2'), ('TOP', 'BOT')]:
                if (ref, a) in pins and (ref, b) in pins:
                    internal.append((pins[(ref, a)], pins[(ref, b)]))
        wires = []
        for w in nodes(self.tree, 'wire'):
            a, b = [tuple(map(float, p[1:3])) for p in nodes(one(w, 'pts'), 'xy')]
            if any(on(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2), a, b) and on(a, p, q) and on(b, p, q)
                   for p, q in internal):
                continue
            wires.append((a, b))
        points = set(pins.values()) | {p for wire in wires for p in wire}
        points |= {tuple(map(float, one(j, 'at')[1:3])) for j in nodes(self.tree, 'junction')}
        parent = {p: p for p in points}
        def find(p):
            if parent[p] != p:
                parent[p] = find(parent[p])
            return parent[p]
        for a, b in wires:
            connected = [p for p in points if on(p, a, b)]
            for p in connected[1:]:
                parent[find(p)] = find(connected[0])
        groups = {}
        for endpoint, p in pins.items():
            groups.setdefault(find(p), set()).add(endpoint)
        return {endpoint: groups[find(p)] for endpoint, p in pins.items()}

    def display_name(self, s):
        ref = prop(s, 'Reference')
        if ref.startswith('TB'):
            return ref
        name = prop(s, 'WireName') or ' '.join((prop(s, 'Part Name') or prop(s, 'Value')).split())
        matching = {prop(other, 'Reference') for other in self.symbols
                    if (prop(other, 'WireName') or ' '.join((prop(other, 'Part Name') or prop(other, 'Value')).split())) == name}
        return name + ' ' + ref if len(matching) > 1 else name

    def display_pin(self, s, pin, physical_side=None):
        ref = prop(s, 'Reference')
        override = prop(s, 'WirePin.' + pin)
        if override:
            return override
        if ref.startswith('TB') and pin in ['1', '2', 'TOP', 'BOT']:
            return {'1': 'TOP', '2': 'BOT', 'TOP': 'TOP', 'BOT': 'BOT'}[pin]
        if pin.endswith(('_TOP', '_BOT', '.TOP', '.BOT')):
            return pin
        return pin + (' ' + physical_side if physical_side in ['TOP', 'BOT', 'LEFT', 'RIGHT'] else '')


def change_fields(text, updates):
    """Patch symbol fields by UUID, preserving all other source bytes."""
    edits, seen = [], set()
    for a, b, raw in children(text):
        if key(raw) != 'symbol':
            continue
        s = parse(raw)
        sid = one(s, 'uuid')[1]
        if sid not in updates:
            continue
        seen.add(sid)
        fields = dict(updates[sid])
        sub = []
        for aa, bb, child in children(raw):
            if key(child) == 'property' and parse(child)[1] in fields:
                p = parse(child)
                value = fields.pop(p[1])
                if value is None:
                    sub.append((aa, bb, ''))
                else:
                    old = json.dumps(p[2], ensure_ascii=False)
                    sub.append((aa, bb, child.replace(old, json.dumps(value, ensure_ascii=False), 1)))
        out = replace(raw, sub)
        at = one(s, 'at')
        extra = [f'(property {json.dumps(name)} {json.dumps(value, ensure_ascii=False)} '
                 f'(at {at[1]} {at[2]} 0) (effects (font (size 1.27 1.27)) (hide yes)))'
                 for name, value in fields.items() if value is not None]
        if extra:
            out = out[:out.rfind(')')] + '\n' + '\n'.join(extra) + '\n)'
        edits.append((a, b, out))
    if seen != set(updates):
        raise ValueError('A symbol changed before the metadata could be updated.')
    return replace(text, edits)


def atomic_write(path, data, expected=None):
    path = Path(path)
    if expected is not None and digest(path.read_bytes()) != expected:
        raise ValueError(f'{path.name} changed while working; save/reload and retry.')
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as output:
            output.write(data)
        if path.exists():
            os.chmod(name, path.stat().st_mode & 0o777)
        if expected is not None and digest(path.read_bytes()) != expected:
            raise ValueError(f'{path.name} changed; the saved file was preserved.')
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def world(local, at):
    x, y = map(float, local)
    theta = math.radians(float(at[3]) if len(at) > 3 else 0)
    return (float(at[1]) + x * math.cos(theta) + y * math.sin(theta),
            float(at[2]) - x * math.sin(theta) + y * math.cos(theta))


class Panel:
    def __init__(self, text):
        board = parse(text)
        self.footprints, self.pads, self.ducts = {}, {}, []
        for f in nodes(board, 'footprint'):
            ref, at = prop(f, 'Reference'), one(f, 'at')
            if at is None:
                continue
            if ref and ref != 'REF**':
                self.footprints[ref] = f
                for p in nodes(f, 'pad'):
                    self.pads[(ref, p[1])] = world(one(p, 'at')[1:3], at)
            if 'T1-1530G1-1_' not in f[1]:
                continue
            points = []
            for g in nodes(f, 'fp_line'):
                points.extend(world(one(g, k)[1:3], at) for k in ['start', 'end'])
            if not points:
                raise ValueError('Wire duct has no modeled outline.')
            xs, ys = zip(*points)
            bounds = min(xs), min(ys), max(xs), max(ys)
            horizontal = bounds[2] - bounds[0] > bounds[3] - bounds[1]
            self.ducts.append({'horizontal': horizontal, 'bounds': bounds,
                               'center': ((bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2)})
        self.horizontal = sorted((d for d in self.ducts if d['horizontal']), key=lambda d: d['center'][1])
        self.vertical = [d for d in self.ducts if not d['horizontal']]
        if not self.horizontal or len(self.vertical) != 1:
            raise ValueError('Routing currently requires horizontal ducts and one vertical trunk.')

    def endpoint(self, ref, pin, side=None):
        if (ref, pin) not in self.pads:
            raise ValueError(f'PCB pad {ref}.{pin} is missing; update the footprint/pad numbering first.')
        f = self.footprints[ref]
        xy = self.pads[(ref, pin)]
        center = tuple(map(float, one(f, 'at')[1:3]))
        side = side or ('TOP' if xy[1] < center[1] else 'BOT')
        wall = any(token in f[1] for token in ['LeftWall', 'BottomWall'])
        if wall:
            # Sidewall devices use the closest open horizontal duct end.
            options = [(math.dist(xy, (x, d['center'][1])), d, (x, d['center'][1]))
                       for d in self.horizontal for x in [d['bounds'][0], d['bounds'][2]]]
            options.extend((math.dist(xy, (d['center'][0], y)), d, (d['center'][0], y))
                           for d in self.vertical for y in [d['bounds'][1], d['bounds'][3]])
            _, duct, end = min(options, key=lambda option: option[0])
            if duct['horizontal']:
                width = duct['bounds'][3] - duct['bounds'][1]
                half_y = duct['center'][1] + (width / 4 if xy[1] >= duct['center'][1] else -width / 4)
                approach = [xy, (xy[0], half_y), (end[0], half_y)]
            else:
                approach = [xy, (end[0], xy[1]), end]
        else:
            if side not in ['TOP', 'BOT']:
                raise ValueError(f'{ref}.{pin}: choose TOP/BOT or provide a manual length.')
            candidates = [d for d in self.horizontal if (d['center'][1] < center[1] if side == 'TOP'
                                                         else d['center'][1] > center[1])]
            if not candidates:
                raise ValueError(f'{ref}.{pin}: no adjacent {side} duct.')
            duct = min(candidates, key=lambda d: abs(d['center'][1] - center[1]))
            width = duct['bounds'][3] - duct['bounds'][1]
            half_y = duct['center'][1] + (width / 4 if side == 'TOP' else -width / 4)
            approach = [xy, (xy[0], half_y)]
        return {'xy': xy, 'side': side, 'duct': duct, 'approach': approach}

    def route(self, source, target):
        a, b = source['approach'][-1], target['approach'][-1]
        points = list(source['approach'])
        if source['duct'] is target['duct']:
            points.extend([(a[0], b[1]), b])
        else:
            trunk = self.vertical[0]
            tx = trunk['center'][0]
            sy = source['duct']['center'][1] if source['duct']['horizontal'] else a[1]
            ty = target['duct']['center'][1] if target['duct']['horizontal'] else b[1]
            low, high = trunk['bounds'][1], trunk['bounds'][3]
            if not low <= min(sy, ty) <= max(sy, ty) <= high:
                raise ValueError('The vertical trunk does not connect both selected horizontal ducts.')
            points.extend([(a[0], sy), (tx, sy), (tx, ty), (b[0], ty), b])
        points.extend(reversed(target['approach'][:-1]))
        cleaned = []
        for p in points:
            if not cleaned or math.dist(p, cleaned[-1]) > 1e-7:
                cleaned.append(p)
        length = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(cleaned, cleaned[1:]))
        return length, cleaned


def make_rows(schematic, panel, records, pin_nets):
    rows, details, used = [], [], set()
    direct = schematic.direct_endpoints()
    for r in records:
        wid = r['id']
        kind = r.get('kind', 'wire')
        if kind not in KINDS:
            raise ValueError(f'{wid}: unknown connection kind {kind}')
        fs, fr, fp = schematic.resolve(r['from_endpoint'])
        ts, tr, tp = schematic.resolve(r['to'])
        fn, tn = pin_nets.get((fr, fp)), pin_nets.get((tr, tp))
        if not fn or fn.startswith('unconnected-') or fn != tn:
            raise ValueError(f'{wid}: {fr}.{fp} ({fn}) and {tr}.{tp} ({tn}) are not on one connected net.')
        pair = frozenset([(fr, fp), (tr, tp)])
        if len(pair) != 2 or pair in used:
            raise ValueError(f'{wid}: duplicate wire endpoints or a wire to itself.')
        used.add(pair)
        detail = {'id': wid, 'section': r.get('section', ''), 'from': f'{fr}.{fp}',
                  'to': f'{tr}.{tp}', 'net': fn, 'kind': kind, 'review': r.get('review', 'pending')}
        if kind in OMITTED:
            details.append(dict(detail, exported=False))
            continue
        for endpoint, other in [((fr, fp), (tr, tp)), ((tr, tp), (fr, fp))]:
            drawn = direct.get(endpoint, {endpoint}) - {endpoint}
            if drawn and other not in drawn:
                raise ValueError(f'{wid}: the drawn wire at {endpoint[0]}.{endpoint[1]} reaches '
                                 f'{sorted(drawn)}, not {other[0]}.{other[1]}; reconcile the drawing and record.')
        awg = str(r.get('awg', ''))
        if not awg.isdigit() or not 1 <= int(awg) <= 40:
            raise ValueError(f'{wid}: expected an AWG size from 1 to 40.')
        length = r.get('length', {'mode': 'auto'})
        route_mm, points = None, []
        if length.get('mode') == 'manual':
            value = str(length.get('mm', ''))
            if not value or not math.isfinite(float(value)) or float(value) <= 0:
                raise ValueError(f'{wid}: manual length must be positive.')
            from_side, to_side = r.get('from_side'), r.get('to_side')
        elif length.get('mode') == 'auto':
            _, physical_fr, physical_fp = schematic.resolve(r.get('route_from', r['from_endpoint']))
            _, physical_tr, physical_tp = schematic.resolve(r.get('route_to', r['to']))
            for physical in [(physical_fr, physical_fp), (physical_tr, physical_tp)]:
                if pin_nets.get(physical) != fn:
                    raise ValueError(f'{wid}: a gland/physical routing endpoint is on a different net.')
            source = panel.endpoint(physical_fr, physical_fp, r.get('from_side'))
            target = panel.endpoint(physical_tr, physical_tp, r.get('to_side'))
            route_mm, points = panel.route(source, target)
            slack = float(length.get('slack_mm', 200))
            step = float(length.get('round_mm', 50))
            minimum = float(length.get('minimum_mm', 0))
            if slack < 0 or step <= 0 or minimum < 0:
                raise ValueError(f'{wid}: invalid cut allowance/rounding/minimum.')
            cut = max(minimum, math.ceil((route_mm + slack - 1e-7) / step) * step)
            value = f'{cut:g}'
            from_side, to_side = source['side'], target['side']
            detail.update(route_from=f'{physical_fr}.{physical_fp}', route_to=f'{physical_tr}.{physical_tp}',
                          route_mm=round(route_mm, 3), slack_mm=slack, cut_mm=cut,
                          route_points=[[round(x, 5), round(y, 5)] for x, y in points])
        else:
            raise ValueError(f'{wid}: length mode must be auto or manual.')
        row = [schematic.display_name(fs), schematic.display_pin(fs, fp, from_side),
               schematic.display_name(ts), schematic.display_pin(ts, tp, to_side),
               awg, value, str(r.get('term1', 'TBD')), str(r.get('term2', 'TBD'))]
        detail.update(exported=True, row=row, length_mode=length['mode'])
        rows.append(row)
        details.append(detail)
    return rows, details
