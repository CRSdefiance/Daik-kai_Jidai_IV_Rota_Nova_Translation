"""Execute all Golden Route footer transfers, placement and complete ASCII pixels."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels

TABLES = (0x12EC10, 0x12EC28, 0x12EC3C)


def main():
    directory = Path('work/analysis/golden_route_viewer_complete_v138')
    source = (directory / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((directory / 'report.json').read_text())
    if sha(source) != allocation['proposed_arm9_sha256']:
        raise ValueError('Golden Route allocation differs')
    cases = []
    for table in TABLES:
        pointers = struct.unpack_from('<6I', source, table)
        labels = [(source[pointer - 0x02000000:source.index(0, pointer - 0x02000000)].decode('ascii')
                   if pointer else None) for pointer in pointers]
        expected_draw_order = [label for label in reversed(labels) if label]
        for mode in (4, 16):
            result = execute(source, 'unused', footer_table=table, mode=mode)
            if [row['text'] for row in result['footer_draws']] != expected_draw_order or result['footer_labels'] != list(pointers):
                raise ValueError('Native footer transfer or complete draw order differs')
            consumed = ''.join(expected_draw_order)
            if any(len(label) % 2 for label in expected_draw_order):
                raise ValueError('Native footer two-byte width drops the final ASCII cell')
            expected_glyphs = [{'code': ord(c), 'style': 1, 'x': i * 6, 'y': 0}
                               for i, c in enumerate(consumed)]
            if result['glyphs'] != expected_glyphs or result['pixels'] != expected_pixels(source, consumed, 0, 0, mode, advance=6):
                raise ValueError('Native footer loses complete glyph/pixel data')
            metadata = result['footer_metadata']
            placements = []
            for slot, label in enumerate(labels):
                left, width, source_x = metadata[slot * 3:slot * 3 + 3]
                if label is None:
                    if left != -1:
                        raise ValueError('Disabled footer slot remains visible')
                    continue
                if width != len(label) * 6 or not 0 <= left <= left + width <= 256:
                    raise ValueError('Complete native footer width/placement clips text')
                if not 0 <= source_x <= source_x + width <= len(consumed) * 6:
                    raise ValueError('Footer packed source range escapes complete raster')
                placements.append({'slot': slot, 'text': label, 'left': left,
                                   'width': width, 'source_x': source_x})
            ordered = sorted(placements, key=lambda row: row['left'])
            if any(a['left'] + a['width'] > b['left'] for a, b in pairwise(ordered)):
                raise ValueError('Native footer labels overlap')
            for offset in (0xCA890, 0xCA780, 0xCA9F0, 0xD5160, 0xD5404, 0xD16B4, 0xD5140):
                if offset not in result['executed_offsets']:
                    raise ValueError('Complete native footer pipeline was not executed')
            cases.append({'table': table, 'mode': mode, 'placements': placements,
                          'draws': result['footer_draws'], 'pixels_sha256': sha(result['pixels']),
                          'native_state_copy_and_font_cleanup': True,
                          'stack_and_registers_preserved': result['stack_and_registers_preserved']})
    report = {'status': 'pass-native-golden-route-footer-transfer-placement-and-complete-ascii-raster',
              'proposed_arm9_sha256': sha(source), 'cases': cases, 'rom_written': False,
              'limitations': ['The 256-by-12 surface view constructor/destructor and origin/glyph copy are bounded contracts.',
                             'Native label transfer, width/gaps/placement, font init/cleanup and complete pixels execute.',
                             'Physical HUD composition/controller input and zero-record modal rendering remain pending.']}
    Path('work/analysis/golden_route_footer_v138_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('All three footer states pass both native pixel formats, complete labels, pointer transfer and non-overlapping placement.')


if __name__ == '__main__':
    main()
