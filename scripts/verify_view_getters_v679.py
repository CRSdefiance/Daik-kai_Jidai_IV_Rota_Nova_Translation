"""Bind actual cached views/relative headers, full native returns and paired UI."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.prepare_view_getters_v679 import PC, ROM, ROOT
from scripts.probe_button_prompt_native import STACK, STOP, call, machine
from scripts.run_village_visits_v664 import CAP
from scripts.verify_resource_dispatch_v668 import validate_caller
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_filter_controls.json')
    assert len(controls['cases']) == 16
    assert controls['observer_sha256'] == sha(Path('scripts/observe_view_getters_v679.py').read_bytes())
    reports, shots, refs = {}, {}, []
    for mode in ('observed', 'baseline', 'observed_cached_headers'):
        folder = CAP / ('view_getters_v679_' + mode)
        path = folder / 'capture_report.json'
        r = read(path)
        assert r['frames'] == config['frames'] == 7900 and r['cold_boot']
        assert not r['savestate_loaded'] and not r['callback_errors'] and not r.get('battery_save_preloaded')
        assert not any(k.startswith('synthetic_') and v for k, v in r.items())
        assert r['ROM_sha256'] == pre['candidate_sha256'] and r['core_DLL_sha256'] == CORE_SHA
        assert r['scripted_input_schedule'] == read(config['inputs'])
        c = read(folder / 'run_contract.json')
        producer = Path('scripts/run_view_getters_v679.py') if mode.endswith('headers') else ROOT / 'initial_runner.py'
        assert c['runner_sha256'] == sha(producer.read_bytes())
        frames = {}
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            im = Image.open(row['path']).convert('RGB')
            if row['frame'] in frames:
                assert im.tobytes() == frames[row['frame']].tobytes()
            frames[row['frame']] = im
        reports[mode], shots[mode] = r, frames
        refs.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    assert all(s.keys() == shots['baseline'].keys() for s in shots.values())
    assert all(s[f].tobytes() == im.tobytes() for s in shots.values() for f, im in shots['baseline'].items())
    assert len({sha((CAP / ('view_getters_v679_' + tag) / 'final_arm9_ram.bin').read_bytes())
                for tag in reports}) == 1
    metadata, streams = [], []
    for tag, source in (('observed', ROOT / 'initial_observer_without_cached_headers.py'),
                         ('observed_cached_headers', Path('scripts/observe_view_getters_v679.py'))):
        m = read(CAP / ('view_getters_v679_' + tag) / 'observer/observer.json')
        assert m['observer_sha256'] == sha(source.read_bytes())
        assert m['host_only_opcode_slot_restored_and_core_file_exact'] and not m['overflow'] and not m['mismatch']
        assert m['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
        blob = Path(m['path']).read_bytes()
        assert sha(blob) == m['sha256'] and len(blob) == m['records'] * 192
        metadata.append(m)
        streams.append(list(struct.iter_unpack('<48I', blob)))
    assert len(streams[0]) == len(streams[1]) == 50656
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xD4170:0xD41A4] == original[0xD4170:0xD41A4]
    assert arm[0x125A20:0x125A40] == original[0x125A20:0x125A40]
    names, cached, callers, footprint, header_counts, view_cases = Counter(), Counter(), {}, Counter(), Counter(), {}
    for before, row in zip(*streams, strict=True):
        assert before[:32] == row[:32] and before[37:] == row[37:]
        assert row[1] == PC and row[2] == row[11] == struct.unpack_from('<I', arm, 0xD4170)[0]
        assert row[9] == PC + 8 and not row[10] & 32 and row[38] == 0
        assert row[25] in (4, 5) and row[37] == 0
        callers[row[8]] = validate_caller(arm, row[8], PC)
        assert arm[row[8] - 0x02000000 - 4:row[8] - 0x02000000] == original[row[8] - 0x02000000 - 4:row[8] - 0x02000000]
        if row[25] == 4:
            assert before == row and row[32] == 0x02160538
            filename = struct.pack('<8I', *row[40:48]).split(b'\0')[0].decode('ascii')
            assert filename and len(filename) < 32
            names[(row[23], row[35], filename)] += 1
            assert filename not in ('_pxl/__frame.pxl', '_pxl/kakutei.pxl')
        else:
            assert before[32:37] == (0,) * 5
            header = row[24]
            words = row[32:37]
            assert words[0] == 4
            palette, pixels = (header + words[3]) & 0xFFFFFFFF, (header + words[4]) & 0xFFFFFFFF
            assert palette == 0x02125A20
            cached[(header, *words, palette, pixels)] += 1
            header_counts[(words[0], words[1], words[2])] += 1
            view_cases.setdefault(tuple(row[20:32]), row)
        footprint[(row[25], *row[27:32])] += 1
    assert sum(names.values()) == 18211 and sum(cached.values()) == 32445 and len(cached) == 10
    assert len(view_cases) == 35 and len(callers) == 10
    native_cases = []
    for version, code in (('current', arm), ('clean', original)):
        u = machine(code)
        for view, row in view_cases.items():
            # Exact observed view fields/pointer are supplied to an isolated full getter.
            pointer, expected = row[3], row[24]
            payload = struct.pack('<12I', *view)
            u.mem_write(pointer, payload)
            writes = []

            def observe(cpu, access, address, size, value, unused, writes=writes):
                writes.append((address, size, value))

            hook = u.hook_add(UC_HOOK_MEM_WRITE, observe)
            try:
                executed = call(u, PC - 0x02000000, (pointer,))
            finally:
                u.hook_del(hook)
            assert u.reg_read(UC_ARM_REG_R0) == expected and bytes(u.mem_read(pointer, 48)) == payload
            assert writes == [(STACK - 4, 4, STOP)]
            assert 0x020D6558 not in executed
            native_cases.append({'version': version, 'original_observed_view_pointer': pointer,
                'observed_fields': list(view), 'original_native_return': expected,
                'complete_getter_return_ABI_no_owner_lookup_and_only_LR_stack_write': True})
    # These owner/source rectangles remain selected inputs, not finished individual paints.
    marker = next(k for k in names if k[2] == '_pxl/__marker.pxl')
    frames = sorted(shots['baseline'])
    selected = [f for f in (3000, 4400, 5000, 5400, 5700, 6100, 6500, 7900) if f in frames]
    canvas = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(canvas)
    for i, frame in enumerate(selected):
        x, y = i % 4 * 256, i // 4 * 410
        draw.text((x + 3, y + 4), f'V678 ordinary editor {frame}', fill='white')
        canvas.paste(shots['observed_cached_headers'][frame], (x, y + 24))
    sheet = ROOT / 'actual_editor_review.png'
    canvas.save(sheet)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'reports': refs, 'three_terminal7900_frame_cold_boots_no_save_or_gameplay_fixture': True,
        'whole_two_screen_pairs_per_observer_version': len(frames),
        'both_observer_versions_all_baseline_frames_and_full_terminal_RAM_exact': True,
        'all50656_original_entry_arguments_views_owner_names_and_flags_repeat_exact': True,
        'source_owner_getter_calls': sum(names.values()), 'cached_direct_getter_calls': sum(cached.values()),
        'actual_owner_filename_bindings': [{'owner': o, 'filename_pointer': p, 'filename': n, 'entries': count}
            for (o, p, n), count in sorted(names.items())],
        'all10_cached_header_palette_pixel_pointer_relationships': [
            {'header': k[0], 'complete_header_words': list(k[1:6]), 'palette_pointer': k[6], 'pixel_pointer': k[7], 'entries': n}
            for k, n in sorted(cached.items())],
        'all_cached_palettes_are_actual_original_text_palette02125A20': True,
        'relocated_headers_are_not_complete_loose_file_images_no_false_full_file_binding': True,
        '70_full_original_native_cached_getter_replays': native_cases,
        'ten_actual_original_direct_caller_bindings': list(callers.values()),
        'selected_type_source_geometry_palette_fields': [{'type': k[0], 'fields': list(k[1:]), 'entries': n} for k, n in sorted(footprint.items())],
        'marker_owner_actual_entries': names[marker],
        'no_Frame_or_Confirm_owner_filename_in_this_schedule': True,
        'cached_pixel_content_origin_rendering_and_six_control_parents_still_open': True,
        'no_global_nonuse_or_new_complete_graphics_display_claim': True,
        'review_sheet': str(sheet), 'review_sheet_sha256': sha(sheet.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'all18_plaques_incomplete22_historical_requirements_retained': True,
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print(f'V679:50656 repeated view entries,10 relocated text-palette headers,70 full native returns and{len(frames)} paired screens per observer verified.', flush=True)


if __name__ == '__main__':
    main()
