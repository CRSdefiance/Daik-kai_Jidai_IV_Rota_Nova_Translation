"""Check complete live control rectangles, exact fixtures and restored screens."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.run_small_controls_v701 import (
    BASE,
    CAP,
    CASES,
    FRAMES,
    ORIGINAL_POSITION,
    POSITION,
    ROM,
    ROOT,
    VIEW,
    redirect,
    word,
)
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save


def checked(row):
    data = Path(row['path']).read_bytes()
    assert sha(data) == row['sha256']
    return data


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path('scripts/run_small_controls_v701.py'), 'producer_sha256'),
                        (Path('scripts/run_gender_exception_v697.py'), 'fixture_methods_sha256'),
                        (ROOT / 'inputs.json', 'inputs_sha256'), (ROOT / 'source_contract.json', 'source_contract_sha256'),
                        (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = current.read_file('/__arm9__.bin')
    clean_machine = machine(clean.read_file('/__arm9__.bin'))
    person = PxlImage.from_bytes(current.read_file('/_pxl/personinfo.pxl'))
    photos, memories, events, reports, source_calls, crops, frames_checked = {}, {}, {}, [], [], [], []
    negative_controls = []
    for case, config in CASES.items():
        folder = CAP / ('small_controls_v701_' + case)
        rp, ep = folder / 'capture_report.json', folder / 'observer/events.json'
        report, event, contract = read(rp), read(ep), read(folder / 'run_contract.json')
        assert report['frames'] == 7000 and report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert not report['callback_errors'] and not report['hardware_device_verification']
        assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        fixture = report['isolated_original_widget_fixture']
        assert fixture['enabled'] == (case != 'baseline') and fixture['receipt_sha256'] == sha(ep.read_bytes())
        assert not fixture['normal_control_location_palette_or_gameplay_context_verified']
        assert bool(report.get('synthetic_exact_control_widget_fixture')) == (case != 'baseline')
        assert event['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        assert event['all_host_slots_restored_core_file_exact'] and not event['errors'] and not event['mismatches']
        assert event['CPU128_host_interval_disjoint_from_WRAM_DTCM_ITCM'] and event['whole_source_copy_recorded']
        original = next(r for r in event['rows'] if r['kind'] == 'original_widget')
        assert original['frame'] == 5923
        if case == 'confirm':
            opens = [r for r in event['rows'] if r['kind'] == 'SDK_open_entry']
            assert len(opens) == 1 and opens[0]['filename'] == '_pxl/kakutei.pxl' and opens[0]['frame'] == 5923
            assert original['source_owner_index_before'] == 0xFFFFFFFF
        writes = event['fixture_writes']
        assert len(writes) == (0 if case == 'baseline' else 2)
        if writes:
            assert [(r['kind'], r['frame']) for r in writes] == [('install', 5923), ('restore', 6401)]
            original_values = {int(k): v for k, v in event['original_view_fields'].items()}
            assert set(original_values) == {VIEW + i * 4 for i in (3, 7, 8, 9, 10, 11)}
            for row in writes:
                before, after = [Path(row[k]).read_bytes() for k in ('before', 'after')]
                assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256']
                expected = bytearray(before)
                values = {int(k): v for k, v in row['declared_word_values'].items()}
                assert set(values) == set(original_values)
                for address, value in values.items():
                    struct.pack_into('<I', expected, address - BASE, value)
                assert after == expected and row['CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact']
                if row['kind'] == 'restore':
                    assert values == original_values
        redirects = event['CPU_argument_redirects']
        assert bool(redirects) == (case != 'baseline')
        for row in redirects:
            before, after = [bytes.fromhex(row[n]) for n in ('before_CPU128_hex', 'after_CPU128_hex')]
            assert after == redirect(before) and 5923 <= row['frame'] < 6401
            assert {i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b} <= set(range(28, 32))
        photos[case], memories[case], events[case] = pictures(report), {}, event
        assert set(photos[case]) == set(FRAMES)
        for row in report['read_only_capture_RAM_snapshots']:
            value = checked(row)
            assert len(value) == 0x400000
            if row['frame'] in memories[case]:
                assert memories[case][row['frame']] == value
            memories[case][row['frame']] = value
        assert set(memories[case]) == set(FRAMES)
        for frame, raw in memories[case].items():
            assert struct.unpack_from('<2I', raw, POSITION - BASE) == (192, 64)
            assert struct.unpack_from('<2I', raw, ORIGINAL_POSITION - BASE) == (84, 76)
            # The widget is alive at6500; B6501 later destroys its parent.
            # Freed/reused heap bytes are not persistent UI input fields.
            if frame == 6500 and case != 'baseline':
                assert all(word(raw, a) == v for a, v in original_values.items())
        draw = next(r for r in event['rows'] if r['kind'] == 'copy_entry')
        raw = checked({'path': draw['RAM'], 'sha256': draw['RAM_sha256']})
        assert list(config['rect']) == draw['source'] + draw['size']
        assert draw['destination'] == ([84, 76] if case == 'baseline' else [192, 64])
        assert draw['source_owner_index_after'] != 0xFFFFFFFF
        source_bytes = current.read_file(config['path'])
        assert raw[draw['whole_source_header'] - BASE:draw['whole_source_header'] - BASE + len(source_bytes)] == source_bytes
        for frame in (6200, 6400):
            raw = memories[case][frame]
            u = machine(arm)
            u.mem_write(BASE, raw)
            executed = call(u, 0xD6558, (config['owner'],))
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), len(source_bytes))) == source_bytes
            assert 0x020DED50 not in executed
            assert all(bytes(u.mem_read(pc, 4)) == bytes(clean_machine.mem_read(pc, 4)) for pc in executed)
            source_calls.append({'case': case, 'frame': frame, 'whole_source_bytes': len(source_bytes),
                'source_sha256': sha(source_bytes), 'whole_actual_native_cache_getter_no_IO_bridge_and_complete_ABI': True})
        reports.append({'case': case, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
                        'receipt': str(ep), 'receipt_sha256': sha(ep.read_bytes())})
    baseline = photos['baseline']
    first_entries = [next(r for r in e['rows'] if r['kind'] == 'original_widget') for e in events.values()]
    assert len({r['CPU128_hex'] for r in first_entries}) == 1
    assert all(r['view_words'] == first_entries[0]['view_words'] for r in first_entries)
    before_files = [Path(events[c]['fixture_writes'][0]['before']).read_bytes() for c in CASES if c != 'baseline']
    assert all(v == before_files[0] for v in before_files)
    for case, config in CASES.items():
        if case == 'baseline':
            continue
        before = [f for f in FRAMES if f <= 5900]
        assert len(before) == 15
        assert all(photos[case][f].tobytes() == baseline[f].tobytes() for f in before)
        assert all(memories[case][f] == memories['baseline'][f] for f in before)
        for frame in (6500, 6600, 7000):
            assert photos[case][frame].tobytes() == baseline[frame].tobytes(), (case, frame, 'restored full screen')
        source = PxlImage.from_bytes(current.read_file(config['path']))
        bank = config['bank']
        palette_offset = struct.unpack_from('<I', source.source, 12)[0] + bank * 32
        palette = struct.unpack_from('<16H', source.source, palette_offset)
        sx, sy, width, height = config['rect']
        for frame in (6200, 6400):
            image, base_image = photos[case][frame], baseline[frame]
            expected = [native5(p) for p in base_image.get_flattened_data()]
            for y in range(76, 92):
                for x in range(84, 100):
                    expected[y * 256 + x] = native5(person.palette[person.indices[y * person.width + x]])
            for y in range(height):
                for x in range(width):
                    index = source.indices[(sy + y) * source.width + sx + x]
                    color = palette[index]
                    if color & 0x8000:
                        expected[(64 + y) * 256 + 192 + x] = native5(bgr555(color))
            actual = [native5(p) for p in image.get_flattened_data()]
            assert actual == expected, (case, frame, 'complete source-predicted image')
            expected_diff = {i for i, (a, b) in enumerate(zip(expected, map(native5, base_image.get_flattened_data()), strict=True)) if a != b}
            actual_diff = {i for i, (a, b) in enumerate(zip(image.get_flattened_data(), base_image.get_flattened_data(), strict=True)) if a != b}
            assert actual_diff == expected_diff
            if frame == 6200:
                wanted = [expected[(64 + y) * 256 + 192 + x] for y in range(height) for x in range(width)]
                shifted = [native5(image.getpixel((193 + x, 64 + y))) for y in range(height) for x in range(width)]
                assert shifted != wanted
                wrong = []
                wrong_palette = struct.unpack_from('<16H', source.source, struct.unpack_from('<I', source.source, 12)[0])
                for y in range(height):
                    for x in range(width):
                        index = source.indices[(sy + y) * source.width + sx + x]
                        color = wrong_palette[index]
                        backdrop = native5(base_image.getpixel((192 + x, 64 + y)))
                        if case == 'confirm':
                            # Rejected assumption: index0 is transparent and all
                            # other indices are opaque, ignoring stored alpha.
                            wrong.append(native5(bgr555(color)) if index else backdrop)
                        else:
                            wrong.append(native5(bgr555(color)) if color & 0x8000 else backdrop)
                assert wrong != wanted
                negative_controls.append({'case': case, 'one_pixel_destination_shift_rejected': True,
                    'wrong_index0_alpha_rejected' if case == 'confirm' else 'wrong_palette_bank0_rejected': True})
            crops.append({'case': case, 'frame': frame, 'complete_source_XYWH': config['rect'],
                'destination': [192, 64], 'bank': bank, 'complete_native5_pixels': width * height,
                'palette_word_alpha_and_every_background_first_final_letter_pixel_exact': True})
            frames_checked.append({'case': case, 'frame': frame,
                'all98304_native5_pixels_exact_full_RGB_changes_only_at_independently_source_predicted_pixels': True})
    sample = bytes.fromhex(first_entries[0]['CPU128_hex'])
    redirect_controls = []
    for name, offset in (('wrong_PC', 8), ('wrong_view', 20), ('wrong_screen', 24), ('wrong_original_point', 28)):
        bad = bytearray(sample)
        struct.pack_into('<I', bad, offset, struct.unpack_from('<I', bad, offset)[0] ^ 4)
        try:
            redirect(bytes(bad))
        except ValueError:
            pass
        else:
            raise AssertionError(name)
        redirect_controls.append(name)
    sheet = Image.new('RGB', (768, 880), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, case in enumerate(c for c in CASES if c != 'baseline'):
        x, y = i % 3 * 256, i // 3 * 440
        draw.text((x + 5, y + 4), CASES[case]['label'] + ': isolated widget fixture', fill='white')
        sheet.paste(photos[case][6200], (x, y + 24))
    sp = ROOT / 'six_actual_control_widget_fixture_screens.png'
    sheet.save(sp)
    restore_sheet = Image.new('RGB', (768, 408), '#263238')
    rd = ImageDraw.Draw(restore_sheet)
    for i, (case, frame) in enumerate((('baseline', 6200), ('confirm', 6500), ('confirm', 6600))):
        rd.text((i * 256 + 4, 5), f'{case}, {frame}' + (' normal baseline' if case == 'baseline' else ' restored'), fill='white')
        restore_sheet.paste(photos[case][frame], (i * 256, 24))
    rs = ROOT / 'ordinary_baseline_and_restored_Info_roster.png'
    restore_sheet.save(rs)
    assert len(crops) == 12 and sum(r['complete_native5_pixels'] for r in crops) == 4608
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'seven_terminal7000_frame_cold_boots': reports,
        'six_exact_assets_original_loader_and_widget_complete_rectangles_verified': crops,
        'complete_control_native5_pixels': 4608, 'whole_original_native_cache_bindings': source_calls,
        'all12_whole_source_predicted_two_screen_images': frames_checked,
        'all90_pre_fixture_whole_RGB_RAM_pairs_and6_before_write_full_RAM_states_exact': True,
        'all18_restored_full_RGB_pairs_in_Info_and_roster_exact': True,
        'Confirm_original_uncached_owner_real_SDK_open_and_full532_byte_file_verified': True,
        'only_six_view_words_and_ephemeral_CPU_R3_changed_all_view_inputs_restored': True,
        'fifteen_native_host_eight_read_and_four_redirect_negative_controls_pass': redirect_controls,
        'palette_alpha_from_stored_word_not_index_zero_Confirm14_transparent0_opaque': True,
        'all12_wrong_placement_palette_or_index0_alpha_controls_rejected': negative_controls,
        'normal_control_contexts_and_intended_palette_geometry_NOT_proven': True,
        'ROM_all_source_art_files_donor_registry_patch_and_pointers_unchanged': True,
        'all18_plaques_incomplete_full_goal_active_no_fixture_guide_promotion': True,
        'review_sheets': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in (sp, rs)],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V701 six exact control widgets:12 whole source-predicted screens4608 rectangle pixels,90 pre-fixture pairs and18 restored full screens pass.', flush=True)


if __name__ == '__main__':
    main()
