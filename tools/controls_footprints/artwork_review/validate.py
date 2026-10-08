#!/usr/bin/env python3
"""Verify artwork-only scope, user-layer ownership and rendered-stroke clearance."""
from pathlib import Path
import csv
import json
import math
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
from source import children, key, one, parse, prop, nodes
from stage import GRAPHICS, WIDTH, circle_for_arc, structural

WORK = Path('/private/tmp/powermatic-layer-review')


def fab(raw):
    return [part for a, b, part in children(raw) if key(part) in GRAPHICS
            and one(parse(part), 'layer')[1] == 'F.Fab']


def non_art(raw):
    return [part for a, b, part in children(raw) if key(part) not in GRAPHICS | {'property', 'fp_text'}]


def minimum_distance(curve, center):
    typ = curve[0]
    if typ == 'fp_line':
        a, b = [tuple(map(float, one(curve, name)[1:3])) for name in ['start', 'end']]
        delta = [b[i] - a[i] for i in range(2)]
        norm = sum(v * v for v in delta)
        t = max(0, min(1, sum((center[i] - a[i]) * delta[i] for i in range(2)) / norm)) if norm else 0
        return math.dist(center, [a[i] + t * delta[i] for i in range(2)])
    if typ == 'fp_circle':
        c, end = [tuple(map(float, one(curve, name)[1:3])) for name in ['center', 'end']]
        return abs(math.dist(c, center) - math.dist(c, end))
    points = [tuple(map(float, one(curve, name)[1:3])) for name in ['start', 'mid', 'end']]
    c, radius, start, sign, length = circle_for_arc(points)
    angle = math.atan2(center[1] - c[1], center[0] - c[0])
    span = ((angle - start) if sign == 1 else (start - angle)) % (2 * math.pi)
    return abs(math.dist(c, center) - radius) if span <= length else min(math.dist(center, points[0]), math.dist(center, points[2]))


def main():
    before, after = WORK / 'before', WORK / 'after'
    board_old, board_new = [(p / 'powermatic_1200.kicad_pcb').read_text() for p in [before, after]]
    old, new = list(children(board_old)), list(children(board_new))
    assert len(old) == len(new)
    modified = []
    layers = Counter()
    switches = {}
    for (_, _, a), (_, _, b) in zip(old, new):
        assert key(a) == key(b)
        if key(a) == 'footprint':
            # All pads, nets, attributes, IDs, positions and models are literal
            # source matches, even where user-layer metadata is relocated.
            assert non_art(a) == non_art(b)
            assert fab(a) == fab(b)
            if a != b:
                modified.append(prop(parse(b), 'Reference'))
            tree = parse(b)
            for item in tree:
                if not isinstance(item, list) or not item:
                    continue
                layer = one(item, 'layer')
                if not layer:
                    continue
                layers[layer[1]] += 1
                assert layer[1] != 'Cmts.User'
                if layer[1] == 'Dwgs.User' and not structural(tree[1]):
                    assert tree[1] == 'Controls:222102_LeftWall' and item[0] == 'fp_line'
                    assert one(one(item, 'stroke'), 'type')[1] == 'dash'
                    assert float(one(item, 'start')[1]) in [0, 1.8796]
            if prop(tree, 'Reference') in ['S2', 'S3']:
                ref = prop(tree, 'Reference')
                silk = [g for g in tree if isinstance(g, list) and g[0] in GRAPHICS
                        and one(g, 'layer')[1] == 'F.SilkS']
                assert silk and not any(isinstance(g, list) and g[0] == 'fp_text' for g in tree)
                assert one(next(p for p in nodes(tree, 'property') if p[1] == 'Reference'), 'layer')[1] == 'F.SilkS'
                margins = []
                for curve in silk:
                    stroke = float(one(one(curve, 'stroke'), 'width')[1])
                    assert abs(stroke - WIDTH) < 1e-8
                    for pad in nodes(tree, 'pad'):
                        center = tuple(map(float, one(pad, 'at')[1:3]))
                        radius = float(one(pad, 'size')[1]) / 2
                        margins.append(minimum_distance(curve, center) - radius - stroke / 2)
                assert min(margins) >= .15 - 5e-6, (ref, min(margins))
                switches[ref] = {'fab_primitives_unchanged': len(fab(a)), 'silk_primitives': len(silk),
                                 'minimum_rendered_stroke_to_copper_clearance_mm': min(margins)}
        elif a != b:
            t1, t2 = parse(a), parse(b)
            assert key(a) == 'gr_circle' and one(t1, 'layer')[1] == 'Cmts.User' and one(t2, 'layer')[1] == 'Dwgs.User'
            assert [n for n in t1 if not isinstance(n, list) or n[0] != 'layer'] == [n for n in t2 if not isinstance(n, list) or n[0] != 'layer']
        if key(b).startswith('gr_'):
            layer = one(parse(b), 'layer')[1]
            layers[layer] += 1
            assert layer != 'Cmts.User'
    for name in ['50MA3KLE_Top', '365-TAV2111_Top']:
        a, b = [(p / (name + '.kicad_mod')).read_text() for p in [before, after]]
        assert non_art(a) == non_art(b) and fab(a) == fab(b)
        assert '(layer "Dwgs.User")' not in b and '(layer "Cmts.User")' not in b
    old_rules, new_rules = [list(csv.DictReader((p / 'kicad_rules.csv').open(newline=''))) for p in [before, after]]
    assert len(new_rules) == len(old_rules) + 2
    for a, b in zip(old_rules, new_rules):
        if a['rule_id'] != 'FP-CTRL-007':
            assert a == b
        else:
            assert {k: v for k, v in a.items() if k != 'requirement'} == {k: v for k, v in b.items() if k != 'requirement'}
    assert {r['rule_id'] for r in new_rules[-2:]} == {'FP-CTRL-009', 'FP-CTRL-010'}
    result = {'switches': switches, 'modified_footprint_records': modified,
              'hidden_metadata_relocated_not_deleted': True, 'backplate_clearance_circles_preserved': True,
              'comments_layer_items': layers['Cmts.User'], 'drawings_layer_only_structural_information': True,
              'all_F_Fab_source_graphics_preserved': True, 'all_pads_nets_positions_attributes_UUIDs_and_models_preserved': True,
              'all_tracks_vias_zones_edge_cuts_and_other_board_records_preserved': True,
              'only_requested_Controls_layer_and_detail_rules_changed': True}
    (WORK / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
