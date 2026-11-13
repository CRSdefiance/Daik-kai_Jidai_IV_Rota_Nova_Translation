"""Classify the remaining 80008000 lead by complete native decimal output.

No file/graphics bridges or pixels are supplied. Original writer returns with
ABI checks; original transfer wrapper stops BEFORE its DMA/memory-copy boundary.
This is source/record evidence, not original comic playback or a GPU capture.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, call, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/digit_records_v731')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
ARRAY, COUNTER, DMA_MODE = 0x02170774, 0x02170368, 0x02169018
WRITER, TRANSFER, DMA_COPY, CPU_COPY = 0x020F4120, 0x020E1F08, 0x020E27BC, 0x020E2910
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    canonical = Path('out/raphael_natural_v2_accepted_base.nds')
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'), canonical)}
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = (r.read_file('/__arm9__.bin') for r in (current, clean))
    ranges = [(0xF4120, 0xF4264), (0xF64F4, 0xF65EC), (0xE1F08, 0xE1F64), (0xEF8, 0xF08)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    assert struct.unpack_from('<I', arm, 0xF424C)[0] == 0x80008000
    assert struct.unpack_from('<I', arm, 0xF4250)[0] == 10_000_000
    assert struct.unpack_from('<I', arm, 0xF4258)[0] == COUNTER
    assert struct.unpack_from('<I', arm, 0xF4260)[0] == ARRAY
    assert struct.unpack_from('<I', arm, 0xE1F60)[0] == DMA_MODE
    u = machine(arm)
    parts, source_parts = sections(current), sections(clean)
    source_words = {}

    def exact(cpu, address, size, unused):
        actual = bytes(cpu.mem_read(address, size))
        for candidates in (parts, source_parts):
            assert any(data[address - base:address - base + size] == actual
                for _, base, data in candidates if base <= address and address + size <= base + len(data)), hex(address)
        assert source_words.setdefault(address, actual) == actual

    h = u.hook_add(UC_HOOK_CODE, exact)
    cases = []
    try:
        for value in (0, 1, 9, 10, 100, 105, 12345, 99999999):
            for width in (0, 1, 3, 8):
                for priority in (0, 3):
                    for right, y, seed in ((238, 0, 0), (-8, 511, 7)):
                        u.mem_write(ARRAY - 16, b'\xA5' * 672)
                        u.mem_write(COUNTER - 4, b'\xA5' * 10)
                        u.mem_write(COUNTER, struct.pack('<H', seed))
                        u.mem_write(STACK, struct.pack('<I', y))
                        before = bytes(u.mem_read(BASE, 0x400000))
                        executed = call(u, WRITER - BASE, (priority, width, value, right & 0xFFFFFFFF))
                        text = str(value)[-width:] if width else ''
                        expected = bytearray(before)
                        struct.pack_into('<H', expected, COUNTER - BASE, seed + len(text))
                        records = []
                        # Independent decimal-string and documented sprite-field
                        # model; no quotient/remainder or ARM-loop simulation.
                        for n, character in enumerate(text):
                            digit, position = int(character), len(text) - n - 1
                            x = (right - position * 15) & 511
                            attr0 = (y & 255) | 0x8000
                            attr1 = x | 0x8000
                            attr2 = 0xA000 | priority << 10 | (512 + digit * 8)
                            index = 79 - seed - n
                            struct.pack_into('<3H', expected, ARRAY - BASE + index * 8, attr0, attr1, attr2)
                            records.append({'record': index, 'digit': character, 'attributes': [attr0, attr1, attr2]})
                        assert bytes(u.mem_read(BASE, 0x400000)) == bytes(expected)
                        cases.append({'value': value, 'field_width': width, 'priority': priority,
                            'right_X': right, 'Y': y, 'initial_counter': seed, 'visible_decimal': text,
                            'records': records, 'whole4MiB_except_expected_counter_and_records_exact': True,
                            'all_record_padding_and_neighbor_guards_exact': True,
                            'native_return_stack_saved_registers_pass': True,
                            'distinct_executed_instructions': len(executed)})
        transfers = []
        for mode, size, offset in ((0, 640, 0), (0xFFFFFFFF, 640, 0), (0, 32, 0), (0, 640, 1024)):
            u.mem_write(DMA_MODE, struct.pack('<I', mode))
            for register, value in zip(REGS, (ARRAY, offset, size, 0)):
                u.reg_write(register, value)
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            boundary = []

            def stop(cpu, address, instruction_size, unused, boundary=boundary):
                if address in (DMA_COPY, CPU_COPY):
                    boundary.append({'PC': address, 'args': [cpu.reg_read(r) for r in REGS]})
                    cpu.emu_stop()

            handle = u.hook_add(UC_HOOK_CODE, stop)
            try:
                u.emu_start(TRANSFER, STOP, count=10000)
            finally:
                u.hook_del(handle)
            assert len(boundary) == 1
            dma = mode != 0xFFFFFFFF and size > 48
            target = DMA_COPY if dma else CPU_COPY
            args = [mode, ARRAY, 0x07000000 + offset, size] if dma else [ARRAY, 0x07000000 + offset, size, size]
            assert boundary[0]['PC'] == target and boundary[0]['args'] == args
            transfers.append({'mode': mode, 'size': size, 'offset': offset, 'copy_boundary': boundary[0],
                'stopped_before_copy_no_hardware_transfer_or_ABI_credit': True})
    finally:
        u.hook_del(h)
    assert len(cases) == 128 and len(transfers) == 4
    callers = []
    for label, base, data in parts:
        for offset in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, offset)[0]
            if word & 0x0F000000 != 0x0B000000:
                continue
            delta = word & 0xFFFFFF
            delta = delta - 0x1000000 if delta & 0x800000 else delta
            if base + offset + 8 + delta * 4 == WRITER:
                callers.append({'section': label, 'PC': base + offset, 'instruction_hex': data[offset:offset + 4].hex()})
    assert [r['PC'] for r in callers] == [0x020F6530, 0x020F6590, 0x020F65E8]
    save(ROOT / 'native_cases.json', {'decimal_writer': cases, 'transfer_boundaries': transfers,
        'all_executed_source_words': [{'PC': a, 'bytes_hex': source_words[a].hex()} for a in sorted(source_words)]})
    previous = Path('work/analysis/opacity_paths_v704/leads.json')
    leads = read(previous)
    assert any(r['PC'] == WRITER + 12 for r in leads['versions']['current']['candidates']) is False
    # The pending source lead is a PC-relative literal load, recorded in the
    # V704 checkpoint rather than its immediate-instruction candidate list.
    proof = {'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'pending_V704_80008000_load': WRITER + 12,
        'source_exact_ranges': ranges, 'all_executed_words_exact_clean_and_current': True,
        'complete_native_writer_cases': 128, 'whole4MiB_and_record_padding_guards_pass': True,
        'sampled_decimal_values': [0, 1, 9, 10, 100, 105, 12345, 99999999],
        'source_field_widths_tested': [0, 1, 3, 8],
        'native_writer_return_stack_saved_register_ABI_pass': True,
        'original_transfer_copy_boundaries': transfers,
        'all_three_aligned_ARM_BL_candidates': callers,
        'caller_census_excludes_computed_Thumb_tail_branches_and_pointer_tables': True,
        'source_decimal_array': ARRAY, 'source_halfword_counter': COUNTER,
        'packed_mask_is_sprite_shape_size_fields_not_pixel_color_alpha': True,
        'original_function_produces_decimal_tile_attributes_not_raw_image_import': True,
        'prior_opacity_leads': str(previous), 'prior_opacity_leads_sha256': sha(previous.read_bytes()),
        'primary_format_reference': 'https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/sprite.h',
        'cases': str(ROOT / 'native_cases.json'), 'cases_sha256': sha((ROOT / 'native_cases.json').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'GPU_display_original_comic_parent_global_unused_or_other_importer_claim': False,
        'release_hashes_unchanged': release, 'full_goal_complete': False}
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V731:128 complete native decimal-writer cases and4 copy boundaries pass; packed mask is sprite attributes,not comic opacity.')


if __name__ == '__main__':
    main()
