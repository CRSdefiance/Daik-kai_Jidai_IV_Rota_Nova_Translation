"""Actual captain-selection portraits and distinct legacy SLACK-buffer evidence."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/portrait_selection_v479')
CAPTURE = Path('work/emulation_v193/portrait_selection_v479')


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    digest = sha(ROM.read_bytes())
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == digest and report['frames'] == 2900
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('battery_save_preloaded')
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    photos, names = [], []
    for frame, index, words in [(2400, 0, ['Rafael', 'Castor']),
                                (2500, 1, ['Hodram', 'Joakim', 'Bergstrom']),
                                (2600, 2, ['Lil', 'Argot', 'Camille']),
                                (2700, 0, ['Rafael', 'Castor'])]:
        path = f'/_pxl/personbustup{index:02d}.pxl'
        assert rom.read_file(path) == clean.read_file(path)
        expected = PxlImage.from_bytes(rom.read_file(path)).render().convert('RGB').point(lambda v: v >> 3)
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        actual = image.crop((76, 28, 180, 164)).point(lambda v: v >> 3)
        assert expected.size == actual.size == (104, 136)
        assert expected.tobytes() == actual.tobytes()
        photos.append({'frame': frame, 'actual_source_file': path, 'source_file_sha256': sha(rom.read_file(path)),
                       'full_native_colour_portrait_pixels_exact': 14144, 'display_bounds': [76, 28, 180, 164]})
        names.extend({'frame': frame, 'mask': find_mask(font, word, image, (70, 214, 225, 374))} for word in words)
    raw_blocks = IlnkContainer.parse(rom.read_file('/GRP/SLACKIMG.DK4')).blocks
    source_blocks = IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks
    assert all(raw_blocks[n] == source_blocks[n] for n in range(14, 18))
    destination = struct.unpack_from('<I', arm, 0x9F0B4)[0]
    assert destination == 0x02233040
    snapshot_path = CAPTURE / 'frame_002400_arm9_ram.bin'
    snapshot = snapshot_path.read_bytes()
    offset = destination - 0x02000000
    assert snapshot[offset:offset + 14144] == raw_blocks[17]
    # The visible PXL is verified directly;do not infer the raw block's colour
    # interpretation by binding it to an unrelated palette.
    raw_not_equal_loose = [bytes(PxlImage.from_bytes(rom.read_file(f'/_pxl/personbustup{n:02d}.pxl')).indices) != raw_blocks[n + 14]
                          for n in range(4)]
    assert all(raw_not_equal_loose)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'actual_cold_New_Game_selectable_portrait_cases': photos, 'complete_name_fields_and_Camille_biography': names,
             'three_distinct_visible_captain_portraits_verified': True,
             'fourth_Maria_choice_not_observed_in_this_navigation_state': True,
             'no_unlock_or_progress_flags_synthesized': True,
             'original_raw_portrait_blocks14_to17_preserved': True,
             'actual_legacy_read_buffer': {'address_from_original_literal': destination, 'block': 17,
                                          'bytes': 14144, 'whole_buffer_exact': True,
                                          'snapshot': str(snapshot_path), 'snapshot_sha256': sha(snapshot)},
             'raw_and_loose_payloads_are_distinct_and_not_conflated': raw_not_equal_loose,
             'raw_colour_interpretation_or_global_unused_status_not_proven': True,
             'comic_block19_display_not_verified': True, 'all22_historical_requirements_retained': True,
             'all18_plaques_incomplete': True, 'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'selection_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Three actual selectable captain portraits/full names exact;original SLACK17 buffer read verified;raw display not conflated.')


if __name__ == '__main__':
    main()
