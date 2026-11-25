"""Current indexed embedded/loose copy consistency and unmatched storage review.

Pairing uses the clean pixel planes, never filenames alone. Storage previews
are not native palette, composition, loading or ordinary-consumer evidence.
"""

import struct
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.inventory_external_palette_graphics_v151 import PAIRS
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/embedded_sync_v725')
ROM = Path('out/all_routes_combined_v712_candidate.nds')


def loose_palette(raw):
    offset, end = struct.unpack_from('<2I', raw, 12)
    return raw[offset:end]


def image(info, bank=0):
    size = 32 if info['depth'] == 4 else 512
    palette = info['palette'][bank * size:(bank + 1) * size]
    assert len(palette) == size
    colors = [bgr555(word)[:3] for word, in struct.iter_unpack('<H', palette)]
    canvas = Image.new('RGB', (info['width'], info['height']))
    canvas.putdata([colors[i] for i in info['indices']])
    return canvas


def key(info):
    return info['width'], info['height'], info['depth'], sha(info['indices'])


def split_pair(blocks, palette_block, pixels_block):
    p, b = blocks[palette_block], blocks[pixels_block]
    pk, pm, plen, pf, pw, ph = struct.unpack_from('<IIIIHH', p)
    kind, mode, extent, flags, words, height = struct.unpack_from('<IIIIHH', b)
    assert (pk, pm, pw) == (19, 2, 16) and len(p) == plen + 8 == 20 + pw * ph * 2
    assert (kind, mode) == (18, 0) and len(b) == extent + 8 == 20 + words * height * 2
    indices = bytes(part for byte in b[20:] for part in (byte & 15, byte >> 4))
    assert bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2)) == b[20:]
    return {'width': words * 4, 'height': height, 'depth': 4, 'indices': indices,
            'palette': p[20:], 'palette_banks': ph, 'palette_flags': pf, 'pixel_flags': flags}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'storage_proof.json').exists()
    digest = sha(ROM.read_bytes())
    assert digest == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
        Path('out/raphael_natural_v2_accepted_base.nds'))}
    loose = defaultdict(list)
    for _, path, raw in clean.iter_files():
        if path.lower().endswith('.pxl') and int.from_bytes(raw[:4], 'little') & 255 in (4, 8):
            pxl = PxlImage.from_bytes(raw)
            loose[pxl.width, pxl.height, pxl.bits_per_pixel, sha(bytes(pxl.indices))].append(path)
    rows, unpaired, block_inventory, archives = [], [], [], {}
    for _, path, raw in clean.iter_files():
        if not path.startswith('/GRP/') or not raw.startswith(b'ILNK'):
            continue
        a, b = IlnkContainer.parse(raw), IlnkContainer.parse(current.read_file(path))
        assert len(a.blocks) == len(b.blocks) and a.to_bytes() == raw
        assert b.to_bytes() == current.read_file(path)
        archives[path] = (a.blocks, b.blocks)
        for number, (old, new) in enumerate(zip(a.blocks, b.blocks, strict=True)):
            assert len(old) == len(new)
            block_inventory.append({'path': path, 'block': number, 'bytes': len(old),
                'clean_sha256': sha(old), 'current_sha256': sha(new), 'extent_preserved': True})
            offset = 0
            while len(old) - offset >= 12:
                before = decode(old[offset:])
                if before is None:
                    break
                after = decode(new[offset:])
                assert after is not None
                end = offset + before['pixels_offset'] + before['pixels_bytes']
                assert old[offset:offset + before['pixels_offset']] == new[offset:offset + after['pixels_offset']]
                assert before['palette'] == after['palette']
                row = {'path': path, 'block': number, 'offset': offset,
                    'dimensions_depth_banks': [before['width'], before['height'], before['depth'], before['palette_banks']],
                    'current_plane_sha256': sha(after['indices']), 'clean_plane_sha256': sha(before['indices']),
                    'all_headers_palette_flags_and_extent_source_exact': True, 'loose_counterparts': []}
                for name in loose[key(before)]:
                    old_loose, new_loose = clean.read_file(name), current.read_file(name)
                    pxl = PxlImage.from_bytes(new_loose)
                    assert bytes(pxl.indices) == after['indices'], (path, number, name)
                    assert loose_palette(old_loose) == loose_palette(new_loose)
                    pa, pb = before['palette'], loose_palette(old_loose)
                    assert len(pa) == len(pb)
                    differences = [(i, x, y) for i, (x, y) in enumerate(zip(
                        struct.unpack(f'<{len(pa) // 2}H', pa), struct.unpack(f'<{len(pb) // 2}H', pb), strict=True)) if x != y]
                    category = ('identical' if not differences else 'only-original-bit15' if
                        all(x ^ y == 0x8000 for _, x, y in differences) else 'original-distinct-palette')
                    row['loose_counterparts'].append({'path': name, 'current_file_sha256': sha(new_loose),
                        'whole_current_indices_exact': True, 'palette_relationship': category,
                        'original_palette_word_differences_preserved': [list(d) for d in differences],
                        'neither_palette_normalized_or_modified': True})
                if not row['loose_counterparts']:
                    assert before['palette_banks'] == 1
                    previews = []
                    for label, info in (('SOURCE', before), ('CURRENT', after)):
                        filename = ROOT / f'{Path(path).stem}_{number}_{offset}_{label}.png'
                        image(info).save(filename)
                        previews.append({'path': str(filename), 'sha256': sha(filename.read_bytes())})
                    row['unmatched_storage_review_previews'] = previews
                    unpaired.append(row)
                rows.append(row)
                offset = end
    assert len(block_inventory) == 57 and len(rows) == 31 and len(unpaired) == 12
    links = [p for row in rows for p in row['loose_counterparts']]
    assert len(links) == 19
    assert sum(p['palette_relationship'] == 'identical' for p in links) == 16
    assert sum(p['palette_relationship'] == 'only-original-bit15' for p in links) == 2
    assert [p['path'] for p in links if p['palette_relationship'] == 'original-distinct-palette'] == ['/_pxl/chara00.pxl']
    sheets = []
    for start in range(0, len(unpaired), 2):
        sheet = Image.new('RGB', (664, 550), '#263238')
        draw = ImageDraw.Draw(sheet)
        for slot, row in enumerate(unpaired[start:start + 2]):
            y = slot * 275
            draw.text((8, y + 3), f'{row["path"]} block {row["block"]} +{row["offset"]} / SOURCE | CURRENT / bank 0 storage', fill='white')
            for col, preview in enumerate(row['unmatched_storage_review_previews']):
                with Image.open(preview['path']) as im:
                    sheet.paste(im, (8 + col * 328, y + 25))
        filename = ROOT / f'unmatched_review_{start // 2}.png'
        sheet.save(filename)
        sheets.append({'path': str(filename), 'sha256': sha(filename.read_bytes())})
    split_rows = []
    for path, pblock, iblock in PAIRS:
        old_blocks, new_blocks = archives[path]
        before, after = split_pair(old_blocks, pblock, iblock), split_pair(new_blocks, pblock, iblock)
        assert old_blocks[pblock] == new_blocks[pblock] and old_blocks[iblock][:20] == new_blocks[iblock][:20]
        matches = []
        if path == '/GRP/CMMNIMG.DK4':
            for name, x in (('/_pxl/__marker.pxl', 0), ('/_pxl/__frame.pxl', 256)):
                original = PxlImage.from_bytes(clean.read_file(name))
                now = PxlImage.from_bytes(current.read_file(name))
                def region(info, x=x):
                    return b''.join(info['indices'][y * info['width'] + x:y * info['width'] + x + 256] for y in range(256))
                assert region(before) == bytes(original.indices) and region(after) == bytes(now.indices)
                matches.append({'path': name, 'x': x, 'width': 256, 'height': 256,
                    'all65536_current_indices_exact': True, 'current_file_sha256': sha(now.source)})
        else:
            assert old_blocks[pblock] == new_blocks[pblock] and old_blocks[iblock] == new_blocks[iblock]
            # Every stored palette bank is previewed, without assigning banks to native cells.
            count = after['palette_banks']
            page = Image.new('RGB', (798, ((count + 2) // 3) * 112), '#263238')
            draw = ImageDraw.Draw(page)
            for bank in range(count):
                x, y = bank % 3 * 266, bank // 3 * 112
                draw.text((x + 4, y + 2), f'palette bank {bank} / storage only', fill='white')
                page.paste(image(after, bank), (x + 4, y + 20))
            filename = ROOT / f'MAPPOINT_{pblock}_{iblock}_all_banks.png'
            page.save(filename)
            sheets.append({'path': str(filename), 'sha256': sha(filename.read_bytes())})
        split_rows.append({'path': path, 'palette_block': pblock, 'pixels_block': iblock,
            'dimensions_banks': [after['width'], after['height'], after['palette_banks']],
            'palette_whole_blocks_and_pixel_headers_exact_clean': True, 'counterparts': matches,
            'whole_pixel_block_clean_exact': old_blocks[iblock] == new_blocks[iblock],
            'native_bank_selection_and_consumer_not_inferred_from_storage': True})
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
        'all57_block_extents_source_exact': block_inventory,
        'all31_type16_images_with_source_headers_and_palettes': rows,
        'nineteen_source_matched_complete_loose_planes_synchronized': links,
        'three_split_palette_pixel_pairs': split_rows,
        'complete_marker_and_frame_halves_synchronized': True,
        'unmatched12_review_sheets_and_all_MAPPOINT_palette_bank_sheets': sheets,
        'visual_review_complete': False, 'no_native_or_ordinary_consumer_credit_from_this_audit': True,
        'other_raw_and_animation_blocks_not_decoded_by_type16_audit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'release_hashes_unchanged': release,
        'full_goal_complete': False}
    for path, expected in release.items():
        assert sha(Path(path).read_bytes()) == expected
    save(ROOT / 'storage_proof.json', proof)
    print('V725: 31 typed images,19 whole counterpart planes,2 complete atlas halves and3 original palette exceptions; sheets await review.')


if __name__ == '__main__':
    main()
