"""Render every PXL/FLS asset for a source-pinned, explicitly incomplete visual audit."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '3a1ff1f8f1734ba41c24057cee160b6b5aa2bdbc9c38dc08da8ce896dd972a8e'
OUT = Path('work/analysis/graphics_v150')


def pxl_render(raw):
    depth, width_words, height, _, pixels_offset = struct.unpack_from('<5I', raw)
    if depth & 255 != 16:
        parsed = PxlImage.from_bytes(raw)
        if parsed.to_bytes() != raw:
            raise ValueError('Palette PXL decode/repack changes source')
        return parsed.render(), 'palette-pxl'
    # Direct-color words use one word per pixel, unlike packed palette PXL.
    packed = raw[pixels_offset:]
    if len(packed) != width_words * height * 2:
        raise ValueError('Direct-color PXL extent differs')
    result = Image.new('RGBA', (width_words, height))
    result.putdata([bgr555(v) for v, in struct.iter_unpack('<H', packed)])
    return result, 'direct-color-bgr555-preview-alpha-unclassified'


def sheets(rows, prefix):
    pages = []
    for start in range(0, len(rows), 8):
        selected = rows[start:start + 8]
        page = Image.new('RGB', (1120, 760), '#343434')
        draw = ImageDraw.Draw(page)
        for slot, row in enumerate(selected):
            preview = Image.open(row['preview']).convert('RGB')
            preview.thumbnail((272, 342), Image.Resampling.NEAREST)
            x, y = (slot % 4) * 280, (slot // 4) * 380
            page.paste(preview, (x + (280 - preview.width) // 2, y + 32))
            draw.text((x + 4, y + 3), str(row['asset_id']) + ' ' + row['path'].split('/')[-1], fill='white')
            draw.text((x + 4, y + 17), f"{row['width']}x{row['height']} {row.get('texture_index', '')}", fill='white')
        filename = OUT / f'{prefix}_{start // 8:03d}.png'
        page.save(filename)
        pages.append({'path': str(filename), 'asset_ids': [r['asset_id'] for r in selected],
                      'visual_review': 'pending', 'thumbnails_may_not_resolve_small_text': True})
    return pages


def main():
    path = Path('out/all_routes_combined_v150_candidate.nds')
    if sha(path.read_bytes()) != SOURCE:
        raise ValueError('Exact saved V150 required')
    OUT.mkdir(parents=True, exist_ok=True)
    image = NdsImage.open(path)
    if sha(Path('work/clean.nds').read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean comparison ROM required')
    clean = NdsImage.open('work/clean.nds')
    rows, errors, files = [], [], []
    for _, name, raw in image.iter_files():
        suffix = name.rsplit('.', 1)[-1].lower()
        if suffix not in ('pxl', 'fls'):
            continue
        metadata = {'path': name, 'sha256': sha(raw), 'length': len(raw),
                    'equals_clean': raw == clean.read_file(name), 'format': suffix}
        files.append(metadata)
        try:
            if suffix == 'pxl':
                preview, mode = pxl_render(raw)
                assets = [(None, preview, mode)]
            else:
                archive = FlsArchive(raw)
                metadata['texture_count'] = archive.count
                assets = []
                for index in range(archive.count):
                    try:
                        if name == '/m02_03.fls':
                            # This source record stores raw palette/pixel extents,
                            # unlike the LZ10 blocks of the other 15-file corpus.
                            if archive.records != [[33554433, 377, 0, 512, 512, 262144]]:
                                raise ValueError('Raw FLS record differs from reviewed extents')
                            base = archive.data_offset
                            palette = [bgr555(v) for v, in struct.iter_unpack('<H', raw[base:base + 512])]
                            pixels = raw[base + 512:base + 512 + 262144]
                            if len(pixels) != 512 * 512 or base + 512 + len(pixels) != len(raw):
                                raise ValueError('Raw FLS storage extent differs')
                            preview = Image.new('RGBA', (512, 512))
                            preview.putdata([palette[v] for v in pixels])
                            assets.append((index, preview, 'raw-fls-512-square-storage-preview-composition-unproved'))
                        else:
                            texture = archive.texture(index)
                            assets.append((index, texture.render(), 'fls-palette-texture'))
                    except (ValueError, IndexError, struct.error) as error:
                        errors.append({'path': name, 'texture_index': index, 'error': str(error)})
            for index, preview, mode in assets:
                asset_id = len(rows)
                filename = OUT / f'asset_{asset_id:04d}.png'
                preview.save(filename)
                rows.append({'asset_id': asset_id, **metadata, 'texture_index': index,
                             'width': preview.width, 'height': preview.height, 'decode_mode': mode,
                             'preview': str(filename), 'visual_review': 'pending',
                             'japanese_text': 'unclassified'})
        except (ValueError, IndexError, struct.error) as error:
            errors.append({'path': name, 'error': str(error)})
    # Ordering helps inspect UI atlases early; filenames do not classify content.
    ui = [r for r in rows if r['path'].startswith('/_pxl/') and
          not any(c.isdigit() for c in r['path'].split('/')[-1])]
    other = [r for r in rows if r not in ui]
    report = {'status': 'rendered-inventory-visual-review-pending',
              'source_rom_sha256': SOURCE, 'files': files, 'assets': rows, 'decode_errors': errors,
              'sheets': sheets(ui, 'ui') + sheets(other, 'remaining'),
              'limitations': ['Rendered or unchanged does not mean Japanese-free or translated.',
                              'All visual-review fields remain pending until pixels are inspected.',
                              'Direct-color previews treat every pixel opaque; native alpha semantics remain unclassified.',
                              'FLS textures are raw storage atlases, not proof of native composition.',
                              'Other graphics/container formats and dynamic text need separate audit.']}
    (OUT / 'inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'pxl_files': sum(f['format'] == 'pxl' for f in files),
                      'fls_files': sum(f['format'] == 'fls' for f in files),
                      'rendered_assets': len(rows), 'decode_errors': len(errors),
                      'contact_sheets': len(report['sheets']), 'ui_first_assets': len(ui)}))


if __name__ == '__main__':
    main()
