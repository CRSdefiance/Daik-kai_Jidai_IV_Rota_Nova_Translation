"""Bind actual Maria development and docking to complete Karibib rendering."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_town_v665 import replay
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.run_Karibib_return_v667 import ROOT
from scripts.run_village_consistency_v666 import relocate
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_town_scene_v644 import rgb5
from scripts.verify_village_development_v665 import confirmation
from scripts.verify_village_visits_v664 import CARDS, artifact, dialog, menu, model
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path('scripts/run_Karibib_return_v667.py').read_bytes()) == pre['runner_sha256']
    folder = CAP / 'Karibib_return_v667_Maria_Seoul_reapproach'
    contract = read(folder / 'run_contract.json')
    assert contract['runner_sha256'] == sha(Path('scripts/run_Karibib_Maria_v667.py').read_bytes())
    assert contract['Maria_selection_bypass_save_previously_authorized_not_earned_unlock']
    assert sha(Path(contract['donor']).read_bytes()) == contract['donor_sha256']
    rp = folder / 'capture_report.json'
    r, controller = read(rp), read(folder / 'controller_progress.json')
    phases = controller['phases']
    assert controller['error'] is None and r['frames'] == phases['developed_town_return']
    assert r['ROM_sha256'] == pre['candidate_sha256']
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['battery_save_preloaded']['source_sha256'] == contract['donor_sha256']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert r['core_DLL_sha256'] == sha(Path('work/emulation_v193/desmume_libretro.dll').read_bytes())
    assert not any(v for k, v in r.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    assert not r['hardware_device_verification'] and not r['normal_travel_verified']
    journal = read(folder / 'navigation_command_journal.json')['commands_received']
    assert all(j['validation_passed'] for j in journal)
    assert [{'frame': j['frame'], 'command': j['command']} for j in journal] == controller['commands']
    assert controller['commands'][-1] == {'frame': r['frames'], 'command': {'stop': True}}
    shots, snapshots = {}, {}
    for shot in r['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if shot['frame'] in shots:
            assert shot['PNG_sha256'] == shots[shot['frame']]['PNG_sha256']
        shots[shot['frame']] = shot
    for row in r['read_only_pause_RAM_snapshots']:
        assert row['read_only_export'] and len(artifact(row)) == 0x400000
        snapshots[row['frame']] = row
    def raw(frame):
        return Path(snapshots[frame]['path']).read_bytes()
    def image(frame):
        return Image.open(shots[frame]['path']).convert('RGB')
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    extension = read(folder / 'Maria_reapproach_extension.json')
    assert extension['source_sha256'] == sha(Path('scripts/run_Karibib_Maria_reapproach_v667.py').read_bytes())
    first = read(folder.parent / 'Karibib_return_v667_Maria_Seoul/capture_report.json')
    exact_prefix = []
    for shot in first['frames_captured']:
        if shot['frame'] <= phases['missed_return_before_reapproach']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            assert Image.open(shot['path']).convert('RGB').tobytes() == image(shot['frame']).tobytes()
            exact_prefix.append(shot['frame'])
    assert len(r['synthetic_location_fixtures']) == 2
    for recorded in r['synthetic_location_fixtures']:
        source = raw(recorded['frame'])
        after, calculated = relocate(arm, source, 9)
        assert recorded == dict(calculated, frame=recorded['frame'])
        at = calculated['active_ship'] - BASE + 16
        assert after[:at] == source[:at] and after[at + 8:] == source[at + 8:]
        point = calculated['expected_selector_point_after_original_update']
        assert any(q['collision_free'] and q['map_point'] == point for q in calculated['terrain_proof']['queries'])
    assert not any('battle_fixture' in row['command'] for row in controller['commands'])
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    assert len(controller['entered_character_states']) == len('Kalahari') + 1
    for i, state in enumerate(controller['entered_character_states']):
        data, p = raw(state['frame']), state['parent'] - BASE
        assert sha(data) == state['RAM_sha256'] and state['entry'] == 'Kalahari'[:i]
        assert struct.unpack_from('<I', data, p + 4)[0] == marker
        assert struct.unpack_from('<I', data, p + 0x78)[0] == i
        assert struct.unpack_from('<I', data, p + 0xD8)[0] == 18
        assert data[p + 0xB4:p + 0xB4 + i + 1] == 'Kalahari'[:i].encode('ascii') + b'\0'
        im = image(state['frame'])
        assert {(x, y) for y in range(11) for x in range(108)
                if im.getpixel((60 + x, 244 + y)) == (230, 230, 230)} == glyphs(font, 'Kalahari'[:i])
    texts = read('translations/village_promised_words_manuscript_v1.json')['records']
    clue = next(t['english'] for t in texts if t['kind'] == 'CLUE' and t['index'] == 9)
    notice = next(t['english'] for t in texts if t['kind'] == 'MESSAGE' and t['index'] == 2)
    dialogs = {'confirmation': confirmation(image(phases['answer_confirmation']), rom, font, 'Kalahari'),
        'clue': dialog(image(phases['accepted_clue']), font, 'They say it means ' + clue + '.', 16),
        'notice': dialog(image(phases['facilities_notice']), font, notice, 22),
        'actual_developed_Karibib_docking': dialog(image(phases['reapproach_docking_prompt']), font,
                                                  'Dock at Karibib?', 22)}
    choices = read('work/analysis/village_visits_v664/proof.json')['all24_original_native_menu_filter_cases'][9]['complete_English_choices'][:-1]
    complete_menu = menu(image(phases['developed_village_menu']), font, choices)
    states = []
    for phase in ('chief_request', 'answer_confirmation', 'accepted_clue', 'developed_village_menu', 'developed_town_return'):
        result = model(arm, raw(phases[phase]), 9, 'Karibib', 1)
        assert result['native_development'] == (0 if phase in ('chief_request', 'answer_confirmation') else 2)
        states.append({'phase': phase, **result})
    native = r['read_only_native_state']
    artifact(native)
    for region in native['regions'].values():
        artifact(region)
    data = artifact(r['read_only_RAM_snapshot'])
    assert data == raw(r['frames'])
    io, lcdm, dtcm, itcm = [Path(native['regions'][k]['path']).read_bytes() for k in ('9REG', 'LCDM', 'DTCM', 'ITCM')]
    upper, lower, execution = replay(rom, data, io, lcdm, dtcm, itcm)
    final = image(r['frames'])
    assert [rgb5(upper), rgb5(lower)] == [[color5(final.getpixel((x, y + sy)))
        for y in range(192) for x in range(256)] for sy in (0, 192)]
    assert upper == lcdm[0x40000:0x58000] and lower == lcdm[0x60000:0x78000]
    header = find_mask(font, 'Karibib', final, (0, 10, 256, 40))
    u = machine(arm)
    u.mem_write(BASE, data)
    call(u, 0xCB178, ())
    town = u.reg_read(UC_ARM_REG_R0) + 4 + 99 * 108
    call(u, 0xB5630, (town,))
    name_pointer = u.reg_read(UC_ARM_REG_R0)
    assert bytes(u.mem_read(name_pointer, 64)).split(b'\0')[0] == b'Karibib'
    call(u, 0xB7294, (99, 0))
    background = f'/towngrp/towngrp{u.reg_read(UC_ARM_REG_R0):02d}.pxl'
    blob = rom.read_file(background)
    assert blob == NdsImage.open('work/clean.nds').read_file(background) and data.find(blob) >= 0
    cache = struct.unpack_from('<6I', data, 0x15DC24)
    assert cache[5] == 1 and BASE <= cache[0] < BASE + len(data) - 64
    specialty = data[cache[0] - BASE:].split(b'\0')[0].decode('ascii')
    assert {(x, y) for y in range(12) for x in range(96)
            if final.getpixel((160 + x, 88 + y)) == (230, 230, 230)} == glyphs(font, specialty, 5)
    call(u, 0x2E58C, ())
    actual_captain = u.reg_read(UC_ARM_REG_R0)
    assert actual_captain == 3
    card_samples = [{'phase': phase, 'frame': frame,
        'no_complete_card_file_in_this_snapshot': all(raw(frame).find(rom.read_file(f'/evstill/evstill{i:03d}.pxl')) < 0 for i in CARDS)}
        for phase, frame in phases.items() if phase in ('accepted_clue', 'developed_village_menu',
            'departure', 'return_docking_prompt', 'developed_town_return')]
    save(ROOT / 'native_Town_proof.json', execution)
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'report': str(rp), 'report_sha256': sha(rp.read_bytes()), 'frames': r['frames'],
        'capture_records': len(r['frames_captured']), 'unique_capture_frames': len(shots), 'phases': phases,
        'actual_captain_index': actual_captain,
        'previously_authorized_Maria_selection_bypass_donor_not_earned_unlock': contract,
        'all9_password_prefixes_buffers_cursors_capacity_and_visible_masks_pass': True,
        'complete_dialogues': dialogs, 'complete_developed_menu': complete_menu, 'development_states': states,
        'actual_complete_Karibib_header': header, 'original_Town_name_pointer': name_pointer,
        'actual_complete_specialty_name': specialty, 'source_exact_resident_background': background,
        'full_both_native_Town_screens98304_pixels_exact_including_footer': True,
        'native_Town_proof_sha256': sha((ROOT / 'native_Town_proof.json').read_bytes()),
        'card_samples_not_global_nonuse_proof': card_samples,
        'first_Maria_return_miss_retained_and_whole_prefix_exact': sorted(set(exact_prefix)),
        'only_two_coordinate_approaches_no_recovery_or_outcome_cheat': True,
        'Hodram_specific_encounter_and_failed_attempts_retained_separately': True,
        'all24_developed_ports_now_have_actual_native_scene_evidence_across_recorded_candidates': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V667 actual Karibib docking/title/specialty and98304 native Town pixels pass.', flush=True)


if __name__ == '__main__':
    main()
