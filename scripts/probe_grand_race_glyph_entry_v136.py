"""Verify native painter setup/selection/pixels with explicit copy-helper scope."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import (
    ASCII_FONT_OFFSET,
    REFERENCE_ASCII_FONT_SHA256,
    GameAsciiFont,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_glyph_entry import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def verify_entry(source, character, mode, x, y=2):
    proof = execute(source, character, mode=mode, x=x, y=y)
    bitmap = GameAsciiFont.from_arm9(source).decode(character)
    palette = struct.unpack_from('<I', source, 0xD181C)[0] - 0x02000000
    color = struct.unpack_from('<H', source, palette + 3 * 2)[0] if mode == 16 else 3
    for row_index, line in enumerate(proof['pixels']):
        for column, pixel in enumerate(line):
            expected = 9
            if y <= row_index < y + 11 and x <= column < x + 6:
                expected = color if bitmap.getpixel((column - x, row_index - y)) else (9 if mode == 16 else 0)
            if pixel != expected:
                raise ValueError('Native painter setup, glyph or neighbor pixels differ')
    expected_source = 0x02000000 + ASCII_FONT_OFFSET + (ord(character) - 33) * 11
    if character == ' ':
        if proof['copy_calls']:
            raise ValueError('Blank space unexpectedly selects a font entry')
    elif len(proof['copy_calls']) != 1 or proof['copy_calls'][0]['source'] != expected_source or proof['copy_calls'][0]['bytes'] != 11:
        raise ValueError('Native selector requests the wrong complete glyph')
    return {'character': character, 'mode': mode, 'x': x, 'y': y,
            'steps': proof['steps'], 'stack_balanced': proof['stack_balanced'],
            'glyph_source_and_all_pixels_verified': True, 'copy_calls': proof['copy_calls']}


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Pinned candidate differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xD16B4, 0xD1898), (0x125A20, 0x125A60), (0x125A60, 0x125E75), (0xE2A5C, 0xE2B64))
    if any(source[lo:hi] != clean[lo:hi] for lo, hi in spans):
        raise ValueError('Native painter/font/palette/copy source differs')
    if sha(GameAsciiFont.from_arm9(source).glyphs) != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Reviewed font hash differs')
    request_path = Path('work/analysis/grand_race_native_ascii_v136_proof.json')
    requests = json.loads(request_path.read_text())
    if requests['candidate_sha256'] != CANDIDATE_SHA:
        raise ValueError('Request proof is not current')
    characters = sorted({row['character'] for proof in requests['complete_allocation_strings'] for row in proof['requests']})
    cases = [verify_entry(source, char, mode, x) for char in characters for mode in (16, 4) for x in range(4)]
    report = {'status': 'pass-native-painter-entry-with-copy-contract', 'rom_written': False,
              'runtime_verified': False, 'candidate_sha256': CANDIDATE_SHA,
              'source_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])} for lo, hi in spans],
              'request_report_sha256': sha(request_path.read_bytes()), 'font_sha256': REFERENCE_ASCII_FONT_SHA256,
              'used_characters': len(characters), 'case_count': len(cases), 'cases': cases,
              'limitations': ['Synthetic initialized image contexts and buffers; physical screen routing not exercised.',
                              'Actual D16B4 entry, D1820 resolver, palette/stride addressing and both inner loops executed.',
                              'External E2A5C copy helper modeled as an exact eleven-byte copy; native helper body not executed.',
                              'Blank-space resolver stores executed; full widget invocation, frame artwork and gameplay remain pending.',
                              'Menu raster is separate; no release batch/ROM or integration credit generated.']}
    Path('work/analysis/grand_race_glyph_entry_v136_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(cases)} native painter entry/resolver/pixel cases pass; explicit external copy contract retained.')


if __name__ == '__main__':
    main()
