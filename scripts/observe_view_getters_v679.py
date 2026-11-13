"""Read complete original view inputs without assuming each view uses a resource owner."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.prepare_view_getters_v679 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

HEADER, STRIDE = 32, 192


def assemble(cpu, wram, buffer, original, capacity, assets, target, address):
    ins = ['pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9',
        'push r10', 'push r11', 'push rsi', 'push rdi', f'mov r10,{cpu}', f'mov r11,{buffer}',
        'cmp dword ptr [r11+12],1', 'jne done', f"cmp dword ptr [r10+8],{target['PC']}", 'jne done',
        f"cmp dword ptr [r10+4],{target['original_instruction']}", 'jne mismatch',
        'cmp ecx,dword ptr [r10+4]', 'jne mismatch', 'mov r8,qword ptr [r11]', f'cmp r8,{capacity}',
        'jae overflow', f'imul r9,r8,{STRIDE}', f'lea r9,[r9+r11+{HEADER}]',
        'mov eax,dword ptr [r11+8]', 'mov dword ptr [r9],eax']
    for dest, src in ((4, 8), (8, 4), (12, 16), (16, 20), (20, 24), (24, 28),
                      (28, 68), (32, 72), (36, 76), (40, 80)):
        ins += [f'mov eax,dword ptr [r10+{src}]', f'mov dword ptr [r9+{dest}],eax']
    ins += ['mov dword ptr [r9+44],ecx']

    def copy(pointer, output, count, flag, label):
        return [f'mov edx,dword ptr {pointer}', 'sub edx,0x02000000', f'cmp edx,{0x400000 - count * 4}',
            f'ja bad_{label}', f'mov rdi,{wram}', 'add rdi,rdx',
            *[item for i in range(count) for item in
                (f'mov eax,dword ptr [rdi+{i * 4}]', f'mov dword ptr [r9+{output + i * 4}],eax')],
            f'jmp after_{label}', f'bad_{label}:', f'or dword ptr [r9+152],{flag}', f'after_{label}:']

    ins += copy('[r10+68]', 48, 8, 1, 'stack')
    ins += copy('[r10+16]', 80, 12, 2, 'view')
    ins += ['test dword ptr [r9+152],2', 'jnz counted', 'cmp dword ptr [r9+100],4', 'jne cached']
    ins += copy('[r9+92]', 128, 5, 4, 'owner')
    ins += ['test dword ptr [r9+152],4', 'jnz counted']
    ins += copy('[r9+140]', 160, 8, 8, 'filename')
    ins += ['jmp counted', 'cached:']
    ins += copy('[r9+96]', 128, 5, 16, 'cached_header')
    ins += ['test dword ptr [r9+152],16', 'jnz counted']
    for i, (pointer, length) in enumerate(assets):
        binding = (1, 2, 6)[i]
        ins += ['mov edx,dword ptr [r9+96]', 'sub edx,0x02000000', 'cmp edx,0x3fffec',
            'ja unsupported_cached', f'mov rdi,{wram}', 'add rdi,rdx', f'mov rsi,{pointer}',
            'mov ecx,20', 'cld', 'repe cmpsb', f'jne after_asset_{i}',
            'mov edx,dword ptr [r9+96]', 'sub edx,0x02000000', f'cmp edx,{0x400000 - length}',
            f'ja bad_length_{i}', f'mov rdi,{wram}', 'add rdi,rdx', f'mov rsi,{pointer}',
            f'mov ecx,{length // 8}', 'repe cmpsq', f'jne after_asset_{i}',
            f'mov ecx,{length % 8}', 'repe cmpsb', f'jne after_asset_{i}',
            f'mov dword ptr [r9+148],{binding}', 'jmp counted', f'bad_length_{i}:',
            'or dword ptr [r9+152],32', 'jmp counted', f'after_asset_{i}:']
    ins += ['jmp counted', 'unsupported_cached:', 'or dword ptr [r9+152],16',
        'counted:', 'inc r8', 'mov qword ptr [r11],r8', 'jmp done',
        'mismatch:', 'inc dword ptr [r11+20]', 'jmp done', 'overflow:', 'inc dword ptr [r11+16]',
        'done:', 'pop rdi', 'pop rsi', 'pop r11', 'pop r10', 'pop r9', 'pop r8', 'pop rdx',
        'pop rcx', 'pop rax', 'popfq']
    assembly = ';'.join(ins)
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


class Observer:
    def __init__(self, core, folder, capacity=1000000):
        self.core, self.folder, self.capacity = core, Path(folder), capacity
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        assert self.image.anchor('9CPS', 4, 1) == self.cpu + 80
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        target = self.source['target']
        self.slot = core._handle + self.source['interpreter_table']['RVA'] + target['instruction_index'] * 8
        self.original = self.image.qword(self.slot)
        assert self.original == core._handle + target['handler_RVA']
        rom = NdsImage.open(ROM)
        self.assets = [ct.create_string_buffer(rom.read_file(r['path'])) for r in self.source['source_assets']]
        arguments = [(ct.addressof(a), r['bytes']) for a, r in zip(self.assets, self.source['source_assets'], strict=True)]
        self.buffer = ct.create_string_buffer(HEADER + STRIDE * capacity)
        self.address = self.native.alloc(None, 4096, 0x3000, 0x04)
        assert self.address
        self.code, self.assembly = assemble(self.cpu, self.wram, ct.addressof(self.buffer), self.original,
            capacity, arguments, target, self.address)
        assert len(self.code) < 4096
        ct.memmove(self.address, self.code, len(self.code))
        old = ct.c_uint32()
        assert self.native.protect(self.address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, self.address, len(self.code))
        struct.pack_into('<I', self.buffer, 12, 1)
        self.frame, self.closed = 0, False

    def install(self):
        assert self.image.qword(self.slot) == self.original
        self.native.pointer(self.slot, self.address)

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
        self.folder.mkdir(parents=True, exist_ok=True)
        path = self.folder / 'view_entries.bin'
        data = ct.string_at(ct.addressof(self.buffer) + HEADER, count * STRIDE)
        path.write_bytes(data)
        save(self.folder / 'observer.json', {'path': str(path), 'sha256': sha(data), 'records': count,
            'frames': frame, 'record_stride': STRIDE, 'overflow': overflow, 'mismatch': mismatch,
            'CPU_source_anchors': self.image.entries, 'filter_hex': self.code.hex(), 'filter_assembly': self.assembly,
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'host_only_opcode_slot_restored_and_core_file_exact': True,
            'no_emulated_state_or_source_asset_writes': True,
            'resource_owner_kind4_and_cached_header_kind_other_recorded_separately': True,
            'record_words32_through36_are_owner_for_type4_else_actual_cached_header20_bytes': True,
            'full_file_comparison_only_for_cached_direct_headers': True,
            'entry_arguments_not_original_getter_return_or_pixel_completion': True, 'full_goal_complete': False})
        assert self.native.free(self.address, 0, 0x8000)
