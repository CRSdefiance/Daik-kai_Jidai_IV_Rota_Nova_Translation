"""Actual first-row margin shift with all unrelated screen pixels preserved."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/analysis/unguarded_alignment_v377')
CAPTURE = Path('work/emulation_v193/unguarded_alignment_v377')


def main():
    rom_path = ROOT / 'research_only_alignment.nds'
    rom = NdsImage.open(rom_path)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    report = json.loads((CAPTURE / 'capture_report.json').read_text())
    old_root = Path('work/emulation_v193/fleet_detail_v375')
    old = json.loads((old_root / 'capture_report.json').read_text())
    assert report['ROM_sha256'] == sha(rom_path.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == old['scripted_input_schedule']
    before = {r['frame']: r for r in old['frames_captured']}
    after = {r['frame']: r for r in report['frames_captured']}
    assert before.keys() == after.keys()
    exact, changed = [], []
    for frame in after:
        a = Image.open(before[frame]['path']).convert('RGB')
        b = Image.open(after[frame]['path']).convert('RGB')
        differences = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
        if not differences:
            exact.append(frame)
            continue
        assert all(16 <= x < 124 and 296 <= y < 307 for x, y in differences), frame
        old_first = dark_text(font, 'Admiral, sailors', a, (10, 292, 252, 317))
        new_first = dark_text(font, 'Admiral, sailors', b, (10, 292, 252, 317))
        continuation = dark_text(font, 'have scurvy!', b, (10, 308, 252, 340))
        assert old_first['bounds'][0] == 16
        assert new_first['bounds'][0] == continuation['bounds'][0] == 22
        assert a.crop((0, 308, 256, 384)).tobytes() == b.crop((0, 308, 256, 384)).tobytes()
        changed.append({'frame': frame, 'changed_pixels': len(differences),
                        'first': new_first, 'continuation': continuation})
    assert changed
    proof = {'candidate_sha256': report['ROM_sha256'], 'changed_frames': changed,
             'unchanged_whole_frames': exact, 'all_changes_confined_to_complete_first_row': True,
             'all_continuation_and_other_pixels_unchanged': True,
             'both_actual_lines_start_x22_all_first_final_letters_and_blank_cells_exact': True,
             'capture_report': str(CAPTURE / 'capture_report.json'),
             'capture_report_sha256': sha((CAPTURE / 'capture_report.json').read_bytes()),
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'{len(changed)} actual first rows aligned, {len(exact)} other complete frames unchanged.')


if __name__ == '__main__':
    main()
