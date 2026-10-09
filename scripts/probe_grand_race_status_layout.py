"""Map complete wireless status text and the native clearing of sibling rows."""

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
from scripts.probe_grand_race_results_layout import fit_lines
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word


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
        raise ValueError('Clean Japanese ARM9 differs')
    locks = []
    for lo, hi in ((0xF80D8, 0xF8370), (0xF8A00, 0xF8B4C),
                   (0xF8CCC, 0xF8D00), (0xF912C, 0xF9174),
                   (0xF98FC, 0xF9A6C), (0xF9F54, 0xF9F90),
                   (0xFA0CC, 0xFA11C), (0x12EEA8, 0x12EEB0),
                   (0x12ECF4, 0x12ECFC), (0x12EC84, 0x12EC8C),
                   (0x16B9DC, 0x16B9E0), (0x16BA24, 0x16BA28),
                   (0xFAFFC, 0xFB038), (0xF37D8, 0xF3830),
                   (0xD1604, 0xD1850), (0x16B290, 0x16B29C)):
        if any(data[lo:hi] != source[lo:hi] for data in inputs[1:]):
            raise ValueError(f'Status caller/source differs at {lo:#x}')
        locks.append({'start': lo, 'end': hi,
                      'sha256': hashlib.sha256(source[lo:hi]).hexdigest()})
    selections = [
        ('ERROR', 0x16B8EC, 0xF8114, 4, 0xF833C, (16, 16), 'owner+0x6c; connection mode 2'),
        ('DISCONNECTED', 0x16B908, 0xF811C, 4, 0xF8340, (16, 16), 'owner+0x6c; connection mode 3'),
        ('FULL', 0x16B91C, 0xF8124, 4, 0xF8344, (16, 16), 'owner+0x6c; connection mode 4'),
        ('WAIT_REGISTRATION', 0x16B9B4, 0xF8CCC, 1, 0xF9158, (16, 64), 'joining body widget at SP+0x7c'),
        ('HOST_STARTING', 0x16BA08, 0xF9F58, 1, 0xFA114, (16, 64), 'hosting body widget at SP+0xa8'),
    ]
    for _, target, at, reg, literal, _, _ in selections:
        resolve_pc_load(source, at, reg, literal)
        if word(source, literal) != BASE + target:
            raise ValueError('Status source selection differs')
    for at, target in ((0xF8CD4, 0xFAFFC), (0xF8CEC, 0xFAFFC),
                       (0xF9F60, 0xFAFFC), (0xF9F78, 0xFAFFC),
                       (0xF8B20, 0xFB004), (0xF9A40, 0xFB004), (0xF3818, 0xD1604)):
        check_branch(source, at, target)
    for at, reg, literal, target in ((0xF8194, 1, 0xF8358, 0x12EEA8),
                                    (0xF8AC4, 0, 0xF9148, 0x12ECF4),
                                    (0xF99D0, 0, 0xFA0E8, 0x12EC84),
                                    (0xF8CD8, 4, 0xF915C, 0x16B9DC),
                                    (0xF9F64, 4, 0xFA118, 0x16BA24)):
        resolve_pc_load(source, at, reg, literal)
        if word(source, literal) != BASE + target:
            raise ValueError('Status geometry/clear-string selection differs')
    for start, xy in ((0x12EEA8, (16, 16)), (0x12ECF4, (16, 64)), (0x12EC84, (16, 64))):
        if struct.unpack_from('<2I', source, start) != xy:
            raise ValueError('Status widget coordinates differ')
    required = {0xF8CD0: 0xE28D007C, 0xF8CDC: 0xE28D509C,
                0xF8CF4: 0xE3560002, 0xF8CF8: 0xE2855020,
                0xF9F5C: 0xE28D00A8, 0xF9F68: 0xE28D50C8,
                0xF9F80: 0xE3560003, 0xF9F84: 0xE2855020}
    if any(word(source, at) != value for at, value in required.items()):
        raise ValueError('Body widget identity/cleared sibling count differs')
    if source[0x16B9DC:0x16B9E0] != bytes(4) or source[0x16BA24:0x16BA28] != bytes(4):
        raise ValueError('Native clear strings differ')
    resolve_pc_load(source, 0xF8174, 1, 0xF8354)
    if word(source, 0xF8354) != BASE + 0x16B290:
        raise ValueError('Error status uses a different native text widget')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {r['id'].removeprefix('GRAND_RACE_UI_'): r for r in
            json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    font = GameAsciiFont.from_arm9(inputs[2])
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native ASCII font differs')
    output = Path('work/qa/grand_race_status_layout')
    output.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1024, 1236), 'white')
    draw = ImageDraw.Draw(sheet)
    results = []
    for n, (name, target, _, _, literal, (x, y), scope) in enumerate(selections):
        row = rows[name]
        part = row['source_parts_in_reading_order'][0]
        raw = bytes.fromhex(part['source_hex'])
        if part['offset'] != target or source[target:target + len(raw)] != raw:
            raise ValueError('Status manuscript source differs')
        line = fit_lines(row['english'], 1, x, y)[0]
        panel = Image.new('RGB', (256, 192), '#eef1f5')
        for index, char in enumerate(line):
            panel.paste('#183047', (x + index * 6, y), font.decode(char))
        sx, sy = n % 2 * 512, n // 2 * 412
        draw.text((sx + 4, sy + 4), name + ' - isolated status text', fill='black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (sx, sy + 28))
        results.append({'id': row['id'], 'english': line, 'position': [x, y],
                        'source_reference': literal, 'widget_scope': scope,
                        'leading_character_intact': True, 'width_px': len(line) * 6})
    sheet.save(output / 'sheet.png')
    report = {'candidate_sha256': CANDIDATE_SHA,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'consumer_locks': locks, 'selections': results,
              'cleared_sibling_rows': {'WAIT_REGISTRATION': [[16, 80]],
                                       'HOST_STARTING': [[16, 80], [16, 96]]},
              'context_correction': 'HOST_STARTING is a body status row, not a transition heading.',
              'preview_reviewed': args.reviewed, 'rom_written': False,
              'limitations': ['Isolated status areas; physical screen routing/full composition/runtime pending.',
                              'Allocation and release gates remain pending.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'selections': len(results), 'preview': str(output / 'sheet.png'),
                      'rom_written': False}))


if __name__ == '__main__':
    main()
