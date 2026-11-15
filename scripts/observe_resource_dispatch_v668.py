"""Trace original resource getter entries through one host interpreter table slot.

Only the calling diagnostic process's opcode function pointer is temporarily
replaced. The native filter restores host registers/flags and tail-jumps to the
unchanged original handler exactly once. It never writes emulated game state.
"""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import ROOT
from scripts.verify_village_wrap_v608 import read, save

STRIDE, HEADER = 80, 32


def assemble(cpu, wram, buffer, original, capacity, address):
    copy = []
    for target, source in ((4, 8), (8, 4), (12, 16), (16, 20), (20, 24), (24, 28),
                           (28, 68), (32, 72), (36, 76), (40, 80)):
        copy += [f'mov eax,dword ptr [r10+{source}]', f'mov dword ptr [r9+{target}],eax']
    assembly = ';'.join([
        'pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9', 'push r10', 'push r11',
        f'mov r10,{cpu}', f'mov r11,{buffer}',
        'cmp dword ptr [r11+12],1', 'jne done',
        'cmp dword ptr [r10+8],0x020d6558', 'jne done',
        'cmp dword ptr [r10+4],0xe92d4070', 'jne mismatch',
        'cmp ecx,dword ptr [r10+4]', 'jne mismatch',
        'mov r8,qword ptr [r11]', f'cmp r8,{capacity}', 'jae overflow',
        f'imul r9,r8,{STRIDE}', f'lea r9,[r9+r11+{HEADER}]',
        'mov eax,dword ptr [r11+8]', 'mov dword ptr [r9],eax',
        *copy, 'mov dword ptr [r9+44],ecx',
        'mov edx,dword ptr [r10+68]', 'sub edx,0x02000000', 'cmp edx,0x3fffe0', 'ja invalid_stack',
        f'mov r10,{wram}', 'add rdx,r10',
        *[item for i in range(8) for item in
          (f'mov eax,dword ptr [rdx+{i * 4}]', f'mov dword ptr [r9+{48 + i * 4}],eax')],
        'jmp counted', 'invalid_stack:', 'inc dword ptr [r11+24]',
        'counted:',
        'inc r8', 'mov qword ptr [r11],r8', 'jmp done',
        'mismatch:', 'inc dword ptr [r11+20]', 'jmp done',
        'overflow:', 'inc dword ptr [r11+16]',
        'done:', 'pop r11', 'pop r10', 'pop r9', 'pop r8', 'pop rdx', 'pop rcx', 'pop rax', 'popfq'])
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


class NativeMemory:
    def __init__(self):
        kernel = ct.windll.kernel32
        self.alloc = kernel.VirtualAlloc
        self.alloc.argtypes, self.alloc.restype = [ct.c_void_p, ct.c_size_t, ct.c_uint32, ct.c_uint32], ct.c_void_p
        self.free = kernel.VirtualFree
        self.free.argtypes, self.free.restype = [ct.c_void_p, ct.c_size_t, ct.c_uint32], ct.c_bool
        self.protect = kernel.VirtualProtect
        self.protect.argtypes = [ct.c_void_p, ct.c_size_t, ct.c_uint32, ct.POINTER(ct.c_uint32)]
        self.protect.restype = ct.c_bool
        self.flush = kernel.FlushInstructionCache
        self.flush.argtypes, self.flush.restype = [ct.c_void_p, ct.c_void_p, ct.c_size_t], ct.c_bool
        kernel.GetCurrentProcess.restype = ct.c_void_p
        self.process = kernel.GetCurrentProcess()

    def executable(self, data):
        address = self.alloc(None, 4096, 0x3000, 0x04)
        assert address and len(data) < 4096
        ct.memmove(address, data, len(data))
        old = ct.c_uint32()
        assert self.protect(address, 4096, 0x20, ct.byref(old))
        assert self.flush(self.process, address, len(data))
        return address

    def pointer(self, address, value):
        old, restored = ct.c_uint32(), ct.c_uint32()
        assert self.protect(address, 8, 0x04, ct.byref(old))
        try:
            ct.c_uint64.from_address(address).value = value
        finally:
            assert self.protect(address, 8, old.value, ct.byref(restored))
        assert ct.c_uint64.from_address(address).value == value


def controls():
    """Native host-only witnesses; neither a loaded emulator nor game RAM is used."""
    native = NativeMemory()
    cpu = ct.create_string_buffer(128)
    wram = ct.create_string_buffer(struct.pack('<32I', *range(32)))
    buffer = ct.create_string_buffer(HEADER + STRIDE * 2)
    result = ct.create_string_buffer(128)
    # Leaf exposes incoming registers/flags before returning its original u32 arg.
    # r12 belongs to this isolated native driver, not to the observer filter.
    leaf_assembly = ';'.join([  # noqa: FLY002 - keep each assembly instruction separate
        'mov qword ptr [r12],rax', 'mov qword ptr [r12+8],rcx', 'mov qword ptr [r12+16],rdx',
        'mov qword ptr [r12+24],r8', 'mov qword ptr [r12+32],r9', 'mov qword ptr [r12+40],r10',
        'mov qword ptr [r12+48],r11', 'mov qword ptr [r12+56],rsp',
        'pushfq', 'pop rax', 'mov qword ptr [r12+64],rax', 'mov eax,ecx', 'ret'])
    leaf = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(leaf_assembly)[0]))
    filter_address = native.alloc(None, 4096, 0x3000, 0x04)
    assert filter_address
    code, assembly = assemble(ct.addressof(cpu), ct.addressof(wram), ct.addressof(buffer), leaf, 2, filter_address)
    ct.memmove(filter_address, code, len(code))
    old = ct.c_uint32()
    assert native.protect(filter_address, 4096, 0x20, ct.byref(old))
    assert native.flush(native.process, filter_address, len(code))
    driver_assembly = ';'.join([
        'push r12', 'sub rsp,32', 'mov r12,rcx', 'mov qword ptr [r12+72],rsp',
        'mov rdx,0x1122334455667788', 'mov r8,0x2233445566778899',
        'mov r9,0x33445566778899aa', 'mov r10,0x445566778899aabb', 'mov r11,0x5566778899aabbcc',
        'xor eax,eax', 'cmp eax,1', 'pushfq', 'pop rax', 'mov qword ptr [r12+80],rax',
        'mov ecx,0xe92d4070', f'mov rax,{filter_address}', 'call rax',
        'mov dword ptr [r12+88],eax', 'mov qword ptr [r12+96],rsp',
        'add rsp,32', 'pop r12', 'ret'])
    driver = native.executable(bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(driver_assembly)[0]))
    run = ct.WINFUNCTYPE(None, ct.c_void_p)(driver)
    rows = []
    try:
        for name, pc, enabled, count, word in (
            ('exact_positive', 0x020D6558, 1, 0, 0xE92D4070),
            ('second_positive', 0x020D6558, 1, 1, 0xE92D4070),
            ('wrong_PC', 0x020D655C, 1, 0, 0xE92D4070),
            ('disabled', 0x020D6558, 0, 0, 0xE92D4070),
            ('overflow_retains_original', 0x020D6558, 1, 2, 0xE92D4070),
            ('wrong_instruction_retains_original', 0x020D6558, 1, 0, 0xE92D4071),
            ('invalid_main_stack_retains_original', 0x020D6558, 1, 0, 0xE92D4070),
        ):
            values = [0x10000000 + i for i in range(32)]
            values[1], values[2], values[4 + 15] = word, pc, pc + 8
            values[17] = 0x02000040
            if name.startswith('invalid_main_stack'):
                values[17] = 0x01000000
            source = struct.pack('<32I', *values)
            ct.memmove(ct.addressof(cpu), source, len(source))
            ct.memset(ct.addressof(buffer), 0, ct.sizeof(buffer))
            struct.pack_into('<QII', buffer, 0, count, 123, enabled)
            run(ct.addressof(result))
            regs = struct.unpack_from('<9Q', result)
            assert regs[:7] == (filter_address, 0xE92D4070, 0x1122334455667788, 0x2233445566778899,
                                0x33445566778899AA, 0x445566778899AABB, 0x5566778899AABBCC)
            before_sp, before_flags, returned, after_sp = struct.unpack_from('<QQI4xQ', result, 72)
            assert regs[7] == before_sp - 8 and after_sp == before_sp
            assert regs[8] == before_flags and returned == 0xE92D4070
            assert bytes(cpu)[:128] == source
            matched = name in ('exact_positive', 'second_positive', 'invalid_main_stack_retains_original')
            actual_count, _, _, overflow, mismatch = struct.unpack_from('<Q4I', buffer)
            assert actual_count == count + int(matched)
            assert overflow == int(name.startswith('overflow')) and mismatch == int(name.startswith('wrong_instruction'))
            if matched:
                record = struct.unpack_from('<20I', buffer, HEADER + count * STRIDE)
                stack = (0,) * 8 if name.startswith('invalid_main_stack') else tuple(range(16, 24))
                expected = (123, pc, word, *values[4:8], values[17], values[18], values[19], values[20], 0xE92D4070, *stack)
                assert record == expected
            invalid = struct.unpack_from('<I', buffer, 24)[0]
            assert invalid == int(name.startswith('invalid_main_stack'))
            rows.append({'case': name, 'host_register_flags_stack_return_and_source_bytes_exact': True,
                         'expected_record_count': actual_count, 'overflow': overflow, 'mismatch': mismatch,
                         'invalid_stack': invalid})
    finally:
        for address in (leaf, filter_address, driver):
            assert native.free(address, 0, 0x8000)
    return {'cases': rows, 'native_filter_hex': code.hex(), 'native_filter_assembly': assembly,
            'host_only_scratch_control_not_gameplay': True}


class Observer:
    def __init__(self, core, folder, capacity=2000000):
        self.core, self.folder, self.capacity = core, Path(folder), capacity
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.frame, self.closed = 0, False
        self.source = read(ROOT / 'interpreter_table_source.json')
        regs = self.image.anchor('9REG', 4, 16)
        self.cpu = regs - 16
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        assert self.image.anchor('9INN', 4, 1) == self.cpu + 12
        assert self.image.anchor('9CPS', 4, 1) == self.cpu + 80
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        table = self.source['interpreter_table']
        self.slot = core._handle + table['RVA'] + self.source['source_instruction_index'] * 8
        self.original = self.image.qword(self.slot)
        assert self.original == core._handle + self.source['selected_ARM9_handler_RVA']
        self.buffer = ct.create_string_buffer(HEADER + STRIDE * capacity)
        self.code_address = self.native.alloc(None, 4096, 0x3000, 0x04)
        assert self.code_address
        self.code, self.assembly = assemble(self.cpu, self.wram, ct.addressof(self.buffer), self.original, capacity, self.code_address)
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
        if self.closed:
            return
        self.native.pointer(self.slot, self.original)
        self.closed = True
        assert self.image.qword(self.slot) == self.original and sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        count, frame, enabled, overflow, mismatch = struct.unpack_from('<Q4I', self.buffer)
        assert 0 < count <= self.capacity and enabled == 1 and not overflow and not mismatch
        assert struct.unpack_from('<I', self.buffer, 24)[0] == 0
        data = bytes(self.buffer)[HEADER:HEADER + count * STRIDE]
        self.folder.mkdir(parents=True, exist_ok=True)
        path = self.folder / 'resource_entries.bin'
        path.write_bytes(data)
        save(self.folder / 'resource_observer.json', {'core_DLL_sha256': CORE_SHA,
            'source_table_proof_sha256': sha((ROOT / 'interpreter_table_source.json').read_bytes()),
            'CPU_source_anchors': self.image.entries, 'host_only_opcode_table_slot': self.slot,
            'original_host_handler': self.original, 'source_instruction_index': self.source['source_instruction_index'],
            'filter_assembly': self.assembly, 'filter_hex': self.code.hex(),
            'record_fields': ['frame', 'PC', 'instruction', 'r0', 'r1', 'r2', 'r3', 'sp', 'lr', 'r15', 'CPSR', 'host_arg',
                              *[f'stack_word_{i}' for i in range(8)]],
            'eight_read_only_stack_words_bounded_to_main_RAM': True,
            'records': int(count), 'last_frame': frame, 'capacity': self.capacity,
            'overflow': overflow, 'mismatch': mismatch, 'path': str(path), 'sha256': sha(data),
            'original_table_entry_restored_and_DLL_file_unchanged': True,
            'no_emulated_ROM_RAM_VRAM_CPU_register_or_input_writes': True,
            'original_selected_handler_runs_once_via_tail_jump_with_preserved_host_state': True,
            'unmodified_core_baseline_and_original_caller_validation_required': True,
            'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        assert self.native.free(self.code_address, 0, 0x8000)


if __name__ == '__main__':
    save(ROOT / 'host_filter_controls.json', controls())
    print('V668 seven independent native host filter controls pass; no emulator loaded.')
