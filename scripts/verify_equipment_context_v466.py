"""Actual empty inventory, original search gates, normal Inn recovery and save reload."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.read_navigation_snapshot_v391 import inspect
from scripts.record_navigation_v327 import dark_text
from scripts.verify_copenhagen_checkpoint_v420 import labels
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v464_candidate.nds')
ROOT = Path('work/analysis/equipment_context_v466')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x79C68, 0x79C88), (0x4A368, 0x4A3A0), (0x4A448, 0x4A468)]:
        assert arm[lo:hi] == original[lo:hi]
    reports = []
    for name, frame in [('equipment_context_v466', 16030), ('rested_equipment_reload_v466', 3600)]:
        path = Path('work/emulation_v193') / name / 'capture_report.json'
        r = read(path)
        assert r['ROM_sha256'] == digest and r['frames'] == frame
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, r))
    source = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(source.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'rested_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    snapshot = reports[0][1]['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha(raw) == snapshot['sha256']
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    store = u.reg_read(UC_ARM_REG_R0)
    cases = []
    for index in range(218):
        ptr = store + 4 + index * 20
        call(u, 0x4A448, (ptr,))
        category = u.reg_read(UC_ARM_REG_R0)
        if category not in (2, 3):
            continue
        call(u, 0x4A394, (ptr,))
        clue = u.reg_read(UC_ARM_REG_R0)
        call(u, 0x4A368, (ptr,))
        excluded = u.reg_read(UC_ARM_REG_R0)
        executed = set()

        def observe(uc, address, size, data):
            data.add(address)
            if address in (0x02079C88, 0x02079E14):
                uc.emu_stop()

        handle = u.hook_add(UC_HOOK_CODE, observe, user_data=executed)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R8, ptr)
        try:
            u.emu_start(0x02079C68, 0x02079E18, count=100)
        finally:
            u.hook_del(handle)
        allowed = clue != 0 and excluded == 0
        assert u.reg_read(UC_ARM_REG_PC) == (0x02079C88 if allowed else 0x02079E14)
        assert u.reg_read(UC_ARM_REG_SP) == STACK and u.reg_read(UC_ARM_REG_R8) == ptr
        assert 0x0204A394 in executed
        assert (0x0204A368 in executed) == (clue != 0)
        cases.append({'item_id': index, 'category': category, 'earned_clue_flag': clue,
                      'native_search_exclusion_flag': excluded, 'passes_initial_search_gates': allowed,
                      'native_executed_addresses': sorted(executed)})
    assert len(cases) == 54
    assert [r['item_id'] for r in cases if r['passes_initial_search_gates']] == [49]
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    font = GameAsciiFont.from_arm9(arm)
    text_masks = []
    for frame, text in [(3200, "You don't have any items."), (3530, 'Shall we call at Copenhagen?'),
                        (4130, 'Welcome! Come in.'), (4830, 'Stay'), (4830, 'nights?'),
                        (11930, 'Overwrite existing data?'), (11930, 'Continue?')]:
        path = Path('work/emulation_v193/equipment_context_v466') / f'frame_{frame:06d}_navigation.png'
        text_masks.append({'frame': frame, 'text': dark_text(font, text, Image.open(path).convert('RGB'),
                                                           (8, 292, 253, 345))})
    fatigue = []
    for path, text in [
        (Path('work/emulation_v193/equipment_context_v466/frame_003930_navigation.png'), '38'),
        (Path('work/emulation_v193/equipment_context_v466/frame_006930_navigation.png'), '0'),
        (Path('work/emulation_v193/rested_equipment_reload_v466/frame_003600_final.png'), '0'),
    ]:
        fatigue.append({'capture': str(path), 'mask': find_mask(font, text, Image.open(path).convert('RGB'),
                                                              (150, 344, 220, 366))})
    reloaded = reports[1][1]['read_only_RAM_snapshot']
    reload_raw = Path(reloaded['path']).read_bytes()
    assert reloaded['read_only_export'] and sha(reload_raw) == reloaded['sha256']
    v = machine(arm)
    v.mem_write(0x02000000, reload_raw)
    call(v, 0xCB190, ())
    call(v, 0x4A394, (v.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20,))
    assert v.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(v.mem_read(0x02000000, len(reload_raw))) == reload_raw
    call(v, 0xCB190, ())
    target = v.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20
    target_vtable = struct.unpack('<I', v.mem_read(target, 4))[0]
    point_method = struct.unpack('<I', v.mem_read(target_vtable + 0x20, 4))[0]
    out = 0x02471020
    v.mem_write(out - 16, b'\xA5' * 40)
    call(v, point_method - 0x02000000, (out, target))
    target_point = struct.unpack('<2i', v.mem_read(out, 8))
    assert target_point == (19464, 5192)
    assert bytes(v.mem_read(out - 16, 16)) == bytes(v.mem_read(out + 8, 16)) == b'\xA5' * 16
    call(v, 0x655B8, ())
    radius = v.reg_read(UC_ARM_REG_R0)
    assert radius == 32 and bytes(v.mem_read(0x02000000, len(reload_raw))) == reload_raw
    sea_path = Path('work/emulation_v193/equipment_context_v466/frame_003000_arm9_ram.bin')
    sea_raw = sea_path.read_bytes()
    w = machine(arm)
    w.mem_write(0x02000000, sea_raw)
    call(w, 0xCB1A8, ())
    fleets = w.reg_read(UC_ARM_REG_R0)
    call(w, 0x2E58C, ())
    fleet = fleets + 4 + w.reg_read(UC_ARM_REG_R0) * 0x84
    fleet_vtable = struct.unpack('<I', w.mem_read(fleet, 4))[0]
    fleet_method = struct.unpack('<I', w.mem_read(fleet_vtable + 0x20, 4))[0]
    w.mem_write(out - 16, b'\xA5' * 40)
    call(w, fleet_method - 0x02000000, (out, fleet))
    fleet_point = struct.unpack('<2i', w.mem_read(out, 8))
    nav = inspect(sea_path, ROM)
    assert list(fleet_point) == [value // 128 for value in nav['world_point']]
    assert bytes(w.mem_read(out - 16, 16)) == bytes(w.mem_read(out + 8, 16)) == b'\xA5' * 16
    assert bytes(w.mem_read(0x02000000, len(sea_raw))) == sea_raw
    geometry = {'item_point_virtual': point_method, 'item49_map_point': list(target_point),
                'fleet_point_virtual': fleet_method, 'actual_fleet_map_point': list(fleet_point),
                'actual_ship_getter_world_point': nav['world_point'], 'native_map_to_world_factor_verified': 128,
                'original_search_radius_getter': 0x020655B8, 'search_radius_map_units': radius,
                'derived_item49_world_point': [value * 128 for value in target_point],
                'derived_search_radius_world_units': radius * 128,
                'isolated_original_point_getters_and_guards_pass': True,
                'no_distance_success_or_treasure_acquisition_claim': True}
    town = labels(font, Image.open('work/emulation_v193/rested_equipment_reload_v466/frame_003600_final.png').convert('RGB'))
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()),
                          'verified_capture_count': len(r['frames_captured'])} for p, r in reports],
             'actual_player_Items_menu_empty_complete_text': text_masks[0],
             'original_search_gate_fragment_all54_actual_weapon_armor_records': cases,
             'original_entry_and_observation_stops_are_explicit_isolated_test_contract': True,
             'no_live_item_flags_or_save_mutation': True,
             'found_flag_does_not_prove_player_inventory_or_occupied_equipment': True,
             'only_Blue_Oak49_passes_initial_clue_and_exclusion_checks': True,
             'later_distance_category_acquisition_Graphics_not_proved': True,
             'original_search_coordinate_units_and_target': geometry,
             'complete_native_dialogue_masks': text_masks, 'normal_Inn_recovery_and_reloaded_zero_fatigue': fatigue,
             'reloaded_complete_town_coordinate_and_goods_masks': town,
             'two_normal_Treat_Everyone_attempts_gave_fleet_rumors_not_new_equipment_clues': True,
             'normal_completed_slot6_save_and_cold_load': True,
             'saved_battery': str(copied), 'saved_battery_sha256': sha(copied.read_bytes()),
             'original_post_Speyer_donor_unchanged': True, 'reloaded_Blue_Oak_clue': 1,
             'ROM_changed': False, 'armor_weapon_occupied_display_verified': False,
             'all18_plaques_incomplete': True, 'all22_historical_requirements_retained': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'context_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Actual empty inventory;54 original search gates;normal38->0 rest/save/reload verified. Occupied equipment remains open.')


if __name__ == '__main__':
    main()
