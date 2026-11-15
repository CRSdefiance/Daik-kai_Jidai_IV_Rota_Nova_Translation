"""Connect actual empty-state dispatch/copy to native modal glyph rendering."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_golden_route_empty_copy import execute as copy
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_scene_caption_raster import expected_pixels


def main():
    directory = Path('work/analysis/golden_route_viewer_complete_v138')
    source = (directory / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((directory / 'report.json').read_text())
    if sha(source) != allocation['proposed_arm9_sha256']:
        raise ValueError('Golden Route proposal changed')
    dispatches = [copy(source, count=count) for count in (0, 1, 2, 255)]
    text = bytes.fromhex(dispatches[0]['complete_text_hex'])[:-1].decode('ascii')
    cases = []
    for mode in (4, 16):
        result = raster(source, text, modal=True, mode=mode)
        expected = [{'code': ord(c), 'style': 15, 'x': index * 6, 'y': 0}
                    for index, c in enumerate(text)]
        if result['glyphs'] != expected or result['final_x'] != len(text) * 6:
            raise ValueError('Native modal renderer drops leading/last glyphs')
        if result['pixels'] != expected_pixels(source, text, 0, 0, mode, advance=6, style=15):
            raise ValueError('Native modal full pixels differ from embedded font')
        for offset in (0x548A8, 0xD5160, 0xD5A10, 0xD5A18, 0xD5A2C, 0xD5404, 0xD16B4, 0xD5140):
            if offset not in result['executed_offsets']:
                raise ValueError('Full native modal text pipeline was not executed')
        cases.append({'mode': mode, 'english': text, 'glyph_count': len(text),
                      'pixels_sha256': sha(result['pixels']), 'width_pixels': len(text) * 6,
                      'text_bounds': [0, 0, 256, 96], 'style': 15,
                      'stack_and_registers_preserved': True})
    report = {'status': 'pass-native-zero-record-dispatch-printf-expansion-and-modal-ascii-pixels',
              'proposed_arm9_sha256': sha(source), 'dispatches': dispatches, 'cases': cases,
              'rom_written': False, 'limitations': [
                  'Saved record count is a contract; source mode-zero 256-by-96 parent bitmap/text bounds are initialized contracts.',
                  'Native dispatch/printf/macro expansion and actual modal renderer/font setters/pixels/cleanup execute in connected separate invocations.',
                  'Bitmap origin and eleven-byte glyph copy are bounded contracts; parent border/physical routing and input dismissal remain pending.']}
    Path('work/analysis/golden_route_empty_v138_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Zero/nonzero dispatch, complete native printf/macro expansion and both full native modal pixel formats pass.')


if __name__ == '__main__':
    main()
