"""Verify current encounter replay and native ship state without claiming victory."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_contexts_v619')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_contexts_v619_actual')
ROM = Path('out/all_routes_combined_v617_candidate.nds')


def main():
    r = read(RUN / 'capture_report.json')
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert r['ROM_sha256'] == digest == '0575673e6a742055d3c6960dbe39ea2479d4c7b9ffc3f9c4b75a3fd2b5e005bc'
    assert r['frames'] == 24500 and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not any(value for key, value in r.items() if key.startswith('synthetic_'))
    donor = r['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '97997ce6fbeda9ff0272c08d7420e96676240b017e0037b721ed7c5eb52770d5'
    prefix = read(ROOT / 'normal_encounter_prefix.json')
    assert r['scripted_input_schedule'][:len(prefix)] == prefix
    shots = {row['frame']: row for row in r['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    snapshots = {row['frame']: row for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots')
                 for row in r.get(key, [])}

    def raw(frame):
        row = snapshots[frame]
        data = Path(row['path']).read_bytes()
        assert row['read_only_export'] and sha(data) == row['sha256'] and len(data) == 0x400000
        return data

    arm, original = rom.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0xCB1A8, 0xCB1B4), (0x36C70, 0x36C94), (0x5543C, 0x55454), (0xAB158, 0xAB18C)):
        assert arm[lo:hi] == original[lo:hi]
    font = GameAsciiFont.from_arm9(arm)
    masks = []
    for frame, text in ((22000, 'Gun-platform powder ignited! A fire!'), (22500, 'Fire extinguished!')):
        im = Image.open(shots[frame]['path']).convert('RGB')
        mask = full_cells(im, font, text, 16, 296, (0, 8, 0))
        expected = {(16 + x, 296 + y) for x, y in glyphs(font, text)}
        actual = {(x, y) for y in range(296, 328) for x in range(16, 244) if im.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected
        masks.append({'frame': frame, **mask, 'whole_notice_text_and_blank_cells_exact': True,
                      'older_awkward_wording_retained_for_later_source_editorial_review': frame == 22000})
    stats = []
    for frame, own_expected in ((20400, (48, 19)), (22000, (48, 16)), (24500, (47, 3))):
        data = raw(frame)
        u = machine(arm)
        u.mem_write(BASE, data)
        call(u, 0xCB1A8, ())
        root = u.reg_read(UC_ARM_REG_R0)
        records = []
        for index, expected in ((1, own_expected), (5, (30, 21))):
            fleet = root + 4 + index * 0x84
            call(u, 0x36C70, (fleet + 12,))
            mobile = u.reg_read(UC_ARM_REG_R0)
            vtable = struct.unpack('<I', u.mem_read(mobile, 4))[0]
            assert vtable == 0x02143A80
            values = []
            for slot, native in ((0x24, 0x0205543C), (0x28, 0x02055444)):
                entry = struct.unpack('<I', u.mem_read(vtable + slot, 4))[0]
                assert entry == native
                call(u, entry - BASE, (mobile,))
                values.append(u.reg_read(UC_ARM_REG_R0))
            assert tuple(values) == expected == struct.unpack_from('<2H', data, mobile - BASE + 0x18)
            call(u, 0xAB158, (mobile,))
            model = u.reg_read(UC_ARM_REG_R0)
            name = bytes(u.mem_read(model + 8, 24)).split(b'\0')[0].decode('cp932')
            records.append({'fleet_index': index, 'mobile_ship': mobile, 'original_mobile_vtable': vtable,
                            'current_Hull': values[0], 'current_Crew': values[1],
                            'underlying_ship_model': model, 'underlying_model_name': name})
        stats.append({'frame': frame, 'original_virtual_getter_results': records})
    assert stats[0]['original_virtual_getter_results'][0]['underlying_model_name'] == 'Vestaros'
    save(ROOT / 'encounter_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest,
         'report': str(RUN / 'capture_report.json'), 'report_sha256': sha((RUN / 'capture_report.json').read_bytes()),
         'normal_source_donor_cold_boot_encounter_prefix_replayed': True, 'no_new_RAM_fixture_savestate_or_save_modification': True,
         'two_complete_actual_fire_notices': masks, 'read_only_original_mobile_ship_Hull_Crew_and_underlying_model_queries': stats,
         'own_mobile_Crew19_to3_and_Hull48_to47_verified': True,
         'enemy_first_mobile_Hull30_Crew21_unchanged_in_sampled_states': True,
         'actual_engagement_or_victory_reward_or_loot_screen_not_proven': True,
         'older_At_N_Spever_Co_spelling_observed_storage_source_not_yet_reviewed': True,
         'upper_black_conversation_composition_not_independently_cleared': True,
         'next_action': 'Use source-bound isolated ship recovery/proximity fixtures and original engagement controls; do not inject a reward header or assume battle victory.',
         'candidate_patch_and_canonical_unchanged': True, 'all18_plaques_incomplete_all22_scopes_retained': True,
         'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('Current ordinary encounter replay,2 complete fire notices and native own/enemy ship state verified;combat victory/reward remains open.')


if __name__ == '__main__':
    main()
