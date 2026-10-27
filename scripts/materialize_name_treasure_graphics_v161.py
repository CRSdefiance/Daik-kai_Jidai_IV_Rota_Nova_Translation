"""Canonical-source alternate name plaques and complete treasure-list header."""

import copy
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_ilnk_pxl_sync_batches,
    apply_pxl_native_label_batch,
)
from scripts.inventory_embedded_graphics_v151 import decode

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v160_candidate.nds')
NAME = '/_pxl/slackimg12.pxl'
TREASURE = '/_pxl/mysterymap/mys_hunt_d.pxl'
ARCHIVE = '/GRP/SLACKIMG.DK4'
NAME_BATCH = Path('translations/name_entry_plaques_graphics_v1.json')
TREASURE_BATCH = Path('translations/treasure_name_header_graphics_v1.json')
SYNC_BATCH = Path('translations/name_entry_plaques_embedded_sync_v1.json')
BUTTON_SYNC = Path('translations/button_prompt_embedded_sync_v1.json')
OUT = Path('work/qa/name_treasure_graphics_v161')
LABELS = (
    ('NAME', '名', 'Name', 'Given name.'),
    ('MIDDLE', 'ミドルネーム', 'Middle', 'Middle name.'),
    ('LAST', '姓', 'Last', 'Surname or last name.'),
    ('COMPANY', '勢力名', 'Company', 'Name of the merchant organization/faction.'),
    ('BIRTH', '誕生日', 'Birth', 'Date of birth.'),
)
SOURCES = {
    NAME: 'd902a7c0c4bef45a6c6e3f75c7e4e7a849ea3457bdeaab0f1bdc0ba4ef1ccd7c',
    TREASURE: '086804a266ecc1e71b8ef80ff5c8f350623b517531cf9d5f2120ba33fa358e50',
}


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def header(path, source, advance, color):
    return {
        'format': 'dk4-pxl-native-label-batch-v1', 'file_path': path,
        'source_file_sha256': sha(source), 'font_file_path': '/__arm9__.bin',
        'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
        'editorial_policy': 'natural-dialogue-v2', 'glyph_width': advance,
        'advance': advance, 'color_index': color, 'erase_palette_indices': [color],
    }


def record(key, jp, text, gloss, box, background, note):
    return {
        'id': key, 'source_japanese': jp, 'text': text, 'source_meaning': gloss,
        'box': list(box), 'background_indices_zlib_hex': zlib.compress(background).hex(),
        'context': 'Shared name-entry plaques.' if key.startswith('DK4_NAME_ENTRY') else 'Treasure-list header.',
        'localization_note': note,
        'review': {'source': True, 'context': True, 'localization': True,
                   'naturalness': True, 'formatting': True, 'visual': False,
                   'physical_gameplay': False},
    }


def make_batches(rom):
    clean = NdsImage.open('work/clean.nds')
    for path, digest in SOURCES.items():
        if sha(rom.read_file(path)) != digest or rom.read_file(path) != clean.read_file(path):
            raise ValueError('Exact clean Japanese canonical artwork required: ' + path)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    if sha(font.glyphs) != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Original native English font differs')
    source = rom.read_file(NAME)
    p = PxlImage.from_bytes(source)
    embedded = decode(IlnkContainer.parse(rom.read_file(ARCHIVE)).blocks[12])
    if ((p.width, p.height, p.bits_per_pixel) != (44, 60, 4)
            or embedded is None or embedded['indices'] != bytes(p.indices)
            or embedded['palette_banks'] != 1 or embedded['unclassified_trailing_bytes']):
        raise ValueError('Complete paired name plaque storage differs')
    names = header(NAME, source, 5, 15)
    names['trim_blank_top_rows'] = 2
    names['scope'] = 'All five alternate name-entry plaques, consistent with existing captain selection.'
    rows = []
    for index, (key, jp, text, gloss) in enumerate(LABELS):
        y0 = index * 12
        box = (3, y0, 41, y0 + 12)
        background = bytearray(p.indices[y * 44 + x]
                               for y in range(y0, y0 + 12) for x in range(3, 41))
        # Column 9 of the first plaque is outside its centered Japanese name
        # glyph. Use that clean vertical ramp only beneath the old lettering.
        # Top/bottom chrome and curved side-border pixels remain untouched.
        for dy in range(1, 10):
            for x in range(4, 40):
                background[dy * 38 + x - 3] = p.indices[dy * 44 + 9]
        rows.append(record('DK4_NAME_ENTRY_' + key + '_GRAPHIC_V1', jp, text, gloss, box, bytes(background),
                           'Uses the established captain-selection field label. Trim only two verified blank font rows and center all nine visible rows inside unchanged plaque borders; every original native glyph pixel is retained.'))
        rows[-1]['draw_box'] = [3, y0 + 1, 41, y0 + 10]
    names['records'] = rows
    source = rom.read_file(TREASURE)
    p = PxlImage.from_bytes(source)
    if (p.width, p.height, p.bits_per_pixel) != (256, 192, 8):
        raise ValueError('Exact treasure-list image geometry required')
    box = (84, 0, 174, 15)
    # Replace dark source lettering only inside its three original glyph cells.
    # All list rows, frame and unrelated header grain remain exact.
    for glyph_box in ((86, 1, 99, 13), (122, 1, 135, 13), (158, 1, 171, 13)):
        p.erase_dark_text(glyph_box, threshold=135)
    background = bytes(p.indices[y * 256 + x] for y in range(15) for x in range(84, 174))
    treasure = header(TREASURE, source, 6, 7)
    treasure['scope'] = 'Complete Treasure Name header; preserve all six list rows and source artwork.'
    treasure['records'] = [record('DK4_TREASURE_NAME_HEADER_GRAPHIC_V1', '秘宝名', 'Treasure Name',
                                  'Name of the treasure.', box, background,
                                  'Natural English heading retains both treasure and name; no shortened fragment or invented category.')]
    return names, treasure


def previews(base, names, treasure, archive):
    OUT.mkdir(parents=True, exist_ok=True)
    page = Image.new('RGB', (1056, 520), '#303030')
    draw = ImageDraw.Draw(page)
    for index, (label, path, raw) in enumerate((('Original plaques', NAME, base.read_file(NAME)),
                                               ('English plaques', NAME, names))):
        p = PxlImage.from_bytes(raw)
        p.render().save(OUT / ('name_' + ('source' if index == 0 else 'english') + '_native.png'))
        draw.text((16 + index * 180, 8), label, fill='white')
        page.paste(p.render().convert('RGB').resize((132, 180), Image.Resampling.NEAREST), (16 + index * 180, 30))
    e = decode(IlnkContainer.parse(archive).blocks[12])
    colors = [bgr555(v)[:3] for v, in struct.iter_unpack('<H', e['palette'])]
    image = Image.new('RGB', (44, 60)); image.putdata([colors[v] for v in e['indices']])
    image.save(OUT / 'name_embedded_english_native.png')
    draw.text((376, 8), 'English embedded plaques', fill='white')
    page.paste(image.resize((132, 180), Image.Resampling.NEAREST), (376, 30))
    for index, raw in enumerate((base.read_file(TREASURE), treasure)):
        p = PxlImage.from_bytes(raw)
        header_image = p.render().convert('RGB').crop((0, 0, 256, 16))
        header_image.save(OUT / ('treasure_' + ('source' if index == 0 else 'english') + '_native.png'))
        draw.text((16, 238 + index * 102), 'Original treasure header' if index == 0 else 'English treasure header', fill='white')
        page.paste(header_image.resize((1024, 64), Image.Resampling.NEAREST), (16, 260 + index * 102))
    PxlImage.from_bytes(treasure).render().resize((512, 384), Image.Resampling.NEAREST).save(OUT / 'treasure_full_english.png')
    page.save(OUT / 'review.png')


def main():
    base, prior = NdsImage.open(BASE), NdsImage.open(PRIOR)
    for path in SOURCES:
        if prior.read_file(path) != base.read_file(path):
            raise ValueError('V160 changed new graphic source')
    names, treasure = make_batches(base)
    save(NAME_BATCH, names); save(TREASURE_BATCH, treasure)
    target_name, _ = apply_pxl_native_label_batch(NAME_BATCH, base.read_file(NAME), base.read_file('/__arm9__.bin'))
    target_treasure, _ = apply_pxl_native_label_batch(TREASURE_BATCH, base.read_file(TREASURE), base.read_file('/__arm9__.bin'))
    original_archive = base.read_file(ARCHIVE)
    sync = {
        'format': 'dk4-ilnk-pxl-sync-v1', 'file_path': ARCHIVE,
        'id': 'DK4_NAME_ENTRY_EMBEDDED_GRAPHICS_V1',
        'source_file_sha256': sha(original_archive),
        'source_block_sha256': sha(IlnkContainer.parse(original_archive).blocks[12]),
        'source_image_path': NAME, 'source_image_sha256': sha(target_name),
        'block_index': 12, 'block_header_size': 64, 'target_width': 44, 'target_height': 60,
        'target_x': 0, 'target_y': 0, 'target_locale': 'en-US',
        'scope': 'Complete five name-entry plaques; synchronize only block 12 pixels, preserve palette/header.'}
    save(SYNC_BATCH, sync)
    target_archive, _ = apply_ilnk_pxl_sync_batches([BUTTON_SYNC, SYNC_BATCH], original_archive,
        {'/_pxl/slackimg20.pxl': prior.read_file('/_pxl/slackimg20.pxl'), NAME: target_name})
    previews(base, target_name, target_treasure, target_archive)
    report = {
        'status': 'draft-paired-name-plaques-and-treasure-header',
        'source_rom': str(BASE), 'source_rom_sha256': sha(BASE.read_bytes()),
        'source_locked_japanese': SOURCES, 'new_english_labels': [row[2] for row in LABELS] + ['Treasure Name'],
        'name_target_sha256': sha(target_name), 'treasure_target_sha256': sha(target_treasure),
        'combined_archive_target_sha256': sha(target_archive),
        'native_use_scope': 'Storage and original font; actual load/crop/palette/input pending.',
        'visual_review': 'pending',
    }
    save(Path('work/analysis/name_treasure_graphics_v161_artwork.json'), report)
    # Register only after visual/native verification, using --register separately.
    print(json.dumps(report, ensure_ascii=False, indent=2))


def register():
    report = json.loads(Path('work/analysis/name_treasure_graphics_v161_artwork.json').read_text(encoding='utf-8'))
    if report['visual_review'] is not True:
        raise ValueError('Reviewed complete previews required before registration')
    native = json.loads(Path('work/analysis/name_treasure_graphics_v161_native.json').read_text(encoding='utf-8'))
    if native['status'] != 'pass-complete-native-compact-glyphs-and-source-image-size':
        raise ValueError('Complete native glyph and sizing evidence required')
    for path in (NAME_BATCH, TREASURE_BATCH):
        value = json.loads(path.read_text(encoding='utf-8'))
        for row in value['records']:
            row['review']['visual'] = True
        save(path, value)
    path = Path('translations/release_stack.json')
    registry = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v160'])
    profile['batches'] += [NAME_BATCH.as_posix(), TREASURE_BATCH.as_posix(), SYNC_BATCH.as_posix()]
    profile['note'] = 'Complete V160 inheritance plus five alternate name plaques and Treasure Name header; experimental, physical crop/input checks pending.'
    profile['description'] = 'All 437 V160 batches and terminal stages plus three source-locked graphics batches (440 total); both embedded atlas updates merge against the canonical source without overwriting each other.'
    registry['profiles']['all-routes-unified-v161'] = profile
    save(path, registry)
    print('Registered all-routes-unified-v161: 440 batches, experimental.')


if __name__ == '__main__':
    import sys
    register() if '--register' in sys.argv else main()
