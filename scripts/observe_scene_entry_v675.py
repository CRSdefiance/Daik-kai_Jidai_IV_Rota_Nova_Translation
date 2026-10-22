"""Private host filter snapshots source memory before the upper scene iterator."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_graphic_paints_v669 import ROM, units
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.research_still_reveal_v675 import CONTEXT, ROOT
from scripts.verify_village_wrap_v608 import save

PC, WORD = 0x020D32B8, 0xE5955004
FRAMES = (3700, *range(3750, 3851, 2), 3900, 4000)


def assemble(cpu, header, selection, callback, original, address):
    instructions = ['pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9',
        'push r10', 'push r11', 'push rsi', 'push rdi', f'mov r10,{cpu}', f'mov r11,{header}',
        'cmp dword ptr [r11+4],1', 'jne done', f'cmp dword ptr [r10+8],{PC}', 'jne done',
        f'cmp dword ptr [r10+4],{WORD}', 'jne mismatch', 'cmp ecx,dword ptr [r10+4]',
        'jne mismatch', f'cmp dword ptr [r10+32],{CONTEXT}', 'jne done',
        f'cmp dword ptr [r10+36],{CONTEXT + 12}', 'jne done',
        'mov eax,dword ptr [r11]', 'cmp eax,4000', 'ja done',
        f'mov rdx,{selection}', 'cmp byte ptr [rdx+rax],1', 'jne done',
        'mov ecx,eax', 'sub rsp,40', f'mov rax,{callback}', 'call rax', 'add rsp,40',
        f'mov r11,{header}', 'inc dword ptr [r11+8]', 'jmp done',
        'mismatch:', 'inc dword ptr [r11+12]', 'done:',
        'pop rdi', 'pop rsi', 'pop r11', 'pop r10', 'pop r9', 'pop r8', 'pop rdx',
        'pop rcx', 'pop rax', 'popfq']
    assembly = ';'.join(instructions)
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


class Observer:
    def __init__(self, core, folder):
        self.image, self.native, self.core = ImageReader(core), NativeMemory(), core
        self.folder, self.rows, self.errors, self.closed = Path(folder), [], [], False
        self.folder.mkdir(parents=True, exist_ok=True)
        current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
        for image in (current, clean):
            word = next(d[PC - a:PC - a + 4] for a, d in units(image) if a <= PC < a + len(d))
            assert int.from_bytes(word, 'little') == WORD
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        assert self.image.anchor('9CPS', 4, 1) == self.cpu + 80
        # CPU registers and MMU I/O share the9REG name with different extents.
        # Keep the helper's tag cache separate instead of relaxing its guard.
        self.mmu_image = ImageReader(core)
        self.regions = {tag: (self.mmu_image.anchor(tag, 1, size), size) for tag, size in (
            ('WRAM', 0x400000), ('ITCM', 32768), ('DTCM', 16384), ('9REG', 8192), ('LCDM', 0xA4000))}
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.selection = (ct.c_ubyte * 4001)()
        for frame in FRAMES:
            self.selection[frame] = 1

        def snapshot(frame):
            try:
                assert len(self.rows) < 128
                cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', cpu)
                assert values[1] == WORD and values[2] == PC and values[8] == CONTEXT and values[9] == CONTEXT + 12
                directory = self.folder / f'frame_{frame:06d}_call_{len(self.rows):03d}'
                directory.mkdir()
                files = {}
                for tag, (pointer, size) in self.regions.items():
                    blob = ct.string_at(pointer, size)
                    path = directory / (tag + '.bin')
                    path.write_bytes(blob)
                    assert ct.string_at(pointer, size) == blob
                    files[tag] = {'path': str(path), 'bytes': size, 'sha256': sha(blob)}
                path = directory / 'cpu_prefix128.bin'
                path.write_bytes(cpu)
                assert ct.string_at(self.cpu, 128) == cpu
                self.rows.append({'frame': frame, 'files': files, 'CPU_prefix': str(path),
                    'CPU_prefix_sha256': sha(cpu), 'original_R4_R5_SP_LR': [values[i] for i in (8, 9, 17, 18)],
                    'before_original_iterator_instruction': True,
                    'CPU_and_all_copied_source_regions_unchanged_by_snapshot': True})
                print('V675 before-paint source snapshot', frame, len(self.rows), flush=True)
            except (AssertionError, ValueError, OSError) as exc:
                self.errors.append(repr(exc))
                self.header[1] = 0

        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(snapshot)
        raw = CORE.read_bytes()
        assert sha(raw) == CORE_SHA
        base, table = tables(raw)
        index = ((WORD >> 16) & 0xFF0) | ((WORD >> 4) & 15)
        handler = struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base
        self.slot = core._handle + table['RVA'] + index * 8
        self.original = self.image.qword(self.slot)
        assert self.original == core._handle + handler
        self.code_address = self.native.alloc(None, 4096, 0x3000, 0x04)
        self.code, self.assembly = assemble(self.cpu, ct.addressof(self.header), ct.addressof(self.selection),
            ct.cast(self.callback, ct.c_void_p).value, self.original, self.code_address)
        assert len(self.code) < 4096
        ct.memmove(self.code_address, self.code, len(self.code))
        old = ct.c_uint32()
        assert self.native.protect(self.code_address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, self.code_address, len(self.code))
        self.contract = {'PC': PC, 'word': WORD, 'instruction_index': index, 'handler_RVA': handler,
            'table': table, 'same_private_process_read_only_source_snapshot_not_game_state_write': True}
        self.contract['CPU_source_anchors'] = self.image.entries
        self.contract['MMU_source_anchors'] = self.mmu_image.entries

    def install(self):
        self.native.pointer(self.slot, self.code_address)

    def next_frame(self):
        self.header[0] += 1

    def close(self):
        if not self.closed:
            self.native.pointer(self.slot, self.original)
            self.closed = True
        assert self.image.qword(self.slot) == self.original and sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'observer.json', {'rows': self.rows, 'errors': self.errors,
            'frame': self.header[0], 'callbacks': self.header[2], 'mismatches': self.header[3],
            'contract': self.contract, 'native_filter_assembly': self.assembly,
            'native_filter_hex': self.code.hex(), 'slot_restored_DLL_unchanged': True,
            'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        assert self.native.free(self.code_address, 0, 0x8000)
        assert not self.errors and not self.header[3] and len(self.rows) == self.header[2]


if __name__ == '__main__':
    raise SystemExit(f'Use run_still_reveal_v675; source evidence stays under {ROOT}.')
