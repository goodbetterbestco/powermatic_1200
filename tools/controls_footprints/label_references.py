#!/usr/bin/env python3
"""Place Controls reference labels using KiCad's actual stroke-font geometry.

Run with KiCad's bundled Python. Only text records are edited; physical geometry,
pad records, models and board placements are preserved verbatim.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

import pcbnew

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT / 'kicad/powermatic_1200'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')
MM = 1000000


def children(text):
    depth = 0
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
        text = text[:a] + new + text[b:]
    return text


def box(item):
    b = item.GetBoundingBox()
    return b.GetX(), b.GetY(), b.GetX()+b.GetWidth(), b.GetY()+b.GetHeight()


def intersects(a, b, gap=0):
    return a[0]-gap <= b[2] and a[2]+gap >= b[0] and a[1]-gap <= b[3] and a[3]+gap >= b[1]


def placement(fp):
    # Current panel-layout instances have zero rotation. Never silently change
    # an instance's orientation in order to normalize its text.
    assert abs(fp.GetOrientationDegrees()) < 1e-8
    graphics = [g for g in fp.GraphicalItems() if isinstance(g, pcbnew.PCB_SHAPE)]
    assert graphics
    bounds = [box(g) for g in graphics]
    xmin, ymin = min(b[0] for b in bounds), min(b[1] for b in bounds)
    xmax, ymax = max(b[2] for b in bounds), max(b[3] for b in bounds)
    cx, mid = round((xmin+xmax)/2), round((ymin+ymax)/2)
    ref = fp.Reference()
    ref.SetTextSize(pcbnew.VECTOR2I(2500000, 2500000))
    ref.SetTextThickness(150000)
    ref.SetTextAngle(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    ref.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    ref.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    ref.SetPosition(pcbnew.VECTOR2I(cx, 0))
    rb = box(ref)
    # Prefer the complete text box inside the upper half. On very short
    # accessory views only the text center can fit in that half.
    lower, upper = ymin-rb[1]+100000, mid-rb[3]-100000
    full_fit = lower <= upper
    if not full_fit:
        lower, upper = ymin+1, mid-1
    ideal = round((ymin+mid)/2)
    step = 50000  # 0.05 mm vertical placement search; no text grid prescribed.
    candidates = {int(lower), int(upper), max(int(lower), min(ideal, int(upper)))}
    candidates.update(range(math.ceil(lower/step)*step, int(upper)+1, step))
    # Pads are also obstacles so a clear label does not cover a wire target.
    objects = graphics + list(fp.Pads())
    obstacles = [(box(g), g.GetEffectiveShape(pcbnew.F_Cu) if isinstance(g, pcbnew.PAD)
                  else g.GetEffectiveShape()) for g in objects
                 if intersects((rb[0], ymin, rb[2], mid), box(g), 200000)]
    best = None
    for y in sorted(candidates):
        ref.SetPosition(pcbnew.VECTOR2I(cx, y))
        bbox = box(ref)
        shape = ref.GetEffectiveTextShape()
        collisions = near = 0
        for gb, gs in obstacles:
            if not intersects(bbox, gb, 200000):
                continue
            if shape.Collide(gs, 0):
                collisions += 1
            elif shape.Collide(gs, 200000):
                near += 1
        score = (collisions, near, abs(y-ideal))
        if best is None or score < best[0]:
            best = (score, y)
    ref.SetPosition(pcbnew.VECTOR2I(cx, best[1]))
    origin = fp.GetPosition()
    local = [(cx-origin.x)/MM, (best[1]-origin.y)/MM]
    return dict(reference=ref.GetText(), at_mm=local,
                bounds_mm=[(xmin-origin.x)/MM, (ymin-origin.y)/MM,
                           (xmax-origin.x)/MM, (ymax-origin.y)/MM],
                text_box_fits_upper_half=full_fit,
                intersected_shapes=best[0][0], shapes_within_0_2mm=best[0][1])


def fmt(v):
    return f'{v:.6f}'.rstrip('0').rstrip('.') if abs(v) > 0.0000005 else '0'


def text_record(node, place=None):
    edits = []
    seen = set()
    for a, b, c in children(node):
        k = key(c)
        seen.add(k)
        if k == 'hide':
            edits.append((a, b, '' if place else '(hide yes)'))
        elif place and k == 'at':
            edits.append((a, b, '(at '+ ' '.join(fmt(v) for v in place) +' 0)'))
        elif place and k == 'layer':
            edits.append((a, b, '(layer "Dwgs.User")'))
        elif k == 'effects':
            if place:
                new = '(effects (font (size 2.5 2.5) (thickness 0.15)))'
            else:
                # Hide is a direct property child in KiCad 9. Preserve font
                # metadata rather than changing hidden values unnecessarily.
                new = re.sub(r'\s+hide(?=\s|\))', '', c)
            edits.append((a, b, new))
    out = replace(node, edits)
    if not place and 'hide' not in seen:
        out = out[:-1] + ' (hide yes))'
    return out


def edit_footprint(text, record):
    edits = []
    for a, b, c in children(text):
        k = key(c)
        if k == 'property':
            is_ref = c.startswith('(property "Reference"')
            edits.append((a, b, text_record(c, record['at_mm'] if is_ref else None)))
        elif k == 'fp_text':
            # Old-style user text uses a bare hide flag outside effects.
            if not re.search(r'\s+hide(?:\s|\))', c):
                edits.append((a, b, c[:-1]+' hide)'))
    out = replace(text, edits)
    # Every non-text record stays byte-for-byte identical, including placement.
    def physical(s):
        return [c for _, _, c in children(s) if key(c) not in ('property', 'fp_text')]
    assert physical(out) == physical(text)
    return out


def process(path):
    old = path.read_text()
    if path.suffix == '.kicad_mod':
        fp = pcbnew.FootprintLoad(str(path.parent), path.stem)
        assert fp
        record = placement(fp)
        record['name'] = path.stem
        new = edit_footprint(old, record)
        records = [record]
    else:
        board = pcbnew.LoadBoard(str(path))
        footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
        records, edits = [], []
        for a, b, c in children(old):
            if key(c) != 'footprint':
                continue
            ref = re.search(r'\(property "Reference" "([^"]+)"', c)[1]
            record = placement(footprints[ref])
            record['name'] = str(footprints[ref].GetFPID().GetLibItemName())
            records.append(record)
            edits.append((a, b, edit_footprint(c, record)))
        new = replace(old, edits)
        assert len(records) == len(footprints)
    return old, new, records


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paths', nargs='+', type=Path)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--stage', type=Path, help='Stage prepared files without editing their sources')
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    paths = []
    for p in args.paths:
        paths.extend(sorted(p.glob('*.kicad_mod')) if p.is_dir() else [p])
    results = []
    for i, path in enumerate(paths):
        old, new, records = process(path)
        rec = dict(path=str(path.resolve()),
                   before_sha256=hashlib.sha256(old.encode()).hexdigest(),
                   after_sha256=hashlib.sha256(new.encode()).hexdigest(), labels=records)
        if args.stage:
            args.stage.mkdir(parents=True, exist_ok=True)
            dest = args.stage / f'{i:02d}-{path.name}'
            dest.write_text(new)
            rec['prepared'] = str(dest.resolve())
        if args.write:
            path.write_text(new)
        results.append(rec)
        print(path.name, [(r['reference'], r['at_mm'], r['intersected_shapes']) for r in records], flush=True)
    if args.report:
        args.report.write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
