"""Rank original PXL/FLS images as leads for raw-comic display counterparts.

This is a visual similarity search, not an exhaustive exclusion of atlas crops,
composed images, alpha variants or other formats.
"""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_graphics_v150 import pxl_render

OUT = Path('work/analysis/comic_current_v506')


def main():
    clean_path = Path('work/clean.nds')
    clean = NdsImage.open(clean_path)
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assets = []
    for _, path, raw in clean.iter_files():
        if path.lower().endswith('.pxl'):
            assets.append((path, None, pxl_render(raw)[0].convert('RGB')))
        elif path.lower().endswith('.fls'):
            archive = FlsArchive(raw)
            for index in range(archive.count):
                if path == '/m02_03.fls':
                    assert archive.records == [[33554433, 377, 0, 512, 512, 262144]]
                    start = archive.data_offset
                    palette = [bgr555(v)[:3] for v, in struct.iter_unpack('<H', raw[start:start+512])]
                    image = Image.new('RGB', (512,512))
                    image.putdata([palette[v] for v in raw[start+512:]])
                else:
                    image = archive.texture(index).render().convert('RGB')
                assets.append((path, index, image))
    assert len(assets) == 921
    small = [im.resize((32,24), Image.Resampling.BOX) for _, _, im in assets]
    block = IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    rows = []
    for frame in range(21):
        raw = block[frame*153600:(frame+1)*153600]
        rgb = bytes(c for w, in struct.iter_unpack('<H', raw) for c in bgr555(w)[:3])
        source = Image.frombytes('RGB', (320,240), rgb)
        reference = source.resize((32,24), Image.Resampling.BOX)
        ranked = sorted((sum(ImageStat.Stat(ImageChops.difference(reference, im)).sum2), i)
                        for i, im in enumerate(small))[:4]
        page = Image.new('RGB', (640, 780), '#dddddd')
        draw = ImageDraw.Draw(page)
        page.paste(source, (0,20))
        draw.text((4,4), f'Raw source frame {frame}; visual-search leads only', fill='black')
        hits = []
        for rank, (distance, index) in enumerate(ranked):
            path, texture, image = assets[index]
            thumb = image.copy()
            thumb.thumbnail((320,240), Image.Resampling.NEAREST)
            x, y = (rank%2)*320, 280+(rank//2)*250
            page.paste(thumb, (x, y+20))
            draw.text((x+3,y+3), f'{path} texture {texture}', fill='black')
            hits.append({'path': path, 'texture': texture, 'dimensions': list(image.size),
                         'RGB_mean_squared_error': distance/(32*24*3)})
        page.save(OUT / f'copy_leads_frame_{frame:02d}.png')
        rows.append({'frame': frame, 'source_frame_sha256': sha(raw), 'closest_whole_images': hits})
    proof = {'clean_sha256': sha(clean_path.read_bytes()), 'all921_original_assets_ranked': True,
             'method': '32x24 BOX-filtered whole-storage RGB squared distance; top four leads per frame',
             'frames': rows, 'visual_similarity_not_identity_or_loading_proof': True,
             'atlas_crops_composition_alpha_and_other_formats_not_excluded': True,
             'unused_resource_claim': False, 'production_ROM_unchanged': True}
    (OUT / 'copy_leads.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print('Ranked all 921 original PXL/FLS assets against all 21 raw comic frames.')


if __name__ == '__main__':
    main()
