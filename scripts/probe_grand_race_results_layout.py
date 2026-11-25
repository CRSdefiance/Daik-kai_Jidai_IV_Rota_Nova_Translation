"""Source-lock result instructions and prize widgets; preview their complete prose."""

import argparse
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    BASE,
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import (
    balanced_lines,
    check_branch,
    resolve_pc_load,
    word,
)


def fit_lines(english, count, x, y):
    lines = balanced_lines(english, count)
    if any(x < 0 or y + n * 16 < 0 or x + len(line) * 6 > 256
           or y + n * 16 + 11 > 192 for n, line in enumerate(lines)):
        raise ValueError('Complete prose exceeds native widget bounds')
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned ROM differs')
    inputs = [NdsImage.open(path).read_file('/__arm9__.bin')
              for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    source = inputs[0]
    if hashlib.sha256(source).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean ARM9 differs')
    spans = ((0xF7950, 0xF8058), (0x12EC8C, 0x12EC94),
             (0x12ECCC, 0x12ECD4), (0x12ED8C, 0x12ED98),
             (0x12EE0C, 0x12EE1C), (0x12EE2C, 0x12EE3C),
             (0x16B290, 0x16B29C), (0xFB004, 0xFB038),
             (0xFAED4, 0xFAF88), (0xF37D8, 0xF3830), (0xD1604, 0xD1850))
    locks = []
    for lo, hi in spans:
        if any(data[lo:hi] != source[lo:hi] for data in inputs[1:]):
            raise ValueError(f'Native consumer differs at {lo:#x}')
        locks.append({'start': lo, 'end': hi,
                      'sha256': hashlib.sha256(source[lo:hi]).hexdigest()})
    loads = ((0xF7998, 2, 0xF8004, 0x16B8D4),
             (0xF7A04, 0, 0xF8014, 0x12EC8C),
             (0xF7A24, 6, 0xF8018, 0x12ED8C),
             (0xF7EEC, 0, 0xF8044, 0x12EE2C),
             (0xF7EF8, 1, 0xF8048, 0x12ECCC))
    for at, reg, literal, target in loads:
        resolve_pc_load(source, at, reg, literal)
        if word(source, literal) != BASE + target:
            raise ValueError('Native source/geometry selection differs')
    for at, target in ((0xF79A4, 0xFAED4), (0xF7A88, 0xFB004),
                       (0xF7A94, 0xFB1EC), (0xF7F04, 0xFB004),
                       (0xF7F10, 0xFB1EC), (0xF3818, 0xD1604)):
        check_branch(source, at, target)
    # Results/instructions append to owner+0x6c; prize appends to owner.
    required = {0xF7A70: 0xE28A406C, 0xF7F0C: 0xE1A0000A,
                0xF7AA0: 0xE2800010, 0xF7AA8: 0xE3590003,
                0xF7AE4: 0xE58D30A4, 0xF7EE4: 0xE3550001,
                0xF7EF0: 0xE2454001, 0xF7EF4: 0xE7902104}
    if any(word(source, at) != value for at, value in required.items()):
        raise ValueError('Widget list/count or prize index differs')
    resolve_pc_load(source, 0xF79CC, 1, 0xF800C)
    resolve_pc_load(source, 0xF7EB0, 2, 0xF8008)
    resolve_pc_load(source, 0xF7EB8, 5, 0xF800C)
    if word(source, 0xF800C) != BASE + 0x16B290:
        raise ValueError('Derived widget vtable differs')
    if struct.unpack_from('<4I', source, 0x12EE0C) != (5000, 2000, 1000, 500):
        raise ValueError('Prize money table differs')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {r['id'].removeprefix('GRAND_RACE_UI_'): r for r in
            json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    for names, table in ((('RESULTS', 'CONTINUE'), 0x12ED8C),
                         (('PRIZE_5000', 'PRIZE_2000', 'PRIZE_1000', 'PRIZE_500'), 0x12EE2C)):
        parts = [p for name in names for p in rows[name]['source_parts_in_reading_order']]
        for n, part in enumerate(parts):
            start = part['offset']
            raw = bytes.fromhex(part['source_hex'])
            if word(source, table + 4 * n) != BASE + start or source[start:start + len(raw)] != raw:
                raise ValueError('Source fragment order differs')
    font = GameAsciiFont.from_arm9(inputs[2])
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native font differs')
    instruction_xy = struct.unpack_from('<2I', source, 0x12EC8C)
    prize_xy = struct.unpack_from('<2I', source, 0x12ECCC)
    if instruction_xy != (48, 144) or prize_xy != (80, 160):
        raise ValueError('Original geometry differs')
    output = Path('work/qa/grand_race_results_layout')
    output.mkdir(parents=True, exist_ok=True)
    panels, selections = [], []

    def panel_for(name, groups):
        panel = Image.new('RGB', (256, 192), '#eef1f5')
        for row_name, count, x, y in groups:
            lines = fit_lines(rows[row_name]['english'], count, x, y)
            for n, line in enumerate(lines):
                for pos, char in enumerate(line):
                    panel.paste('#183047', (x + pos * 6, y + n * 16), font.decode(char))
            selections.append({'id': rows[row_name]['id'], 'lines': lines,
                               'position': [x, y], 'line_stride': 16,
                               'complete_english': ' '.join(lines)})
        panels.append((name, panel))

    panel_for('Results instruction list (owner + 0x6c)', [
        ('RESULTS', 1, 48, 144), ('CONTINUE', 2, 48, 160)])
    for name in ('PRIZE_5000', 'PRIZE_2000', 'PRIZE_1000', 'PRIZE_500'):
        panel_for(name + ' (owner list)', [(name, 1, 80, 160)])
    sheet = Image.new('RGB', (1024, 1236), 'white')
    draw = ImageDraw.Draw(sheet)
    for n, (name, panel) in enumerate(panels):
        x, y = n % 2 * 512, n // 2 * 412
        draw.text((x + 4, y + 4), name, fill='black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (x, y + 28))
    sheet.save(output / 'sheet.png')
    report = {'candidate_sha256': CANDIDATE_SHA,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'consumer_locks': locks, 'selections': selections,
              'preview_reviewed': args.reviewed, 'rom_written': False,
              'limitations': ['Isolated text areas only; no full-screen painting or gameplay acceptance.',
                              'Placement/number compound image widgets require separate proof.',
                              'List ownership is proven; physical screen routing remains pending.',
                              'Allocation/release gates remain pending.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'preview': str(output / 'sheet.png'), 'selections': len(selections),
                      'preview_reviewed': args.reviewed, 'rom_written': False}))


if __name__ == '__main__':
    main()
