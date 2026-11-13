"""Apply reviewed full ship plaque faces within their historical erase ownership."""
import json
import zlib
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ship-plaque-texture-v1':
        raise ValueError('Unknown ship plaque texture format')
    path = config['file_path']
    data, original = candidate.read_file(path), clean.read_file(path)
    if sha(data) != config['source_sha256'] or sha(original) != config['clean_sha256']:
        raise ValueError('Inherited or original ship plaque atlas differs')
    if sha(clean.read_file('/_pxl/towninfo.pxl')) != config['donor_sha256']:
        raise ValueError('Ship plaque original grain/bevel donor differs')
    image = PxlImage.from_bytes(data)
    before = bytes(image.indices)
    owned = set()
    for row in config['records']:
        l, t, r, b = row['box']
        pixels = zlib.decompress(bytes.fromhex(row['reviewed_indices_zlib_hex']))
        if not (0 <= l < r <= image.width and 0 <= t < b <= image.height) or len(pixels) != (r-l)*(b-t):
            raise ValueError('Ship plaque region escapes original ownership')
        for y in range(t, b):
            for x in range(l, r):
                at = y * image.width + x
                value = pixels[(y-t)*(r-l)+x-l]
                if at in owned and image.indices[at] != value:
                    raise ValueError('Overlapping plaque restoration regions disagree')
                image.indices[at] = value
                owned.add(at)
    for row in config['records']:
        l, _, r, _ = row['box']
        t, b = row['font_band']
        expected = {tuple(p) for p in row['expected_ink']}
        prior = {(x, y) for y in range(t, b) for x in range(l, r) if before[y*image.width+x] == 1}
        actual = {(x, y) for y in range(t, b) for x in range(l, r) if image.indices[y*image.width+x] == 1}
        structural = set()
        if row.get('source_divider_row_verified') == 143:
            source = PxlImage.from_bytes(original)
            if any(image.indices[143*image.width+x] != source.indices[143*source.width+x] for x in range(l, r)):
                raise ValueError('Original Hull divider changed')
            structural = {(x, 143) for x in range(l, r) if source.indices[143*source.width+x] == 1}
        if prior != expected or actual != expected | structural:
            raise ValueError('Ship plaque complete English mask changed')
    if any(a != b for n, (a, b) in enumerate(zip(before, image.indices, strict=True)) if n not in owned):
        raise ValueError('Ship plaque changed unowned pixels')
    output = image.to_bytes()
    if output[:image.pixels_offset] != data[:image.pixels_offset] or sha(output) != config['target_sha256']:
        raise ValueError('Reviewed ship plaque target or metadata differs')
    return path, output, {'file_path': path, 'source_sha256': sha(data), 'target_sha256': sha(output),
                          'changed_records': [r['id'] + '_SOURCE_TEXTURE' for r in config['records']],
                          'all11_English_masks_and_positions_retained': True,
                          'header_palette_geometry_and_unowned_pixels_retained': True}
