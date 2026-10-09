"""Map four wireless text screens; preserve and report full-prose layout failures."""

import argparse
import hashlib
import json
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

# Source table, caller geometry and complete message groups. Counts belong to
# the mapped native widgets; paragraph breaks are generated from English.
SCREENS = [
    {'id': 'search', 'header': 'JOIN_SEARCH', 'header_offset': 0x16B9A4,
     'header_call': 0xF8A4C, 'header_load': (0xF8A40, 2, 0xF9134),
     'table': 0x12ECD4, 'geometry': 0x12ECF4,
     'loads': [(0xF8AC4, 0, 0xF9148), (0xF8AC8, 6, 0xF914C)],
     'loop': (0xF8B10, 0xF8B4C), 'call': 0xF8B20,
     'stride': 0xF8B38, 'count': (0xF8B40, 2),
     'span': (0xF8A00, 0xF8B4C), 'literal_span': (0xF912C, 0xF9150),
     'messages': [('SEARCH', 1), ('WAIT', 1)]},
    {'id': 'host_choosing', 'header': 'JOIN_AREA', 'header_offset': 0x16B990,
     'header_call': 0xF84D8, 'header_load': (0xF84CC, 2, 0xF89C4),
     'table': 0x12ECEC, 'geometry': 0x12EC9C,
     'loads': [(0xF8550, 0, 0xF89D8), (0xF8554, 6, 0xF89DC)],
     'loop': (0xF859C, 0xF85D8), 'call': 0xF85AC,
     'stride': 0xF85C4, 'count': (0xF85CC, 2),
     'span': (0xF848C, 0xF85D8), 'literal_span': (0xF89B8, 0xF89E0),
     'messages': [('HOST_SELECTING', 2)]},
    {'id': 'choose_area', 'header': 'HOST_AREA', 'header_offset': 0x16B9E0,
     'header_call': 0xF91F4, 'header_load': (0xF91E8, 2, 0xF98B0),
     'table': 0x12EC60, 'geometry': 0x12ECFC,
     'loads': [(0xF9250, 0, 0xF98C4), (0xF9260, 6, 0xF98C8)],
     'loop': (0xF928C, 0xF92C8), 'call': 0xF929C,
     'stride': 0xF92B4, 'count': (0xF92BC, 1),
     'span': (0xF91A8, 0xF92C8), 'literal_span': (0xF98A8, 0xF98CC),
     'messages': [('CHOOSE_AREA', 1)]},
    {'id': 'host_waiting', 'header': 'HOST_OPEN', 'header_offset': 0x16B9F4,
     'header_call': 0xF9948, 'header_load': (0xF993C, 2, 0xFA0D4),
     'table': 0x12ED68, 'geometry': 0x12EC84,
     'loads': [(0xF99D0, 0, 0xFA0E8), (0xF99E0, 6, 0xFA0EC)],
     'loop': (0xF9A30, 0xF9A6C), 'call': 0xF9A40,
     'stride': 0xF9A58, 'count': (0xF9A60, 3),
     'span': (0xF98FC, 0xF9A6C), 'literal_span': (0xFA0CC, 0xFA0F0),
     'messages': [('WAIT_PLAYERS', 1), ('CONFIRM_PLAYERS', 2)]},
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned ROM differs')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open(CANONICAL).read_file('/__arm9__.bin')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    if hashlib.sha256(clean).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese ARM9 differs')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {row['id'].removeprefix('GRAND_RACE_UI_'): row
            for row in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    font = GameAsciiFont.from_arm9(current)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native font differs')
    output = Path('work/qa/grand_race_wireless_screens')
    output.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1024, 824), 'white')
    sheet_draw = ImageDraw.Draw(sheet)
    screens = []
    for index, screen in enumerate(SCREENS):
        count = screen['count'][1]
        locks = []
        spans = [screen['span'], screen['literal_span'],
                 (screen['table'], screen['table'] + count * 4),
                 (screen['geometry'], screen['geometry'] + 8),
                 (0xFAED4, 0xFAF88), (0xFB004, 0xFB038),
                 (0xF37D8, 0xF3830), (0xD1604, 0xD1850)]
        for lo, hi in spans:
            if clean[lo:hi] != canonical[lo:hi] or canonical[lo:hi] != current[lo:hi]:
                raise ValueError(f"{screen['id']}: code/context differs")
            locks.append({'start': lo, 'end': hi, 'sha256': hashlib.sha256(clean[lo:hi]).hexdigest()})
        for load in screen['loads']:
            resolve_pc_load(clean, *load)
        if word(clean, screen['loads'][0][2]) != BASE + screen['geometry'] or word(clean, screen['loads'][1][2]) != BASE + screen['table']:
            raise ValueError('Wrong geometry or source table load')
        if (word(clean, screen['geometry']), word(clean, screen['geometry'] + 4)) != (16, 64):
            raise ValueError('Mapped screen position differs')
        if word(clean, screen['stride']) != 0xE2800010 or word(clean, screen['count'][0]) != 0xE3590000 | count:
            raise ValueError('Native row count/stride differs')
        check_branch(clean, screen['call'], 0xFB004)
        check_branch(clean, screen['header_call'], 0xFAED4)
        resolve_pc_load(clean, *screen['header_load'])
        if word(clean, screen['header_load'][2]) != BASE + screen['header_offset']:
            raise ValueError('Header selection differs')
        header = rows[screen['header']]
        if header['source_parts_in_reading_order'][0]['offset'] != screen['header_offset']:
            raise ValueError('Header manuscript source differs')
        panel = Image.new('RGB', (256, 192), '#eef1f5')
        header_x = (256 - len(header['english']) * 6) // 2
        if header_x < 0:
            raise ValueError('Complete screen heading overflows')
        for n, char in enumerate(header['english']):
            panel.paste('#183047', (header_x + n * 6, 2), font.decode(char))
        groups, source_index = [], 0
        for name, line_count in screen['messages']:
            row = rows[name]
            parts = row['source_parts_in_reading_order']
            if len(parts) != line_count:
                raise ValueError('Source message fragment count differs')
            for n, part in enumerate(parts):
                if word(clean, screen['table'] + (source_index + n) * 4) != BASE + part['offset']:
                    raise ValueError('Complete source reading order differs')
            try:
                lines = balanced_lines(row['english'], line_count)
                blockers = []
            except ValueError:
                lines = None
                blockers = ['Complete English cannot fit the mapped line widgets at 40 cells; layout must gain a line or another proven display method.']
            group = {'id': row['id'], 'english': row['english'], 'native_line_count': line_count,
                     'initial_position': [16, 64 + source_index * 16], 'lines': lines,
                     'layout_blockers': blockers}
            if lines is not None:
                for n, line in enumerate(lines):
                    y = 64 + (source_index + n) * 16
                    if 16 + len(line) * 6 > 256 or y + 11 > 192:
                        raise ValueError('Native glyph bounds overflow')
                    for pos, char in enumerate(line):
                        panel.paste('#183047', (16 + pos * 6, y), font.decode(char))
                group['encoded_bytes_including_nuls'] = sum(len(line) + 1 for line in lines)
                group['original_padded_bytes'] = sum(part['aligned_source_bytes_including_nul'] for part in parts)
                group['requires_relocation'] = group['encoded_bytes_including_nuls'] > group['original_padded_bytes']
            groups.append(group)
            source_index += line_count
        if source_index != count:
            raise ValueError('Screen source count differs')
        blocked = any(group['layout_blockers'] for group in groups)
        panel.resize((512, 384), Image.Resampling.NEAREST).save(output / f"{screen['id']}.png")
        x, y = index % 2 * 512, index // 2 * 412
        sheet_draw.text((x + 4, y + 4), screen['id'] + (' - full body layout blocked' if blocked else ' - mapped text preview'), fill='red' if blocked else 'black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (x, y + 28))
        screens.append({'id': screen['id'], 'header': header['english'], 'header_position': [header_x, 2],
                        'consumer_locks': locks, 'groups': groups, 'layout_blocked': blocked,
                        'preview_reviewed': args.reviewed and not blocked,
                        'geometry_scope': 'Header and instruction widgets only; other screen widgets/runtime still require verification.'})
    sheet.save(output / 'sheet.png')
    report = {'status': 'research-native-screen-layouts-with-explicit-blockers',
              'candidate_changed': False, 'runtime_verified': False, 'screens': screens,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'layout_blocked_screens': [screen['id'] for screen in screens if screen['layout_blocked']]}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'layout_blocked_screens': report['layout_blocked_screens'],
                      'screen_count': len(screens), 'candidate_changed': False}))


if __name__ == '__main__':
    main()
