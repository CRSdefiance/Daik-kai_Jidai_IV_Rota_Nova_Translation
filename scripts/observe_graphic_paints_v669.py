"""Read original copy arguments and compare whole target assets in host memory.

One private-process interpreter pointer is restored after use. No original game
instruction, register, RAM, VRAM, source asset or input is written by the filter.
"""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_graphic_paints_v669 import ROM, ROOT
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.verify_village_wrap_v608 import read, save

HEADER, STRIDE = 32, 160


def assemble(cpu, wram, buffer, original, capacity, assets, targets, address):
    instructions = ['pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9',
                    'push r10', 'push r11', 'push rsi', 'push rdi',
                    f'mov r10,{cpu}', f'mov r11,{buffer}',
                    'cmp dword ptr [r11+12],1', 'jne done']
    for i, target in enumerate(targets):
        instructions += [f"cmp dword ptr [r10+8],{target['PC']}", f'je selected_{i}']
    instructions += ['jmp done']
    for i, target in enumerate(targets):
        instructions += [f'selected_{i}:', f"cmp dword ptr [r10+4],{target['original_instruction']}",
                         'jne mismatch', 'jmp selected']
    instructions += ['selected:', 'cmp ecx,dword ptr [r10+4]', 'jne mismatch',
        'mov r8,qword ptr [r11]', f'cmp r8,{capacity}', 'jae overflow',
        f'imul r9,r8,{STRIDE}', f'lea r9,[r9+r11+{HEADER}]',
        'mov eax,dword ptr [r11+8]', 'mov dword ptr [r9],eax']
    for target, source in ((4, 8), (8, 4), (12, 16), (16, 20), (20, 24), (24, 28),
                           (28, 68), (32, 72), (36, 76), (40, 80)):
        instructions += [f'mov eax,dword ptr [r10+{source}]', f'mov dword ptr [r9+{target}],eax']
    instructions += ['mov dword ptr [r9+44],ecx']

    def copy(pointer, output, count, flag, label):
        return [f'mov edx,dword ptr {pointer}', 'sub edx,0x02000000',
            f'cmp edx,{0x400000 - count * 4}', f'ja bad_{label}',
            f'mov rdi,{wram}', 'add rdi,rdx',
            *[item for i in range(count) for item in
              (f'mov eax,dword ptr [rdi+{i * 4}]', f'mov dword ptr [r9+{output + i * 4}],eax')],
            f'jmp after_{label}', f'bad_{label}:', f'or dword ptr [r9+152],{flag}', f'after_{label}:']

    instructions += copy('[r10+68]', 48, 8, 2, 'stack')
    instructions += ['cmp dword ptr [r9+4],0x01ffae70', 'je tile_arguments']
    instructions += copy('[r10+28]', 80, 2, 1, 'copy_source')
    instructions += copy('[r9+48]', 96, 2, 8, 'copy_size')
    instructions += ['cmp dword ptr [r9+4],0x01ff8e4c', 'je scaled_destination']
    instructions += copy('[r9+52]', 112, 2, 16, 'corner_destination')
    instructions += ['jmp arguments_done', 'scaled_destination:']
    instructions += copy('[r9+52]', 112, 4, 16, 'scaled_destination')
    instructions += ['jmp arguments_done', 'tile_arguments:']
    instructions += copy('[r10+28]', 80, 4, 1, 'tile_source')
    instructions += copy('[r9+48]', 96, 4, 8, 'tile_destination')
    instructions += ['arguments_done:']
    instructions += copy('[r10+20]', 128, 5, 4, 'source_header')
    instructions += ['test dword ptr [r9+152],4', 'jnz counted']
    for i, (pointer, length) in enumerate(assets):
        binding, wrong = ((1, 3), (2, 4), (6, 7))[i]
        instructions += ['mov edx,dword ptr [r10+20]', 'sub edx,0x02000000',
            f'mov rdi,{wram}', 'add rdi,rdx', f'mov rsi,{pointer}',
            'mov ecx,20', 'cld', 'repe cmpsb', f'jne after_asset_{i}',
            'mov edx,dword ptr [r10+20]', 'sub edx,0x02000000',
            f'cmp edx,{0x400000 - length}', f'ja asset_length_guard_{i}',
            f'mov rdi,{wram}', 'add rdi,rdx', f'mov rsi,{pointer}',
            f'mov ecx,{length // 8}', 'repe cmpsq', f'jne asset_mismatch_{i}',
            f'mov ecx,{length % 8}', 'repe cmpsb', f'jne asset_mismatch_{i}',
            f'mov dword ptr [r9+148],{binding}', 'jmp counted',
            f'asset_mismatch_{i}:', f'mov dword ptr [r9+148],{wrong}', f'jmp after_asset_{i}',
            f'asset_length_guard_{i}:', 'or dword ptr [r9+152],32',
            'mov dword ptr [r9+148],5', 'jmp counted', f'after_asset_{i}:']
    instructions += ['counted:', 'inc r8', 'mov qword ptr [r11],r8', 'jmp done',
        'mismatch:', 'inc dword ptr [r11+20]', 'jmp done',
        'overflow:', 'inc dword ptr [r11+16]',
        'done:', 'pop rdi', 'pop rsi', 'pop r11', 'pop r10', 'pop r9', 'pop r8',
        'pop rdx', 'pop rcx', 'pop rax', 'popfq']
    assembly = ';'.join(instructions)
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


def controls():
    """Original ROM bytes are inputs to isolated host-only scratch tests."""
    native, rom = NativeMemory(), NdsImage.open(ROM)
    source = read(ROOT / 'source_contract.json')
    assets = [ct.create_string_buffer(rom.read_file(r['path'])) for r in source['source_assets']]
    asset_args = [(ct.addressof(a), r['bytes']) for a, r in zip(assets, source['source_assets'], strict=True)]
    cpu, wram = ct.create_string_buffer(128), ct.create_string_buffer(0x400000)
    buffer, result = ct.create_string_buffer(HEADER + STRIDE * 2), ct.create_string_buffer(144)
    leaf_assembly = ';'.join([  # noqa: FLY002 - separate native instructions
        'mov qword ptr [r12],rax', 'mov qword ptr [r12+8],rcx', 'mov qword ptr [r12+16],rdx',
        'mov qword ptr [r12+24],r8', 'mov qword ptr [r12+32],r9', 'mov qword ptr [r12+40],r10',
        'mov qword ptr [r12+48],r11', 'mov qword ptr [r12+56],rsi', 'mov qword ptr [r12+64],rdi',
        'mov qword ptr [r12+72],rsp', 'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(leaf_assembly)[0]))
    code_address = native.alloc(None, 4096, 0x3000, 0x04)
    assert code_address
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(wram), ct.addressof(buffer), leaf,
                              2, asset_args, source['targets'], code_address)
    assert len(code) < 4096
    ct.memmove(code_address, code, len(code))
    old = ct.c_uint32()
    assert native.protect(code_address, 4096, 0x20, ct.byref(old))
    assert native.flush(native.process, code_address, len(code))
    driver_assembly = ';'.join([
        'push r12', 'push rsi', 'push rdi', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+88],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899', 'mov r9,0x33445566778899aa',
        'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'mov rsi,0x66778899aabbccdd', 'mov rdi,0x778899aabbccddee',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+96],rax',
        f'mov rcx,{ct.addressof(cpu)}', 'mov ecx,dword ptr [rcx+4]',
        f'mov rax,{code_address}', 'call rax', 'mov dword ptr [r12+104],eax', 'mov qword ptr [r12+112],rsp',
        'add rsp,32', 'pop rdi', 'pop rsi', 'pop r12', 'ret'])
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_assembly)[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    rows = []
    try:
        for name, target_index, asset_index, enabled, count, mutate, invalid in (
            ('Frame_corner', 1, 0, 1, 0, False, False), ('Frame_tiled', 2, 0, 1, 0, False, False),
            ('Frame_scaled', 0, 0, 1, 0, False, False), ('Confirm_corner', 1, 1, 1, 0, False, False),
            ('Marker_corner_shared_header', 1, 2, 1, 0, False, False),
            ('Frame_last_byte_differs', 1, 0, 1, 0, True, False),
            ('Confirm_last_byte_differs', 1, 1, 1, 0, True, False),
            ('Marker_last_byte_differs', 1, 2, 1, 0, True, False),
            ('disabled_retains_original', 1, 0, 0, 0, False, False),
            ('overflow_retains_original', 1, 0, 1, 2, False, False),
            ('unsupported_source_pointer_retains_original', 1, 0, 1, 0, False, True),
            ('wrong_PC_retains_original', 1, 0, 1, 0, False, False),
            ('wrong_instruction_retains_original', 1, 0, 1, 0, False, False),
        ):
            target = source['targets'][target_index]
            ct.memset(ct.addressof(wram), 0, ct.sizeof(wram))
            blob = rom.read_file(source['source_assets'][asset_index]['path'])
            ct.memmove(ct.addressof(wram) + 0x4000, blob, len(blob))
            if mutate:
                ct.c_ubyte.from_address(ct.addressof(wram) + 0x4000 + len(blob) - 1).value ^= 1
            struct.pack_into('<4I', wram, 0x1000, 208, 32, 48, 8)
            struct.pack_into('<8I', wram, 0x2000, 0x02002100, 0x02002200, 3, 4, 5, 6, 7, 8)
            struct.pack_into('<4I', wram, 0x2100, *([10, 20, 58, 28] if target_index == 2 else [48, 8, 0, 0]))
            struct.pack_into('<4I', wram, 0x2200, 10, 20, 58, 28)
            values = [0x10000000 + i for i in range(32)]
            values[1], values[2], values[19] = target['original_instruction'], target['PC'], target['PC'] + 8
            if name.startswith('wrong_PC'):
                values[2] += 4
                values[19] += 4
            if name.startswith('wrong_instruction'):
                values[1] ^= 1
            values[4:8] = [0, 0x01000000 if invalid else 0x02004000, 9, 0x02001000]
            values[17] = 0x02002000
            raw = struct.pack('<32I', *values)
            ct.memmove(ct.addressof(cpu), raw, len(raw))
            before_ram = sha(bytes(wram))
            ct.memset(ct.addressof(buffer), 0, ct.sizeof(buffer))
            struct.pack_into('<QII', buffer, 0, count, 321, enabled)
            run(ct.addressof(result))
            registers = struct.unpack_from('<11Q', result)
            assert registers[:9] == (code_address, values[1], 0x1122334455667788, 0x2233445566778899,
                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC,
                0x66778899AABBCCDD, 0x778899AABBCCDDEE)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 88)
            assert registers[9] == before_sp - 8 and registers[10] == before_flags
            assert before_sp == after_sp and returned == values[1]
            assert bytes(cpu)[:128] == raw and sha(bytes(wram)) == before_ram
            actual_count, _, _, overflow, mismatch = struct.unpack_from('<Q4I', buffer)
            matched = enabled == 1 and count < 2 and not name.startswith(('wrong_PC', 'wrong_instruction'))
            assert actual_count == count + int(matched) and mismatch == int(name.startswith('wrong_instruction'))
            assert overflow == int(name.startswith('overflow'))
            binding, flags = struct.unpack_from('<2I', buffer, HEADER + count * STRIDE + 148) if matched else (None, None)
            if matched:
                expected_binding = ((1, 3), (2, 4), (6, 7))[asset_index][int(mutate)]
                if mutate and asset_index == 0:
                    expected_binding = 7  # Shared metadata matches neither complete atlas.
                assert binding == (0 if invalid else expected_binding), (name, binding, expected_binding)
                assert bool(flags & 4) == invalid
                record = struct.unpack_from('<40I', buffer, HEADER + count * STRIDE)
                assert record[:12] == (321, values[2], values[1], *values[4:8], values[17], values[18], values[19], values[20], values[1])
                assert record[20:24] == ((208, 32, 48, 8) if target_index == 2 else (208, 32, 0, 0))
                assert record[24:28] == ((10, 20, 58, 28) if target_index == 2 else (48, 8, 0, 0))
                assert record[28:32] == ((0, 0, 0, 0) if target_index == 2 else
                                         (10, 20, 58, 28) if target_index == 0 else (10, 20, 0, 0))
            rows.append({'case': name, 'binding_ID': binding, 'guard_flags': flags,
                         'host_registers_flags_stack_original_return_and_entire_source_RAM_exact': True})
    finally:
        for address in (leaf, code_address, driver):
            assert native.free(address, 0, 0x8000)
    return {'cases': rows, 'native_filter_hex': code.hex(), 'native_filter_assembly': assembly,
            'whole_expected_files_compared_including_last_byte_controls': True,
            'host_only_scratch_witnesses_not_gameplay': True}


class Observer:
    def __init__(self, core, folder, capacity=2000000):
        self.core, self.folder, self.capacity = core, Path(folder), capacity
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.source, self.frame, self.closed = read(ROOT / 'source_contract.json'), 0, False
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        assert self.image.anchor('9CPS', 4, 1) == self.cpu + 80
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        first = self.source['targets'][0]
        self.slot = core._handle + self.source['interpreter_table']['RVA'] + first['instruction_index'] * 8
        self.original = self.image.qword(self.slot)
        assert all(self.original == core._handle + r['handler_RVA'] for r in self.source['targets'])
        rom = NdsImage.open(ROM)
        self.assets = [ct.create_string_buffer(rom.read_file(r['path'])) for r in self.source['source_assets']]
        arguments = [(ct.addressof(a), r['bytes']) for a, r in zip(self.assets, self.source['source_assets'], strict=True)]
        self.buffer = ct.create_string_buffer(HEADER + STRIDE * capacity)
        self.code_address = self.native.alloc(None, 4096, 0x3000, 0x04)
        assert self.code_address
        self.code, self.assembly = assemble(self.cpu, self.wram, ct.addressof(self.buffer), self.original,
            capacity, arguments, self.source['targets'], self.code_address)
        assert len(self.code) < 4096
        ct.memmove(self.code_address, self.code, len(self.code))
        old = ct.c_uint32()
        assert self.native.protect(self.code_address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, self.code_address, len(self.code))
        struct.pack_into('<I', self.buffer, 12, 1)

    def install(self):
        assert self.image.qword(self.slot) == self.original
        self.native.pointer(self.slot, self.code_address)

    def next_frame(self):
        self.frame += 1
        struct.pack_into('<I', self.buffer, 8, self.frame)

    def close(self):
        if not self.closed:
            self.native.pointer(self.slot, self.original)
            self.closed = True
        assert self.image.qword(self.slot) == self.original and sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        count, frame, enabled, overflow, mismatch = struct.unpack_from('<Q4I', self.buffer)
        assert 0 < count <= self.capacity and enabled == 1 and not overflow and not mismatch
        data = ct.string_at(ct.addressof(self.buffer) + HEADER, count * STRIDE)
        self.folder.mkdir(parents=True, exist_ok=True)
        path = self.folder / 'paint_entries.bin'
        path.write_bytes(data)
        save(self.folder / 'paint_observer.json', {'core_DLL_sha256': CORE_SHA,
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'CPU_source_anchors': self.image.entries, 'host_only_opcode_table_slot': self.slot,
            'original_host_handler': self.original, 'filter_assembly': self.assembly, 'filter_hex': self.code.hex(),
            'record_stride': STRIDE, 'record_fields': ['frame', 'PC', 'instruction', 'r0', 'r1', 'r2', 'r3',
                'sp', 'lr', 'r15', 'CPSR', 'host_arg', *[f'stack_{i}' for i in range(8)],
                *[f'source_descriptor_{i}' for i in range(4)], *[f'stack0_target_{i}' for i in range(4)],
                *[f'stack1_target_{i}' for i in range(4)], *[f'header_{i}' for i in range(5)], 'binding_ID', 'guard_flags', 'reserved'],
            'binding_IDs': {'0': 'other_or_unsupported', '1': 'whole_Frame_file_exact', '2': 'whole_Confirm_file_exact',
                            '3': 'Frame_metadata_matches_whole_file_differs', '4': 'Confirm_metadata_matches_whole_file_differs',
                            '5': 'target_metadata_matches_full_length_guard_failed',
                            '6': 'whole_Marker_file_exact', '7': 'shared_Frame_Marker_metadata_neither_complete_file_matches'},
            'records': count, 'last_frame': frame, 'overflow': overflow, 'mismatch': mismatch,
            'path': str(path), 'sha256': sha(data), 'original_slot_restored_and_DLL_file_unchanged': True,
            'all_target_bindings_compare_complete_source_file_bytes_not_hash_or_prefix_only': True,
            'no_emulated_ROM_RAM_VRAM_CPU_register_or_input_writes': True,
            'every_selected_opcode_still_executes_once_via_original_handler': True,
            'actual_entry_arguments_not_individual_paint_completion_or_final_pixel_proof': True,
            'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        assert self.native.free(self.code_address, 0, 0x8000)


if __name__ == '__main__':
    save(ROOT / 'host_filter_controls.json', controls())
    print('V669 thirteen native host controls pass, including header collision and complete-file last-byte controls.')
