#!/usr/bin/env python3
"""Assign only SW1/H1/J1 and replace their saved PCB graphics/model/pad locations.

Preserves the surrounding files verbatim, including existing placements, nets,
UUIDs and user fields. No enclosure placement is inferred from the working PCB.
"""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROJECT = ROOT/'kicad/powermatic_1200'
SPECS = json.loads((HERE/'geometry.json').read_text())
BACKUP = Path('/tmp/powermatic-left-wall-before')
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')


def children(text):
    depth = 0
    start = None
    for m in TOKEN.finditer(text):
        if m[0] == '(':
            if depth == 1:
                start = m.start()
            depth += 1
        elif m[0] == ')':
            depth -= 1
            if depth == 1:
                yield start, m.end(), text[start:m.end()]
    assert depth == 0


def key(node):
    return next(TOKEN.finditer(node[1:]))[0]


def replace(text, edits):
    for a, b, new in sorted(edits, reverse=True):
        text = text[:a]+new+text[b:]
    return text


def field(node, name):
    m = re.search(r'\(property "'+re.escape(name)+r'" "([^"\n]*)"', node)
    return m[1] if m else None


def footprint(old, s):
    fresh = (Path.home()/'Projects/_parts/footprints/Controls.pretty'/(s['name']+'.kicad_mod')).read_text()
    fresh_nodes = [c for _, _, c in children(fresh)]
    fresh_pads = {re.match(r'\(pad "([^"\n]*)"', c)[1]: c for c in fresh_nodes if key(c) == 'pad'}
    old_ids = [re.match(r'\(pad "([^"\n]*)"', c)[1] for _, _, c in children(old) if key(c) == 'pad']
    assert sorted(old_ids) == sorted(fresh_pads)
    physical = {'fp_line','fp_arc','fp_circle','fp_rect','fp_poly','fp_curve','model'}
    edits = []
    for a, b, c in children(old):
        k = key(c)
        if k in physical:
            edits.append((a, b, ''))
        elif k == 'pad':
            n = re.match(r'\(pad "([^"\n]*)"', c)[1]
            at = re.search(r'\(at [^)]*\)', fresh_pads[n])[0]
            edits.append((a, b, re.sub(r'\(at [^)]*\)', lambda m: at, c, count=1)))
        elif k == 'property' and (c.startswith('(property "Reference"') or c.startswith('(property "Value"')):
            field_name = 'Reference' if c.startswith('(property "Reference"') else 'Value'
            f = next(v for v in fresh_nodes if v.startswith('(property "'+field_name+'"'))
            at = re.search(r'\(at [^)]*\)', f)[0]
            edits.append((a, b, re.sub(r'\(at [^)]*\)', lambda m: at, c, count=1)))
        elif k in ['descr', 'tags']:
            edits.append((a, b, next(v for v in fresh_nodes if key(v) == k)))
    out = replace(old, edits)
    out = re.sub(r'^\(footprint "[^"]*"', '(footprint "Controls:'+s['name']+'"', out, count=1)
    # Collapse only whitespace left by removed drawing records in this footprint.
    out = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*', '\n', out)
    out = out.rstrip()[:-1].rstrip()+'\n\t\t'+'\n\t\t'.join(v for v in fresh_nodes if key(v) in physical)+'\n\t)'
    return out


def main():
    specs = {s['ref']: s for s in SPECS}
    results = []
    for filename, kind in [('powermatic_1200.kicad_sch', 'symbol'), ('powermatic_1200.kicad_pcb', 'footprint')]:
        path = PROJECT/filename
        original = path.read_text()
        edits, seen = [], set()
        for a, b, node in children(original):
            if key(node) != kind or field(node, 'Reference') not in specs:
                continue
            ref = field(node, 'Reference'); s = specs[ref]
            assert field(node, 'Value') == s['part']
            if kind == 'symbol':
                new, n = re.subn(r'(\(property "Footprint" ")[^"]*(")',
                                lambda m: m[1]+'Controls:'+s['name']+m[2], node)
                assert n == 1
            else:
                assert re.search(r'\(at [-\d.]+ [-\d.]+\)', node)
                new = footprint(node, s)
            edits.append((a, b, new)); seen.add(ref)
        assert seen == set(specs), seen
        updated = replace(original, edits)
        assert len(list(children(original))) == len(list(children(updated)))
        old_nodes = list(children(original)); new_nodes = list(children(updated))
        for (_, _, old), (_, _, new) in zip(old_nodes, new_nodes):
            if key(old) == kind and field(old, 'Reference') in specs:
                continue
            assert old == new
        BACKUP.mkdir(exist_ok=True)
        backup = BACKUP/filename
        if not backup.exists():
            backup.write_text(original)
        # Catch a concurrent save before applying the prepared edit.
        assert path.read_text() == original, 'File changed during edit'
        path.write_text(updated)
        results.append(dict(file=filename, references=sorted(seen),
                            before_sha256=hashlib.sha256(original.encode()).hexdigest(),
                            after_sha256=hashlib.sha256(updated.encode()).hexdigest(),
                            other_top_level_records_unchanged=True))
        print(filename, 'updated', ', '.join(sorted(seen)))
    (HERE/'installation.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
