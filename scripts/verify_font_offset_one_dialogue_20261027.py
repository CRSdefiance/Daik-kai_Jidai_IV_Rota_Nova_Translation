"""Check complete actual modal/progressive letters, including empty rows below them."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/font_offset_one_20261027')
ROM = Path('out/font_v2_draw_down_one_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    digest = sha(ROM.read_bytes())
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    report_path = ROOT / 'cold_boot_hodram/capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == 7001
    frames = {r['frame']: r for r in report['frames_captured']}
    for row in frames.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    image = Image.open(frames[2000]['path']).convert('RGB')
    count, bounds = complete_mask(font, 'Everything correct?', image, 16, 333, (0, 8, 0))
    assert count == 213
    extra = [(x, y) for y in range(344, 357) for x in range(16, 130)
             if image.getpixel((x, y)) == (0, 8, 0)]
    assert not extra
    bio = Image.open(frames[1600]['path']).convert('RGB')
    rows = [find_mask(font, text, bio, (8, 325, 250, 368)) for text in [
        'An admiral of newly free Sweden', 'Commands a navy of privateers',
        'Aims to make his fleet the strongest']]
    assert [r['bounds'][1] for r in rows] == [330, 342, 354]
    assert rows[1]['bounds'][1] - rows[0]['bounds'][1] == rows[2]['bounds'][1] - rows[1]['bounds'][1] == 12
    terminal = read(ROOT / 'newgame_terminal.json')
    lil_report = read(terminal['report'])
    assert lil_report['ROM_sha256'] == digest and lil_report['cold_boot'] and not lil_report['savestate_loaded']
    frame = next(r for r in lil_report['frames_captured'] if r['frame'] == 4000)
    assert sha(Path(frame['path']).read_bytes()) == frame['PNG_sha256']
    image = Image.open(frame['path']).convert('RGB')
    lines = [dark_text(font, text, image, region) for text, region in [
        ('Hee hee! I finally got my trade', (10, 292, 245, 313)),
        ("permit! Just you watch--I'm going", (10, 308, 250, 329)),
        ('to make a fortune!', (10, 324, 245, 348))]]
    # Inspect the former overflow row beyond each 11-row glyph mask as well.
    # Matching only the glyph rectangle missed this defect in the earlier test.
    for row in lines:
        x, y, right, bottom = row['bounds']
        color = tuple(row['color'])
        stray = [(px, py) for py in range(bottom, min(y + 15, 348)) for px in range(x, right)
                 if image.getpixel((px, py)) == color]
        assert not stray, (row['text'], stray)
    result = dict(candidate_sha256=digest, hodram_report=str(report_path),
        hodram_report_sha256=sha(report_path.read_bytes()), confirmation_full_ink_pixels=count,
        confirmation_full_mask=bounds, confirmation_extra_pixels_below=[],
        all_three_biography_lines_complete=rows, biography_line_spacing_pixels=12,
        biography_line_spacing_unchanged=True, progressive_Lil_full_masks=lines,
        progressive_extra_pixels_below_glyph_rectangles=False,
        no_loaded_savestate_or_injected_story_state=True)
    (ROOT / 'dialogue_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Hodram confirmation and three biography lines pass; line spacing remains12. Progressive dialogue tails and rows below are complete and clean.')
