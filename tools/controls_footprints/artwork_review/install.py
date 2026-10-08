#!/usr/bin/env python3
"""Install reviewed artwork/layer changes with saved-checkpoint hash guards."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
WORK = Path('/private/tmp/powermatic-layer-review')
REVIEW = ROOT / 'reviews/artwork_layers_2026-10-08'
PARTS = Path.home() / 'Projects/_parts'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((WORK / 'staging.json').read_text())
    assert (WORK / 'validation.json').is_file()
    for name, item in manifest['files'].items():
        assert digest(Path(name)) == item['sha256_before'], 'Concurrent edit: ' + name
    for name, expected in manifest['immutable_sources'].items():
        assert digest(Path(name)) == expected, 'Concurrent source edit: ' + name
    REVIEW.mkdir(parents=True, exist_ok=True)
    shutil.copytree(WORK / 'before', REVIEW / 'before', dirs_exist_ok=True)
    shutil.copytree(WORK / 'after', REVIEW / 'after', dirs_exist_ok=True)
    for name in ['validation.json', 'artwork-source.json', 'S2-silk-curves.json', 'S3-silk-curves.json']:
        shutil.copy2(WORK / name, REVIEW / name)
    for name, item in manifest['files'].items():
        source, candidate = Path(name), Path(item['candidate'])
        shutil.copy2(candidate, source)
        item['sha256_after'] = digest(source)
        assert source.read_bytes() == candidate.read_bytes()
    for name, expected in manifest['immutable_sources'].items():
        assert digest(Path(name)) == expected
    (REVIEW / 'installed.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Installed S2/S3 silkscreens, enclosure-only user layers, empty comments layer and Controls layer/detail rules.')


if __name__ == '__main__':
    main()
