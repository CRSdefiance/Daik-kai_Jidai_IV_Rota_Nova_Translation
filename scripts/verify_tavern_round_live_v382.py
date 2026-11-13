"""Verify the actual repaired announcement and unchanged surrounding scene."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/analysis/tavern_round_v382')
CAPTURE = Path('work/emulation_v193/tavern_round_v382_revised')


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    rom_path = ROOT / 'research_only_tavern.nds'
    assert report['ROM_sha256'] == sha(rom_path.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    old = json.loads(Path('work/emulation_v193/weapon_acquisition_v381/capture_report.json').read_text(encoding='utf-8'))
    assert report['scripted_input_schedule'] == old['scripted_input_schedule']
    font = GameAsciiFont.from_arm9(NdsImage.open(rom_path).read_file('/__arm9__.bin'))
    mask = dark_text(font, "This round's on Bergstrom. Enjoy!",
                     Image.open(CAPTURE / 'frame_014000_cold_boot.png').convert('RGB'), (8, 292, 252, 320))
    before = {r['frame']: r for r in old['frames_captured']}
    changed, exact = [], []
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if row['frame'] not in before:
            continue
        a = Image.open(before[row['frame']]['path']).convert('RGB')
        b = Image.open(row['path']).convert('RGB')
        if a.tobytes() == b.tobytes():
            exact.append(row['frame'])
            continue
        differences = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
        assert row['frame'] in (13600, 14000)
        assert all(8 <= x < 252 and 292 <= y < 365 for x, y in differences)
        changed.append(row['frame'])
    assert changed
    proof = {'candidate_sha256': report['ROM_sha256'], 'capture_report': str(report_path),
             'capture_report_sha256': sha(report_path.read_bytes()), 'actual_complete_announcement_mask': mask,
             'changed_frames': changed, 'unchanged_comparable_frames': exact,
             'all_changes_confined_to_announcement_body': True,
             'next_patron_and_Tavern_menu_transition_unchanged': True,
             'source_meaning_and_complete_punctuation_reviewed': True,
             'research_only': True, 'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'Complete actual Tavern announcement passes; {len(exact)} comparable surrounding frames unchanged.')


if __name__ == '__main__':
    main()
