"""Decode original native views for a local, transformed-copy lead search."""
import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_graphics_v150 import pxl_render
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/local_art_correspondence_v649')


def main():
    pre = read(ROOT / 'preflight.json')
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    clean = NdsImage.open('work/clean.nds')
    assert sha(Path('work/clean.nds').read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    targets, counts = [], {'PXL': 0, 'FLS': 0}
    folder = ROOT / 'Original native source views'
    folder.mkdir(exist_ok=True)
    for _, path, data in clean.iter_files():
        if path.lower().endswith('.pxl'):
            image = pxl_render(data)[0].convert('RGB')
            views = [(None, image, list(image.size), list(image.size))]
            counts['PXL'] += 1
        elif path.lower().endswith('.fls'):
            movie, views = FlsArchive(data), []
            for i, record in enumerate(movie.records):
                texture = movie.texture(i)
                nw, nh = record[0] >> 16, record[1] & 65535
                assert 0 < nw <= texture.width and 0 < nh <= texture.height, (path, i, nw, nh)
                image = texture.render().convert('RGB').crop((0, 0, nw, nh))
                views.append((i, image, [nw, nh], [texture.width, texture.height]))
                counts['FLS'] += 1
        else:
            continue
        for tid, image, native, storage in views:
            target = folder / f'asset_{len(targets):04d}_ORIGINAL_NATIVE.png'
            image.save(target)
            targets.append({'path': path, 'texture': tid, 'source_file_sha256': sha(data),
                'native_size': native, 'storage_size': storage, 'PNG': str(target),
                'PNG_sha256': sha(target.read_bytes()), 'native_crop_only_not_full_scene_composition': True})
    assert counts == {'PXL': 660, 'FLS': 261} and len(targets) == 921
    block = IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    assert len(block) == 21 * 153600
    queries = []
    for i in range(21):
        packed = block[i * 153600:(i + 1) * 153600]
        image = Image.new('RGB', (320, 240))
        image.putdata([bgr555(w)[:3] for w, in struct.iter_unpack('<H', packed)])
        target = folder / f'raw_comic_{i:02d}_ORIGINAL.png'
        image.save(target)
        queries.append({'frame': i, 'source_bytes_sha256': sha(packed), 'PNG': str(target),
                        'PNG_sha256': sha(target.read_bytes())})
    save(ROOT / 'decoded_sources.json', {'counts': counts, 'targets': targets, 'queries': queries,
        'all_original_source_byte_identities_recorded': True,
        'opaque_RGB_preview_alpha_composition_not_inferred': True,
        'not_a_runtime_loader_or_unused_asset_proof': True})
    print('V649 decoded921 original native views and21 raw source frames.', flush=True)


if __name__ == '__main__':
    main()
