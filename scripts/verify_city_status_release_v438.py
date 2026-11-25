"""Actual cold-boot normal-path preservation for the source-owned status release."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/city_status_release_v438')
CAPTURE = Path('work/emulation_v193/city_status_v438')
PARENT_CAPTURE = Path('work/emulation_v193/city_help_v436')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    proof = read(ROOT / 'release_proof.json')
    current, previous = [read(folder / 'capture_report.json') for folder in (CAPTURE, PARENT_CAPTURE)]
    assert current['ROM_sha256'] == proof['candidate_sha256']
    assert current['cold_boot'] and not current['savestate_loaded'] and not current['callback_errors']
    assert current['frames'] == 25600
    previous_frames = {r['frame']: r for r in previous['frames_captured'] if 'cold_boot' in r['path']}
    matched = []
    for row in current['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        if 'cold_boot' not in row['path']:
            continue
        old = previous_frames[row['frame']]
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        assert Image.open(path).tobytes() == Image.open(old['path']).tobytes()
        matched.append(row['frame'])
    assert len(matched) == 67
    proof['cold_boot_regression_pending'] = False
    proof['all67_normal_title_New_Game_story_town_and_HELP_frames_pixel_exact'] = True
    proof['regression_report'] = str(CAPTURE / 'capture_report.json')
    proof['regression_report_sha256'] = sha((CAPTURE / 'capture_report.json').read_bytes())
    proof['matched_frames'] = matched
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('All67 normal title/New Game/story/town/HELP captures are pixel-exact to V436;no callback errors.')


if __name__ == '__main__':
    main()
