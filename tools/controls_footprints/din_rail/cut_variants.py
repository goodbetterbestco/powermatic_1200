#!/usr/bin/env python3
"""Stage the user-supplied cut rail/duct models and exact front projections."""
import argparse
import csv
import hashlib
import io
import json
import shutil
from pathlib import Path

from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from end_origin import mass, model_node, project
from normalize_devices import bounds, count, read_shape, transform, vertex_error, write_placed_step

SPECS = [('DN-R35S1_280mm', 280, 35, 7.5),
         ('T1-1530G1-1_300mm', 300, 40, 80),
         ('T1-1530G1-1_360mm', 360, 40, 80)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=Path.home()/'Downloads')
    parser.add_argument('--parts', type=Path, default=Path.home()/'Projects/_parts')
    parser.add_argument('--output', type=Path, default=Path('/tmp/powermatic-cut-variants'))
    a = parser.parse_args()
    models = a.output/'3dmodels/Controls'
    fps = a.output/'footprints/Controls.pretty'
    review = a.output/'reviews/Controls/Rail_Duct_EndOrigin'
    for p in [models, fps, review, a.output/'database']:
        p.mkdir(parents=True, exist_ok=True)
    # All supplied cuts have length along +Y, back mounting plane Z=0.
    matrix = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    trsf = transform(matrix, [0, 0, 0])
    report = []
    for part, length, width, height in SPECS:
        source = a.sources/(part+'.step')
        src = read_shape(source)
        assert BRepCheck_Analyzer(src).IsValid()
        source_box = [-width/2, 0, 0, width/2, length, height]
        assert max(abs(x-y) for x,y in zip(bounds(src), source_box)) < 1e-5
        shutil.copy2(source, models/source.name)
        assert sha(source) == sha(models/source.name)
        derived = models/(part+'_LeftOrigin.step')
        write_placed_step(source, derived, trsf)
        shape = read_shape(derived)
        expected = BRepBuilderAPI_Transform(src, trsf, True).Shape()
        target = [0, -width/2, 0, length, width/2, height]
        assert BRepCheck_Analyzer(shape).IsValid()
        assert max(abs(x-y) for x,y in zip(bounds(shape), target)) < 1e-5
        for kind in [TopAbs_SOLID, TopAbs_FACE]:
            assert count(shape, kind) == count(src, kind)
        err = max(vertex_error(shape, expected), vertex_error(expected, shape))
        volume_error = abs(mass(shape)-mass(expected))/mass(expected)
        assert volume_error < 5e-5, volume_error
        graphics = project(shape)
        name = part+'_Front'
        label_y = -8 if part.startswith('DN-') else -10
        desc = 'DIN rail' if part.startswith('DN-') else 'Wire duct with cover'
        text = f'''(footprint "{name}"
  (version 20241229)
  (generator "pcbnew")
  (generator_version "9.0")
  (layer "F.Cu")
  (descr "{desc}; {length} x {width} x {height:g} mm user STEP envelope; origin at center of left rear edge; length along +X")
  (tags "Controls mechanical {part}")
  (attr board_only exclude_from_pos_files exclude_from_bom)
  (property "Reference" "REF**" (at {length/2:g} {label_y}) (layer "Dwgs.User")
    (effects (font (size 2.5 2.5) (thickness 0.15))))
  (property "Value" "{name}" (at {length/2:g} {width/2+2:g}) (layer "Dwgs.User") (hide yes)
    (effects (font (size 2.5 2.5) (thickness 0.15))))
{chr(10).join(graphics)}
{model_node(derived.name)})
'''
        (fps/(name+'.kicad_mod')).write_text(text)
        entry = dict(part=part, source=source.name, source_sha256=sha(source),
                     derived=derived.name, derived_sha256=sha(derived),
                     source_bounds_mm=bounds(src), bounds_mm=bounds(shape),
                     matrix=matrix, offset_mm=[0,0,0], scale=1,
                     solids=count(shape,TopAbs_SOLID), faces=count(shape,TopAbs_FACE),
                     valid=True, max_vertex_error_mm=err, relative_volume_error=volume_error,
                     footprint='Controls:'+name, graphic_count=len(graphics))
        report.append(entry)
        print(json.dumps(entry), flush=True)
    (review/'cut_variants_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    csv_path = a.parts/'database/non_lcsc_parts.csv'
    original = csv_path.read_text()
    reader = csv.DictReader(io.StringIO(original))
    rows = list(reader)
    mapping = {s[0]:'Controls:'+s[0]+'_Front' for s in SPECS}
    found = set()
    for row in rows:
        if row['PartID'] in mapping:
            assert not row['Footprint'] or row['Footprint'] == mapping[row['PartID']]
            row['Footprint'] = mapping[row['PartID']]
            found.add(row['PartID'])
    assert found == set(mapping)
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, reader.fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    (a.output/'database/non_lcsc_parts.csv').write_text(out.getvalue())
    plan_path = a.parts/'reviews/Controls/Rail_Duct_EndOrigin/catalog_plan.json'
    plan = json.loads(plan_path.read_text())
    plan['pending_step_files'] = []
    plan['status'] = 'All five rail and duct lengths have catalog footprints and aligned models. Cut-variant originals retained; derived models rotated into +X with zero footprint model offsets and rotation. Board placement unchanged.'
    plan['cut_variant_validation'] = 'cut_variants_validation.json'
    (review/'catalog_plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    manifest = []
    for staged in sorted(a.output.rglob('*')):
        if staged.is_file() and staged.name != 'install_manifest.json':
            relative = staged.relative_to(a.output)
            target = a.parts/relative
            manifest.append(dict(path=str(relative), staged_sha256=sha(staged),
                                 before_sha256=sha(target) if target.exists() else None))
    (a.output/'install_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    main()
