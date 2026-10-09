"""Source-derived race region/role/player labels; full wireless runtime pending."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_player_index import prove_guard
from scripts.prepare_grand_race_remaining_ui_manuscript import BASE, CLEAN_ARM9_SHA
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word

CANDIDATE = 'out/all_routes_combined_v136_candidate.nds'
CANDIDATE_SHA = '967343c300ce23cc1665ee497b1a85f734460f9ca71aa1f3bee479027d96ca6c'
SPANS = ((0xF8C58, 0xF8CCC), (0xFB5C4, 0xFB618), (0xF913C, 0xF9140),
         (0xFA0DC, 0xFA0E0), (0xF86E4, 0xF89FC), (0xF93D4, 0xF98F0), (0xFA308, 0xFA5A8),
         (0xF8E14, 0xF8E80), (0xF9164, 0xF916C), (0xF9CC4, 0xF9D1C),
         (0xFA100, 0xFA108), (0xFAF88, 0xFB120), (0xF37D8, 0xF3830),
         (0xD1604, 0xD1850), (0x16B290, 0x16B2B4),
         (0x12EE3C, 0x12EE4C), (0x12ED24, 0x12ED2C),
         (0x12EE1C, 0x12EE2C), (0x12ECE4, 0x12ECEC), (0x12ECC4, 0x12ECCC))


def geometry(kind, index):
    if kind == 'region' and 0 <= index < 4:
        # F8720/F9410: grid origin (4+126*(i&1),4+84*(i>>1)); then +4.
        x, y = 8 + 126 * (index & 1), 8 + 84 * (index >> 1)
        return (x, y), (x, y, 108, 12)
    if kind == 'role' and 0 <= index < 2:
        # FA350: initial 12ECE4.x=32; r8 starts 32, advances by 32.
        x, y = 32, 32 + 32 * index
        return (x, y), (x - 8, y - 8, 124, 28)
    if kind == 'player' and 0 <= index < 4:
        return (80, 160), None
    raise ValueError('Invalid native label group/index')


def check_fit(english, position, frame):
    if not english or english != english.strip() or any(not 32 <= ord(c) <= 126 for c in english):
        raise ValueError('Complete printable English required')
    x, y = position
    width = len(english) * 6
    if x < 0 or y < 0 or x + width > 256 or y + 11 > 192:
        raise ValueError('Full text exceeds screen bounds')
    if frame:
        left, top, w, h = frame
        if x < left or y < top or x + width > left + w or y + 11 > top + h:
            raise ValueError('Full text exceeds native frame')
    return width


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    if sha(Path(CANDIDATE).read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Current combined candidate differs')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    if sha(clean) != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese source differs')
    locks = []
    for lo, hi in SPANS:
        if clean[lo:hi] != current[lo:hi]:
            raise ValueError(f'Native consumer differs at {lo:#x}')
        locks.append({'start': lo, 'end': hi, 'sha256': sha(current[lo:hi])})
    for at, register, literal, target in (
        (0xF87A8, 2, 0xF89F8, 0x12EE3C), (0xF9498, 2, 0xF98E4, 0x12EE3C),
        (0xFA390, 0, 0xFA5A4, 0x12ED24), (0xFA308, 0, 0xFA5A0, 0x12ECE4),
        (0xF8E4C, 1, 0xF9164, 0x12EE1C), (0xF9CEC, 1, 0xFA100, 0x12EE1C),
        (0xF8E60, 1, 0xF9168, 0x12ECC4), (0xF9CFC, 1, 0xFA104, 0x12ECC4)):
        resolve_pc_load(current, at, register, literal)
        if word(current, literal) != BASE + target:
            raise ValueError('Native table/geometry selection differs')
    for at, target in ((0xF87BC, 0xFAF90), (0xF94AC, 0xFAF90),
                       (0xFA3A4, 0xFAF90), (0xFAFF0, 0xFB004),
                       (0xFB09C, 0xD1604), (0xF3818, 0xD1604)):
        check_branch(current, at, target)
    if struct.unpack_from('<2I', current, 0x12ECE4) != (32, 0) or struct.unpack_from('<2I', current, 0x12ECC4) != (80, 160):
        raise ValueError('Native geometry differs')
    if struct.unpack_from('<4I', current, 0x16B2A4) != tuple(BASE + p for p in (0xFB038, 0xFB004, 0xFAFFC, 0xFAF88)):
        raise ValueError('Framed-label virtual draw/setter/style differs')
    guard = prove_guard(current)
    if word(current, 0xF913C) != BASE + 0x16B290 or word(current, 0xFA0DC) != BASE + 0x16B290:
        raise ValueError('Joining or hosting player-status vtable differs')
    if struct.unpack_from('<3I', current, 0x16B290) != tuple(BASE + p for p in (0xF37D8, 0xFB004, 0xFAFFC)):
        raise ValueError('Player status draw/setter/style slots differ')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {r['id'].removeprefix('GRAND_RACE_UI_'): r for r in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    font = GameAsciiFont.from_arm9(current)
    if sha(font.glyphs) != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Exact ASCII font differs')
    panels, selections = [], []
    for kind, table, names in (
        ('region', 0x12EE3C, ('NORTH_SEA', 'MEDITERRANEAN', 'SOUTHEAST_ASIA', 'EAST_ASIA')),
        ('role', 0x12ED24, ('HOST', 'JOIN')),
        ('player', 0x12EE1C, ('PLAYER_1', 'PLAYER_2', 'PLAYER_3', 'PLAYER_4'))):
        for index, name in enumerate(names):
            row = rows[name]
            part, = row['source_parts_in_reading_order']
            offset = word(current, table + index * 4) - BASE
            raw = bytes.fromhex(part['source_hex'])
            if offset != part['offset'] or clean[offset:offset + len(raw)] != raw or current[offset:offset + len(raw)] != raw:
                raise ValueError('Complete Japanese table order differs')
            position, frame = geometry(kind, index)
            width = check_fit(row['english'], position, frame)
            panel = Image.new('RGB', (256, 192), '#eef1f5')
            draw = ImageDraw.Draw(panel)
            if frame:
                x, y, w, h = frame
                draw.rectangle((x, y, x + w - 1, y + h - 1), outline='#aab4c0')
            for i, char in enumerate(row['english']):
                panel.paste('#183047', (position[0] + i * 6, position[1]), font.decode(char))
            panels.append((name, panel))
            selections.append({'id': row['id'], 'english': row['english'], 'table_field': table + index * 4,
                               'position': position, 'frame': frame, 'width_px': width,
                               'complete_source_and_leading_character': True})
    sheet = Image.new('RGB', (1024, 2060), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, (name, panel) in enumerate(panels):
        x, y = i % 2 * 512, i // 2 * 412
        draw.text((x + 4, y + 4), name, fill='black')
        sheet.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (x, y + 28))
    output = Path('work/qa/grand_race_region_player_layout_v136')
    output.mkdir(parents=True, exist_ok=True)
    sheet.save(output / 'sheet.png')
    report = {'status': 'research-native-label-layout', 'rom_written': False, 'runtime_verified': False,
              'candidate_sha256': CANDIDATE_SHA, 'source_locks': locks, 'selections': selections,
              'native_signed_player_index_guard': guard,
              'player_status_virtual_tables_source_verified': True,
              'manuscript_sha256': sha(manuscript_path.read_bytes()), 'preview_reviewed': args.reviewed,
              'preview_sha256': sha((output / 'sheet.png').read_bytes()),
              'draw_paths': {'region_and_role': ['FAF90', 'FB004', 'FB038', 'D1604'],
                             'player_status': ['FB004', 'F37D8', 'D1604']},
              'limitations': ['Source-derived label coordinates/frame only; artwork and whole-screen composition pending.',
                              'Native player index guard is proven; complete virtual execution and physical screen routing still require checks.',
                              'No release gates or ROM integration generated.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Ten complete region/role/player labels fit native bounds; runtime pending.')


if __name__ == '__main__':
    main()
