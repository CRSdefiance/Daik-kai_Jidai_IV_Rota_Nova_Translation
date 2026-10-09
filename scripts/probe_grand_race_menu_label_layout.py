"""Source-locked native menu label areas; full screen/gameplay remain pending."""

import argparse
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_menu_copy import execute_copy
from scripts.probe_grand_race_wireless_return import check_branch, word

GROUPS = (('main', ('START', 'READ_RULES')), ('rules', ('ABOUT', 'BASIC_RULES', 'MAP_SUPPLIES', 'LIMITS')))


def label_geometry(text, maximum_units, *, advance=6, line_height=12, horizontal_margin=0, vertical_margin=4):
    if not text or any(not 0x20 <= ord(char) <= 0x7E for char in text) or len(text) > 48:
        raise ValueError('One complete printable native menu label is required')
    width = max(8, maximum_units) * advance + 2 * horizontal_margin
    height = line_height + 2 * vertical_margin
    text_width = len(text) * advance
    x = horizontal_margin + (width - 2 * horizontal_margin - text_width) // 2
    if x < horizontal_margin or x + text_width > width - horizontal_margin:
        raise ValueError('Full English overflows the native label area')
    return {'width': width, 'height': height, 'x': x, 'y': vertical_margin,
            'text_width': text_width, 'line_height': line_height}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned ROM differs')
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese source differs')
    spans = ((0x14062C, 0x14066C), (0x293A0, 0x293A8), (0x522FC, 0x5231C),
             (0xACEA4, 0xACF1C), (0xACF7C, 0xAD018), (0xACB10, 0xACBEC),
             (0x521E8, 0x52228), (0xCF0A8, 0xCF208), (0xD5340, 0xD5404),
             (0x116438, 0x116448), (0xACC64, 0xACC9C))
    locks = []
    for lo, hi in spans:
        if not sources[0][lo:hi] == sources[1][lo:hi] == sources[2][lo:hi]:
            raise ValueError('Alignment/geometry context changed')
        locks.append({'start': lo, 'end': hi, 'sha256': hashlib.sha256(sources[0][lo:hi]).hexdigest()})
    original = sources[2]
    if word(original, 0x140644) != 0x020293A0 or word(original, 0x293A0) != 0xE3A00001:
        raise ValueError('Selector must retain initialized alignment flag')
    for offset, expected in ((0xACEB8, 0xE3A03001), (0xACEF4, 0xE5853064),
                             (0x52314, 0x05854064), (0xACB74, 0xE5940064)):
        if word(original, offset) != expected:
            raise ValueError('Mapped alignment flag or condition differs')
    check_branch(original, 0xACB88, 0xD5340)
    check_branch(original, 0xD53A0, 0xCF0A8)
    check_branch(original, 0xD53E0, 0xD5404)
    if struct.unpack_from('<4I', original, 0x116438) != (0, 4, 6, 12):
        raise ValueError('Native margin/glyph metrics differ')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {row['id'].removeprefix('GRAND_RACE_UI_'): row for row in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    font = GameAsciiFont.from_arm9(original)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native ASCII font differs')
    sheet = Image.new('RGB', (640, 480), 'white')
    draw = ImageDraw.Draw(sheet)
    selections = []
    index = 0
    for group, names in GROUPS:
        maximum = max(len(rows[name]['english']) for name in names)
        for name in names:
            row = rows[name]
            raw = row['english'].encode('ascii') + b'\0'
            if execute_copy(original, raw) != raw:
                raise ValueError('Native menu copy drops text')
            geometry = label_geometry(row['english'], maximum)
            panel = Image.new('RGB', (geometry['width'], geometry['height']), '#eef1f5')
            for position, char in enumerate(row['english']):
                panel.paste('#183047', (geometry['x'] + position * 6, geometry['y']), font.decode(char))
            left, top = (index % 2) * 320 + 20, (index // 2) * 160 + 15
            draw.text((left, top), f'{group}: {name} - {geometry["width"]} x {geometry["height"]}', fill='black')
            sheet.paste(panel.resize((geometry['width'] * 3, geometry['height'] * 3), Image.Resampling.NEAREST), (left, top + 30))
            selections.append({'id': row['id'], 'english': row['english'], 'group': group,
                               'geometry': geometry, 'preview_reviewed': args.reviewed})
            index += 1
    output = Path('work/qa/grand_race_menu_label_layout')
    output.mkdir(parents=True, exist_ok=True)
    preview = output / 'sheet.png'
    sheet.save(preview)
    report = {'status': 'research-native-label-areas-full-screen-and-integration-pending',
              'rom_written': False, 'runtime_verified': False, 'source_locks': locks,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'preview_sha256': hashlib.sha256(preview.read_bytes()).hexdigest(),
              'selections': selections, 'alignment_flag': 1, 'draw_path': ['0xD5340', '0xCF0A8', '0xD5404'],
              'limitations': ['Isolated label areas; not full-screen position/paint proof.',
                              'Full native glyph drawing and inherited D5404 behavior still need verification.',
                              'Template copy and dynamic call activation require complete release enforcement.',
                              'No release manuscript gate or integrated translation count advanced.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Six complete source-derived label areas generated; full screen/runtime remain pending')


if __name__ == '__main__':
    main()
