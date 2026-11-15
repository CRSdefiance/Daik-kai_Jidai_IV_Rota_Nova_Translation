"""Verify both complete title selections, native printf and downstream glyph pixels."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_golden_route_heading import execute
from scripts.execute_scene_caption_raster import execute as raster
from scripts.prepare_golden_route_viewer import MANUSCRIPT
from scripts.probe_scene_caption_raster import expected_pixels


def main():
    directory = Path('work/analysis/golden_route_viewer_complete_v138')
    proposal = (directory / 'proposed_arm9.bin').read_bytes()
    allocation = json.loads((directory / 'report.json').read_text())
    if sha(proposal) != allocation['proposed_arm9_sha256'] or sha(MANUSCRIPT.read_bytes()) != allocation['manuscript_sha256']:
        raise ValueError('Complete Golden Route proposal/manuscript changed')
    labels = {row['id']: row['english'] for row in json.loads(MANUSCRIPT.read_text(encoding='utf-8'))['records']}
    cases = []
    for selection, key in ((0, 'FOUND'), (1, 'RECORDS')):
        text = labels['GOLDEN_ROUTE_VIEWER_' + key]
        for y in (0, 12):
            native = execute(proposal, selection, y=y)
            if bytes.fromhex(native['full_text_hex']) != text.encode('ascii') + b'\0':
                raise ValueError('Actual title selection/printf changes complete English')
            for mode in (4, 16):
                painted = raster(proposal, text, tracking=0, x=native['x'], y=y, mode=mode)
                consumed = text + (' ' if len(text) % 2 else '')
                expected = [{'code': ord(c), 'style': 1, 'x': native['x'] + i * 6, 'y': y}
                            for i, c in enumerate(consumed)]
                if painted['glyphs'] != expected or painted['final_x'] != native['x'] + len(text) * 6:
                    raise ValueError('Native title leading/last glyph or paired advance differs')
                if painted['pixels'] != expected_pixels(proposal, consumed, native['x'], y, mode, advance=6):
                    raise ValueError('Complete native title pixels differ from embedded font')
                cases.append({'selection': selection, 'english': text, 'mode': mode,
                              'pixels_sha256': sha(painted['pixels']), 'native': native})
    report = {'status': 'pass-both-golden-route-title-selections-native-printf-and-ascii-pixels',
              'proposed_arm9_sha256': sha(proposal), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
              'cases': cases, 'rom_written': False,
              'limitations': ['Native selector/strlen/printf execute; renderer consumes the actual copied text in a separate invocation.',
                             'Initialized font metrics, bitmap origin and glyph copy are contracts.',
                             'Y0/Y12 are parameterized geometry cases; actual parent physical routing remains pending.',
                             'Footer control transfer/placement and zero-record formatted dialog still require full native proofs.']}
    Path('work/analysis/golden_route_heading_v138_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Both complete Golden Route titles pass native selection/centering/printf and eight full pixel cases; footer/modal/physical gates pending.')


if __name__ == '__main__':
    main()
