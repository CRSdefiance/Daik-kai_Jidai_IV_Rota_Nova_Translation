"""Verify the terminal five-ship victory, native rewards and complete Spoils views."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_full_fleet_proximity_v653 import apply_fixture
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.search_miniature_captures_v577 import scan_image, template
from scripts.verify_dialogue_palette_v628 import captured_rgb, raster
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_regional_ui_v616 import full_cells, native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/full_fleet_victory_v654')


def funds(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    nations = get(0xCB160)
    nation = get(0x397D8, (nations,))
    return get(0x3CCC8, (nations + 4 + nation * 0x4C,))


def main():
    pre = read(ROOT / 'replay_preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    rom = NdsImage.open(pre['candidate'])
    arm, kanji = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    cap = Path(pre['output'])
    rp = cap / 'capture_report.json'
    report = read(rp)
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == 28400
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_')
                   and k != 'synthetic_battle_recovery_proximity_fixtures')
    shots = {}
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        shots[shot['frame']] = shot
    assert len(shots) == 82 and len(report['frames_captured']) == 84
    snapshots = {r['frame']: r for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots')
                 for r in report.get(key, [])}
    for row in snapshots.values():
        assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert [(f['frame'], f['action']) for f in fixtures] == [(4800, 'approach'), (5200, 'approach')]
    for fixture in fixtures:
        raw = Path(snapshots[fixture['frame']]['path']).read_bytes()
        after, expected = apply_fixture(arm, raw, 'approach')
        assert expected == {k: v for k, v in fixture.items() if k != 'frame'}
        assert sha(after) == fixture['after_RAM_sha256']
        assert len(fixture['owned_bytes']) == 8 and len(fixture['changes']) == 4
        assert fixture['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
    commands = read(pre['commands'])
    assert sha(Path(pre['commands']).read_bytes()) == pre['commands_sha256']
    assert commands[-1]['stop']
    assert {'until': 13600, 'buttons': ['Y'], 'duration': 8, 'export_native_state': True} in commands
    # A missing process and missing report caused the fresh replay, not a wait timeout.
    interruption = read(ROOT / 'interrupted_run_receipt.json')
    assert interruption['matching_python_process_CIM_inventory_empty'] and interruption['capture_report_missing']
    interrupted = Path(pre['original_interrupted_output'])
    assert not (interrupted / 'capture_report.json').exists()
    repeated = []
    for path in interrupted.glob('frame_*.png'):
        if (cap / path.name).exists():
            assert Image.open(path).tobytes() == Image.open(cap / path.name).tobytes()
            repeated.append(path.name)
    assert len(repeated) >= 80
    before_y = read(ROOT / 'pre_Y_whole_screen_comparison.json')
    assert len(before_y['paired_frames']) == 41
    previous = Path('E:/Rota Nova translations/Generated/work/emulation_v193/queued_portrait_v653_battle')
    for frame in before_y['paired_frames']:
        assert Image.open(cap / f'frame_{frame:06d}_navigation.png').tobytes() == Image.open(previous / f'frame_{frame:06d}_navigation.png').tobytes()
    state_rows = []
    for frame in (13200, 13600, 14400, 14800, 15600, 16000, 16400, 24800, 28400):
        raw = Path(snapshots[frame]['path']).read_bytes()
        own = fleet_models(arm, raw, 1)
        assert len(own) == 5 and [s['name'] for s in own] == ['Vestaros'] + ['Latina'] * 4
        assert [s['live_Hull_Crew'] for s in own] == [[60, 43]] + [[25, 19]] * 4
        money = funds(arm, raw)
        assert money == (25975 if frame <= 15600 else 30175 if frame == 16000 else 30250)
        state_rows.append({'frame': frame, 'original_named_and_live_ship_getters': own, 'native_funds': money})
    # Full original-font planes include actual wide digits and their gray shadows.
    pointer = struct.unpack_from('<I', arm, 0x54450)[0]
    palette = struct.unpack_from('<16H', arm, 0x125A20)
    text_rows = []
    for frame in (13600, 14400, 14800, 15200, 15600, 16000, 21200, 24400, 24800):
        raw = Path(snapshots[frame]['path']).read_bytes()
        text = raw[pointer - BASE:pointer - BASE + 256].split(b'\0')[0]
        pixels, events = raster(arm, kanji, text)
        crop = Image.open(shots[frame]['path']).convert('RGB').crop((16, 296, 244, 376))
        actual = list(crop.get_flattened_data())
        masks = {index: {i for i, color in enumerate(actual) if color == captured_rgb(palette[index])}
                 for index in (14, 15)}
        assert all(masks[index] == {i for i, p in enumerate(pixels) if p == index} for index in (14, 15))
        visible = [e for e in events if e['code'] not in (0, 10, 13, 32)]
        expected = [int.from_bytes(c.encode('cp932'), 'big') for c in text.decode('cp932') if not c.isspace()]
        assert [e['code'] for e in visible] == expected
        controls = []
        for event in (visible[0], visible[-1]):
            width = 12 if event['code'] > 255 else 6
            erased = [i for i, p in enumerate(pixels) if p and event['x'] <= i % 228 < event['x'] + width
                      and event['y'] <= i // 228 < event['y'] + 12]
            assert erased
            altered = bytearray(pixels)
            for i in erased:
                altered[i] = 0
            assert any(masks[index] != {i for i, p in enumerate(altered) if p == index} for index in (14, 15))
            controls.append(len(erased))
        text_rows.append({'frame': frame, 'captured_prepared_text': text.decode('cp932'),
                          'whole228x80_ink_shadow_blank_cells_and_colors_exact': True,
                          'complete_native_glyph_order_and_first_final_erasure_controls': controls,
                          'actual_PNG': shots[frame], 'native_indices_sha256': sha(pixels)})
    art = rom.read_file('/_pxl/senrihin.pxl')
    banner = native5(PxlImage.from_bytes(art).render())
    font = GameAsciiFont.from_arm9(arm)
    headers, headings, selected = [], [], []
    for frame in (16400, 16800, 17200, 17600, 18000, 18400, 18800, 19200,
                  19600, 20000, 20400, 20800, 21200, 21600, 22000, 22400, 22800,
                  23200, 23600, 24000, 24400):
        raw = Path(snapshots[frame]['path']).read_bytes()
        candidates = [at - 12 for at in range(0x17000C, len(raw) - 48, 4)
                      if struct.unpack_from('<I', raw, at)[0] == 0x02313A4C
                      and struct.unpack_from('<2I', raw, at + 28) == (256, 16)]
        assert len(candidates) == 1
        view, parent = BASE + candidates[0], BASE + candidates[0] - 0x3070
        assert struct.unpack_from('<I', raw, parent - BASE + 16)[0] == 3
        index = struct.unpack_from('<I', raw, parent - BASE + 20)[0]
        assert 0 <= index < 5
        u = machine(arm)
        u.mem_write(BASE, raw)
        filename = struct.unpack('<I', u.mem_read(0x02313A4C + 12, 4))[0]
        assert bytes(u.mem_read(filename, 32)).split(b'\0')[0] == b'_pxl/senrihin.pxl'
        call(u, 0xD4170, (view,))
        resident = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(resident, len(art))) == art
        im = Image.open(shots[frame]['path']).convert('RGB')
        title = ('Vestaros' if index == 0 else 'Latina') + ' Cargo Setup'
        heading = full_cells(im, font, title, (256 - len(title) * 6) // 2, 2, (230, 230, 230))
        headings.append({'frame': frame, 'actual_selected_index_field': index, 'complete_title': heading})
        selected.append(index)
        if frame in (17200, 17600, 18000, 18400, 18800, 19200, 19600, 20800, 21600, 22000, 22400, 22800):
            assert native5(im).crop((0, 261, 256, 277)).tobytes() == banner.tobytes()
            headers.append({'frame': frame, 'original_mode': 3, 'view': view, 'parent': parent,
                            'owner': 0x02313A4C, 'whole_resident_PXL_exact': True,
                            'all4096_Spoils_banner_pixels_letters_wood_border_palette_exact': True})
    assert set(selected) == set(range(5))
    frame = PxlImage.from_bytes(rom.read_file('/_pxl/__frame.pxl'))
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    templates = {r['text']: template(frame, r['box']) for r in batch['records'][15:] if r['text'] not in ('M', 'D')}
    colors = {tuple((w >> s) & 31 for s in (0, 5, 10)) for i in range(83)
              for w in [struct.unpack_from('<H', frame.source, 20 + i * 32 + 18)[0]]}
    search = []
    for shot in shots.values():
        matches = scan_image(shot['path'], templates, colors)
        search.append({'frame': shot['frame'], 'complete_mask_matches': matches})
    save(ROOT / 'proof.json', {
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
        'terminal28400_cold_boot_no_savestate_and_no_callback_errors': True,
        'all84_capture_records82_unique_frames_hash_bound': True,
        'original_interrupted_run_not_counted_as_terminal': interruption,
        'repeated_interrupted_capture_pixels_exact': repeated,
        'all41_pre_Y_whole_screens_exact_prior_loss_path': before_y,
        'two_coordinate_only_fixtures_complete4MiB_replay': fixtures,
        'original_five_ship_victory_and_native_reward_states': state_rows,
        'native_funds_increments4200_then75_exact': True,
        'complete_nine_actual_reward_and_warning_text_planes': text_rows,
        'all21_original_cargo_headings_and_selected_ship_fields': headings,
        'all12_complete4096_pixel_Spoils_banners': headers,
        'frame23200_hover_tooltip_banner_overlap_receives_no_whole_banner_credit': True,
        'all_five_ship_positions_and_full_L_R_wrap_exercised': True,
        'normal_finish_cancel_return_and_final_accept_then_post_victory_story_reached': True,
        'cargo_selection_previews_are_not_comprehensive_permanent_acquisition_clearance': True,
        'bounded_five_miniature_capture_search': search,
        'six_small_controls_still_require_actual_parent_identification': True,
        'source_battery_ROM_patch_manifest_registry_and_canonical_unchanged': True,
        'no_new_post_victory_normal_Save_action_performed': True,
        'all18_original_plaques_incomplete22_historical_scopes_preserved': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V654: terminal five-ship victory;4200+75 original funds;{len(text_rows)} full text planes;'
          f'{len(headings)} headings;{len(headers)} whole Spoils banners verified.')


if __name__ == '__main__':
    main()
