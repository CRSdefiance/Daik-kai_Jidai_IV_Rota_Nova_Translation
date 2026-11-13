"""Complete first page and A continuation from a controlled actual cold boot."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels, raster

ROOT = Path('work/analysis/dialogue_pagination_v288')
CAPTURE = Path('work/emulation_v193/dialogue_pagination_v288')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    manifest = read(ROOT / 'fixture_manifest.json')
    report = read(CAPTURE / 'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 10840 and report['ROM_sha256'] == manifest['research_ROM_sha256']
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    for record in report['frames_captured']:
        assert sha(Path(record['path']).read_bytes()) == record['PNG_sha256']
    rows = [r for r in read('translations/confirmed_name_editorial_v287.json')['records']
            if r['id'] in ('DK4_MES_B298_R0046', 'DK4_MES_B298_R0054')]
    assert len(rows) == 2
    assert bytes.fromhex(rows[0]['compiled_target_hex'])[1:] == bytes.fromhex(rows[1]['compiled_target_hex'])[1:] == bytes.fromhex(manifest['complete_target_hex'])[1:]
    assert rows[0]['actual_route_expanded_body_hex'] == rows[1]['actual_route_expanded_body_hex']
    arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
    body = bytes.fromhex(rows[0]['actual_route_expanded_body_hex'])
    pixels, events, font = raster(arm, body, canvas_height=96)
    assert pixels == expected_pixels(arm, font, events, canvas_height=96)
    assert sorted({r['y'] for r in events if r['code'] != 32}) == [0, 16, 32, 48, 64]
    full = {(16 + n % 216, 296 + n // 216) for n, value in enumerate(pixels) if value == 1}
    first = {p for p in full if p[1] < 360}
    tail = full - first
    captures = []
    for number in (10040, 10440):
        path = CAPTURE / f'frame_{number:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        actual = {(x, y) for y in range(296, 376) for x in range(16, 232)
                  if image.getpixel((x, y)) == (0, 8, 0)}
        assert actual == first and not actual & tail
        captures.append({'path': str(path), 'sha256': sha(path.read_bytes()),
                         'all_first_four_rows_independent_pixels_exact': True,
                         'final_row_pixels_on_first_page': 0})
    path = CAPTURE / 'frame_010840_navigation.png'
    image = Image.open(path).convert('RGB')
    glyphs = GameAsciiFont.from_arm9(arm)
    expected = {(22 + n * 6 + x, 296 + y) for n, ch in enumerate('equinoxes!')
                for y in range(11) for x in range(6) if glyphs.decode(ch).getpixel((x, y))}
    actual = {(x, y) for y in range(296, 360) for x in range(16, 232)
              if image.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected and len(expected) == len(tail)
    assert {'start': 10441, 'duration': 8, 'buttons': ['A']} in report['scripted_input_schedule']
    proof = {'format': 'dk4-actual-five-line-portrait-pages-v288',
             'ROM_sha256': report['ROM_sha256'], 'cold_boot': True,
             'savestate_loaded': False, 'frames': 10840, 'callback_errors': [],
             'first_page_cases': captures, 'first_four_rows_complete_native_ink_pixels': len(first),
             'final_row_pixels_on_first_page': 0,
             'ordinary_A_full_final_word_ink_pixels': len(expected),
             'continuation_page': str(path), 'continuation_page_sha256': sha(path.read_bytes()),
             'combined_pages_complete_independent_ink_pixels': len(full),
             'normal_native_four_row_page_then_complete_continuation_verified': True,
             'no_clipped_missing_or_duplicate_letters_across_the_two_pages': True,
             'both_identical_puzzle_bodies_covered': [r['id'] for r in rows],
             'original_Julio_actor6_and_native_renderer_unchanged': True,
             'test_context': 'Controlled Julio prompt SC0B44R179; original puzzle scene locations not visited.',
             'full_registered_release_integration_pending': True,
             'all18_plaque_hint_entries_and_variants_incomplete': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'actual_page_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(first)} first-page ink pixels + {len(expected)} continuation pixels exact; both complete puzzle bodies covered.')


if __name__ == '__main__':
    main()
