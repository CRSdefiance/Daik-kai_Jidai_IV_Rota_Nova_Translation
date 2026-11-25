"""Prove and preview full error-return instructions in three native line widgets."""

import argparse
import hashlib
import itertools
import json
import struct
from pathlib import Path

from PIL import Image

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

REGION = (0x16B93C, 0x16B980)
FIELDS = (0xF835C, 0xF8360, 0xF8368)
ORIGINAL_STARTS = (0x16B93C, 0x16B954, 0x16B968)
GEOMETRIES = (0x12EEA8, 0x12EEB0, 0x12EEB8)
SPANS = ((0xF81EC, 0xF8338), (0xF834C, 0xF8370),
         (0x16B290, 0x16B29C), (0xFB004, 0xFB038),
         (0xFAFFC, 0xFB004), (0xF37D8, 0xF3830),
         (0xD1604, 0xD1850), (0x12EEA8, 0x12EEC0))


def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def resolve_pc_load(data, offset, register, literal):
    # ARM LDR Rd,[PC,#positive immediate], with PC = instruction + 8.
    instruction = word(data, offset)
    if instruction & 0xFFFFF000 != 0xE59F0000 | register << 12:
        raise ValueError(f'Unexpected PC-relative load at {offset:#x}')
    if offset + 8 + (instruction & 0xFFF) != literal:
        raise ValueError(f'Wrong literal target at {offset:#x}')


def check_branch(data, offset, target):
    instruction = word(data, offset)
    if instruction >> 24 != 0xEB:
        raise ValueError('Expected ARM BL')
    displacement = instruction & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 0x1000000
    if offset + 8 + displacement * 4 != target:
        raise ValueError('Wrong native draw branch')


def balanced_lines(english, count=3):
    if (not english or english != english.strip() or '  ' in english
            or any(ord(char) < 0x20 or ord(char) > 0x7E for char in english)):
        raise ValueError('Native widget prose must be one printable ASCII paragraph without authored spacing')
    if count < 1:
        raise ValueError('Native widget count must be positive')
    words = english.split(' ')
    possibilities = []
    for cuts in itertools.combinations(range(1, len(words)), count - 1):
        boundaries = (0, *cuts, len(words))
        lines = [' '.join(words[lo:hi]) for lo, hi in itertools.pairwise(boundaries)]
        lengths = [len(line) for line in lines]
        if max(lengths) <= 40:
            possibilities.append(((max(lengths), sum(n * n for n in lengths), cuts), lines))
    if not possibilities:
        raise ValueError(f'Full paragraph does not fit {count} native line widgets')
    lines = min(possibilities)[1]
    if ' '.join(lines) != english:
        raise ValueError('Formatting changed complete English')
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true', help='Record completed exact-font preview review.')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned input ROM differs')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open(CANONICAL).read_file('/__arm9__.bin')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    if hashlib.sha256(clean).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean ARM9 differs')
    locks = []
    for lo, hi in SPANS:
        if clean[lo:hi] != canonical[lo:hi] or canonical[lo:hi] != current[lo:hi]:
            raise ValueError(f'Consumer/context changed at {lo:#x}')
        locks.append({'start': lo, 'end': hi,
                      'sha256': hashlib.sha256(clean[lo:hi]).hexdigest()})
    if tuple(word(clean, 0x16B290 + n * 4) - BASE for n in range(3)) != (0xF37D8, 0xFB004, 0xFAFFC):
        raise ValueError('Derived text-widget virtual methods differ')
    check_branch(clean, 0xF3818, 0xD1604)
    # Constructor loads overwrite the abstract base table with this derived table.
    resolve_pc_load(clean, 0xF81FC, 1, 0xF8354)
    if word(clean, 0xF8354) != BASE + 0x16B290:
        raise ValueError('Wrong derived text widget')
    for instruction, register, literal in ((0xF8214, 2, FIELDS[0]),
                                           (0xF8218, 1, 0xF8358),
                                           (0xF8264, 2, FIELDS[1]),
                                           (0xF8268, 1, 0xF8364),
                                           (0xF82B4, 2, FIELDS[2]),
                                           (0xF82B8, 1, 0xF836C)):
        resolve_pc_load(clean, instruction, register, literal)
    if tuple(word(clean, field) - BASE for field in FIELDS) != ORIGINAL_STARTS:
        raise ValueError('Instruction text ownership differs')
    if tuple(word(clean, field) - BASE for field in (0xF8358, 0xF8364, 0xF836C)) != GEOMETRIES:
        raise ValueError('Instruction geometry pointers differ')
    coords = [struct.unpack_from('<2i', clean, offset) for offset in GEOMETRIES]
    if coords != [(16, 16), (16, 32), (16, 48)]:
        raise ValueError('Mapped line positions differ')
    refs = [(p, word(clean, p) - BASE) for p in range(0, len(clean) - 3, 4)
            if REGION[0] <= word(clean, p) - BASE < REGION[1]]
    if refs != list(zip(FIELDS, ORIGINAL_STARTS, strict=True)):
        raise ValueError('Additional references into the shared instruction region')
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    row = next(row for row in manuscript['records'] if row['id'] == 'GRAND_RACE_UI_RETURN_MENU')
    if tuple(part['offset'] for part in row['source_parts_in_reading_order']) != ORIGINAL_STARTS:
        raise ValueError('Full source sentence has a different reading order')
    for part in row['source_parts_in_reading_order']:
        raw = bytes.fromhex(part['source_hex'])
        if clean[part['offset']:part['offset'] + len(raw)] != raw:
            raise ValueError('Source sentence differs')
    lines = balanced_lines(row['english'])
    blob = b''
    starts = []
    for line in lines:
        starts.append(REGION[0] + len(blob))
        blob += line.encode('ascii') + b'\0'
    used = len(blob)
    if used > REGION[1] - REGION[0]:
        raise ValueError('Complete formatted text exceeds the shared source allocation')
    blob += bytes(REGION[1] - REGION[0] - used)
    research = bytearray(current)
    research[REGION[0]:REGION[1]] = blob
    for field, start in zip(FIELDS, starts, strict=True):
        struct.pack_into('<I', research, field, BASE + start)
    font = GameAsciiFont.from_arm9(current)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Exact ASCII font differs')
    panel = Image.new('RGB', (256, 192), '#eef1f5')
    selections = []
    for field, line, (x, y) in zip(FIELDS, lines, coords, strict=True):
        start = word(research, field) - BASE
        selected = research[start:research.index(0, start)].decode('ascii')
        if selected != line or x + len(line) * 6 > 256 or y + 11 > 192:
            raise ValueError('Saved line selection or native glyph bounds differ')
        draws = [{'character': char, 'x': x + n * 6, 'y': y} for n, char in enumerate(selected)]
        for draw in draws:
            panel.paste('#183047', (draw['x'], draw['y']), font.decode(draw['character']))
        selections.append({'pointer_field': field, 'start': start, 'line': selected,
                           'position': [x, y], 'draws': draws})
    if ' '.join(selection['line'] for selection in selections) != row['english']:
        raise ValueError('Saved native selections drop source-reviewed English')
    output = Path('work/qa/grand_race_wireless_return')
    output.mkdir(parents=True, exist_ok=True)
    panel.resize((768, 576), Image.Resampling.NEAREST).save(output / 'preview.png')
    report = {'status': ('research-native-widget-layout-reviewed-integration-and-runtime-pending'
                         if args.reviewed else 'research-native-widget-format-proven-preview-review-and-integration-pending'),
              'runtime_verified': False, 'candidate_changed': False,
              'preview_reviewed': args.reviewed,
              'preview_sha256': hashlib.sha256((output / 'preview.png').read_bytes()).hexdigest(),
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'id': row['id'], 'complete_english': row['english'], 'consumer_locks': locks,
              'derived_widget_vtable': 0x16B290, 'constructor': 0xFB004,
              'draw': 0xF37D8, 'native_glyph_draw': 0xD1604,
              'region': list(REGION), 'capacity': REGION[1] - REGION[0], 'used': used,
              'source_references': refs, 'selections': selections,
              'replacement_region_hex': blob.hex(),
              'formatting': 'Automatically balance a complete paragraph across three independently positioned NUL-terminated ASCII strings. No LF, pair guards or discarded characters.'}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'lines': lines, 'used': used,
                      'capacity': report['capacity'], 'candidate_changed': False}))


if __name__ == '__main__':
    main()
