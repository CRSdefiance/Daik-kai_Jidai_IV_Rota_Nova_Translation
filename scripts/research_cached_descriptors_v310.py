"""Native direct-call argument resolution through genuine cached descriptors."""

import json
import struct

from unicorn import UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.research_fls_stream_v310 import ROM, ROOT, SNAPSHOT
from scripts.research_graphics_file_open_v301 import resolve, scan


def main():
    rom = NdsImage.open(ROM)
    arm, ram = rom.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    census = scan(rom, arm, (BASE + 0xD6558,))
    cases = []
    for row in census['aligned_ARM_BL_calls']:
        assert row['unit'] == 'main-0'
        offset = row['address'] - BASE
        candidates = []
        for at in range(offset - 128, offset, 4):
            instruction = struct.unpack_from('<I', arm, at)[0]
            if instruction & 0xFFFFF000 != 0xE59F0000:
                continue
            field = at + 8 + (instruction & 0xFFF)
            descriptor = struct.unpack_from('<I', arm, field)[0]
            if not BASE <= descriptor < BASE + len(ram) - 16:
                continue
            filename = struct.unpack_from('<I', ram, descriptor - BASE + 12)[0]
            if not BASE <= filename < BASE + len(ram):
                continue
            try:
                name = ram[filename - BASE:filename - BASE + 128].split(b'\0')[0].decode('ascii')
            except UnicodeDecodeError:
                continue
            path = resolve(rom, name)
            if path and path.casefold().endswith('.pxl'):
                candidates.append((at, field, descriptor, filename, path))
        assert candidates, row
        start, field, descriptor, filename, path = candidates[-1]
        assert arm[start:offset + 4] == ram[start:offset + 4]
        u = machine(arm)
        u.mem_write(BASE, ram)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        # BD0EC follows an earlier caller vtable read. Its unrelated R1/R5
        # parent metadata is a controlled scratch input, not captured context.
        # The independently checked literal R0 descriptor remains authoritative.
        if row['address'] == BASE + 0xBD0F8:
            u.mem_write(0x02466000, bytes(128))
            u.reg_write(UC_ARM_REG_R1, 0x02466010)
            u.reg_write(UC_ARM_REG_R5, 0x02466040)
        try:
            u.emu_start(BASE + start, row['address'], count=1000)
        except UcError as error:
            raise ValueError(f"Caller {row['address']:08X}, start {BASE + start:08X}, PC {u.reg_read(UC_ARM_REG_PC):08X}: {error}") from error
        assert u.reg_read(UC_ARM_REG_PC) == row['address']
        assert u.reg_read(UC_ARM_REG_R0) == descriptor and u.reg_read(UC_ARM_REG_SP) == STACK
        assert bytes(u.mem_read(descriptor, 20)) == ram[descriptor - BASE:descriptor - BASE + 20]
        cases.append({'native_call_site': row['address'], 'native_argument_segment_start': BASE + start,
                      'source_literal_field': BASE + field, 'actual_captured_descriptor': descriptor,
                      'captured_filename_pointer': filename, 'actual_path': path,
                      'file_sha256': sha(rom.read_file(path)),
                      'unrelated_parent_R1_R5_scratch_input_contract': row['address'] == BASE + 0xBD0F8,
                      'native_argument_and_descriptor_bytes_verified': True,
                      'full_parent_return_cache_read_GPU_or_display_claimed': False})
    assert len(cases) == 21 and len(census['literal_pointers']) == 1 and not census['Thumb_calls']
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'captured_RAM_sha256': sha(ram), 'direct_caller_census': census,
             'native_direct_argument_cases': cases, 'resource_families': sorted({r['actual_path'] for r in cases}),
             'virtual_method_literal_still_requires_context': census['literal_pointers'],
             'negative_direct_path_results_do_not_prove_legacy_archives_globally_unused': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'cached_descriptor_callers.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_direct_argument_cases': len(cases), 'unique_PXL_paths': proof['resource_families'],
                      'virtual_method_literals_remaining': len(census['literal_pointers'])}))


if __name__ == '__main__':
    main()
