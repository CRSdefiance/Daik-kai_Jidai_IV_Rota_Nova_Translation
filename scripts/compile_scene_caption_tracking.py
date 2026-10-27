"""Scope existing native five-pixel tracking to complete scene captions only."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_scene_caption_selection import execute

# Context initialization already returns r0=context and sets style +30 to 1.
# Replace redundant ADD r0,sp,#0 with SUB tracking,mode_argument,#1, and store
# into +1C. All original wrapper callers supply mode 1, which gives tracking 0.
# Only the caption caller changes its argument to zero, giving tracking -1.
PATCHES = ((0x42FDC, 0xE3A0C006, 0xE3A0C005),
           (0x42FF0, 0xE58D6004, 0xE58D5004),
           (0x456E4, 0xE28D0000, 0xE2433001),
           (0x456EC, 0xE58D3030, 0xE58D301C))


def compile_tracking(source, document):
    proposed = bytearray(source)
    for offset, old, new in PATCHES:
        if struct.unpack_from('<I', source, offset)[0] != old:
            raise ValueError('Caption caller/wrapper source changed')
        struct.pack_into('<I', proposed, offset, new)
    font = GameAsciiFont.from_arm9(source)
    for character in set(''.join(row['english'] for row in document['records'])):
        bitmap = font.decode(character)
        if any(bitmap.getpixel((5, y)) for y in range(11)):
            raise ValueError('Five-pixel tracking would overlap complete caption glyphs')
    counts = {0: 46, 1: 41, 2: 39, 3: 38}
    tables = {0: 0x115CAC, 1: 0x115A04, 2: 0x115968, 3: 0x115834}
    cases = []
    for row in document['records']:
        case = execute(proposed, tables[row['route_index']], row['index'],
                       counts[row['route_index']], advance=5)
        raw = row['english'].encode('ascii') + b'\0'
        if bytes.fromhex(case['full_text_hex']) != raw:
            raise ValueError('Native narrow caption loses complete manuscript text')
        end = case['x'] + len(row['english']) * 5
        if case['x'] > 255 or end > 256:
            raise ValueError('Complete caption still exceeds native screen width')
        cases.append({'id': row['id'], 'right_edge': end, **case})
    return bytes(proposed), {'case_count': len(cases), 'cases': cases,
                             'font_sixth_column_empty_for_all_caption_characters': True,
                             'tracking': -1, 'advance': 5,
                             'max_width': max(len(row['english']) * 5 for row in document['records'])}


def main():
    allocation = Path('work/analysis/scene_caption_complete_allocation_v137')
    report = json.loads((allocation / 'report.json').read_text())
    source = (allocation / 'proposed_arm9.bin').read_bytes()
    if sha(source) != report['proposed_arm9_sha256']:
        raise ValueError('Complete allocation proposal differs')
    path = Path('translations/scene_caption_manuscript_v2.json')
    if sha(path.read_bytes()) != report['manuscript_sha256']:
        raise ValueError('Complete English changed after allocation')
    proposed, proof = compile_tracking(source, json.loads(path.read_text(encoding='utf-8')))
    proof.update({'status': 'pass-complete-caption-selection-centering-tracking-with-raster-contracts',
                  'allocation_arm9_sha256': sha(source), 'proposed_arm9_sha256': sha(proposed),
                  'manuscript_sha256': sha(path.read_bytes()), 'rom_written': False,
                  'runtime_verified': False,
                  'limitations': ['Actual selection/strlen/centering/wrapper; native raster body and full pixels still require verification.',
                                  'All other wrapper callers need saved mode-1 compatibility execution/source gates.',
                                  'Strict staged ownership/dependency release component and registration pending.']})
    output = Path('work/analysis/scene_caption_complete_tracking_v137')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'proposed_arm9.bin').write_bytes(proposed)
    (output / 'report.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('All 164 complete captions fit at native five-pixel tracking; maximum 220 pixels; glyphs retain full ink. Raster/release/gameplay gates pending.')


if __name__ == '__main__':
    main()
