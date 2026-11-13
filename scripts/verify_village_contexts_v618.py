"""Verify original Narvik discovery/development, complete text and source water fixtures."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import paragraph
from dk4tool.rom.nds import NdsImage
from scripts.native_village_contexts_v618 import ARM, relocate
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_contexts_v618')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/village_contexts_v618_syracuse')
ROM = Path('out/all_routes_combined_v617_candidate.nds')
WORDS = ('Resupply', 'Stay', 'Repair Ship', 'Recruit Sailors', 'Set Sail', 'Promised Words')


def native_menu_filters(arm, raw):
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x789AC:0x78A54] == original[0x789AC:0x78A54]
    u = machine(arm)
    u.mem_write(BASE, raw)
    rows = []
    for index in range(24):
        u.mem_write(STACK - 16, b'\xA5' * 432)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R8, index)
        u.emu_start(0x020789AC, 0x02078A54, count=500)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02078A54
        assert bytes(u.mem_read(STACK - 16, 16)) == bytes(u.mem_read(STACK + 400, 16)) == b'\xA5' * 16
        records = [list(struct.unpack('<4I', u.mem_read(STACK + 0x11C + 16 * i, 16))) for i in range(6)]
        texts = [bytes(u.mem_read(r[0], 64)).split(b'\0')[0].decode('ascii') for r in records]
        flags = [r[1] for r in records]
        assert tuple(texts) == WORDS
        assert flags == [1, int(index % 2 == 0), int(index % 3 == 0), int(index % 5 == 0), 1, 1]
        assert all(r[2:] == [1, 0] for r in records)
        rows.append({'village': index, 'actual_source_menu_flags': flags,
                     'complete_English_choices': [t for t, enabled in zip(texts, flags, strict=True) if enabled],
                     'original_copy_and_modulo_filter_instructions_execute': True})
    return rows


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == '0575673e6a742055d3c6960dbe39ea2479d4c7b9ffc3f9c4b75a3fd2b5e005bc'
    arm = rom.read_file('/__arm9__.bin')
    assert sha(arm) == ARM
    r = read(RUN / 'capture_report.json')
    assert r['ROM_sha256'] == digest and r['frames'] == 15700
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['battery_save_preloaded']['source_sha256'] == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    assert sha(Path(r['battery_save_preloaded']['source']).read_bytes()) == r['battery_save_preloaded']['source_sha256']
    assert not any(v for k, v in r.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    shots = {s['frame']: s for s in r['frames_captured']}
    for s in shots.values():
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
    snapshots = {s['frame']: s for s in r['read_only_pause_RAM_snapshots']}

    def raw(frame):
        row = snapshots[frame]
        data = Path(row['path']).read_bytes()
        assert row['read_only_export'] and len(data) == 0x400000 and sha(data) == row['sha256']
        return data

    images = {}

    def image(frame):
        if frame not in images:
            images[frame] = Image.open(shots[frame]['path']).convert('RGB')
        return images[frame]

    initial = raw(5200)
    _, fixture = relocate(arm, initial, 15)
    assert r['synthetic_location_fixtures'] == [dict(fixture, frame=5200)]
    assert fixture['expected_selector_point_after_original_update'] == [22048, 2234]
    source_water = read(ROOT / 'actual_V617_RAM_all24_water_proof.json')
    assert source_water['source_RAM_sha256'] == sha(initial) and len(source_water['cases']) == 24
    assert source_water['fixture_script_sha256'] == sha(Path('scripts/native_village_contexts_v618.py').read_bytes())
    for row in source_water['cases']:
        assert row['only_eight_ship_coordinate_bytes_owned'] and row['no_discovery_development_dialogue_resource_or_scene_flags_changed']
        p = row['expected_selector_point_after_original_update']
        assert any(t['map_point'] == p and t['collision_free'] for t in row['terrain_proof']['queries'])
        assert sum((a - b) ** 2 for a, b in zip(row['village_center'], p, strict=True)) < 32 ** 2
    negatives = read(ROOT / 'fixture_negative_controls.json')
    assert len(negatives['negative_controls']) == 5 and all(row['rejected'] for row in negatives['negative_controls'])
    assert negatives['fixture_source_sha256'] == sha(Path('scripts/native_village_contexts_v618.py').read_bytes())
    menus = native_menu_filters(arm, initial)
    font = GameAsciiFont.from_arm9(arm)
    menu_masks = []
    for frame, labels in ((7200, menus[15]['complete_English_choices']),
                          (13400, menus[15]['complete_English_choices'][:-1])):
        assert len(labels) in (4, 5)
        top = 292 - len(labels) * 10
        masks = [full_cells(image(frame), font, text, (256 - len(text) * 6) // 2, top + i * 20, (8, 8, 8))
                 for i, text in enumerate(labels)]
        menu_masks.append({'frame': frame, 'complete_menu_cells': masks,
                           'Promised_Words_removed_only_after_original_success': frame == 13400})
    manuscript = read('translations/village_promised_words_manuscript_v1.json')['records']
    clue = next(x['english'] for x in manuscript if x['id'] == 'VILLAGE_CLUE_15')
    facilities = next(x['english'] for x in manuscript if x['id'] == 'VILLAGE_MESSAGE_2')
    dialogs = []
    for frame, text in ((6000, 'Discovered Narvik.'), (6400, 'Dock at Narvik?'),
            (8000, 'Captain, the village chief asks to hear the promised words.'),
            (8400, 'Enter the promised words.'), (12600, 'They say it means ' + clue + '.'), (13000, facilities)):
        lines = [s.strip() for s in paragraph(text).split('\n')]
        origin = 22 if len(lines) > 1 else 16
        masks = [full_cells(image(frame), font, line, origin, 296 + i * 16, (0, 8, 0)) for i, line in enumerate(lines)]
        expected = {(origin + x, 296 + i * 16 + y) for i, line in enumerate(lines) for x, y in glyphs(font, line)}
        actual = {(x, y) for y in range(296, 344) for x in range(16, 240) if image(frame).getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected
        dialogs.append({'frame': frame, 'full_source_reviewed_paragraph': text, 'complete_lines': masks,
                        'entire_text_mask_and_blank_cells_exact': True})
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    entered = raw(11800)
    needle = struct.pack('<I', marker)
    candidates = [i - 4 for i in range(0x170000, len(entered) - 4, 4) if entered[i:i + 4] == needle]
    assert len(candidates) == 1
    editor = candidates[0]
    assert entered[editor + 0xB4:editor + 0xBE] == b'Svartisen\0'
    assert struct.unpack_from('<I', entered, editor + 0x78)[0] == 9
    assert struct.unpack_from('<I', entered, editor + 0xD8)[0] == 18
    states = []
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x69B5C:0x69E00] == clean_arm[0x69B5C:0x69E00]
    assert arm[0x78AF4:0x78B24] == clean_arm[0x78AF4:0x78B24]
    for frame, expected in ((7200, 0), (11800, 0), (12600, 2), (15700, 2)):
        data = raw(frame)
        u = machine(arm)
        u.mem_write(BASE, data)
        call(u, 0xCB178, ())
        town = u.reg_read(UC_ARM_REG_R0) + 4 + 105 * 108
        call(u, 0xB50D8, (town,))
        assert u.reg_read(UC_ARM_REG_R0) == expected
        states.append({'frame': frame, 'original_town105_development': expected})
    # The ordinary post-development panel supplies this real specialty; no name pointer fixture.
    data = raw(15700)
    cache = struct.unpack_from('<6I', data, 0x15DC24)
    assert cache[5] == 1
    pointer = cache[0]
    assert data[pointer - BASE:pointer - BASE + 20] == b'Black Glacier Sword\0'
    name = 'Black Glacier Sword'
    ink = glyphs(font, name, 5)
    im = image(15700)
    actual = {(x, y) for y in range(12) for x in range(96)
              if im.getpixel((160 + x, 88 + y)) == (230, 230, 230)}
    assert ink == actual and len(ink) == 215
    for index in (0, len(name) - 1):
        edge = {(index * 5 + x, y) for x, y in glyphs(font, name[index])}
        assert edge and ink - edge != actual
    cards = [168, 169, 170, 171, 206, 207, 208, 209]
    absence = []
    for frame in (6000, 7200, 8000, 12600, 13000, 13400, 15700):
        data = raw(frame)
        assert all(data.find(rom.read_file(f'/evstill/evstill{card:03d}.pxl')) < 0 for card in cards)
        absence.append({'frame': frame, 'no_complete_village_card_file_resident_in_this_snapshot': True})
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest,
         'candidate_and_existing_patch_unchanged': True, 'report': str(RUN / 'capture_report.json'),
         'report_sha256': sha((RUN / 'capture_report.json').read_bytes()), 'frames': r['frames'],
         'actual_coordinate_only_fixture': fixture, 'all24_source_water_points_and5_negative_controls_pass': True,
         'all24_original_menu_filter_cases': menus, 'actual_pre_and_post_development_menu_masks': menu_masks,
         'six_complete_actual_dialogue_boxes': dialogs, 'ordinary_Svartisen_keyboard_entry': {
             'actual_parent': editor + BASE, 'text': 'Svartisen', 'cursor': 9, 'capacity': 18},
         'original_password_acceptance_and_town105_development': states,
         'normal_departure_and_return_to_developed_Narvik': True,
         'actual_complete_Black_Glacier_Sword_ordinary_Town_field': {'source_name_pointer': pointer,
             'origin': [160, 88], 'whole96x12_foreground_positions': 1152, 'all215_ink_points': True,
             'first_B_and_final_d_erasure_controls_rejected': True, 'initial_visual_clipping_suspicion_disproved': True,
             'old_V502_five_pixel_advance_renderer_works_unchanged': True},
         'sampled_village_card_absence_not_global_unused_proof': absence,
         'all8_village_card_ordinary_contexts_still_open': True,
         'other_villages_have_source_fixture_credit_only_not_new_gameplay_credit': True,
         'normal_long_distance_travel_or_user_save_progress_or_hardware_not_claimed': True,
         'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
         'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V618 research on unchanged V617:24 source water/menu cases;actual Narvik development,6 complete boxes,2 menu states and full long specialty pass.')


if __name__ == '__main__':
    main()
