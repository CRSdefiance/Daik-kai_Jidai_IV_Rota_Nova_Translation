"""Whole ordinary cursor frames and original native scene variants, without ring masks."""

import struct
import sys
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_equipment_cursor_v663 import paint
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_transition_scanlines_v659 import core_entries, prologue_controls
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/equipment_cursor_v663')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def mixed_source_rows(frames, images):
    folder = CAP / 'equipment_cursor_v663_scanlines'
    report_path = folder / 'capture_report.json'
    observed = read(report_path)
    assert observed['frames'] == 8063 and observed['cold_boot'] and not observed['savestate_loaded']
    assert not observed['callback_errors']
    assert observed['scripted_input_schedule'] == read(ROOT / 'inputs.json')
    assert observed['ROM_sha256'] == read(ROOT / 'preflight.json')['candidate_sha256']
    assert not any(v for k, v in observed.items() if k.startswith('synthetic_'))
    shots = {r['frame']: r for r in observed['frames_captured']}
    assert shots.keys() == images.keys()
    for frame, item in shots.items():
        assert sha(Path(item['path']).read_bytes()) == item['PNG_sha256']
        assert Image.open(item['path']).convert('RGB').tobytes() == images[frame].tobytes()
    path = folder / 'scanlines/scanline_observer.json'
    observer = read(path)
    assert observer['script_sha256'] == sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes())
    assert observer['all_entry_bytes_restored_and_DLL_file_unchanged']
    assert observer['every_original_RenderLine_called_once'] and not observer['errors']
    assert observer['no_game_ROM_RAM_VRAM_register_or_input_writes']
    assert set(map(int, observer['frames'])) == set(frames)
    for name, digest in observer['source_files'].items():
        assert sha(Path(name).read_bytes()) == digest
    binding = core_entries(observer)
    abi = prologue_controls()
    assert len(abi) == 12
    cases = []
    for frame in frames:
        item = observer['frames'][str(frame)]
        for info in item['files'].values():
            assert sha(Path(info['path']).read_bytes()) == info['sha256']
        words = struct.unpack('<49152H', Path(item['files']['bitmap_row']['path']).read_bytes())
        io = Path(item['files']['IO']['path']).read_bytes()
        start = 6400 + ((frame - 6400) // 400) * 400
        off, on = (struct.unpack('<49152H', (ROOT / f'native_lower_{start}_{kind}.bin').read_bytes())
                   for kind in ('off', 'on'))
        assert all(w == a or w == b for w, a, b in zip(words, off, on, strict=True))
        assert len(item['rows']) == 192
        for line, row in enumerate(item['rows']):
            assert (row['line'], row['VCount'], row['frame'], row['format']) == (line, line, frame, '555')
            assert row['original_render_called_once_and_returned']
            r = io[line * 8192:(line + 1) * 8192]
            assert struct.unpack_from('<I', r)[0] == 0x1191B
            assert struct.unpack_from('<H', r, 14)[0] == 0x4084
            assert struct.unpack_from('<H', r, 8)[0] & 3 == 1 and r[0x243] == 0x81
            assert struct.unpack_from('<4h2I', r, 0x30) == (256, 0, 0, 256, 0, line * 256)
            assert struct.unpack_from('<3H', r, 0x50) == (0, 0, 0)
            assert struct.unpack_from('<H', r, 0x6C)[0] == 0
        expected = Image.new('RGB', (256, 192))
        expected.putdata(rgb(words))
        assert expected.tobytes() == images[frame].crop((0, 192, 256, 384)).tobytes(), frame
        cases.append({'frame': frame, 'all49152_bitmap_words_from_original_native_variants': True,
            'all192_actual_before_RenderLine_rows_and_IO_verified': True,
            'complete49152_same_frame_lower_RGB_pixels_exact_without_row_phase_or_delay_fit': True})
    return {'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'observer': str(path), 'observer_sha256': sha(path.read_bytes()), 'cases': cases,
        'all325_whole_observed_vs_unmodified_core_screens_exact': True,
        'source_HBlank_call_bindings': binding, 'twelve_host_prefix_ABI_controls': abi,
        'no_game_memory_writes_host_detours_restored': True}


def report(label, digest):
    path = CAP / ('equipment_cursor_v663_' + label) / 'capture_report.json'
    data = read(path)
    assert data['frames'] == 8063 and data['ROM_sha256'] == digest
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not any(v for k, v in data.items() if k.startswith('synthetic_'))
    shots = {s['frame']: s for s in data['frames_captured']}
    for s in shots.values():
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
    snapshots = {r['frame']: r for r in data.get('read_only_capture_RAM_snapshots', [])}
    for r in snapshots.values():
        assert sha(Path(r['path']).read_bytes()) == r['sha256']
    for n in data.get('read_only_capture_native_states', []):
        assert n['read_only_export'] and not n['state_loaded'] and n['main_RAM_unchanged_by_export']
        assert n['serialized_RAM_matches_same_frame_direct_export']
        assert sha(Path(n['path']).read_bytes()) == n['sha256']
        for r in n['regions'].values():
            assert sha(Path(r['path']).read_bytes()) == r['sha256']
    return data, shots, snapshots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    current, shots, ram, receipt = report('current', pre['candidate_sha256'])
    control, controls, _, control_receipt = report('control', pre['control_sha256'])
    assert current['scripted_input_schedule'] == control['scripted_input_schedule'] == read(ROOT / 'inputs.json')
    assert current['core_options'] == control['core_options'] and current['core_DLL_sha256'] == control['core_DLL_sha256']
    assert current['battery_save_preloaded']['source_sha256'] == control['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert shots.keys() == controls.keys() and len(shots) == 325
    images = {}
    for frame in shots:
        image = Image.open(shots[frame]['path']).convert('RGB')
        assert image.tobytes() == Image.open(controls[frame]['path']).convert('RGB').tobytes(), frame
        images[frame] = image
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0xF9C, 0xFF4), (0x7FA0C, 0x7FA6C), (0x7FB74, 0x7FD20),
             (0xD13A4, 0xD149C), (0x81950, 0x81960)]
    for a, b in spans:
        assert arm[a:b] == clean_arm[a:b]
    font = GameAsciiFont.from_arm9(arm)
    palette_review = read('work/analysis/plaque_review_v632/current_plaque_review_proof.json')
    plaques = palette_review['all18_current_native_review_entries'][7:17]
    assert len(plaques) == 10
    rows, native_rows, plaque_count, mixed_frames, hints, hint_controls = [], [], 0, [], [], []
    prepared = None
    if '--prepare-phases' not in sys.argv:
        prepared = read(ROOT / 'phase_candidates.json')
        assert prepared['native_script_sha256'] == sha(Path('scripts/research_equipment_cursor_v663.py').read_bytes())
    for slot, start in enumerate((6400, 6800, 7200, 7600, 8000)):
        hint_text, hint_left = [('Weapon', 16), ('Blue Oak Shield', 64), ('Equipped Items', 112),
                                ('Equipped Items', 136), ('Equipped Items', 136)][slot]
        variants = {}
        for visible in (False, True):
            row = paint(start, visible) if prepared is None else next(
                r for r in prepared['native_rows'] if r['frame'] == start and r['controlled_blink_visible'] == visible)
            assert row['whole98304_bytes_written_over_poison']
            native_rows.append(row)
            suffix = 'on' if visible else 'off'
            binary = (ROOT / f'native_lower_{start}_{suffix}.bin').read_bytes()
            assert sha(binary) == row['lower_sha256']
            native = Image.open(ROOT / f'native_lower_{start}_{suffix}.png').convert('RGB')
            checked = Image.new('RGB', (256, 192))
            checked.putdata(rgb([v for v, in struct.iter_unpack('<H', binary)]))
            assert checked.tobytes() == native.tobytes()
            variants[visible] = native.tobytes()
        assert variants[False] != variants[True]
        phases = []
        for frame in range(start, start + 64):
            raw = Path(ram[frame]['path']).read_bytes()
            selected = struct.unpack_from('<I', raw, 0x189E24 + 0x6B90)[0]
            assert selected == slot + 3
            image = images[frame]
            ink, bounds = complete_mask(font, hint_text, image, hint_left + 2, 210, (0, 8, 0))
            hints.append({'frame': frame, 'text': hint_text, 'bounds': bounds, 'complete_ink': ink})
            if slot < 3 and frame == start:
                for index in (0, len(hint_text) - 1):
                    bad = image.copy()
                    point = next((hint_left + 2 + index * 6 + x, 210 + y)
                                 for y in range(11) for x in range(6)
                                 if font.decode(hint_text[index]).getpixel((x, y)))
                    bad.putpixel(point, (255, 0, 0))
                    try:
                        complete_mask(font, hint_text, bad, hint_left + 2, 210, (0, 8, 0))
                    except ValueError:
                        hint_controls.append({'text': hint_text, 'letter': hint_text[index], 'rejected': True})
                    else:
                        raise AssertionError('Missing hint edge letter was accepted')
            lower = image.crop((0, 192, 256, 384)).tobytes()
            matches = [visible for visible, pixels in variants.items() if pixels == lower]
            if len(matches) == 1:
                phases.append(matches[0])
            else:
                assert not matches
                aa, bb = (Image.frombytes('RGB', (256, 192), variants[v]) for v in (False, True))
                assert all(p == a or p == b for p, a, b in zip(
                    image.crop((0, 192, 256, 384)).get_flattened_data(),
                    aa.get_flattened_data(), bb.get_flattened_data(), strict=True)), frame
                mixed_frames.append(frame)
                phases.append('mixed')
            for plaque in plaques:
                reference = Path(plaque['current_crop'])
                assert sha(reference.read_bytes()) == plaque['current_crop_sha256']
                assert image.crop(plaque['bounds']).tobytes() == Image.open(reference).convert('RGB').tobytes()
                plaque_count += 1
        assert phases.count(True) > 0 and phases.count(False) > 0
        on, off = (ROOT / f'native_lower_{start}_{x}.bin' for x in ('on', 'off'))
        a, b = on.read_bytes(), off.read_bytes()
        differences = [i for i, (x, y) in enumerate(zip(struct.unpack('<49152H', a), struct.unpack('<49152H', b), strict=True)) if x != y]
        # The original hint is drawn later and can cover part of the top ring.
        assert 0 < len(differences) <= 272
        x0 = 14 + slot * 48
        assert all(x0 <= i % 256 < x0 + 36 and 30 <= i // 256 < 66 for i in differences)
        rows.append({'slot': slot, 'frames': [start, start + 63], 'selected_controller_id': slot + 3,
            'whole_blink_on_frames': phases.count(True), 'whole_blink_off_frames': phases.count(False),
            'mixed_frames_needing_source_scanline_evidence': [start + i for i, p in enumerate(phases) if p == 'mixed'],
            'actual_on_off_visible_ring_difference_pixels': len(differences),
            'tooltip_overlap_not_excluded': True})
        print('Whole slot window verified:', slot, len(differences), flush=True)
    save(ROOT / 'phase_candidates.json', {'mixed_frames': mixed_frames,
        'slot_rows': rows, 'native_rows': native_rows,
        'native_script_sha256': sha(Path('scripts/research_equipment_cursor_v663.py').read_bytes()),
        'full_goal_complete': False})
    if '--prepare-phases' in sys.argv:
        print('Prepared source variants; mixed source frames still require observation:', mixed_frames)
        return
    scanlines = mixed_source_rows(mixed_frames, images)
    # The actual cached footer is Select followed by Back. Independently verify
    # all active cells before removing first/final letter cells in isolated copies.
    state = read(CAP / 'equipment_cursor_v663_current/capture_native_state_006400/native_state.json')
    dtcm = Path(state['regions']['DTCM']['path']).read_bytes()
    source_indices = bytes(n for byte in dtcm[:1536] for n in (byte & 15, byte >> 4))
    mask = glyphs(font, 'SelectBack')
    assert all(source_indices[y * 256 + x] == int((x, y) in mask) for y in range(12) for x in range(60))
    footer_controls = []
    for label, cell, ch in [('Select_first', 0, 'S'), ('Select_last', 30, 't'),
                            ('Back_first', 36, 'B'), ('Back_last', 54, 'k')]:
        result = paint(6400, True, cell)
        assert result['complete_lower_RGB_difference_count'] == len(glyphs(font, ch))
        footer_controls.append({'label': label, 'source_cell_x': cell,
            'missing_visible_ink': result['complete_lower_RGB_difference_count'], 'rejected': True})
    # Review the active ten skill labels, rather than an older unused profile.
    skill_labels = []
    for data, locale in ((clean_arm, 'Japanese'), (arm, 'English')):
        u = machine(data)
        if locale == 'English':
            u.mem_write(POOL, bytes(MainCodeFile(data, BASE).sections[3].data[:-48]))
        labels = []
        for i in range(10):
            call(u, 0x7EEB0, (i,))
            labels.append(bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0].decode('cp932'))
        skill_labels.append({'locale': locale, 'original_getter_labels': labels})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': {'current': receipt, 'V636_control': control_receipt},
        'two_terminal8063_frame_ordinary_saved_cold_boots_no_gameplay_or_code_fixtures': True,
        'all325_whole_two_screen_pairs31948800_RGB_pixels_exact': True,
        'five_actual_slot_windows320_frames': rows,
        'all15728640_lower_RGB_pixels_match_native_variants_or_actual_source_rows_without_exclusions': True,
        'ten_mixed_transition_frames_resolved_at_actual_source_row_reads': scanlines,
        'ten_original_native_lower_scene_replays': native_rows,
        'native_clock_inputs_are_explicit_SDK_bridge_not_observed_CPU_tick_phase': True,
        'original_64bit_blink_period': 0x88FA4, 'original_on_cutoff': 0x77DAF,
        'all_native_framebuffer_outputs_poisoned_visible_VRAM_erased_not_used_as_input': True,
        'all3200_static_plaque_crops_exact_reviewed_V632': plaque_count,
        'all320_complete_hint_font_masks': hints,
        'six_hint_first_last_letter_deletion_controls': hint_controls,
        'complete720_active_footer_source_cells_and_all_first_last_letters_verified': True,
        'four_footer_deletion_controls': footer_controls,
        'actual_skill_label_source_review': skill_labels,
        'source_unchanged_ring_constructor_predicate_and_colour_spans': [
            {'start': a, 'end': b, 'sha256': sha(arm[a:b])} for a, b in spans],
        'no_new_upper_scene_native_source_timing_hardware_or_every_character_claim': True,
        'older_V637_exclusion_retained_historically_not_relabelled_as_retested': True,
        'all18_original_plaques_incomplete_and22_historical_scope_objects_retained': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'full_goal_complete': False,
        'scripts': {p: sha(Path(p).read_bytes()) for p in ('scripts/run_equipment_cursor_v663.py',
            'scripts/research_equipment_cursor_v663.py', 'scripts/verify_equipment_cursor_v663.py',
            'scripts/run_equipment_scanlines_v663.py', 'scripts/observe_transition_scanlines_v659.py')}})
    print('V663: 325 whole control pairs;320 full lower source matches;3200 plaques;4 footer boundary controls; full goal active.')


if __name__ == '__main__':
    main()
