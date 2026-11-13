"""Verify every standalone source pixel through declared original-widget tiles."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.lower_native_reference_v702 import reference
from scripts.prepare_standalone_tiles_v702 import (
    BORROWED,
    CASES,
    PRE_FRAMES,
    ROOT,
    SOURCES,
    contents,
)
from scripts.probe_button_prompt_native import call, machine
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.run_small_controls_v701 import BASE, ORIGINAL_POSITION, POSITION, VIEW, word
from scripts.run_standalone_tiles_v702 import redirect
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save


def checked(row):
    data = Path(row['path']).read_bytes()
    assert sha(data) == row['sha256']
    return data


def checker(size):
    image = Image.new('RGB', size)
    image.putdata([((85, 85, 85) if (x // 8 + y // 8) % 2 else (125, 125, 125))
                   for y in range(size[1]) for x in range(size[0])])
    return image


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path('scripts/run_standalone_tiles_v702.py'), 'producer_sha256'),
        (Path('scripts/prepare_standalone_tiles_v702.py'), 'preparer_sha256'),
        (Path('scripts/run_gender_exception_v697.py'), 'fixture_methods_sha256'),
        (ROOT / 'source_contract.json', 'source_contract_sha256'), (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    initial = read(ROOT / 'initial_preflight.json')
    assert initial['producer_sha256'] == sha((ROOT / 'initial_import_failure_runner.py').read_bytes())
    assert {k: v for k, v in initial.items() if k != 'producer_sha256'} == {k: v for k, v in pre.items() if k != 'producer_sha256'}
    production, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    before = contents(production)
    for group, row in pre['research_ROMs'].items():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        image = NdsImage.open(row['path'])
        after = contents(image)
        assert set(after) == set(before)
        assert [p for p in before if before[p] != after[p]] == [BORROWED]
        assert after[BORROWED] == before[SOURCES[group][0]] == clean.read_file(SOURCES[group][0])
        assert image.path_map() == production.path_map()
        assert all(bytes(getattr(image.rom, f)) == bytes(getattr(production.rom, f))
                   for f in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner'))
    arm = production.read_file('/__arm9__.bin')
    clean_machine = machine(clean.read_file('/__arm9__.bin'))
    person = PxlImage.from_bytes(production.read_file('/_pxl/personinfo.pxl'))
    lower_variants, lower_reference = reference(production)
    shots, ram, events, reports = {}, {}, {}, []
    for case, config in CASES.items():
        folder = CAP / ('standalone_tiles_v702_' + case)
        rp, ep = folder / 'capture_report.json', folder / 'observer/events.json'
        report, event, contract = read(rp), read(ep), read(folder / 'run_contract.json')
        expected_ROM = pre['candidate_sha256'] if config['baseline'] else pre['research_ROMs'][config['group']]['sha256']
        assert report['ROM_sha256'] == contract['ROM_sha256'] == expected_ROM
        assert report['frames'] == config['final_frame'] and report['cold_boot'] and not report['savestate_loaded']
        assert report['core_DLL_sha256'] == CORE_SHA and not report['callback_errors']
        assert not report['hardware_device_verification']
        inputs = ROOT / (case + '_inputs.json')
        assert sha(inputs.read_bytes()) == pre['case_input_hashes'][case]
        assert report['scripted_input_schedule'] == read(inputs)
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        fixture = report['isolated_standalone_tile_fixture']
        assert fixture['receipt_sha256'] == sha(ep.read_bytes()) and fixture['enabled'] == (not config['baseline'])
        assert not fixture['original_filename_consumer_or_scene_verified']
        assert bool(report.get('synthetic_borrowed_file_and_tiled_widget_fixture')) == (not config['baseline'])
        assert event['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        assert event['all_host_slots_restored_core_file_exact'] and not event['errors'] and not event['mismatches']
        assert event['whole_source_copy_recorded'] and event['CPU128_host_interval_disjoint_from_WRAM_DTCM_ITCM']
        writes = event['fixture_writes']
        assert len(writes) == (0 if config['baseline'] else len(config['tiles']) + 1)
        original = {int(k): v for k, v in event['original_view_fields'].items()}
        for i, row in enumerate(writes):
            expected_addresses = {VIEW + j * 4 for j in ((3, 7, 8, 9, 10, 11) if i in (0, len(writes) - 1) else (7, 8, 10, 11))}
            values = {int(k): v for k, v in row['declared_word_values'].items()}
            assert set(values) == expected_addresses
            before_ram, after_ram = [Path(row[k]).read_bytes() for k in ('before', 'after')]
            assert sha(before_ram) == row['before_sha256'] and sha(after_ram) == row['after_sha256']
            expected = bytearray(before_ram)
            for address, value in values.items():
                struct.pack_into('<I', expected, address - BASE, value)
            assert after_ram == expected and row['CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact']
            if i == len(writes) - 1:
                assert row['kind'] == 'restore' and row['frame'] == config['restore_frame'] and values == original
            else:
                rect = config['tiles'][i]
                assert row['frame'] == (5923 if i == 0 else 6001 + i * 100)
                assert [values[VIEW + j * 4] for j in (7, 8, 10, 11)] == rect
        for row in event['CPU_argument_redirects']:
            old, new = [bytes.fromhex(row[k]) for k in ('before_CPU128_hex', 'after_CPU128_hex')]
            assert new == redirect(old) and 5923 <= row['frame'] < config['restore_frame']
        assert bool(event['CPU_argument_redirects']) == (not config['baseline'])
        copies = [r for r in event['rows'] if r['kind'] == 'copy_entry']
        assert len(copies) == (1 if config['baseline'] else len(config['tiles']))
        if not config['baseline']:
            first = next(r for r in event['rows'] if r['kind'] == 'original_widget')
            assert first['source_owner_index_before'] == 0xFFFFFFFF
            opens = [r for r in event['rows'] if r['kind'] == 'SDK_open_entry']
            assert len(opens) == 1 and opens[0]['filename'] == '_pxl/kakutei.pxl'
            assert [r['phase'] for r in copies] == list(range(len(config['tiles'])))
            source = production.read_file(config['legacy_source'])
            for row, rect, sample in zip(copies, config['tiles'], config['sample_frames'], strict=True):
                assert row['source'] + row['size'] == rect and row['destination'] == [192, 64]
                assert row['frame'] <= sample
                raw = checked({'path': row['RAM'], 'sha256': row['RAM_sha256']})
                assert raw[row['whole_source_header'] - BASE:row['whole_source_header'] - BASE + len(source)] == source
                assert row['source_owner_index_after'] != 0xFFFFFFFF
                for field in ('DTCM', 'ITCM'):
                    assert sha(Path(row[field]).read_bytes()) == row[field + '_sha256']
        shots[case], ram[case], events[case] = pictures(report), {}, event
        assert set(shots[case]) == set(config['capture_frames'])
        for row in report['read_only_capture_RAM_snapshots']:
            raw = checked(row)
            assert len(raw) == 0x400000
            if row['frame'] in ram[case]:
                assert ram[case][row['frame']] == raw
            ram[case][row['frame']] = raw
        assert set(ram[case]) == set(config['capture_frames'])
        for frame, raw in ram[case].items():
            assert struct.unpack_from('<2I', raw, POSITION - BASE) == (192, 64)
            assert struct.unpack_from('<2I', raw, ORIGINAL_POSITION - BASE) == (84, 76)
            if frame == config['restore_frame'] + 79:
                assert all(word(raw, address) == value for address, value in original.items())
        reports.append({'case': case, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
                        'receipt': str(ep), 'receipt_sha256': sha(ep.read_bytes())})
    tile_results, source_calls, reconstructions, pixel_total = [], [], [], 0
    lower_states = []
    for group, (path, width, height) in SOURCES.items():
        config = CASES[group]
        baseline = 'baseline_' + group
        assert all(shots[group][f].tobytes() == shots[baseline][f].tobytes() for f in PRE_FRAMES)
        for frame in (config['restore_frame'] + 79, config['exit_frame'] + 99, config['final_frame']):
            assert shots[group][frame].tobytes() == shots[baseline][frame].tobytes(), (group, frame, 'restored')
        source_bytes = production.read_file(path)
        source = PxlImage.from_bytes(source_bytes)
        palette_offset = struct.unpack_from('<I', source_bytes, 12)[0]
        colors = struct.unpack_from('<256H', source_bytes, palette_offset)
        coverage = bytearray(width * height)
        rebuilt = Image.new('RGBA', (width, height))
        source_alpha = Image.new('RGBA', (width, height))
        source_alpha.putdata([(*bgr555(colors[index])[:3], 255 if colors[index] & 0x8000 else 0) for index in source.indices])
        for phase, (rect, frame) in enumerate(zip(config['tiles'], config['sample_frames'], strict=True)):
            image, base_image = shots[group][frame], shots[baseline][frame]
            expected = [native5(p) for p in base_image.get_flattened_data()]
            for y in range(76, 92):
                for x in range(84, 100):
                    expected[y * 256 + x] = native5(person.palette[person.indices[y * person.width + x]])
            sx, sy, tw, th = rect
            for y in range(th):
                for x in range(tw):
                    at = (sy + y) * width + sx + x
                    coverage[at] += 1
                    color = colors[source.indices[at]]
                    actual_color = image.getpixel((192 + x, 64 + y))
                    if color & 0x8000:
                        expected[(64 + y) * 256 + 192 + x] = native5(bgr555(color))
                        rebuilt.putpixel((sx + x, sy + y), (*actual_color, 255))
                    else:
                        rebuilt.putpixel((sx + x, sy + y), (0, 0, 0, 0))
            actual = [native5(p) for p in image.get_flattened_data()]
            assert actual[:49152] == expected[:49152], (group, phase, frame, 'complete upper source model')
            # The research file changes loading work. Independently check the
            # whole lower plane against both complete, version-bound original
            # native cursor states; do not require/claim matching SDK tick phase.
            states = []
            for name, captured in ((group, image), (baseline, base_image)):
                lower = captured.crop((0, 192, 256, 384)).tobytes()
                matches = [k for k, value in lower_variants.items() if value == lower]
                assert len(matches) == 1, (name, phase, 'whole native lower state')
                states.append(matches[0])
                lower_states.append({'case': name, 'phase': phase, 'frame': frame,
                    'all49152_RGB_pixels_match_complete_original_native_state': matches[0],
                    'not_a_same_frame_tick_prediction': True})
            predicted_diff = {i for i, (a, b) in enumerate(zip(expected[:49152], map(native5, base_image.crop((0, 0, 256, 192)).get_flattened_data()), strict=True)) if a != b}
            actual_diff = {i for i, (a, b) in enumerate(zip(image.crop((0, 0, 256, 192)).get_flattened_data(), base_image.crop((0, 0, 256, 192)).get_flattened_data(), strict=True)) if a != b}
            assert actual_diff == predicted_diff
            raw = ram[group][frame]
            view = struct.unpack_from('<12I', raw, VIEW - BASE)
            assert view[3] == 0x023139C0 and view[7:9] + view[10:12] == tuple(rect) and view[9] & 0xFFFF == 0
            u = machine(arm)
            u.mem_write(BASE, raw)
            executed = call(u, 0xD6558, (0x023139C0,))
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), len(source_bytes))) == source_bytes
            assert 0x020DED50 not in executed
            assert all(bytes(u.mem_read(pc, 4)) == bytes(clean_machine.mem_read(pc, 4)) for pc in executed)
            tile_results.append({'group': group, 'phase': phase, 'frame': frame, 'source_XYWH': rect,
                'complete_source_pixels': tw * th, 'all49152_upper_native5_pixels_and_exact_RGB_difference_positions_match': True,
                'whole_native_lower_state': states[0], 'baseline_whole_native_lower_state': states[1]})
            source_calls.append({'group': group, 'phase': phase, 'whole_source_file_bytes': len(source_bytes),
                'whole_source_file_sha256': sha(source_bytes), 'native_cached_getter_full_ABI_no_IO_bridge': True})
        assert coverage == bytes([1]) * (width * height)
        pixel_total += width * height
        for a, b in zip(source_alpha.get_flattened_data(), rebuilt.get_flattened_data(), strict=True):
            assert a[3] == b[3] and (not a[3] or native5(a) == native5(b))
        left, right = checker((width, height)), checker((width, height))
        left.paste(source_alpha, (0, 0), source_alpha)
        right.paste(rebuilt, (0, 0), rebuilt)
        scale = 3 if group == 'copyright' else 2
        review = Image.new('RGB', (width * scale * 2, height * scale + 32), '#263238')
        draw = ImageDraw.Draw(review)
        draw.text((5, 6), group + ': original source | assembled actual tiles (NOT one game frame)', fill='white')
        review.paste(left.resize((width * scale, height * scale), Image.Resampling.NEAREST), (0, 32))
        review.paste(right.resize((width * scale, height * scale), Image.Resampling.NEAREST), (width * scale, 32))
        rp = ROOT / (group + '_source_and_actual_TILE_COMPOSITE.png')
        review.save(rp)
        reconstructions.append({'group': group, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
            'source_extent': [width, height], 'each_source_pixel_covered_exactly_once': True,
            'transparent_palette_colors_preserved_by_source_file_not_inferred_from_framebuffer': True})
    sheet = Image.new('RGB', (1024, 408), '#263238')
    sd = ImageDraw.Draw(sheet)
    for i, (group, phase) in enumerate((('copyright', 0), ('copyright', 5), ('ship', 0), ('ship', 62))):
        frame = CASES[group]['sample_frames'][phase]
        sd.text((i * 256 + 4, 5), f'{group}, tile{phase}, {frame} - fixture', fill='white')
        sheet.paste(shots[group][frame], (i * 256, 24))
    sp = ROOT / 'four_unmodified_actual_tile_fixture_screens.png'
    sheet.save(sp)
    assert len(tile_results) == len(source_calls) == 69 and pixel_total == 80848
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'four_terminal_cold_boot_runs': reports, 'complete_actual_source_tile_results': tile_results,
        'all80848_source_pixels_covered_exactly_once': True,
        'all69_whole_upper_source_models3391488_pixels_and_RGB_change_positions_exact': True,
        'all138_complete_lower_planes_match_original_native_cursor_states': lower_states,
        'whole_native_lower_reference': lower_reference,
        'same_frame_lower_clock_phase_equality_to_different_research_ROM_baselines_NOT_claimed': True,
        'initial_phase006_two_screen_equality_assumption_rejected_all236_lower_differences_retained': True,
        'all30_pre_fixture_and6_restored_full_RGB_pairs_match_normal_production_baselines': True,
        'pre_fixture_full_RAM_equality_not_claimed_across_rebuilt_research_ROM_file_layouts': True,
        'whole_source_native_cache_bindings': source_calls,
        'two_uncached_original_SDK_opens_use_borrowed_kakutei_name_not_original_standalone_filenames': True,
        'production_files_all_palettes_headers_pixels_original_source_copyright_and_ship_exact': True,
        'research_ROMs_only_borrowed_slot_file_changes_ARM_code_all_other_files_ids_overlays_banner_exact': True,
        'only_declared_six_or_four_view_words_and_temporary_CPU_R3_changes_restore_before_exit': True,
        'actual_original_standalone_consumers_full_picture_scene_or_intended_crops_NOT_proven': True,
        'fifteen_native_host_and8_read_controls_pass': True,
        'all18_plaques_incomplete_all22_historical_scopes_and_full_goal_active': True,
        'initial_import_failures_before_emulation_retained_current_producer_frozen_for_all_four_runs': True,
        'review_sheets': [*reconstructions, {'path': str(sp), 'sha256': sha(sp.read_bytes())}],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V702:69 actual tiles cover every80848 source pixels once;69 complete upper source models,138 whole native lower states and30 pre/6 restored RGB pairs pass. No clock-phase/ordinary-consumer claim.', flush=True)


if __name__ == '__main__':
    main()
