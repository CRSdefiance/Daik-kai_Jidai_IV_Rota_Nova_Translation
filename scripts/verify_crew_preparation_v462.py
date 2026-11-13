"""Normal Inn recovery, actual four-room assignments and complete save reload."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/crew_preparation_v462')
ROM = Path('out/all_routes_combined_v461_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    reports = []
    for name, frames in (('crew_preparation_v462', 37000), ('crew_preparation_reload_v462', 7200)):
        path = Path('work/emulation_v193') / name / 'capture_report.json'
        r = read(path)
        assert r['ROM_sha256'] == digest and r['cold_boot'] and not r['savestate_loaded']
        assert not r['callback_errors'] and r['frames'] == frames
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, r))
    original = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(original.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'rested_prepared_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert reports[1][1]['battery_save_preloaded']['source_sha256'] == sha(copied.read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    before = Image.open('work/emulation_v193/crew_preparation_v462/frame_005400_navigation.png').convert('RGB')
    after = Image.open('work/emulation_v193/crew_preparation_reload_v462/frame_003600_navigation.png').convert('RGB')
    fatigue = [find_mask(font, text, image, (150, 344, 220, 366)) for text, image in (('36', before), ('0', after))]
    date = {'visually_observed': 'June16', 'capture': 'frame_003600_navigation.png',
            'independent_date_arithmetic_or_custom_date_font_not_claimed': True}
    stay_image = Image.open('work/emulation_v193/crew_preparation_v462/frame_010400_navigation.png').convert('RGB')
    stay = {'literal_word_masks': [dark_text(font, word, stay_image, (8, 292, 253, 320))
                                   for word in ('Stay', 'nights?')],
            'substituted_number_visually_observed': 30,
            'independent_numeric_glyph_renderer_not_claimed': True}
    placements = []
    for frame, room, name in ((6000, 'Galley', 'Gerhard Ardelknatts'),
                             (6400, 'Survey', 'Manuel Almeida'),
                             (6800, 'Helm', 'Charles Jean Rochefort'),
                             (7200, 'Captain', 'Hodram Joakim Bergstrom')):
        path = Path('work/emulation_v193/crew_preparation_reload_v462') / f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        placements.append({'frame': frame, 'room': room, 'name': name,
                           'complete_room': find_mask(font, room, image, (75, 15, 255, 38)),
                           'complete_name': find_mask(font, name, image, (75, 35, 255, 60)),
                           'capture': str(path), 'capture_sha256': sha(path.read_bytes())})
    snapshot = reports[1][1]['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and snapshot['read_only_export']
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    items = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A394, (items + 4 + 49 * 20,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'normal30_night_rest_and_fatigue36_to0': fatigue, 'complete_rest_prompt': stay,
             'actual_reloaded_date': date, 'normal_four_room_assignments_persist': placements,
             'original_Copenhagen_donor_unchanged': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'normal_slot6_overwrite_completed_then_cold_loaded': True,
             'earned_Blue_Oak_clue_flag1_retained': True,
             'no_live_RAM_stat_item_unlock_or_save_injection': True,
             'armor_acquired_or_equipped': False, 'ROM_changed': False,
             'new_terminology_audit': {'Deck': ['Vigor', 'Speech'], 'Sailor_Info': ['Vigor', 'Sword', 'Talk'],
                                      'older_Help_term_consistency_requires_review': True},
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'preparation_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Normal30-night rest/fatigue36->0;four persisted room/name masks and clue1 pass. Armor not acquired.')


if __name__ == '__main__':
    main()
