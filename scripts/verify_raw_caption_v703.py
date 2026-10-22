"""Verify accepted raw16 loading, exact copied words and matched display alpha."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, SOURCE
from scripts.lower_native_reference_v702 import reference
from scripts.prepare_raw_caption_v703 import BORROWED, CASES, ROOT, TILES, caption, contents
from scripts.probe_button_prompt_native import machine
from scripts.run_raw_caption_v703 import redirect
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.run_small_controls_v701 import BASE, VIEW, word
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save

FB = 0x022F9794


def checked(row):
    data = Path(row['path']).read_bytes()
    assert sha(data) == row['sha256']
    return data


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path('scripts/run_raw_caption_v703.py'), 'producer_sha256'),
        (Path('scripts/prepare_raw_caption_v703.py'), 'preparer_sha256'),
        (Path('scripts/run_gender_exception_v697.py'), 'fixture_methods_sha256'),
        (ROOT / 'source_contract.json', 'source_contract_sha256'), (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    production, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    pixels, source_proof = caption(production)
    assert source_proof == pre['source']
    source_words = struct.unpack('<2304H', pixels)
    descriptor = struct.pack('<5I', 16, 72, 32, 20, 20)
    payloads = {'source': descriptor + pixels,
                'opaque_CONTROL': descriptor + struct.pack('<2304H', *(w | 32768 for w in source_words))}
    original = contents(production)
    for case, row in pre['research_ROMs'].items():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        image = NdsImage.open(row['path'])
        actual = contents(image)
        assert set(actual) == set(original)
        assert [p for p in original if original[p] != actual[p]] == [BORROWED]
        assert actual[BORROWED] == payloads[case] and image.path_map() == production.path_map()
        assert all(bytes(getattr(image.rom, f)) == bytes(getattr(production.rom, f))
                   for f in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner'))
    current_code, old_code = [machine(i.read_file('/__arm9__.bin')) for i in (production, clean)]
    assert bytes(current_code.mem_read(0x01FF92D8, 0x380)) == bytes(old_code.mem_read(0x01FF92D8, 0x380))
    person = PxlImage.from_bytes(production.read_file('/_pxl/personinfo.pxl'))
    native_lower, lower_ref = reference(production)
    shots, memories, events, native, reports, tile_rows = {}, {}, {}, {}, [], []
    for case, config in CASES.items():
        folder = CAP / ('raw_caption_v703_' + case)
        rp, ep = folder / 'capture_report.json', folder / 'observer/events.json'
        report, event, contract = read(rp), read(ep), read(folder / 'run_contract.json')
        digest = pre['candidate_sha256'] if config['baseline'] else pre['research_ROMs'][case]['sha256']
        assert report['ROM_sha256'] == contract['ROM_sha256'] == digest
        assert report['frames'] == 6800 and report['cold_boot'] and not report['savestate_loaded']
        assert report['core_DLL_sha256'] == CORE_SHA and not report['callback_errors'] and not report['hardware_device_verification']
        inputs = ROOT / (case + '_inputs.json')
        assert sha(inputs.read_bytes()) == pre['case_input_hashes'][case]
        assert report['scripted_input_schedule'] == read(inputs)
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        fixture = report['isolated_standalone_tile_fixture']
        assert fixture['receipt_sha256'] == sha(ep.read_bytes()) and fixture['enabled'] == (case != 'baseline')
        assert not fixture['original_filename_consumer_or_scene_verified']
        assert event['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        assert event['all_host_slots_restored_core_file_exact'] and not event['errors'] and not event['mismatches']
        writes = event['fixture_writes']
        assert len(writes) == (0 if case == 'baseline' else 5)
        original_fields = {int(k): v for k, v in event['original_view_fields'].items()}
        for i, row in enumerate(writes):
            before, after = [Path(row[k]).read_bytes() for k in ('before', 'after')]
            assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256']
            expected = bytearray(before)
            values = {int(k): v for k, v in row['declared_word_values'].items()}
            assert set(values) == {VIEW + j * 4 for j in ((3, 7, 8, 9, 10, 11) if i in (0, 4) else (7, 8, 10, 11))}
            for address, value in values.items():
                struct.pack_into('<I', expected, address - BASE, value)
            assert after == expected and row['CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact']
            if i == 4:
                assert row['frame'] == 6401 and values == original_fields
            else:
                assert row['frame'] == (5923 if not i else 6001 + i * 100)
                assert [values[VIEW + j * 4] for j in (7, 8, 10, 11)] == TILES[i]
        for row in event['CPU_argument_redirects']:
            assert bytes.fromhex(row['after_CPU128_hex']) == redirect(bytes.fromhex(row['before_CPU128_hex']))
        assert bool(event['CPU_argument_redirects']) == (case != 'baseline')
        copies = [r for r in event['rows'] if r['kind'] == 'copy_entry']
        assert len(copies) == (1 if case == 'baseline' else 4)
        if case != 'baseline':
            assert next(r for r in event['rows'] if r['kind'] == 'original_widget')['source_owner_index_before'] == 0xFFFFFFFF
            opens = [r for r in event['rows'] if r['kind'] == 'SDK_open_entry']
            assert len(opens) == 1 and opens[0]['filename'] == '_pxl/kakutei.pxl'
            assert [r['phase'] for r in copies] == list(range(4))
            for row, rect in zip(copies, TILES, strict=True):
                raw = checked({'path': row['RAM'], 'sha256': row['RAM_sha256']})
                assert raw[row['whole_source_header'] - BASE:row['whole_source_header'] - BASE + len(payloads[case])] == payloads[case]
                assert row['source'] + row['size'] == rect and row['destination'] == [192, 64]
                assert struct.unpack_from('<5I', raw, row['whole_source_header'] - BASE) == (16, 72, 32, 20, 20)
        shots[case], memories[case], events[case] = pictures(report), {}, event
        assert set(shots[case]) == set(config['capture_frames'])
        for row in report['read_only_capture_RAM_snapshots']:
            raw = checked(row)
            assert len(raw) == 0x400000
            if row['frame'] in memories[case]:
                assert memories[case][row['frame']] == raw
            memories[case][row['frame']] = raw
        assert set(memories[case]) == set(config['capture_frames'])
        assert all(word(memories[case][6480], a) == v for a, v in original_fields.items())
        state = report['read_only_capture_native_states'][0]
        assert state['frame'] == 6080 and state['read_only_export'] and not state['state_loaded']
        assert state['serialized_RAM_matches_same_frame_direct_export'] and state['main_RAM_unchanged_by_export']
        assert sha(Path(state['path']).read_bytes()) == state['sha256']
        regions = {k: checked(v) for k, v in state['regions'].items()}
        # WRAX is the separately serialized extra-RAM region. The unchanged
        # exporter checks WRAM against its same-frame direct main-RAM read before
        # emitting these guards; it does not export WRAM again under WRAX.
        assert len(regions['WRAX']) == state['MMU_serialized_field_extents']['WRAM'] == 0x400000
        native[case] = regions
        reports.append({'case': case, 'report': str(rp), 'sha256': sha(rp.read_bytes()),
            'receipt': str(ep), 'receipt_sha256': sha(ep.read_bytes()),
            'native_state': state['path'], 'native_state_sha256': state['sha256']})
    io = native['source']['9REG']
    assert all(native['source'][k] == native['opaque_CONTROL'][k] for k in ('9REG', 'VMEM', 'OAMS'))
    assert struct.unpack_from('<I', io, 0x1000)[0] == 0x11813
    assert struct.unpack_from('<H', io, 0x100E)[0] == 0x4084 and io[0x242] == 0x84
    assert struct.unpack_from('<4h2I', io, 0x1030) == (256, 0, 0, 256, 0, 0)
    assert struct.unpack_from('<3H', io, 0x1050) == (0, 0, 0)
    assert struct.unpack_from('<H', io, 0x106C)[0] == 0
    backdrop = struct.unpack_from('<H', native['source']['VMEM'], 0x400)[0]
    assert backdrop == 0
    assert all(struct.unpack_from('<3H', native['source']['OAMS'], 0x400 + i * 8) == (192, 0, 192) for i in range(128))
    vram_a, vram_b = [native[c]['LCDM'] for c in ('source', 'opaque_CONTROL')]
    differing = {i for i, (a, b) in enumerate(zip(vram_a, vram_b, strict=True)) if a != b}
    expected_offsets = {0x40000 + ((64 + y) * 256 + 192 + x) * 2 + 1 for y in range(28) for x in range(48)}
    assert differing == expected_offsets and all(vram_a[i] ^ vram_b[i] == 128 for i in differing)
    cpp = SOURCE / 'GPU.cpp'
    cpp_text = cpp.read_text(encoding='utf-8')
    assert 'outIndex = ((outColor & 0x8000) == 0) ? 0 : 1;' in cpp_text
    coverage = bytearray(2304)
    rebuilt = Image.new('RGB', (72, 32))
    lower_states = []
    for phase, (rect, frame) in enumerate(zip(TILES, CASES['source']['sample_frames'], strict=True)):
        sx, sy, width, height = rect
        for case in ('source', 'opaque_CONTROL'):
            image, base = shots[case][frame], shots['baseline'][frame]
            expected = [native5(p) for p in base.crop((0, 0, 256, 192)).get_flattened_data()]
            for y in range(76, 92):
                for x in range(84, 100):
                    expected[y * 256 + x] = native5(person.palette[person.indices[y * person.width + x]])
            raw = memories[case][frame]
            for y in range(height):
                for x in range(width):
                    at = (sy + y) * 72 + sx + x
                    source_word = source_words[at] | (32768 if case == 'opaque_CONTROL' else 0)
                    software = struct.unpack_from('<H', raw, FB - BASE + ((64 + y) * 256 + 192 + x) * 2)[0]
                    assert software == source_word
                    expected[(64 + y) * 256 + 192 + x] = native5(bgr555(source_word if source_word & 32768 else backdrop))
                    if frame == 6080:
                        actual_vram = struct.unpack_from('<H', native[case]['LCDM'], 0x40000 + ((64 + y) * 256 + 192 + x) * 2)[0]
                        assert actual_vram == source_word
                    if case == 'opaque_CONTROL':
                        coverage[at] += 1
                        rebuilt.putpixel((sx + x, sy + y), image.getpixel((192 + x, 64 + y)))
            assert [native5(p) for p in image.crop((0, 0, 256, 192)).get_flattened_data()] == expected
            lower = image.crop((0, 192, 256, 384)).tobytes()
            match = [k for k, p in native_lower.items() if p == lower]
            assert len(match) == 1
            lower_states.append({'case': case, 'phase': phase, 'whole_native_lower_state': match[0]})
            tile_rows.append({'case': case, 'phase': phase, 'frame': frame, 'source_XYWH': rect,
                'all_raw_source_words_in_software_bitmap_exact': True,
                'full49152_upper_pixels_match_source_word_alpha_and_captured_backdrop': True})
        assert shots['source'][frame].crop((0, 192, 256, 384)).tobytes() == shots['opaque_CONTROL'][frame].crop((0, 192, 256, 384)).tobytes()
    assert coverage == bytes([1]) * 2304
    assert [native5(p) for p in rebuilt.get_flattened_data()] == [native5(bgr555(w)) for w in source_words]
    for case in ('source', 'opaque_CONTROL'):
        assert all(shots[case][f].tobytes() == shots['baseline'][f].tobytes() for f in CASES[case]['capture_frames'] if f <= 5900)
        assert all(shots[case][f].tobytes() == shots['baseline'][f].tobytes() for f in (6480, 6600, 6800))
    comparison = Image.new('RGB', (768, 408), '#263238')
    draw = ImageDraw.Draw(comparison)
    for i, case in enumerate(('source', 'opaque_CONTROL', 'baseline')):
        draw.text((i * 256 + 4, 5), case + ' - isolated fixture' if case != 'baseline' else 'normal baseline', fill='white')
        comparison.paste(shots[case][6080], (i * 256, 24))
    sp = ROOT / 'accepted_raw16_source_opacity_control_and_baseline.png'
    comparison.save(sp)
    caption_sheet = Image.new('RGB', (864, 224), '#263238')
    original = Image.new('RGB', (72, 32))
    original.putdata([bgr555(w)[:3] for w in source_words])
    cd = ImageDraw.Draw(caption_sheet)
    cd.text((5, 6), 'Original RGB crop | assembled actual OPAQUE CONTROL tiles (NOT production fix)', fill='white')
    caption_sheet.paste(original.resize((432, 192), Image.Resampling.NEAREST), (0, 32))
    caption_sheet.paste(rebuilt.resize((432, 192), Image.Resampling.NEAREST), (432, 32))
    cp = ROOT / 'caption_RGB_and_actual_opaque_CONTROL_tile_composite.png'
    caption_sheet.save(cp)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'three_terminal6800_frame_cold_boots': reports,
        'both_raw16_source_and_control_accepted_loaded_whole_not_rejected_as_indexed8': True,
        'source_crop2304_RGB_words_all_high_bits_clear_CONTROL_only_ORs_bit15': True,
        'eight_complete_actual_tiles_software_words_and_upper_pixel_models': tile_rows,
        'all2304_CONTROL_display_pixels_reconstruct_original_caption_RGB_exactly_once': True,
        'source_all_tiles_show_captured_black_backdrop_while_same_RGB_CONTROL_is_visible': True,
        'matching_IO_palette_OAM_no_target_sprites_identity_BG3_direct_bitmap_bankC_bound': True,
        'all671744_LCDM_bytes_match_except_exact1344_first_tile_bit15_bytes': True,
        'native_GPU_CPP_rot_BMP_map_bit15_gate': {'path': str(cpp), 'sha256': sha(cpp.read_bytes())},
        'unchanged_native_exporter_source_sha256': sha(Path('scripts/inspect_desmume_state_v249.py').read_bytes()),
        'initial_WRAX_extra_RAM_misidentification_rejected_not_main_RAM_difference': True,
        'complete_native_lower_states': lower_states, 'whole_native_lower_reference': lower_ref,
        'all30_pre_fixture_and6_restored_whole_RGB_pairs_match_normal_baseline': True,
        'all4_source_CONTROL_lower_screen_pairs_exact': True,
        'source_archive_caption_original_brown_marks_production_ROM_and_release_stack_unchanged': True,
        'supplied_raw16_descriptor_and_viewport_not_original_comic_parent_or_opacity_contract': True,
        'NO_production_alpha_correction_or_all_comics_clearance_inferred': True,
        'all18_plaques_incomplete_full_goal_active_no_guide_promotion': True,
        'review_sheets': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in (sp, cp)],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V703 accepted raw16 source/control:exact software words and bit15 VRAM difference; source backdrop versus complete2304-pixel visible RGB control bound. No production alpha fix inferred.', flush=True)


if __name__ == '__main__':
    main()
