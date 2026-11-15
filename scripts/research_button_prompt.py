"""Source-locked paired button-label artwork; research, not a playable release.

The original label owns a baked text/background rectangle. Its background is
reconstructed from the untouched side margins, not claimed pixel-identical.
"""

import json
import struct
from pathlib import Path

from PIL import Image, ImageFilter

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode

TEXT = 'Press a button!'
LOOSE = '/_pxl/slackimg20.pxl'
ARCHIVE = '/GRP/SLACKIMG.DK4'
BLOCK = 20
OUT = Path('work/qa/button_prompt_research')
ROM = Path('out/all_routes_combined_v159_candidate.nds')
SOURCE_ROM = '51a89ca2cf0ec6beab6e2a68670eb1cc6368d069fee1947fe5fc367a644d83a5'
PIXELS = '128b792451fc74a75de9b928a16b56fb057ecf24e336985a687c1a044ebf229c'
BOX = (4, 1, 152, 23)


def design(indices, font, text=TEXT):
    if sha(font.glyphs) != REFERENCE_ASCII_FONT_SHA256 or text != TEXT:
        raise ValueError('Reviewed original game font and complete prompt required')
    if len(indices) != 156 * 24:
        raise ValueError('Original full label dimensions required')
    original = bytes(indices)
    result = bytearray(original)
    left, top, right, bottom = BOX
    dither = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
    # Both side columns are outside the original lettering and its shadow.
    for y in range(top, bottom):
        a, b = original[y * 156 + 2], original[y * 156 + 154]
        for x in range(left, right):
            numerator = a * 152 + (b - a) * (x - 2)
            whole, fraction = divmod(numerator, 152)
            result[y * 156 + x] = whole + (fraction * 16 > dither[y % 4][x % 4] * 152)
    mask = Image.new('L', (156, 24))
    origin = ((156 - len(text) * 6) // 2, (24 - 11) // 2)
    for index, character in enumerate(text):
        glyph = font.decode(character).convert('L')
        mask.paste(glyph, (origin[0] + index * 6, origin[1]))
    outline = mask.filter(ImageFilter.MaxFilter(3))
    # A two-pixel lower/right shadow and one-pixel dark edge retain the
    # original label's gold-on-brown treatment without changing its palette.
    layers = ((outline, 2, 2, 1), (outline, 0, 0, 0), (mask, 0, 0, 14))
    for layer, dx, dy, color in layers:
        for y in range(24):
            for x in range(156):
                if not layer.getpixel((x, y)):
                    continue
                xx, yy = x + dx, y + dy
                if not left <= xx < right or not top <= yy < bottom:
                    raise ValueError('Complete prompt or shadow escapes its owned label')
                result[yy * 156 + xx] = color
    for y in range(24):
        for x in range(156):
            if (not (left <= x < right and top <= y < bottom)
                    and result[y * 156 + x] != original[y * 156 + x]):
                raise ValueError('Graphic edit escapes owned text rectangle')
    return bytes(result), mask, origin


def pack(indices):
    if len(indices) % 2 or any(i > 15 for i in indices):
        raise ValueError('Four-bit paired pixels required')
    return bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2))


def make(rom):
    loose = rom.read_file(LOOSE)
    archive_raw = rom.read_file(ARCHIVE)
    archive = IlnkContainer.parse(archive_raw)
    embedded = archive.blocks[BLOCK]
    pxl = PxlImage.from_bytes(loose)
    info = decode(embedded)
    if ((pxl.width, pxl.height, pxl.bits_per_pixel) != (156, 24, 4)
            or info is None or (info['width'], info['height'], info['depth']) != (156, 24, 4)
            or info['palette_banks'] != 1 or info['unclassified_trailing_bytes']
            or bytes(pxl.indices) != info['indices']
            or sha(pack(pxl.indices)) != PIXELS):
        raise ValueError('Original paired Japanese prompt differs')
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    indices, mask, origin = design(pxl.indices, font)
    pxl.indices[:] = indices
    new_loose = pxl.to_bytes()
    start = info['pixels_offset']
    new_embedded = embedded[:start] + pack(indices) + embedded[start + info['pixels_bytes']:]
    archive.blocks[BLOCK] = new_embedded
    new_archive = archive.to_bytes()
    reread = IlnkContainer.parse(new_archive)
    old_archive = IlnkContainer.parse(archive_raw)
    if (len(new_loose) != len(loose) or new_loose[:pxl.pixels_offset] != loose[:pxl.pixels_offset]
            or len(new_embedded) != len(embedded) or new_embedded[:start] != embedded[:start]
            or any(a != b for i, (a, b) in enumerate(zip(old_archive.blocks, reread.blocks)) if i != BLOCK)
            or len(old_archive.blocks) != len(reread.blocks)
            or decode(reread.blocks[BLOCK])['indices'] != indices):
        raise ValueError('Paired artwork storage/header/palette preservation failed')
    return new_loose, new_archive, mask, origin


def main():
    if sha(ROM.read_bytes()) != SOURCE_ROM:
        raise ValueError('Exact V159 research input required')
    rom = NdsImage.open(ROM)
    loose, archive, mask, origin = make(rom)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'slackimg20_english.pxl').write_bytes(loose)
    (OUT / 'SLACKIMG_english.DK4').write_bytes(archive)
    mask.save(OUT / 'english_glyph_mask.png')
    original = rom.read_file(LOOSE)
    cards = []
    for name, raw in (('loose_source', original), ('loose_english', loose)):
        p = PxlImage.from_bytes(raw)
        raster = p.render().convert('RGB')
        raster.save(OUT / (name + '_native.png'))
        raster.resize((624, 96), Image.Resampling.NEAREST).save(OUT / (name + '.png'))
        cards.append(raster)
    e = decode(IlnkContainer.parse(archive).blocks[BLOCK])
    palette = [bgr555(v)[:3] for v, in struct.iter_unpack('<H', e['palette'])]
    raster = Image.new('RGB', (156, 24))
    raster.putdata([palette[v] for v in e['indices']])
    raster.save(OUT / 'embedded_english_native.png')
    raster.resize((624, 96), Image.Resampling.NEAREST).save(OUT / 'embedded_english.png')
    cards.append(raster)
    sheet = Image.new('RGB', (624, 3 * 112), '#303030')
    for index, card in enumerate(cards):
        sheet.paste(card.resize((624, 96), Image.Resampling.NEAREST), (0, index * 112))
    sheet.save(OUT / 'paired_review.png')
    row = {
        'status': 'paired-artwork-research-not-integrated',
        'source_rom_sha256': SOURCE_ROM,
        'source_japanese': 'ボタンを押してください！',
        'source_meaning': 'Please press a button.',
        'english': TEXT, 'target_locale': 'en-US', 'translation_policy': 'natural-dialogue-v2',
        'localization_note': 'Retains the generic button instruction and exclamation; concise natural UI English.',
        'dimensions': [156, 24], 'owned_label_rectangle': list(BOX),
        'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'glyph_origin': list(origin),
        'advance': 6, 'complete_glyph_mask_sha256': sha(mask.tobytes()),
        'loose_path': LOOSE, 'loose_source_sha256': sha(original), 'loose_target_sha256': sha(loose),
        'embedded_path': ARCHIVE, 'embedded_block': BLOCK,
        'archive_source_sha256': sha(rom.read_file(ARCHIVE)), 'archive_target_sha256': sha(archive),
        'source_pixel_sha256': PIXELS, 'target_pixel_sha256': sha(loose[PxlImage.from_bytes(loose).pixels_offset:]),
        'preserved': ['both headers and palettes', 'dimensions and pixel extents',
                      'pixels outside the owned label rectangle', 'all other archive blocks'],
        'background': 'Owned text background reconstructed by interpolating untouched side-margin indices with four-by-four ordered dithering.',
        'limitations': ['No new ROM or release profile.', 'Native file load, palette/alpha and input/physical behavior remain pending.'],
        'review': {'source': True, 'localization': True, 'naturalness': True, 'visual': 'pending'},
    }
    Path('work/analysis/button_prompt_artwork_research.json').write_text(
        json.dumps(row, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: row[k] for k in ('status', 'english', 'dimensions', 'target_pixel_sha256')}, indent=2))


if __name__ == '__main__':
    main()
