"""Full glyph masks in a normal New Game Guild offer, plus frame regression."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/analysis/guild_description_release_v443')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def checked_report(folder, digest):
    path = Path('work/emulation_v193') / folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, report


def main():
    proof = read(ROOT / 'release_proof.json')
    offer_path, offer = checked_report('guild_offer_v443', proof['candidate_sha256'])
    current_path, current = checked_report('guild_description_v443', proof['candidate_sha256'])
    assert offer['frames'] == 17000 and current['frames'] == 21400
    plan = read(ROOT / 'live_inputs.json')
    assert current['scripted_input_schedule'] == plan
    parent = read(Path('work/emulation_v193/map_viewer_v441/capture_report.json'))
    assert parent['ROM_sha256'] == proof['parent_sha256']
    assert parent['cold_boot'] and not parent['savestate_loaded'] and not parent['callback_errors']
    previous = {row['frame']: row for row in parent['frames_captured'] if 'cold_boot' in row['path']}
    matched = []
    for row in current['frames_captured']:
        if row['frame'] in previous:
            old = previous[row['frame']]
            assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
            assert Image.open(row['path']).tobytes() == Image.open(old['path']).tobytes()
            matched.append(row['frame'])
    assert len(matched) == 56
    final = next(row for row in current['frames_captured'] if row['frame'] == 21400)
    assert Image.open(final['path']).tobytes() == Image.open('work/emulation_v193/map_viewer_v441/frame_021400_navigation.png').tobytes()
    capture = next(row for row in offer['frames_captured'] if row['frame'] == 17000)
    image = Image.open(capture['path']).convert('RGB')
    font = GameAsciiFont.from_arm9(NdsImage.open(proof['candidate']).read_file('/__arm9__.bin'))
    native = read(Path('work/analysis/guild_description_v442/native_proof.json'))
    entry = next(row for row in native['whole20_Guild_treasure_descriptions'] if row['message_id'] == 3665)
    masks = [dark_text(font, line.strip(), image, (10, 292 + index * 16, 250, 313 + index * 16))
             for index, line in enumerate(entry['native_wrapped_lines'])]
    assert all(mask['bounds'][0] == 22 for mask in masks)
    assert sum(mask['ink_pixels'] for mask in masks) == entry['complete_native_glyph_ink_pixels'] == 995
    proof.update({
        'actual_cold_boot_guild_verification_pending': False,
        'actual_complete_Guild_description': masks,
        'all_first_interior_and_last_glyphs_and_blank_cells_exact': True,
        'all_three_lines_left_aligned_at_x22': True,
        'actual_offer_capture': capture['path'], 'actual_offer_capture_sha256': capture['PNG_sha256'],
        'actual_offer_report': str(offer_path), 'actual_offer_report_sha256': sha(offer_path.read_bytes()),
        'regression_report': str(current_path), 'regression_report_sha256': sha(current_path.read_bytes()),
        'matched_regression_frames': matched,
        'all56_comparable_frames_and_purchased_map_view_pixel_exact': True,
        'hardware_device_verification': False,
    })
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Actual Guild offer: 995 full glyph pixels, all3 rows aligned x22;56 surrounding frames and map viewer pixel-exact.')


if __name__ == '__main__':
    main()
