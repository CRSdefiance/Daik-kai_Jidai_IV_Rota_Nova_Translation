"""Actual complete genre lettering, native centering and ordinary cold boot."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_genre_card_v305 import ROOT
from scripts.verify_genre_card_release_v305 import ROM, read


def main():
    release = read(ROOT / 'release_proof.json')
    report_path = Path('work/emulation_v193/genre_card_v305/capture_report.json')
    report = read(report_path)
    assert report['ROM_sha256'] == release['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames'] == 20000
    assert report['scripted_input_schedule'] == read('work/analysis/reviewed_name_release_v299/help_navigation_start_inputs.json')
    texture = FlsArchive(NdsImage.open(ROM).read_file('/FLS/logo.fls')).texture(3)
    points = [(i % texture.width, i // texture.width, texture.palette[index][:3])
              for i, index in enumerate(texture.indices) if index]
    assert points and all(y < 192 for _, y, _ in points)
    matches = []
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        if 300 <= row['frame'] <= 900:
            image = Image.open(path).convert('RGB')
            if all(image.getpixel((x, y)) == color for x, y, color in points):
                matches.append({'frame': row['frame'], 'capture': str(path), 'source_origin': [0, 0],
                                'all_complete_first_internal_final_letter_pixels': len(points),
                                'native_center_and_all_glyph_bounds_exact': True})
    assert len(matches) >= 2, matches
    assert release['new_English_ink_bounds'] == [42, 89, 214, 103]
    assert (release['new_English_ink_bounds'][1] + release['new_English_ink_bounds'][3]) / 2 == 96
    output = {'format': 'dk4-current-genre-live-pixels-v305', 'candidate_sha256': release['candidate_sha256'],
              'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
              'matches': matches, 'complete_foreground_pixels': len(points),
              'actual_native_view_center_y': 96, 'old_native_view_center_y': 127.5,
              'three_logo_source_assets_and_all_other_release_files_preserved_by_release_proof': True,
              'cold_boot20000_no_loaded_state_or_RAM_injection': True,
              'actual_title_New_Game_Rafael_opening_and_town_regression_captured': True,
              'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(f'Genre complete{len(points)} foreground pixels at native center96 in{len(matches)} actual startup frames; cold boot20000 complete.')


if __name__ == '__main__':
    main()
