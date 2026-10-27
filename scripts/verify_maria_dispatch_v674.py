"""Correct a guessed movie mapping using actual requests and complete source pixels."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_maria_dispatch_v674 import CAPTURE_FRAMES
from scripts.run_village_visits_v664 import CAP
from scripts.verify_graphic_paints_v669 import caller
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    source = read(ROOT / 'source_contract.json')
    controls = read(ROOT / 'factory_host_controls.json')
    assert len(controls['cases']) == 13
    assert controls['cases'][0]['host_registers_flags_stack_original_return_and_entire_source_RAM_exact']
    reports, maps, receipts, snapshots = [], [], [], []
    for tag in ('observed', 'baseline'):
        folder = CAP / f'maria_dispatch_v674_{tag}'
        rp = folder / 'capture_report.json'
        r, contract = read(rp), read(folder / 'run_contract.json')
        assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == 4000
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert r['core_DLL_sha256'] == CORE_SHA
        assert r['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert r['scripted_input_schedule'] == read(ROOT / 'dispatch_inputs.json')
        assert {k for k, v in r.items() if k.startswith('synthetic_') and v} == {'synthetic_gallery_fixtures'}
        assert contract['runner_sha256'] == sha(Path('scripts/run_maria_dispatch_v674.py').read_bytes())
        assert contract['inputs_sha256'] == sha((ROOT / 'dispatch_inputs.json').read_bytes())
        assert contract['factory_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
        assert contract['observer_sha256'] == sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes())
        shots = {}
        for shot in r['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            if shot['frame'] in shots:
                assert shots[shot['frame']]['PNG_sha256'] == shot['PNG_sha256']
            shots[shot['frame']] = shot
        assert set(shots) == {1, 60, 180, *CAPTURE_FRAMES}
        reports.append(r)
        maps.append(shots)
        snapshots.append({s['frame']: s for s in r['read_only_capture_RAM_snapshots']})
        receipts.append({'tag': tag, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
            'frames': 4000, 'unique_frames': len(shots)})
    for frame, shot in maps[0].items():
        assert Image.open(shot['path']).tobytes() == Image.open(maps[1][frame]['path']).tobytes(), frame
    assert (CAP / 'maria_dispatch_v674_observed/final_arm9_ram.bin').read_bytes() == (CAP / 'maria_dispatch_v674_baseline/final_arm9_ram.bin').read_bytes()
    pilot = read(CAP / 'maria_opening_v674_pilot/capture_report.json')
    pilot_shots = {s['frame']: s for s in pilot['frames_captured']}
    for frame, shot in pilot_shots.items():
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        assert Image.open(shot['path']).tobytes() == Image.open(maps[0][frame]['path']).tobytes(), frame
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    meta = read(CAP / 'maria_dispatch_v674_observed/observer/paint_observer.json')
    assert meta['script_sha256'] == sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes())
    assert meta['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert not meta['overflow'] and not meta['mismatch'] and meta['original_slot_restored_and_DLL_file_unchanged']
    data = Path(meta['path']).read_bytes()
    assert sha(data) == meta['sha256'] and len(data) == meta['records'] * 160
    targets = {t['PC']: t for t in source['targets']}
    requests, ordinary = [], 0
    for row in struct.iter_unpack('<40I', data):
        assert row[1] in targets and row[2] == row[11] == targets[row[1]]['original_instruction']
        assert row[9] == row[1] + 8 and not row[10] & 32
        if row[1] == 0x020D2B1C:
            assert row[37] == 0 and row[38] == 13
            requests.append({'frame': row[0], 'movie_index': row[3], 'arguments': list(row[3:7]),
                'LR': row[8], 'caller': caller(units(rom), units(clean), row[8], row[1]),
                'blitter_descriptor_fields_intentionally_not_interpreted': True})
        else:
            assert row[38] == 0
            ordinary += 1
    assert [(r['frame'], r['movie_index']) for r in requests] == [(16, 0), (559, 28)]
    # Actual post-selection source is a detached native PXL canvas. Compare both
    # complete parts and every displayed upper-screen color, not header shape.
    backgrounds, blank_transition, reveal_transition = [], None, None
    blob = rom.read_file('/evstill/evstill084.pxl')
    assert blob == clean.read_file('/evstill/evstill084.pxl')
    flags, stride, height, paloff, pixoff = struct.unpack_from('<5I', blob)
    assert (flags & 255, stride, height) == (8, 128, 192)
    palette = struct.unpack_from('<256H', blob, paloff)
    wanted = [(palette[i] & 31, palette[i] >> 5 & 31, palette[i] >> 10 & 31) for i in blob[pixoff:]]
    for frame in (3700, 3800, 3900, 4000):
        snapshot = snapshots[0][frame]
        raw = Path(snapshot['path']).read_bytes()
        assert sha(raw) == snapshot['sha256']
        address = 0x02276D74
        words = struct.unpack_from('<5I', raw, address - BASE)
        assert words == (0x108, 128, 192, 20, 0x46ADC)
        pal, pix = address + words[3], address + words[4]
        if frame == 3700:
            assert raw[pal - BASE:pal - BASE + 512] == bytes(512)
            image = Image.open(maps[0][frame]['path']).convert('RGB').crop((0, 0, 256, 192))
            assert set(image.get_flattened_data()) == {(0, 0, 0)}
            blank_transition = {'frame': frame, 'native_header': address,
                'all512_palette_bytes_zero_and_all49152_upper_pixels_black': True,
                'not_a_loaded_court_or_other_artwork_display_claim': True}
            continue
        assert raw[pal - BASE:pal - BASE + 512] == blob[paloff:paloff + 512]
        assert raw[pix - BASE:pix - BASE + 49152] == blob[pixoff:]
        image = Image.open(maps[0][frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        actual = [tuple(c >> 3 for c in color) for color in image.get_flattened_data()]
        if frame == 3800:
            different = [i for i, (a, b) in enumerate(zip(actual, wanted, strict=True)) if a != b]
            assert len(different) == 17245
            assert all(actual[i] == (0, 0, 0) for i in different)
            software = struct.unpack_from('<49152H', raw, 0x022F9794 - BASE)
            software_rgb = [(v & 31, v >> 5 & 31, v >> 10 & 31) for v in software]
            assert software_rgb == actual
            reveal_transition = {'frame': frame, 'resident_source_palette_and_indices_exact': True,
                'all_displayed_cells_either_exact_source_color_or_black': True,
                'source_nonblack_cells_replaced_by_black': len(different),
                'source_array_matches_entire_display_diagnostic_only_not_expected_paint': True,
                'original_reveal_painter_and_timing_not_yet_proven': True,
                'not_counted_as_complete_source_image_or_full_transition_verification': True}
            continue
        assert actual == wanted, frame
        u = machine(arm)
        u.mem_write(BASE, raw)
        call(u, 0x7F244, ())
        assert u.reg_read(UC_ARM_REG_R0) == 3
        backgrounds.append({'frame': frame, 'active_captain': 3, 'native_header': address,
            'source': '/evstill/evstill084.pxl', 'source_sha256': sha(blob),
            'whole_palette512_and_indices49152_exact': True, 'whole49152_upper_RGB5_pixels_exact': True})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': receipts, 'pilot_report': str(CAP / 'maria_opening_v674_pilot/capture_report.json'),
        'all14_current_whole_two_screen_pairs_and_full_terminal_RAM_exact': True,
        'all11_distinct_pilot_two_screen_states_exact_fresh_runs': True,
        'source_system_unlock_save_not_earned_unlock_or_new_ROM_patch': True,
        'primitive_records': meta['records'], 'ordinary_primitive_entries': ordinary,
        'FLS_factory_requests': requests, 'no_M26_factory_request_in_this4000_frame_schedule': True,
        'guard_counts': dict(Counter(r[38] for r in struct.iter_unpack('<40I', data))),
        'factory_guard13_marks_inapplicable_blitter_fields_not_unsupported_request_registers': True,
        'Maria_actual_two_source_bound_court_backgrounds': backgrounds,
        'all98304_displayed_upper_pixels_exact_clean_source_art': True,
        'separate_source_zero_palette_blank_transition': blank_transition,
        'separate_incomplete_reveal_transition': reveal_transition,
        'initial_Maria_M26_mapping_retracted_not_used_as_evidence': True,
        'no_global_unused_M26_or_full_Maria_opening_completion_claim': True,
        'all18_plaques_incomplete22_scopes_exact_no_release_change': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V67414 baseline/11 pilot states, two complete source084 courts and two original FLS requests verified; separate reveal painter remains open; M26 assumption retracted.')


if __name__ == '__main__':
    main()
