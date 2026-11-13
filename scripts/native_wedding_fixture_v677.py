"""Opt-in Lil chapter-loader argument fixture; no ROM or source-script edits."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/wedding_playback_v677')
PC, WORD = 0x02024134, 0xE92D4070
ARM_SHA = 'b92df335942af8db216b149f54c0eac75626ddde2cf573b6f41c20f3e217bda8'


def plan(arm, cpu, raw, *, already=False, enabled=True):
    if sha(arm) != ARM_SHA or len(cpu) != 128 or len(raw) != 0x400000:
        raise ValueError('Exact V666 ARM9, CPU prefix and 4 MiB RAM required')
    words = struct.unpack('<32I', cpu)
    if words[2] != PC or words[1] != WORD:
        raise ValueError('Original CS loader entry/word required')
    if not enabled or already or words[5] != 22:
        return cpu, {'applied': False, 'reason': 'disabled, previously applied or another requested chapter'}
    if struct.unpack_from('<I', raw, 0x022796B0 - 0x02000000)[0] != 2:
        raise ValueError('Lil active captain2 required')
    obj = words[4]
    if not 0x02000000 <= obj <= 0x02400000 - 0x2420:
        raise ValueError('Original CS loader object escapes main RAM')
    expected_reader = struct.unpack_from('<2I', arm, 0x24228)
    assert expected_reader == (0x02134578, 0xFFF)
    if struct.unpack_from('<2I', raw, obj - 0x02000000) != expected_reader:
        raise ValueError('Original constructed empty CS reader required')
    after = bytearray(cpu)
    struct.pack_into('<I', after, 20, 70)
    return bytes(after), {'applied': True, 'incoming_block': 22, 'requested_block': 70,
        'active_captain': 2, 'loader_object': obj, 'changed_CPU_field': 'ARM9 R1 only',
        'changed_CPU_byte_offsets': [i for i, (a, b) in enumerate(zip(cpu, after, strict=True)) if a != b],
        'synthetic_story_fixture_not_earned_wedding_or_route_completion': True}


def assemble(cpu, header, callback, original, address):
    instructions = ['pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9',
        'push r10', 'push r11', 'push rsi', 'push rdi', f'mov r10,{cpu}', f'mov r11,{header}',
        'cmp dword ptr [r11+4],1', 'jne done', f'cmp dword ptr [r10+8],{PC}', 'jne done',
        f'cmp dword ptr [r10+4],{WORD}', 'jne mismatch', 'cmp ecx,dword ptr [r10+4]',
        'jne mismatch', 'mov ecx,dword ptr [r11]', 'sub rsp,40', f'mov rax,{callback}',
        'call rax', 'add rsp,40', f'mov r11,{header}', 'inc dword ptr [r11+8]', 'jmp done',
        'mismatch:', 'inc dword ptr [r11+12]', 'done:',
        'pop rdi', 'pop rsi', 'pop r11', 'pop r10', 'pop r9', 'pop r8', 'pop rdx',
        'pop rcx', 'pop rax', 'popfq']
    assembly = ';'.join(instructions)
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


class Fixture:
    def __init__(self, core, folder, rom_path, *, enabled=True):
        self.image, self.native, self.core = ImageReader(core), NativeMemory(), core
        self.folder, self.enabled = Path(folder), enabled
        self.folder.mkdir(parents=True, exist_ok=True)
        self.arm = NdsImage.open(rom_path).read_file('/__arm9__.bin')
        assert sha(self.arm) == ARM_SHA and self.arm[PC - 0x02000000:PC - 0x02000000 + 4] == struct.pack('<I', WORD)
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.rows, self.errors, self.applied, self.closed = [], [], False, False
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        from scripts.inspect_resource_dispatch_v668 import tables
        _, table = tables(CORE.read_bytes())
        self.slot = core._handle + table['RVA'] + 0x927 * 8
        self.original = self.image.qword(self.slot)

        def callback(frame):
            before = None
            try:
                assert len(self.rows) < 128
                before, raw = ct.string_at(self.cpu, 128), ct.string_at(self.wram, 0x400000)
                after, receipt = plan(self.arm, before, raw, already=self.applied, enabled=self.enabled)
                folder = self.folder / f'entry_{len(self.rows):03d}_frame_{frame:06d}'
                folder.mkdir()
                files = {}
                for name, data in (('CPU_before.bin', before), ('RAM_before.bin', raw), ('CPU_expected_after.bin', after)):
                    path = folder / name
                    path.write_bytes(data)
                    files[name] = {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}
                if receipt['applied']:
                    ct.memmove(self.cpu + 20, after[20:24], 4)
                assert ct.string_at(self.cpu, 128) == after and ct.string_at(self.wram, 0x400000) == raw
                self.applied |= receipt['applied']
                self.rows.append({'frame': frame, 'receipt': receipt, 'files': files,
                    'actual_CPU_after_exact_and_full_WRAM_unchanged_at_fixture': True})
                print('V677 isolated chapter loader:', frame, receipt, flush=True)
            except BaseException as exc:  # noqa: BLE001 - restore before returning across a native callback.
                if before is not None:
                    ct.memmove(self.cpu, before, 128)
                self.errors.append(repr(exc))
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        self.address = self.native.alloc(None, 4096, 0x3000, 0x04)
        self.code, self.assembly = assemble(self.cpu, ct.addressof(self.header),
            ct.cast(self.callback, ct.c_void_p).value, self.original, self.address)
        assert len(self.code) < 4096
        ct.memmove(self.address, self.code, len(self.code))
        old = ct.c_uint32()
        assert self.native.protect(self.address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, self.address, len(self.code))

    def install(self):
        assert self.image.qword(self.slot) == self.original
        self.native.pointer(self.slot, self.address)

    def next_frame(self):
        self.header[0] += 1

    def close(self):
        if not self.closed:
            self.native.pointer(self.slot, self.original)
            self.closed = True
        assert self.image.qword(self.slot) == self.original and sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'fixture.json', {'rows': self.rows, 'errors': self.errors,
            'applied': self.applied, 'enabled': self.enabled, 'callbacks': self.header[2],
            'mismatches': self.header[3], 'slot_restored_before_filter_free': True,
            'assembly': self.assembly, 'code_hex': self.code.hex(),
            'CPU_and_WRAM_source_anchors': self.image.entries,
            'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        assert self.native.free(self.address, 0, 0x8000)
        assert not self.errors and not self.header[3]
