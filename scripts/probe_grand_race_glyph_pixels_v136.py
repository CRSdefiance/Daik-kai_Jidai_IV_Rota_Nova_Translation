"""Compare native pixel-loop output with the reviewed font for every used glyph."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import (
    ASCII_FONT_OFFSET,
    REFERENCE_ASCII_FONT_SHA256,
    GameAsciiFont,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_glyph_pixels import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def verify_glyph(source, character, mode, x):
    bitmap = GameAsciiFont.from_arm9(source).decode(character)
    offset = ASCII_FONT_OFFSET + (ord(character) - 33) * 11
    rows = bytes(11) if character == ' ' else source[offset:offset + 11]
    proof = execute(source, rows, mode=mode, x=x, pitch=16)
    for y, line in enumerate(proof['pixels']):
        for column, actual in enumerate(line):
            expected = 9
            if x <= column < x + 6:
                expected = 3 if bitmap.getpixel((column - x, y)) else (9 if mode == 16 else 0)
            if actual != expected:
                raise ValueError(f'Native glyph/neighbor pixels differ: {character!r}, mode={mode}, x={x}')
    return {'character': character, 'mode': mode, 'x': x, 'steps': proof['steps'],
            'writes': proof['writes'], 'glyph_and_neighbor_pixels_exact': True}


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Current integrated source differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if source[0xD16B4:0xD1898] != clean[0xD16B4:0xD1898]:
        raise ValueError('Native painter or glyph resolver differs')
    if sha(GameAsciiFont.from_arm9(source).glyphs) != REFERENCE_ASCII_FONT_SHA256:
        raise ValueError('Reviewed font differs')
    requests_path = Path('work/analysis/grand_race_native_ascii_v136_proof.json')
    requests = json.loads(requests_path.read_text())
    characters = sorted({row['character'] for proof in requests['complete_allocation_strings'] for row in proof['requests']})
    cases = [verify_glyph(source, char, mode, x) for char in characters
             for mode in (16, 4) for x in range(4)]
    report = {'status': 'pass-native-glyph-pixel-loops', 'candidate_sha256': CANDIDATE_SHA,
              'rom_written': False, 'runtime_verified': False,
              'renderer_span': [0xD16B4, 0xD1898], 'renderer_sha256': sha(source[0xD16B4:0xD1898]),
              'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'request_report_sha256': sha(requests_path.read_bytes()),
              'used_character_count': len(characters), 'case_count': len(cases), 'cases': cases,
              'limitations': ['Actual inner painting loops; synthetic initialized buffers and supplied glyph rows.',
                              '16-bit and 4-bit modes tested at all four x phases, preserving neighboring pixels.',
                              'Complete D16B4 entry/context/bitmap selection and actual physical screen routing remain pending.',
                              'Blank-space rows agree with native D1858-D1888 zero stores; resolver is source-traced, not executed.',
                              'Not menu raster or wireless/gameplay runtime proof; no new integrated translations.']}
    Path('work/analysis/grand_race_glyph_pixels_v136_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(characters)} used characters / {len(cases)} native pixel-loop cases pass with exact neighbor preservation.')


if __name__ == '__main__':
    main()
