"""Restore reviewed original plaque margins without glyph-shaped texture seams."""
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-local-plaque-texture-v1':
        raise ValueError('Unknown local plaque texture format')
    outputs, reports = {}, []
    for group in config['files']:
        path = group['file_path']
        data = candidate.read_file(path)
        original_data = clean.read_file(path)
        if sha(data) != group['source_sha256'] or sha(original_data) != group['clean_sha256']:
            raise ValueError('Original or inherited plaque atlas differs: ' + path)
        image, original = PxlImage.from_bytes(data), PxlImage.from_bytes(original_data)
        before = bytes(image.indices)
        owned = set()
        for row in group['records']:
            l, t, r, b = row['localized_plaque']
            sx, sy, ex, ey = row['source_interior']
            pl, pt, pr, pb = row['conservative_protected_Japanese_band']
            for x, y, old, new in row['changes']:
                at = y * image.width + x
                if at in owned or before[at] != old or old == 1 or new == 1:
                    raise ValueError('Plaque change overlaps ink or another owned point')
                if not (l + 2 <= x < r - 2 and t + 2 <= y < b - 2 and
                        sx <= x < ex and sy <= y < ey):
                    raise ValueError('Plaque change exceeds source interior or touches a border')
                if pl <= x < pr and pt <= y < pb:
                    raise ValueError('Plaque change enters protected Japanese reconstruction band')
                rgb = original.palette[original.indices[y * original.width + x]]
                if sum(rgb[:3]) < 286 or image.palette[new] != rgb:
                    raise ValueError('Plaque change does not restore exact original material colour')
                image.indices[at] = new
                owned.add(at)
        if any(a != b for i, (a, b) in enumerate(zip(before, image.indices, strict=True)) if i not in owned):
            raise ValueError('Plaque change affected unowned pixels')
        output = image.to_bytes()
        if output[:image.pixels_offset] != data[:image.pixels_offset] or sha(output) != group['target_sha256']:
            raise ValueError('Plaque metadata or reviewed target differs')
        outputs[path] = output
        reports.append({'file_path': path, 'source_sha256': sha(data), 'target_sha256': sha(output),
                        'changed_records': [r['id'] + '_SOURCE_MARGIN' for r in group['records'] if r['changes']],
                        'original_material_pixels_restored': len(owned),
                        'letters_borders_palette_geometry_and_unowned_pixels_retained': True})
    return outputs, reports
