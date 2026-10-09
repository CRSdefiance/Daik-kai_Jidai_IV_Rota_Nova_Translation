"""Lock and disassemble the local third-widget rewrite; do not write a ROM."""

import argparse
import hashlib
import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from PIL import Image

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.patch.grand_race_waiting_widget import END, START, rewrite_function
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_waiting_widgets import execute
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    BASE,
    CANDIDATE,
    CANDIDATE_SHA,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import balanced_lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned input ROM differs')
    sources = [NdsImage.open(path).read_file('/__arm9__.bin')
               for path in ('work/clean.nds', CANONICAL, CANDIDATE)]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError('Clean ARM9 differs')
    spans = ((START, 0xF89E8), (0x16B290, 0x16B29C),
             (0xFB004, 0xFB038), (0xFAFFC, 0xFB004), (0x12EC9C, 0x12ECA4))
    locks = []
    for lo, hi in spans:
        if not sources[0][lo:hi] == sources[1][lo:hi] == sources[2][lo:hi]:
            raise ValueError('Original code/context differs across locked inputs')
        locks.append({'start': lo, 'end': hi,
                      'sha256': hashlib.sha256(sources[0][lo:hi]).hexdigest()})
    original = sources[2]
    proposed, changes = rewrite_function(original)
    execution = execute(proposed, (0x02200000, 0x02200100, 0x02200200))
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    rows = {row['id']: row for row in json.loads(manuscript_path.read_text(encoding='utf-8'))['records']}
    body = rows['GRAND_RACE_UI_HOST_SELECTING']
    heading = rows['GRAND_RACE_UI_JOIN_AREA']
    if [part['offset'] for part in body['source_parts_in_reading_order']] != [0x16B328, 0x16B348]:
        raise ValueError('Full source paragraph fragments differ')
    for row in (body, heading):
        for part in row['source_parts_in_reading_order']:
            raw = bytes.fromhex(part['source_hex'])
            offset = part['offset']
            if any(source[offset:offset + len(raw)] != raw for source in sources):
                raise ValueError('Complete Japanese source differs')
    lines = balanced_lines(body['english'], 3)
    font = GameAsciiFont.from_arm9(original)
    if hashlib.sha256(font.glyphs).hexdigest() != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Game ASCII font differs')
    panel = Image.new('RGB', (256, 192), '#eef1f5')
    heading_x = (256 - len(heading['english']) * 6) // 2
    if heading_x < 0:
        raise ValueError('Heading overflows')
    for index, char in enumerate(heading['english']):
        panel.paste('#183047', (heading_x + index * 6, 2), font.decode(char))
    for widget, line in zip(execution['widgets'], lines, strict=True):
        if widget['x'] + len(line) * 6 > 256 or widget['y'] + 11 > 192:
            raise ValueError('Native text bounds overflow')
        for index, char in enumerate(line):
            panel.paste('#183047', (widget['x'] + index * 6, widget['y']), font.decode(char))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    original_rows = list(decoder.disasm(original[START:END], BASE + START))
    proposed_rows = list(decoder.disasm(proposed[START:END], BASE + START))
    if len(original_rows) != (END - START) // 4 or len(proposed_rows) != len(original_rows):
        raise ValueError('Function is not completely decoded')
    # No branch/call instruction outside the replaced initialization block moves.
    for old, new in zip(original_rows, proposed_rows, strict=True):
        offset = old.address - BASE
        if (not 0xF8508 <= offset < 0xF8584 and old.mnemonic.startswith('b')
                and (old.bytes != new.bytes or old.op_str != new.op_str)):
            raise ValueError('Existing control flow changed')
    adjustments = [row for row in proposed_rows if row.op_str.startswith('sp, sp,')]
    if len(adjustments) != 6 or any(row.op_str != 'sp, sp, #0x27c' for row in adjustments):
        raise ValueError('Entry and all five return paths must use the expanded frame')
    if struct.unpack_from('<I', proposed, 0xF89DC)[0] != BASE + 0x12ECEC:
        raise ValueError('Research compiler unexpectedly allocated a string table')
    directory = Path('work/analysis/grand_race_waiting_widget')
    directory.mkdir(parents=True, exist_ok=True)
    preview = directory / 'preview.png'
    panel.resize((768, 576), Image.Resampling.NEAREST).save(preview)
    report = {'research_only': True, 'rom_written': False, 'input_sha256': CANDIDATE_SHA,
              'function': [START, END], 'source_locks': locks, 'changes': changes,
              'original_frame_bytes': 604, 'proposed_frame_bytes': 636,
              'entry_and_return_frame_adjustments': len(adjustments),
              'bounded_native_execution': execution,
              'english': body['english'], 'lines': lines,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'preview_sha256': hashlib.sha256(preview.read_bytes()).hexdigest(),
              'preview_reviewed': args.reviewed,
              'preview_scope': 'heading and instruction text only; full screen composition/runtime pending',
              'remaining': ['reserve owned three-pointer table and complete text allocation',
                            'release compiler gates',
                            'cold-boot wireless navigation and all return paths']}
    (directory / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (directory / 'proposed_disassembly.txt').write_text('\n'.join(
        f'{row.address - BASE:06X} {row.bytes.hex()} {row.mnemonic} {row.op_str}'
        for row in proposed_rows) + '\n', encoding='utf-8')
    print(f'{len(changes)} changed instructions; original control flow preserved; no ROM written')


if __name__ == '__main__':
    main()
