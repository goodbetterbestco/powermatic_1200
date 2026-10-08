#!/usr/bin/env python3
"""Stage switch silkscreen and enclosure-only user-layer cleanup, preserving layout."""
from pathlib import Path
import csv
import hashlib
import io
import json
import math
import sys
import uuid

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, replace, nodes

WORK = Path('/private/tmp/powermatic-layer-review')
PARTS = Path.home() / 'Projects/_parts'
WIDTH = .25
GRAPHICS = {'fp_line', 'fp_arc', 'fp_circle', 'fp_curve', 'fp_rect', 'fp_poly'}
SWITCHES = {'50MA3KLE_Top': 'S2', '365-TAV2111_Top': 'S3'}
NAMESPACE = uuid.UUID('5aed8d35-947e-45fd-aec3-a147df88c78d')


def structural(name):
    return name.split(':')[-1].startswith(('EN4SD', 'DN-R35S1_', 'T1-1530G1-1_'))


def layer(raw, target):
    return replace(raw, [(a, b, f'(layer "{target}")')
                         for a, b, child in children(raw) if key(child) == 'layer'])


def circle_for_arc(points):
    a, m, b = points
    determinant = 2 * (a[0] * (m[1] - b[1]) + m[0] * (b[1] - a[1]) + b[0] * (a[1] - m[1]))
    assert abs(determinant) > 1e-10
    norms = [p[0] ** 2 + p[1] ** 2 for p in points]
    cx = (norms[0] * (m[1] - b[1]) + norms[1] * (b[1] - a[1]) + norms[2] * (a[1] - m[1])) / determinant
    cy = (norms[0] * (b[0] - m[0]) + norms[1] * (a[0] - b[0]) + norms[2] * (m[0] - a[0])) / determinant
    center = (cx, cy)
    radius = math.dist(center, a)
    start, mid, end = [math.atan2(p[1] - cy, p[0] - cx) for p in points]
    positive = (end - start) % (2 * math.pi)
    sign = 1 if (mid - start) % (2 * math.pi) <= positive else -1
    length = positive if sign == 1 else (start - end) % (2 * math.pi)
    return center, radius, start, sign, length


def clip(curves, pads):
    # 0.15 mm clearance measured from the actual stroke edge to logical copper.
    obstacles = [(tuple(map(float, one(p, 'at')[1:3])), float(one(p, 'size')[1]) / 2 + WIDTH / 2 + .15)
                 for p in pads]
    output = []
    for kind, pts in curves:
        cuts = [0, 1]
        if kind == 'line':
            line_start, line_end = pts
            delta = [line_end[i] - line_start[i] for i in range(2)]
            norm = sum(v * v for v in delta)
            if norm < 1e-12:
                continue
            def point(t):
                return [line_start[i] + t * delta[i] for i in range(2)]
            for c, r in obstacles:
                offset = [line_start[i] - c[i] for i in range(2)]
                dot = 2 * sum(offset[i] * delta[i] for i in range(2))
                disc = dot * dot - 4 * norm * (sum(v * v for v in offset) - r * r)
                if disc > 0:
                    cuts.extend(t for t in [(-dot - math.sqrt(disc)) / (2 * norm), (-dot + math.sqrt(disc)) / (2 * norm)] if 0 < t < 1)
        else:
            if kind == 'circle':
                center, radius = pts[0], math.dist(*pts)
                start, sign, length = 0, 1, 2 * math.pi
            else:
                center, radius, start, sign, length = circle_for_arc(pts)
            def point(t):
                angle = start + sign * length * t
                return [center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)]
            for c, r in obstacles:
                d = math.dist(center, c)
                if d < 1e-10 or d > radius + r or d < abs(radius - r):
                    continue
                angle = math.atan2(c[1] - center[1], c[0] - center[0])
                half = math.acos(max(-1, min(1, (d * d + radius * radius - r * r) / (2 * d * radius))))
                for theta in [angle - half, angle + half]:
                    span = ((theta - start) if sign == 1 else (start - theta)) % (2 * math.pi)
                    if 0 < span < length:
                        cuts.append(span / length)
        cuts = sorted(set(cuts))
        intervals = [(a, b) for a, b in zip(cuts, cuts[1:])
                     if all(math.dist(point((a + b) / 2), c) >= r - 1e-8 for c, r in obstacles)]
        if intervals == [(0, 1)]:
            output.append((kind, pts))
            continue
        for a, b in intervals:
            if (math.dist(point(a), point(b)) if kind == 'line' else radius * length * (b - a)) < .02:
                continue
            output.append(('line', [point(a), point(b)]) if kind == 'line'
                          else ('arc', [point(a), point((a + b) / 2), point(b)]))
    return output


def graphics(curves, identity):
    output = []
    for i, (kind, points) in enumerate(curves):
        coordinates = ' '.join(f'({key} {p[0]:.6f} {p[1]:.6f})' for key, p in
                               zip({'line': ['start', 'end'], 'arc': ['start', 'mid', 'end'], 'circle': ['center', 'end']}[kind], points))
        fill = ' (fill none)' if kind == 'circle' else ''
        ident = uuid.uuid5(NAMESPACE, f'{identity}:{i}')
        output.append(f'(fp_{kind} {coordinates} (stroke (width {WIDTH}) (type solid)){fill} (layer "F.SilkS") (uuid "{ident}"))')
    return output


def transform_switch(raw, ref, identity):
    curves = json.loads((WORK / f'{ref}-silk-curves.json').read_text())
    clipped = clip(curves, nodes(parse(raw), 'pad'))
    edits = []
    for a, b, child in children(raw):
        typ, tree = key(child), parse(child)
        item_layer = one(tree, 'layer')
        if typ in GRAPHICS and item_layer and item_layer[1] in ['Dwgs.User', 'F.SilkS']:
            edits.append((a, b, ''))
        elif typ == 'property' and tree[1] == 'Reference':
            updated = layer(child, 'F.SilkS')
            if ref == 'S3':
                updated = replace(updated, [(x, y, '(at 10.5 -31.75 0)')
                                            for x, y, element in children(updated) if key(element) == 'at'])
            edits.append((a, b, updated))
        elif item_layer and item_layer[1] in ['Dwgs.User', 'Cmts.User']:
            edits.append((a, b, layer(child, 'F.Fab')))
    updated = replace(raw, edits)
    updated = updated[:updated.rfind(')')] + '\n' + '\n'.join(graphics(clipped, identity)) + '\n)'
    return updated, len(curves), len(clipped)


def main():
    before, after = WORK / 'before', WORK / 'after'
    report = {'switches': {}, 'moved_hidden_metadata': 0, 'moved_backplate_clearance_circles': 0, 'files': {}}
    for filename, ref in SWITCHES.items():
        path = before / (filename + '.kicad_mod')
        updated, count, clipped = transform_switch(path.read_text(), ref, 'library:' + filename)
        (after / path.name).write_text(updated + '\n')
        report['switches'][ref] = {'silk_before_clipping': count, 'silk_after_clipping': clipped, 'stroke_mm': WIDTH}
        target = PARTS / 'footprints/Controls.pretty' / path.name
        report['files'][str(target)] = {'candidate': str(after / path.name), 'sha256_before': hashlib.sha256(path.read_bytes()).hexdigest()}
    board = before / 'powermatic_1200.kicad_pcb'
    original = board.read_text()
    edits = []
    for a, b, raw in children(original):
        typ = key(raw)
        if typ == 'footprint':
            # Avoid parsing unrelated large artwork except when a user-layer
            # field exists, or this is one of the requested switches.
            if '(layer "Dwgs.User")' not in raw and '(layer "Cmts.User")' not in raw and not any(f'(property "Reference" "{r}"' in raw for r in ['S2', 'S3']):
                continue
            tree = parse(raw)
            ref = prop(tree, 'Reference')
            if ref in ['S2', 'S3']:
                updated, _, _ = transform_switch(raw, ref, 'board:' + ref)
            else:
                sub = []
                for x, y, item in children(raw):
                    node = parse(item)
                    item_layer = one(node, 'layer')
                    if not item_layer:
                        continue
                    if node[0] == 'property' and item_layer[1] in ['Dwgs.User', 'Cmts.User']:
                        if node[1] in ['Sheetfile', 'Sheetname']:
                            sub.append((x, y, layer(item, 'F.Fab')))
                            report['moved_hidden_metadata'] += 1
                    elif item_layer[1] in ['Dwgs.User', 'Cmts.User'] and not structural(tree[1]):
                        # These two dashed lines are the enclosure wall section
                        # datum, not disconnect-device detail.
                        if tree[1] == 'Controls:222102_LeftWall' and node[0] == 'fp_line' and one(node, 'stroke') and one(one(node, 'stroke'), 'type')[1] == 'dash':
                            continue
                        destination = 'F.SilkS' if node[0] == 'property' and node[1] == 'Reference' else 'F.Fab'
                        sub.append((x, y, layer(item, destination)))
                updated = replace(raw, sub)
            if updated != raw:
                edits.append((a, b, updated))
        elif typ.startswith('gr_'):
            tree = parse(raw)
            item_layer = one(tree, 'layer')
            if item_layer and item_layer[1] == 'Cmts.User':
                assert typ == 'gr_circle', 'Unclassified comment-layer object'
                edits.append((a, b, layer(raw, 'Dwgs.User')))
                report['moved_backplate_clearance_circles'] += 1
    output = after / board.name
    output.write_text(replace(original, edits))
    target = ROOT / 'kicad/powermatic_1200' / board.name
    report['files'][str(target)] = {'candidate': str(output), 'sha256_before': hashlib.sha256(board.read_bytes()).hexdigest()}
    # Record the owner's explicit layer policy in the governing Controls rules.
    rules = before / 'kicad_rules.csv'
    raw = rules.read_text()
    lines = raw.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(raw, newline=''))
    header = next(reader)
    previous = reader.line_num
    changes = []
    for row in reader:
        end = reader.line_num
        if row[header.index('rule_id')] == 'FP-CTRL-007':
            row[header.index('requirement')] = 'Use KiCad Font at 2.5 x 2.5 mm, 0.15 mm stroke, centered horizontally and vertically. Keep device references horizontal on F.Silkscreen with the elevation artwork. Enclosure, backplate, wire-duct and DIN-rail references may remain on Dwgs.User.'
            stream = io.StringIO(newline='')
            csv.writer(stream, lineterminator='\n').writerow(row)
            changes.append((previous, end, stream.getvalue()))
        previous = end
    assert len(changes) == 1
    for a, b, text in reversed(changes):
        lines[a:b] = [text]
    updated = ''.join(lines).rstrip('\n') + '\n'
    for identity, title, requirement in [
        ('FP-CTRL-009', 'Panel user-layer ownership', 'For panel-layout projects, Dwgs.User contains only enclosure, backplate, wire-duct and DIN-rail information, including enclosure wall sections and backplate mounting/clearance datums. Move hidden device sheet metadata to F.Fab. Cmts.User must be empty.'),
        ('FP-CTRL-010', 'Controls elevation artwork detail', 'For panel-layout Controls, retain the complete source elevation detail on F.Fab. Use the approved Q1-style 0.25 mm F.Silkscreen drawing for major casing profiles, buttons/handles, terminals, brackets, jumpers and plain screw rims. Omit screw slots, threads, engraved legends/numbers and fine molding detail from silkscreen. Keep only the visible Reference field. These Controls elevation exceptions do not define a PCB manufacturing land pattern; apply copper clearance to the rendered stroke where it passes logical wire-target pads.')]:
        assert identity not in raw
        row = {column: '' for column in header}
        row.update({'artifact_type': 'Footprint', 'rule_id': identity, 'rule_title': title, 'requirement': requirement})
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=header, lineterminator='\n').writerow(row)
        updated += stream.getvalue()
    output = after / rules.name
    output.write_text(updated)
    report['files'][str(PARTS / rules.name)] = {'candidate': str(output), 'sha256_before': hashlib.sha256(rules.read_bytes()).hexdigest()}
    (WORK / 'staging.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, indent=2))


if __name__ == '__main__':
    main()
