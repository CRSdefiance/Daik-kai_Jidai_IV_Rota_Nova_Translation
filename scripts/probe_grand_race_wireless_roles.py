"""Prove full wireless role instructions in the four mapped native widgets."""

import argparse
import hashlib
import itertools
import json
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
from scripts.probe_grand_race_wireless_return import check_branch, resolve_pc_load, word

SPANS = ((0xFA0F8, 0xFA2B0), (0xFA570, 0xFA598), (0x12ED14, 0x12ED1C),
         (0x12EDFC, 0x12EE0C), (0x16B290, 0x16B29C),
         (0xFB004, 0xFB038), (0xFAFFC, 0xFB004),
         (0xF37D8, 0xF3830), (0xD1604, 0xD1850))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned input ROM differs')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open(CANONICAL).read_file('/__arm9__.bin')
    current = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    if hashlib.sha256(clean).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean Japanese source differs')
    locks = []
    for lo, hi in SPANS:
        if clean[lo:hi] != canonical[lo:hi] or canonical[lo:hi] != current[lo:hi]:
            raise ValueError('Traced role widget code/context changed')
        locks.append({'start': lo, 'end': hi, 'sha256': hashlib.sha256(clean[lo:hi]).hexdigest()})
    resolve_pc_load(clean, 0xFA200, 0, 0xFA58C)
    resolve_pc_load(clean, 0xFA214, 6, 0xFA590)
    if word(clean, 0xFA58C) != BASE + 0x12ED14 or word(clean, 0xFA590) != BASE + 0x12EDFC:
        raise ValueError('Role geometry/table differs')
    if (word(clean, 0x12ED14), word(clean, 0x12ED18)) != (16, 64):
        raise ValueError('Initial role text position differs')
    for offset, expected in ((0xFA270, 0xE3A05001), (0xFA29C, 0xE2800010),
                             (0xFA2A4, 0xE3590004), (0xFA2A8, 0xE2888020)):
        if word(clean, offset) != expected:
            raise ValueError('Role style, line stride, count or object stride differs')
    check_branch(clean, 0xFA284, 0xFB004)
    check_branch(clean, 0xF3818, 0xD1604)
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    row = next(row for row in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']
               if row['id'] == 'GRAND_RACE_UI_ROLES')
    parts = row['source_parts_in_reading_order']
    if [part['offset'] for part in parts] != [word(clean, 0x12EDFC + n * 4) - BASE for n in range(4)]:
        raise ValueError('Role source sentence order differs')
    capacities = []
    for part in parts:
        offset, size = part['offset'], part['aligned_source_bytes_including_nul']
        raw = bytes.fromhex(part['source_hex'])
        if any(data[offset:offset + len(raw)] != raw for data in (clean, canonical, current)):
            raise ValueError('Full Japanese role source differs')
        if any(clean[offset + len(raw):offset + size]):
            raise ValueError('Role alignment padding contains unrelated data')
        capacities.append(min(40, size - 1))
    words = row['english'].split(' ')
    candidates = []
    for cuts in itertools.combinations(range(1, len(words)), 3):
        lines = [' '.join(words[lo:hi]) for lo, hi in itertools.pairwise((0, *cuts, len(words)))]
        lengths = [len(line) for line in lines]
        if all(length <= capacity for length, capacity in zip(lengths, capacities, strict=True)):
            candidates.append(((max(lengths), sum(length * length for length in lengths), cuts), lines))
    if not candidates:
        raise ValueError('Full English must be relocated; do not shorten it to fit')
    lines = min(candidates)[1]
    if ' '.join(lines) != row['english']:
        raise ValueError('Formatting drops complete English')
    font = GameAsciiFont.from_arm9(current)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Native font differs')
    panel = Image.new('RGB', (256, 192), '#eef1f5')
    selections = []
    for n, (part, line) in enumerate(zip(parts, lines, strict=True)):
        x, y = 16, 64 + n * 16
        raw = line.encode('ascii') + b'\0'
        if any(byte < 0x20 or byte > 0x7E for byte in raw[:-1]):
            raise ValueError('Native line must be printable ASCII without LF/guards')
        if x + len(line) * 6 > 256 or y + 11 > 192:
            raise ValueError('Native glyph bounds overflow')
        for index, char in enumerate(line):
            panel.paste('#183047', (x + index * 6, y), font.decode(char))
        selections.append({'pointer_field': 0x12EDFC + n * 4, 'offset': part['offset'],
                           'line': line, 'position': [x, y], 'style': 1,
                           'replacement_hex': (raw + bytes(part['aligned_source_bytes_including_nul'] - len(raw))).hex(),
                           'width_pixels': len(line) * 6})
    output = Path('work/qa/grand_race_wireless_roles')
    output.mkdir(parents=True, exist_ok=True)
    panel.resize((768, 576), Image.Resampling.NEAREST).save(output / 'preview.png')
    report = {'status': 'research-static-role-layout-reviewed-integration-and-runtime-pending'
              if args.reviewed else 'research-static-role-layout-proven-preview-review-pending',
              'preview_reviewed': args.reviewed, 'runtime_verified': False,
              'candidate_changed': False, 'complete_english': row['english'],
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'consumer_locks': locks, 'selections': selections,
              'paragraph_bytes_preserved': ' '.join(lines) == row['english'],
              'original_pointer_fields_preserved': True}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'lines': lines, 'candidate_changed': False}))


if __name__ == '__main__':
    main()
