"""Source-pinned storage previews of legacy ILNK graphics; no native-use claims."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.rom.nds import NdsImage

SOURCE = 'd61241e3f9d29debcc41cedcf7824aa06ac36e5e07643c714e7b045465c40345'
OUT = Path('work/analysis/embedded_graphics_v151')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    kind, mode, palette_field = struct.unpack_from('<3I', raw)
    if kind != 16 or mode not in (8, 9):
        return None
    depth = 4 if mode == 8 else 8
    palette_size = palette_field - 12
    bank_size = 32 if depth == 4 else 512
    if palette_size < bank_size or palette_size % bank_size:
        raise ValueError('Palette extent is not a whole bank')
    info_offset = palette_field + 8
    extent, flags, width_words, height = struct.unpack_from('<IIHH', raw, info_offset)
    width = width_words * (16 // depth)
    payload_offset = info_offset + 12
    payload_size = width_words * 2 * height
    if not width or not height or extent != payload_size + 12:
        raise ValueError('Legacy pixel extent disagrees with dimensions')
    if payload_offset + payload_size > len(raw):
        raise ValueError('Legacy image crosses the block boundary')
    packed = raw[payload_offset:payload_offset + payload_size]
    indices = packed if depth == 8 else bytes(
        part for value in packed for part in (value & 15, value >> 4))
    repacked = indices if depth == 8 else bytes(
        indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2))
    if repacked != packed or len(indices) != width * height:
        raise ValueError('Pixel decode/repack mismatch')
    palette = raw[20:20 + palette_size]
    if len(palette) != palette_size or 20 + palette_size != info_offset:
        raise ValueError('Palette overlaps dimension metadata')
    return {'depth': depth, 'width': width, 'height': height,
            'palette_banks': palette_size // bank_size, 'flags_unclassified': flags,
            'palette_offset': 20, 'palette_bytes': palette_size,
            'pixels_offset': payload_offset, 'pixels_bytes': payload_size,
            'unclassified_trailing_bytes': len(raw) - payload_offset - payload_size,
            'packed_sha256': sha(packed), 'palette_sha256': sha(palette),
            'indices': indices, 'palette': palette}


def main():
    path = Path('out/all_routes_combined_v151_candidate.nds')
    if sha(path.read_bytes()) != SOURCE:
        raise ValueError('Exact V151 required')
    rom = NdsImage.open(path)
    loose = []
    for _, name, raw in rom.iter_files():
        if name.lower().endswith('.pxl') and struct.unpack_from('<I', raw)[0] & 255 in (4, 8):
            p = PxlImage.from_bytes(raw)
            palette = raw[20:p.pixels_offset]
            loose.append((name, p, palette))
    OUT.mkdir(parents=True, exist_ok=True)
    rows, previews = [], []
    for _, name, raw in rom.iter_files():
        if not name.startswith('/GRP/') or not raw.startswith(b'ILNK'):
            continue
        archive = IlnkContainer.parse(raw)
        if archive.to_bytes() != raw:
            raise ValueError('Archive roundtrip differs')
        for index, block in enumerate(archive.blocks):
            row = {'path': name, 'archive_sha256': sha(raw), 'block_index': index,
                   'block_sha256': sha(block), 'block_bytes': len(block),
                   'visual_review': 'pending', 'native_use': 'unproved'}
            decoded = decode(block)
            if decoded is None:
                row['format_status'] = 'unclassified-no-preview'
                rows.append(row)
                continue
            indices = decoded.pop('indices')
            palette = decoded.pop('palette')
            row.update(decoded)
            row['format_status'] = 'bounded-type16-storage-image'
            row['exact_indexed_loose_matches'] = []
            for loose_name, pxl, loose_palette in loose:
                if (pxl.width, pxl.height, pxl.bits_per_pixel, bytes(pxl.indices)) == (
                        row['width'], row['height'], row['depth'], indices):
                    row['exact_indexed_loose_matches'].append({
                        'path': loose_name, 'palette_exact': palette == loose_palette})
            # Bank zero is only a storage preview; bank selection/alpha is unproved.
            bank_bytes = 32 if row['depth'] == 4 else 512
            colors = [bgr555(v) for v, in struct.iter_unpack('<H', palette[:bank_bytes])]
            preview = Image.new('RGBA', (row['width'], row['height']))
            preview.putdata([colors[v] for v in indices])
            filename = OUT / f'asset_{len(previews):03d}.png'
            preview.save(filename)
            row['preview'] = str(filename)
            row['preview_sha256'] = sha(filename.read_bytes())
            row['preview_palette_bank'] = 0
            row['native_palette_and_alpha_proved'] = False
            previews.append(row)
            if row['unclassified_trailing_bytes']:
                offset = row['pixels_offset'] + row['pixels_bytes']
                second = decode(block[offset:])
                if second is not None:
                    second_indices = second.pop('indices')
                    second_palette = second.pop('palette')
                    second.update({'path': name, 'block_index': index,
                                   'block_offset': offset, 'visual_review': 'pending',
                                   'native_use': 'unproved', 'preview_palette_bank': 0,
                                   'native_palette_and_alpha_proved': False})
                    bank_size = 32 if second['depth'] == 4 else 512
                    colors = [bgr555(v) for v, in struct.iter_unpack('<H', second_palette[:bank_size])]
                    preview = Image.new('RGBA', (second['width'], second['height']))
                    preview.putdata([colors[v] for v in second_indices])
                    filename = OUT / f'asset_{len(previews):03d}.png'
                    preview.save(filename)
                    second['preview'] = str(filename)
                    second['preview_sha256'] = sha(filename.read_bytes())
                    second['exact_indexed_loose_matches'] = []
                    for loose_name, pxl, loose_palette in loose:
                        if (pxl.width, pxl.height, pxl.bits_per_pixel, bytes(pxl.indices)) == (
                                second['width'], second['height'], second['depth'], second_indices):
                            second['exact_indexed_loose_matches'].append({
                                'path': loose_name, 'palette_exact': second_palette == loose_palette})
                    row['trailing_image'] = second
                    row['unclassified_trailing_bytes'] = second['unclassified_trailing_bytes']
                    previews.append(second)
            rows.append(row)
    sheets = []
    for start in range(0, len(previews), 8):
        page = Image.new('RGB', (1120, 760), '#343434')
        draw = ImageDraw.Draw(page)
        for slot, row in enumerate(previews[start:start + 8]):
            p = Image.open(row['preview']).convert('RGB')
            p.thumbnail((272, 342), Image.Resampling.NEAREST)
            x, y = slot % 4 * 280, slot // 4 * 380
            page.paste(p, (x + (280 - p.width) // 2, y + 35))
            draw.text((x + 4, y + 3), f"{row['path']} [{row['block_index']}] +{row.get('block_offset', 0)}", fill='white')
            draw.text((x + 4, y + 18), f"{row['width']}x{row['height']} banks {row['palette_banks']}", fill='white')
        filename = OUT / f'sheet_{start // 8:02d}.png'
        page.save(filename)
        sheets.append({'path': str(filename), 'sha256': sha(filename.read_bytes()),
                       'visual_review': 'pending'})
    report = {'source_rom_sha256': SOURCE, 'blocks': rows, 'sheets': sheets,
              'limitations': ['Storage previews do not prove native usage, alpha or composition.',
                              'Multiple palette banks are not mapped to native regions.',
                              'Trailing bytes and unrecognized block formats remain pending.',
                              'Exact loose pixel matches do not prove shared native consumers.']}
    (OUT / 'inventory.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'blocks': len(rows), 'previews': len(previews),
                      'unclassified_blocks': sum(r['format_status'] == 'unclassified-no-preview' for r in rows),
                      'pixel_matches': sum(bool(r['exact_indexed_loose_matches']) for r in previews),
                      'multi_bank_previews': sum(r['palette_banks'] > 1 for r in previews),
                      'previews_with_trailing_data': sum(bool(r['unclassified_trailing_bytes']) for r in previews)}, indent=2))


if __name__ == '__main__':
    main()
