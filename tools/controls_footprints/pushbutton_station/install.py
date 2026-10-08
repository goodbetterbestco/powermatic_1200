#!/usr/bin/env python3
"""Install verified S2 assets after checking the saved, paused file checkpoint."""
from pathlib import Path
import hashlib
import json
import shutil
import argparse

ROOT = Path(__file__).resolve().parents[3]
WORK = Path('/private/tmp/powermatic-s2-model')
PARTS = Path.home() / 'Projects/_parts'
REVIEW = ROOT / 'reviews/S2_model_2026-10-08'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Refresh installed footprint/board after checked artwork-only changes')
    args = parser.parse_args()
    staging = json.loads((WORK / 'staging.json').read_text())
    assert (WORK / 'validation.json').is_file()
    assert (WORK / 'native-alignment.json').is_file()
    if args.refresh:
        report = json.loads((REVIEW / 'installed-sha256.json').read_text())
        for name, expected in report.items():
            assert digest(Path(name)) == expected, 'Concurrent installed file edit: ' + name
        targets = {PARTS / 'footprints/Controls.pretty/50MA3KLE_Top.kicad_mod': WORK / 'assets/footprints/Controls.pretty/50MA3KLE_Top.kicad_mod',
                   ROOT / 'kicad/powermatic_1200/powermatic_1200.kicad_pcb': WORK / 'after/powermatic_1200.kicad_pcb'}
        for target, candidate in targets.items():
            shutil.copy2(candidate, target)
            report[str(target)] = digest(target)
            assert digest(target) == digest(candidate)
        (REVIEW / 'installed-sha256.json').write_text(json.dumps(report, indent=2) + '\n')
        print('Refreshed verified S2 footprint styling and board instance.')
        return
    for source, expected in staging['before_sha256'].items():
        assert digest(Path(source)) == expected, 'Concurrent shared file edit: ' + source
    project = ROOT / 'kicad/powermatic_1200'
    for suffix in ['kicad_sch', 'kicad_pcb', 'kicad_pro']:
        name = 'powermatic_1200.' + suffix
        assert digest(project / name) == digest(REVIEW / 'before' / name), 'Concurrent project edit: ' + name
    shared = {Path(source): Path(candidate) for source, candidate in staging['shared_files'].items()}
    shared[PARTS / 'database/non_lcsc_parts.db'] = WORK / 'database/non_lcsc_parts.db'
    for relative in ['footprints/Controls.pretty/50MA3KLE_Top.kicad_mod', '3dmodels/Controls/Furnas_50MA3KLE.step']:
        target = PARTS / relative
        assert not target.exists(), 'New asset already exists: ' + str(target)
        shared[target] = WORK / 'assets' / relative
    for target in shared:
        if target.exists():
            backup = REVIEW / 'shared-before' / target.relative_to(PARTS)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
    report = {}
    for target, candidate in shared.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate, target)
        assert digest(target) == digest(candidate)
        report[str(target)] = digest(target)
    for suffix in ['kicad_sch', 'kicad_pcb']:
        name = 'powermatic_1200.' + suffix
        shutil.copy2(WORK / 'after' / name, project / name)
        assert digest(project / name) == digest(WORK / 'after' / name)
        report[str(project / name)] = digest(project / name)
    (REVIEW / 'installed-sha256.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Installed S2 footprint, colored source model, symbol, catalog and project association.')


if __name__ == '__main__':
    main()
