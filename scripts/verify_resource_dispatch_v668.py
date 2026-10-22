"""Verify original caller entries, indirect return slots and unchanged captures."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_resource_dispatch_v668 import ROM, ROOT
from scripts.probe_button_prompt_native import STACK, STOP, call
from scripts.run_village_visits_v664 import CAP
from scripts.trace_resource_owner_tables_v585 import initialize
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_village_wrap_v608 import read, save


def validate_caller(arm, lr, target, values=None):
    assert lr % 4 == 0 and 0x02000004 <= lr <= 0x02170000
    word = struct.unpack_from('<I', arm, lr - 0x02000000 - 4)[0]
    if word & 0x0F000000 == 0x0B000000:
        displacement = word & 0xFFFFFF
        displacement -= 0x1000000 if displacement & 0x800000 else 0
        actual = lr + 4 + displacement * 4
        assert actual == target, (hex(lr), hex(actual), hex(target))
        return {'return_address': lr, 'instruction': word, 'kind': 'original_ARM_BL', 'target': target}
    assert word & 0x0FFFFFF0 == 0x012FFF30, (hex(lr), hex(word))
    register = word & 15
    row = {'return_address': lr, 'instruction': word, 'kind': 'original_ARM_BLX_register', 'register': register}
    if values is not None:
        assert register < 4 and values[register] == target
        row['actual_recorded_register_target'] = target
    else:
        row['caller_register_value_not_observed_at_parent_entry'] = True
    return row


def unwind_controls(rom):
    rows = []
    for owner, kind in ((0x02313F60, 4), (0x023139C0, 4), (0x02313F60, 0)):
        u, arm, _, _, _, _ = initialize(rom)
        clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
        assert arm[0xD4170:0xD41A4] == clean[0xD4170:0xD41A4]
        head = struct.unpack('<I', u.mem_read(0x020D6600, 4))[0]
        u.mem_write(head, struct.pack('<2I', head, head))
        u.mem_write(owner + 16, struct.pack('<I', 7))
        header, view = 0x02440000, 0x02460020
        u.mem_write(header, rom.read_file('/_pxl/__frame.pxl'))
        data = struct.pack('<6I', 0, 0, 0, owner, header, kind)
        u.mem_write(view, data)
        entries, lookups = [], []

        def observe(cpu, address, size, unused, entries=entries, lookups=lookups, header=header):
            if address == 0x020D6558:
                sp = cpu.reg_read(UC_ARM_REG_SP)
                entries.append({'entry_sp': sp, 'LR': cpu.reg_read(UC_ARM_REG_LR),
                    'owner': cpu.reg_read(UC_ARM_REG_R0),
                    'parent_saved_return_word_at_SP_plus4': struct.unpack('<I', cpu.mem_read(sp + 4, 4))[0]})
            if address == 0x020D68F0:
                lookups.append(address)
                cpu.reg_write(UC_ARM_REG_R0, header)
                cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, observe)
        try:
            executed = call(u, 0xD4170, (view,))
        finally:
            u.hook_del(hook)
        assert u.reg_read(UC_ARM_REG_R0) == header and u.reg_read(UC_ARM_REG_SP) == STACK
        assert bytes(u.mem_read(view, len(data))) == data
        if kind == 4:
            assert entries == [{'entry_sp': STACK - 8, 'LR': 0x020D419C, 'owner': owner,
                                'parent_saved_return_word_at_SP_plus4': STOP}]
            assert len(lookups) == 1 and 0x020D6558 in executed
        else:
            assert not entries and not lookups
        rows.append({'owner': owner, 'view_type': kind, 'entries': entries,
            'original_full_view_getter_executed': True, 'only_cached_header_lookup_bridged': True,
            'stack_return_slot_and_restored_SP_verified': True, 'not_actual_gameplay': True})
    return rows


def intersects(rect):
    x, y, width, height = rect
    return [name for name, (left, top, right, bottom) in CELLS
            if x < right and y < bottom and x + width > left and y + height > top]


def source_rectangle_controls(rom, actual_rectangles):
    """Original parents prepare these source fields before resource lookup.

    The final pixel call is captured rather than rendered. These witnesses
    validate the actual trace's field interpretation, not new gameplay pixels.
    """
    results = []
    samples = [(tuple(rect), False) for rect in actual_rectangles]
    samples += [((208, 32, 48, 8), True), ((184, 48, 24, 8), True)]
    for rect, positive in samples:
        for parent, expected_lr in ((0xCFD6C, 0x020CFDC0), (0xCFE64, 0x020CFFA0)):
            u, arm, _, _, _, _ = initialize(rom)
            original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
            assert arm[0xCFD6C:0xD0000] == original[0xCFD6C:0xD0000]
            header, view, point, owner = 0x02440000, 0x02460020, 0x02460100, 0x02313F60
            head = struct.unpack('<I', u.mem_read(0x020D6600, 4))[0]
            u.mem_write(head, struct.pack('<2I', head, head))
            u.mem_write(owner + 16, struct.pack('<I', 7))
            u.mem_write(header, rom.read_file('/_pxl/__frame.pxl'))
            data = bytearray(48)
            struct.pack_into('<I', data, 12, owner)
            struct.pack_into('<I', data, 20, 4)
            struct.pack_into('<2I', data, 28, *rect[:2])
            struct.pack_into('<2I', data, 40, *rect[2:])
            u.mem_write(view, bytes(data))
            u.mem_write(point, struct.pack('<4I', 0, 0, *rect[2:]))
            u.mem_write(STACK, bytes(4))
            at_getter, at_copy = [], []

            def capture(cpu, address, size, unused, at_getter=at_getter, at_copy=at_copy,
                        header=header, expected_lr=expected_lr):
                sp = cpu.reg_read(UC_ARM_REG_SP)
                if address == 0x020D6558:
                    assert cpu.reg_read(UC_ARM_REG_LR) == 0x020D419C
                    assert struct.unpack('<I', cpu.mem_read(sp + 4, 4))[0] == expected_lr
                    at_getter.append(struct.unpack('<4I', cpu.mem_read(sp + 16, 16)))
                elif address == 0x020D68F0:
                    cpu.reg_write(UC_ARM_REG_R0, header)
                    cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
                elif address == 0x01FF92D8:
                    assert cpu.reg_read(UC_ARM_REG_R1) == header
                    xy = struct.unpack('<2I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_R3), 8))
                    size_pointer = struct.unpack('<I', cpu.mem_read(sp, 4))[0]
                    at_copy.append(xy + struct.unpack('<2I', cpu.mem_read(size_pointer, 8)))
                    cpu.reg_write(UC_ARM_REG_R0, 0)
                    cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
            hook = u.hook_add(UC_HOOK_CODE, capture)
            try:
                call(u, parent, (0, view, 0, point))
            finally:
                u.hook_del(hook)
            assert at_getter == at_copy == [rect]
            assert bool(intersects(rect)) == positive
            assert bytes(u.mem_read(view, len(data))) == bytes(data)
            results.append({'original_parent': 0x02000000 + parent, 'source_XYWH': rect,
                'observed_getter_stack_words4_to7_equal_original_final_copy_arguments': True,
                'intersecting_caption_cells': intersects(rect), 'synthetic_positive_control': positive,
                'cached_file_lookup_and_final_pixel_call_bridged_no_gameplay_credit': True})
    return results


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(ROM)
    _, arm, _, _, owners, names = initialize(rom)
    controls = read(ROOT / 'host_filter_controls.json')
    assert len(controls['cases']) == 7 and all(r['host_register_flags_stack_return_and_source_bytes_exact'] for r in controls['cases'])
    cases, captures = [], {}
    for tag in ('observed', 'baseline', 'observed_stack'):
        folder = CAP / ('resource_dispatch_v668_newgame_' + tag)
        rp = folder / 'capture_report.json'
        r = read(rp)
        assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == 24100
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert not any(v for k, v in r.items() if k.startswith('synthetic_'))
        shots = {}
        for shot in r['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            shots[shot['frame']] = shot
        assert len(shots) == 89
        captures[tag] = shots
        cases.append({'tag': tag, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
            'frames': r['frames'], 'capture_records': len(r['frames_captured'])})
    for tag in ('observed', 'observed_stack'):
        assert captures[tag].keys() == captures['baseline'].keys()
        for frame, shot in captures[tag].items():
            assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(captures['baseline'][frame]['path']).convert('RGB').tobytes()
    first_folder = CAP / 'resource_dispatch_v668_newgame_observed/observer'
    second_folder = CAP / 'resource_dispatch_v668_newgame_observed_stack/observer'
    first_meta, second_meta = read(first_folder / 'resource_observer.json'), read(second_folder / 'resource_observer.json')
    assert first_meta['script_sha256'] == sha((ROOT / 'executed_observer_before_lint.py').read_bytes())
    assert second_meta['script_sha256'] == sha(Path('scripts/observe_resource_dispatch_v668.py').read_bytes())
    first_blob, second_blob = Path(first_meta['path']).read_bytes(), Path(second_meta['path']).read_bytes()
    assert sha(first_blob) == first_meta['sha256'] and sha(second_blob) == second_meta['sha256']
    first = list(struct.iter_unpack('<12I', first_blob))
    second = list(struct.iter_unpack('<20I', second_blob))
    assert len(first) == first_meta['records'] == len(second) == second_meta['records']
    assert first == [row[:12] for row in second]
    assert all(m['original_table_entry_restored_and_DLL_file_unchanged'] and not m['overflow'] and not m['mismatch']
               for m in (first_meta, second_meta))
    all_callers, indirect, frame_indirect = {}, [], []
    for row in second:
        frame, pc, instruction, owner, r1, r2, r3, sp, lr, r15, cpsr, host_arg, *stack = row
        assert 1 <= frame <= 24100 and pc == 0x020D6558 and instruction == host_arg == 0xE92D4070
        assert r15 == pc + 8 and not cpsr & 32 and 0x02000000 <= sp <= 0x023FFFE0
        assert owner in owners
        witness = validate_caller(arm, lr, 0x020D6558, (owner, r1, r2, r3))
        all_callers[lr] = witness
        if lr == 0x020D419C:
            parent = stack[1]
            parent_witness = validate_caller(arm, parent, 0x020D4170)
            indirect.append((owner, parent, frame))
            if owner == 0x02313F60:
                frame_indirect.append((parent, frame))
                all_callers.setdefault('frame_indirect_parents', {})[parent] = parent_witness
    assert frame_indirect
    counts = Counter(row[3] for row in second)
    parent_counts = Counter(parent for owner, parent, frame in indirect if owner == 0x02313F60)
    rectangles = Counter(tuple(row[16:20]) for row in second if row[3] == 0x02313F60 and row[8] == 0x020D419C)
    assert sum(rectangles.values()) == len(frame_indirect) and len(rectangles) == 6
    assert all(not intersects(rect) for rect in rectangles)
    rectangle_controls = source_rectangle_controls(rom, rectangles)
    source_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[lr - 0x02000000 - 4:lr - 0x02000000] == source_arm[lr - 0x02000000 - 4:lr - 0x02000000]
               for lr in all_callers if isinstance(lr, int))
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'reports': cases, 'seven_native_host_controls': controls['cases'], 'native_view_unwind_controls': unwind_controls(rom),
        'all178_observer_baseline_whole_two_screen_pairs_match': True,
        'all_resource_records_identical_before_and_after_stack_extension': True,
        'resource_request_records': len(second), 'distinct_original_initialized_owners': len(counts),
        'owner_counts': [{'owner': owner, 'filename': names[owner], 'requests': n} for owner, n in counts.most_common()],
        'all_resource_entries_original_PC_instruction_ARG_R15_ARM_state_owner_and_direct_or_virtual_callers_verified': True,
        'direct_and_virtual_caller_source_bindings': all_callers,
        'all_Frame_requests': counts[0x02313F60], 'actual_Frame_virtual_getter_requests': len(frame_indirect),
        'actual_Frame_parent_return_counts': [{'return_address': parent, 'requests': count}
            for parent, count in sorted(parent_counts.items())],
        'all11444_actual_uncached_view_source_rectangles': [{'source_XYWH': rect, 'requests': count,
            'intersecting_five_caption_cells': intersects(rect)} for rect, count in sorted(rectangles.items())],
        'native_source_rectangle_controls': rectangle_controls,
        'all_six_actual_source_rectangles_exclude_five_miniature_cells': True,
        'Confirm_requests_in_this_actual_run': counts[0x023139C0],
        'no_Confirm_request_in_one_schedule_is_not_global_nonuse_or_six_parent_completion': True,
        'remaining_Frame_requests_cached_direct_views_other_schedules_and_actual_six_control_parents_open': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V668 actual original requests/callers/parent return slots and178 whole-screen baseline pairs pass.', flush=True)


if __name__ == '__main__':
    main()
