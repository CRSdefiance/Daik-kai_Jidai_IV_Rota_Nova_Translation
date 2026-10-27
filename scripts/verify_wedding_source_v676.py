"""Verify Lil's original wedding-movie command and an ordinary live-path control."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_graphics_file_open_v301 import generated
from scripts.research_wedding_command_v676 import ROOT, selector, walk
from scripts.run_village_visits_v664 import CAP
from scripts.verify_graphic_paints_v669 import caller
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    current, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arms = [image.read_file('/__arm9__.bin') for image in (current, clean)]
    ranges = ((0x293B8, 0x2A600), (0x28A28, 0x28A64), (0x24124, 0x24230),
              (0x23FFC, 0x24124), (0xD2B1C, 0xD2BB0))
    code = []
    for lo, hi in ranges:
        assert arms[0][lo:hi] == arms[1][lo:hi]
        code.append({'address': BASE + lo, 'bytes': hi - lo, 'sha256': sha(arms[0][lo:hi])})
    extents, saved_cases = read(ROOT / 'native_extent_research.json'), read(ROOT / 'chapter_selector_cases.json')
    loader = read(ROOT / 'native_block_loader.json')
    assert loader['script_sha256'] == sha(Path('scripts/load_wedding_block_v676.py').read_bytes())
    filenames, block22_walks = {}, {}
    for tag, image, arm in zip(('current', 'clean'), (current, clean), arms, strict=True):
        b70 = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[70]
        result = walk(arm, b70)
        assert extents[tag] == {'source_sha256': sha(b70), **result}
        assert result['error'] is None and result['stopped_offset'] == result['logical_end'] == 6762
        assert len(result['rows']) == 207
        assert result['native_movie_requests'] == [{'source_offset': 4324, 'args': [26, 0, 1, 0]}]
        assert next(row for row in result['rows'] if row['offset'] == 4324)['word'] == 0x4906
        assert saved_cases[tag] == selector(arm) and len(saved_cases[tag]) == 256
        assert loader['cases'][tag]['block_sha256'] == sha(b70)
        assert loader['cases'][tag]['whole_original_block_bytes'] == len(b70) == 6764
        assert loader['cases'][tag]['full_constructor_and_block_loader_return_ABI_and_guards_exact']
        ops = loader['cases'][tag]['native_file_operations']
        assert ops[0]['operation'] == 'open' and ops[0]['requested'] == '/DATA/SC2.DK4'
        assert ops[-1]['operation'] == 'close'
        assert all(op['path'] == '/data/SC2.DK4' for op in ops)
        filenames[tag] = [generated(image, arm, index) for index in (22, 26)]
        block22 = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
        block22_walks[tag] = walk(arm, block22)
        assert block22_walks[tag]['error'] is None
        assert block22_walks[tag]['native_movie_requests'] == [{'source_offset': 18, 'args': [22, 0, 1, 0]}]
    assert saved_cases['current'] == saved_cases['clean']
    assert [(r['offset'], r['native_extent'], r['word']) for r in extents['current']['rows']] == [
        (r['offset'], r['native_extent'], r['word']) for r in extents['clean']['rows']]
    source = read(ROOT / 'source_contract.json')
    assert {t['instruction_index'] for t in source['targets']} == {0x921, 0x927, 0x92F}
    assert {t['handler_RVA'] for t in source['targets']} == {0x513F0}
    host_cases = []
    for target in source['targets'][3:]:
        folder = ROOT / ('controls_' + target['name'])
        controlled = read(folder / 'source_contract.json')
        assert controlled['targets'] == source['targets'][:3] + [target]
        cases = read(folder / 'native_host_controls.json')['cases']
        assert len(cases) == 13 and all(c['host_registers_flags_stack_original_return_and_entire_source_RAM_exact'] for c in cases)
        host_cases.append({'PC': target['PC'], 'cases': cases})
    config = read(ROOT / 'runtime_contract.json')
    assert config['script_sha256'] == sha(Path('scripts/prepare_wedding_runtime_v676.py').read_bytes())
    assert config['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert config['inputs_sha256'] == sha((ROOT / 'ordinary_inputs.json').read_bytes())
    reports, shots, receipts = {}, {}, []
    for tag in ('observed', 'baseline'):
        folder = CAP / ('wedding_source_v676_' + tag)
        rp, report = folder / 'capture_report.json', read(folder / 'capture_report.json')
        assert report['frames'] == 4000 and report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert not report['callback_errors'] and not report.get('battery_save_preloaded')
        assert not any(key.startswith('synthetic_') for key in report)
        assert report['scripted_input_schedule'] == read(ROOT / 'ordinary_inputs.json')
        contract = read(folder / 'run_contract.json')
        assert contract['runner_sha256'] == sha(Path('scripts/run_wedding_runtime_v676.py').read_bytes())
        assert contract['observer_sha256'] == sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes())
        assert contract['source_contract_sha256'] == config['source_contract_sha256']
        frames = {}
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            pixels = Image.open(shot['path']).convert('RGB').tobytes()
            if shot['frame'] in frames:
                assert frames[shot['frame']] == pixels
            frames[shot['frame']] = pixels
        assert set(frames) == {1, 60, 180, *config['capture_frames']}
        reports[tag], shots[tag] = report, frames
        receipts.append({'tag': tag, 'path': str(rp), 'sha256': sha(rp.read_bytes())})
    assert shots['observed'] == shots['baseline'] and len(shots['observed']) == 12
    assert (CAP / 'wedding_source_v676_observed/final_arm9_ram.bin').read_bytes() == (
        CAP / 'wedding_source_v676_baseline/final_arm9_ram.bin').read_bytes()
    op = CAP / 'wedding_source_v676_observed/observer/paint_observer.json'
    observer = read(op)
    assert observer['script_sha256'] == sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes())
    assert observer['private_wrapper_sha256'] == sha(Path('scripts/observe_wedding_runtime_v676.py').read_bytes())
    assert observer['original_slot_restored_and_DLL_file_unchanged'] and not observer['overflow'] and not observer['mismatch']
    assert observer['all_three_original_slot_pointers_restored_before_filter_free']
    assert [s['index'] for s in observer['additional_host_slots']] == [0x921, 0x927]
    assert observer['source_contract_sha256'] == config['source_contract_sha256']
    raw_entries = Path(observer['path']).read_bytes()
    assert sha(raw_entries) == observer['sha256'] and len(raw_entries) == 160 * observer['records']
    events, primitive_count = [], 0
    targets = {t['PC']: t for t in source['targets']}
    for row in struct.iter_unpack('<40I', raw_entries):
        assert row[1] in targets and row[2] == row[11] == targets[row[1]]['original_instruction']
        assert row[9] == row[1] + 8 and not row[10] & 32
        if row[1] in (0x02024134, 0x02028A28, 0x020D2B1C):
            events.append({'frame': row[0], 'PC': row[1], 'args': list(row[3:7]), 'LR': row[8],
                'original_caller': caller(units(current), units(clean), row[8], row[1]),
                'inapplicable_blitter_fields_guard_flags': row[38], 'first12_fields_only_interpreted': True})
        else:
            assert row[38] == 0
            primitive_count += 1
    assert [(e['frame'], e['PC']) for e in events] == [
        (16, 0x020D2B1C), (559, 0x020D2B1C), (2222, 0x02024134),
        (2224, 0x02028A28), (2224, 0x020D2B1C)]
    assert [e['args'] for e in events if e['PC'] == 0x020D2B1C] == [[0, 0, 0, 0], [28, 1, 0, 0], [22, 0, 1, 0]]
    loader_event, select_event = events[2:4]
    assert loader_event['args'][1] == 22 and select_event['args'][:2] == [0x02276F88, 2]
    actual_object = loader_event['args'][0]
    block22 = IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[22]
    assert select_event['args'][3] == actual_object + 8 + 18
    loaded = []
    snapshots = {s['frame']: s for s in reports['observed']['read_only_capture_RAM_snapshots']}
    for frame in (2300, 2400, 2600, 2800):
        state = snapshots[frame]
        raw = Path(state['path']).read_bytes()
        assert sha(raw) == state['sha256']
        start = actual_object + 8 - BASE
        assert raw[start:start + len(block22)] == block22
        assert struct.unpack_from('<H', raw, start + 18)[0] == 0x4902
        u = machine(arms[0])
        u.mem_write(BASE, raw)
        call(u, 0x7F244, ())
        assert u.reg_read(UC_ARM_REG_R0) == 2
        loaded.append({'frame': frame, 'source_block22_bytes': len(block22),
                       'whole_loaded_block_and_actual_command_pointer_exact': True, 'actual_captain': 2})
    movie = current.read_file('/FLS/M26.fls')
    assert movie == clean.read_file('/FLS/M26.fls')
    archive = FlsArchive(movie)
    assert archive.count == 2
    views = []
    for index in range(2):
        assert (archive.texture(index).width, archive.texture(index).height) == (256, 256)
        assert (archive.records[index][0] >> 16, archive.records[index][1] & 65535) == (256, 192)
        old = Path(f'work/analysis/maria_opening_v674/M26_SOURCE_{index}.png')
        assert Image.open(old).convert('RGBA').tobytes() == archive.texture(index).render().tobytes()
        views.append({'texture': index, 'source_preview': str(old), 'sha256': sha(old.read_bytes()),
                      'stored_dimensions': [256, 256], 'original_native_extent': [256, 192],
                      'plain_scene_art_visually_reviewed_no_text_change_indicated': True})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': pre['previous_goal_turn_classification'],
        'original_code_ranges_exact_clean': code,
        'original_Lil_CS2_block70_command': {'offset': 4324, 'word': 0x4906, 'native_movie_args': [26, 0, 1, 0]},
        'all414_original_clean_current_linear_command_extents_and_guards': True,
        'opaque_side_effect_bridges_not_runtime_branch_or_earned_story_reachability': True,
        'all512_original_selector_commands_complete_ABI_and_guards': True,
        'selector_playback_and_scene_reset_are_explicit_bridges_not_execution_claims': True,
        'two_full_original_CS_block70_loaders_exact6764_bytes_with_only_SDK_IO_bridges': loader,
        'native_generated_filenames_before_movie_decoder': filenames,
        'ordinary_actual_runtime_entries': events, 'all12_whole_screen_pairs_and_terminal_RAM_exact': True,
        'all_four_loaded_actual_B22_buffers_and_captain2': loaded,
        'runtime_reports': receipts, 'runtime_observer': str(op), 'runtime_observer_sha256': sha(op.read_bytes()),
        'primitive_entry_count': primitive_count, 'total_records': observer['records'],
        'nonprimitive_guard_flags_explicit': dict(Counter(e['inapplicable_blitter_fields_guard_flags'] for e in events)),
        'three_source_table_indices_share_original_handler_513F0_and_are_restored': True,
        '39_native_host_filter_controls': host_cases,
        'M26_source_sha256': sha(movie), 'M26_original_scene_art': views,
        'M26_Lil_chapter70_source_consumer_identified_actual_wedding_playback_still_open': True,
        'no_M26_Maria_intro_global_nonuse_full_Lil_route_or_gameplay_wedding_completion_claim': True,
        'all18_plaques_incomplete22_original_scopes_retained_ROM_unchanged': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V676 source consumer: Lil B70/4906 -> M26. Native loaders/512 selectors and actual B22/4902 -> M22 control verified; wedding playback remains open.', flush=True)


if __name__ == '__main__':
    main()
