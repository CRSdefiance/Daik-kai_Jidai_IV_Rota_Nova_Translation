"""Map and preview the final four unclassified scoped race UI messages."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_ascii_requests import execute
from scripts.plan_grand_race_ui_allocation_v136 import BASE, CANDIDATE, CANDIDATE_SHA
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Current candidate differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xF7998, 0xF79B4), (0xF83B4, 0xF83D0), (0xFA15C, 0xFA178),
             (0xFAED4, 0xFAF88), (0xFABB0, 0xFADE4), (0x12EFB8, 0x12F018),
             (0x16B0E4, 0x16B0E8), (0x16B0FC, 0x16B100), (0x16B290, 0x16B29C))
    if any(source[lo:hi] != clean[lo:hi] for lo, hi in spans):
        raise ValueError('Native heading/player-label consumer differs')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {r['id'].removeprefix('GRAND_RACE_UI_'): r for r in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    for name in ('OVER', 'TITLE', 'CHOOSE_ROLE', 'EMPTY_PLAYER'):
        part, = rows[name]['source_parts_in_reading_order']
        raw = bytes.fromhex(part['source_hex'])
        padded = raw.ljust(part['aligned_source_bytes_including_nul'], b'\0')
        start = part['offset']
        if any(a[start:start + len(padded)] != padded for a in (clean, source)):
            raise ValueError('Complete Japanese message/padding differs')
    selections = []
    for name, at, field, call, numeric_id in (
        ('OVER', 0xF7998, 0xF8004, 0xF79A4, 11),
        ('TITLE', 0xF83B4, 0xF8440, 0xF83C0, 0),
        ('CHOOSE_ROLE', 0xFA15C, 0xFA578, 0xFA168, 3)):
        row = rows[name]
        part, = row['source_parts_in_reading_order']
        resolve_pc_load(source, at, 2, field)
        if word(source, field) != BASE + part['offset']:
            raise ValueError('Heading source pointer differs')
        check_branch(source, call, 0xFAED4)
        # The r1 argument identifies artwork; constructor's text y is always 2.
        x = (256 - len(row['english']) * 6) // 2
        if x < 0:
            raise ValueError('Complete heading exceeds centered display')
        selections.append({'id': row['id'], 'english': row['english'], 'position': [x, 2],
                           'artwork_selector': numeric_id, 'native_requests': execute(source, row['english'], x, 2, 1)})
    if word(source, 0xFADAC) != 0x059F0028 or word(source, 0xFADA8) != 0xE3500000:
        raise ValueError('Conditional null-name fallback load differs')
    empty = rows['EMPTY_PLAYER']
    if word(source, 0xFADDC) != BASE + empty['source_parts_in_reading_order'][0]['offset']:
        raise ValueError('Null player-name fallback pointer differs')
    resolve_pc_load(source, 0xFACBC, 2, 0xFAD2C)
    if word(source, 0xFAD2C) != BASE + 0x12EFB8:
        raise ValueError('Player text-position table differs')
    check_branch(source, 0xFACD4, 0xD1604)
    if word(source, 0x16B0E4) != BASE + 0xFABB0 or word(source, 0x16B0FC) != BASE + 0xFADE4:
        raise ValueError('Player-info/heading draw callback differs')
    for index in range(4):
        x, y = struct.unpack_from('<2I', source, 0x12EFB8 + index * 24 + 8)
        if x + len(empty['english']) * 6 > 256 or y + 11 > 192:
            raise ValueError('Complete empty-player label exceeds display')
        selections.append({'id': empty['id'], 'slot': index, 'english': empty['english'], 'position': [x, y],
                           'native_requests': execute(source, empty['english'], x, y, 1)})
    font = GameAsciiFont.from_arm9(source)
    sheet = Image.new('RGB', (1024, 1648), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(selections):
        panel = Image.new('RGB', (256, 192), '#eef1f5')
        for i, char in enumerate(row['english']):
            panel.paste('#183047', (row['position'][0] + i * 6, row['position'][1]), font.decode(char))
        left, top = index % 2 * 512, index // 2 * 412
        draw.text((left + 4, top + 4), row['id'] + f" slot {row.get('slot', '-')}", fill='black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (left, top + 28))
    output = Path('work/qa/grand_race_final_labels_v136')
    output.mkdir(parents=True, exist_ok=True)
    sheet.save(output / 'sheet.png')
    report = {'status': 'research-final-four-native-labels', 'rom_written': False, 'runtime_verified': False,
              'candidate_sha256': CANDIDATE_SHA, 'manuscript_sha256': sha(manuscript_path.read_bytes()),
              'source_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])} for lo, hi in spans],
              'selections': selections, 'preview_reviewed': args.reviewed,
              'preview_sha256': sha((output / 'sheet.png').read_bytes()),
              'limitations': ['Text positions and source-traced consumers only; frame artwork/fullscreen/runtime pending.',
                              'Player slot index is supplied by the native caller; complete virtual/widget activation remains pending.',
                              'No release batch or ROM integration generated.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Four remaining messages mapped; three centered headings and four empty-player slot positions fit.')


if __name__ == '__main__':
    main()
