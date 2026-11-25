"""Inspect separate palette/pixel storage pairs without asserting native usage."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.rom.nds import NdsImage

SOURCE = 'd61241e3f9d29debcc41cedcf7824aa06ac36e5e07643c714e7b045465c40345'
CLEAN = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
OUT = Path('work/analysis/external_palette_graphics_v151')
PAIRS = [('/GRP/CMMNIMG.DK4', 4, 5), ('/GRP/MAPPOINT.DK4', 0, 1),
         ('/GRP/MAPPOINT.DK4', 2, 3)]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    current_path = Path('out/all_routes_combined_v151_candidate.nds')
    clean_path = Path('work/clean.nds')
    if sha(current_path.read_bytes()) != SOURCE or sha(clean_path.read_bytes()) != CLEAN:
        raise ValueError('Exact saved V151 and clean ROM required')
    rom = NdsImage.open(current_path)
    clean = NdsImage.open(clean_path)
    loose = []
    for version, image in [('current', rom), ('clean', clean)]:
        for _, name, raw in image.iter_files():
            if name.lower().endswith('.pxl') and struct.unpack_from('<I', raw)[0] & 255 == 4:
                loose.append((version, name, PxlImage.from_bytes(raw)))
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for path, palette_block, pixels_block in PAIRS:
        archive_raw = rom.read_file(path)
        archive = IlnkContainer.parse(archive_raw)
        if archive.to_bytes() != archive_raw:
            raise ValueError('Archive reconstruction mismatch')
        palette_raw = archive.blocks[palette_block]
        pixels_raw = archive.blocks[pixels_block]
        pk, pm, ps, pf, pw, ph = struct.unpack_from('<IIIIHH', palette_raw)
        ik, im, extent, flags, width_words, height = struct.unpack_from('<IIIIHH', pixels_raw)
        if (pk, pm, pw) != (19, 2, 16) or len(palette_raw) != ps + 8:
            raise ValueError('Separate palette header differs')
        if len(palette_raw) != 20 + pw * ph * 2:
            raise ValueError('Separate palette extent differs')
        if (ik, im) != (18, 0) or len(pixels_raw) != extent + 8:
            raise ValueError('Separate pixel header differs')
        if len(pixels_raw) != 20 + width_words * height * 2:
            raise ValueError('Separate pixel extent differs')
        # This is the packed-four-bit interpretation. Native bank selection is open.
        packed = pixels_raw[20:]
        indices = bytes(part for value in packed for part in (value & 15, value >> 4))
        width = width_words * 4
        if bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2)) != packed:
            raise ValueError('Packed-four-bit reconstruction mismatch')
        colors = [bgr555(v) for v, in struct.iter_unpack('<H', palette_raw[20:52])]
        preview = Image.new('RGBA', (width, height))
        preview.putdata([colors[v] for v in indices])
        output = OUT / f'asset_{len(rows):02d}.png'
        preview.save(output)
        matches = []
        for version, name, pxl in loose:
            if pxl.height != height or pxl.width > width:
                continue
            for x in range(0, width - pxl.width + 1, pxl.width):
                region = b''.join(indices[y * width + x:y * width + x + pxl.width]
                                  for y in range(height))
                if region == bytes(pxl.indices):
                    matches.append({'version': version, 'path': name, 'x': x,
                                    'width': pxl.width, 'height': height,
                                    'exact_indices': True,
                                    'palette_or_native_consumer_equivalence_proved': False})
        rows.append({'path': path, 'archive_sha256': sha(archive_raw),
                     'palette_block': palette_block, 'palette_block_sha256': sha(palette_raw),
                     'pixels_block': pixels_block, 'pixels_block_sha256': sha(pixels_raw),
                     'palette_banks_16_colors': ph, 'palette_flags_unclassified': pf,
                     'pixel_flags_unclassified': flags, 'width': width, 'height': height,
                     'packed_depth_interpretation': 4, 'pixel_repack_exact': True,
                     'preview_palette_bank': 0, 'preview': str(output),
                     'preview_sha256': sha(output.read_bytes()),
                     'exact_loose_regions': matches, 'visual_review': 'pending',
                     'native_pairing_palette_selection_and_composition_proved': False})
    page = Image.new('RGB', (1040, 550), '#343434')
    draw = ImageDraw.Draw(page)
    for i, row in enumerate(rows):
        p = Image.open(row['preview']).convert('RGB')
        x, y = (8, 30) if i == 0 else (560, 30 + (i - 1) * 250)
        draw.text((x, y - 22), f"{row['path']} blocks {row['palette_block']}/{row['pixels_block']}", fill='white')
        page.paste(p, (x, y))
    sheet = OUT / 'sheet.png'
    page.save(sheet)
    report = {'source_rom_sha256': SOURCE, 'clean_rom_sha256': CLEAN,
              'observed_storage_pairs': rows, 'sheet': str(sheet),
              'sheet_sha256': sha(sheet.read_bytes()),
              'limitations': ['Adjacent palette/pixel blocks are storage hypotheses, not native loader proof.',
                              'Bank-zero color previews do not map all palette banks or alpha.',
                              'No native screen cropping, formatting or integration approval.']}
    (OUT / 'inventory.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'storage_pairs': len(rows), 'classified_blocks': len(rows) * 2,
                      'loose_regions': [r['exact_loose_regions'] for r in rows]}, indent=2))


if __name__ == '__main__':
    main()
