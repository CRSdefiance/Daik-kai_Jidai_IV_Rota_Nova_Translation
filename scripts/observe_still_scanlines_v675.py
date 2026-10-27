# V675 private extension: capture both bank D/main and bank C/sub bitmap rows.
"""Isolated host RenderLine observer. Game ROM/RAM/VRAM are never written.

Only the calling diagnostic process's exact-hash core entry prologues are
temporarily detoured. Original prologues run through relocation-free trampolines;
every original RenderLine executes once. File bytes remain unchanged. Baseline
frame comparisons are mandatory before any original-display verification credit.
"""

import ctypes as ct
import struct
from pathlib import Path

from capstone import CS_ARCH_X86, CS_MODE_64, Cs

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, SOURCE, ImageReader
from scripts.verify_village_wrap_v608 import save

ENTRIES = ((0x2BFFF0, 16, '555'), (0x2C0810, 16, '666'), (0x2C11F0, 18, '888'))
PROLOGUES = ('4154555756534883ec504889cb4889d6', '4154555756534883ec504889cb4889d6',
             '41564154555756534883ec484889cb4889d6')
FUNCTION = ct.WINFUNCTYPE(None, ct.c_void_p, ct.c_size_t)


def jump(address):
    return b'\xff\x25\0\0\0\0' + struct.pack('<Q', address)


class Observer:
    def __init__(self, core, folder, frames):
        self.core, self.folder, self.frames = core, Path(folder), set(frames)
        self.image = ImageReader(core)
        self.frame, self.patches, self.rows, self.errors = 0, [], {}, []
        self.closed = False
        self.anchors = {name: self.image.anchor(name, size, count) for name, size, count in (
            ('_VCT', 4, 1), ('LCDM', 1, 0xA4000), ('WRAM', 1, 0x400000),
            ('9REG', 1, 0x2000), ('9INA', 4, 1))}
        # Same tag with a different source SFORMAT type/count identifies CPU GPRs.
        self.cpu_image = ImageReader(core)
        self.cpu_regs = self.cpu_image.anchor('9REG', 4, 16)
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

    def write_code(self, address, data):
        old, restored = ct.c_uint32(), ct.c_uint32()
        assert self.protect(address, len(data), 0x40, ct.byref(old))
        try:
            ct.memmove(address, data, len(data))
            assert self.flush(self.process, address, len(data))
        finally:
            assert self.protect(address, len(data), old.value, ct.byref(restored))
        assert ct.string_at(address, len(data)) == data

    def install(self):
        decoder = Cs(CS_ARCH_X86, CS_MODE_64)
        for (rva, count, label), expected_hex in zip(ENTRIES, PROLOGUES, strict=True):
            address = self.core._handle + rva
            original = self.image.read(address, count)
            assert original.hex() == expected_hex and count >= 14
            instructions = list(decoder.disasm(original, self.image.link_base + rva))
            assert sum(i.size for i in instructions) == count
            assert all(i.mnemonic in ('push', 'sub', 'mov') and 'rip' not in i.op_str for i in instructions)
            trampoline = self.alloc(None, 4096, 0x3000, 0x40)
            assert trampoline
            code = original + jump(address + count)
            ct.memmove(trampoline, code, len(code))
            assert self.flush(self.process, trampoline, len(code))
            original_call = FUNCTION(trampoline)

            def callback(this, line, original_call=original_call, label=label):
                record = None
                try:
                    if self.frame in self.frames:
                        count_now = struct.unpack('<I', self.image.read(self.anchors['_VCT'], 4))[0]
                        assert 0 <= line < 192 and count_now == line
                        key = (self.frame, int(line))
                        assert key not in self.rows
                        record = {'frame': self.frame, 'line': int(line), 'format': label,
                            'GPU_this': int(this), 'VCount': count_now,
                            'ARM9_PC': struct.unpack('<I', self.image.read(self.anchors['9INA'], 4))[0],
                            'CPU_registers': ct.string_at(self.cpu_regs, 64),
                            'IO': ct.string_at(self.anchors['9REG'], 0x2000),
                            'bitmap_row': ct.string_at(self.anchors['LCDM'] + 0x60000 + line * 512, 512),
                            'sub_bitmap_row': ct.string_at(self.anchors['LCDM'] + 0x40000 + line * 512, 512)}
                        self.rows[key] = record
                except BaseException as exc:  # noqa: BLE001 - a host callback must never skip original rendering.
                    self.errors.append({'frame': self.frame, 'line': int(line), 'error': repr(exc)})
                # Observation failures never skip or replace original rendering.
                original_call(this, line)
                if record is not None:
                    record['original_render_called_once_and_returned'] = True
            callback_fn = FUNCTION(callback)
            patch = jump(ct.cast(callback_fn, ct.c_void_p).value) + b'\x90' * (count - 14)
            self.patches.append({'RVA': rva, 'address': address, 'stolen_bytes': count,
                'format': label, 'original_hex': original.hex(), 'detour_hex': patch.hex(),
                'trampoline': trampoline, 'trampoline_hex': code.hex(),
                'callback_keepalive': callback_fn, 'original_call_keepalive': original_call,
                'relocated_prefix_has_no_PC_relative_memory_branch_or_call': True})
            self.write_code(address, patch)

    def close(self):
        if self.closed:
            return
        for patch in self.patches:
            self.write_code(patch['address'], bytes.fromhex(patch['original_hex']))
        self.closed = True
        assert sha(CORE.read_bytes()) == CORE_SHA
        for patch in self.patches:
            assert ct.string_at(patch['address'], patch['stolen_bytes']).hex() == patch['original_hex']

    def save(self):
        assert self.closed and not self.errors
        self.folder.mkdir(parents=True, exist_ok=True)
        frames = {}
        for frame in sorted(self.frames):
            rows = [self.rows[(frame, line)] for line in range(192)]
            assert all(r['original_render_called_once_and_returned'] for r in rows)
            files = {}
            for field, filename in (('bitmap_row', 'bitmap_rows.bin'), ('IO', 'scanline_IO.bin'),
                                    ('CPU_registers', 'scanline_CPU_registers.bin'),
                                    ('sub_bitmap_row', 'sub_bitmap_rows.bin')):
                path = self.folder / f'frame_{frame:06d}_{filename}'
                data = b''.join(r[field] for r in rows)
                path.write_bytes(data)
                files[field] = {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}
            frames[frame] = {'files': files, 'rows': [{k: v for k, v in r.items()
                if k not in ('bitmap_row', 'sub_bitmap_row', 'IO', 'CPU_registers')} for r in rows]}
        patches = [{k: v for k, v in p.items() if not k.endswith('keepalive')} for p in self.patches]
        save(self.folder / 'scanline_observer.json', {'core': str(CORE), 'core_DLL_sha256': CORE_SHA,
            'source_commit': '95b4d798731caa809125b6c3c11d17cc332ff6ef',
            'source_files': {str(SOURCE / name): sha((SOURCE / name).read_bytes())
                             for name in ('GPU.cpp', 'GPU.h', 'NDSSystem.cpp', 'saves.cpp')},
            'SFORMAT_anchors': self.image.entries, 'CPU_register_anchor': self.cpu_image.entries['9REG'],
            'host_core_entry_detours_only_in_diagnostic_process': patches,
            'all_entry_bytes_restored_and_DLL_file_unchanged': True,
            'no_game_ROM_RAM_VRAM_register_or_input_writes': True,
            'every_original_RenderLine_called_once': True, 'errors': self.errors,
            'frames': frames, 'baseline_and_original_source_composition_still_required': True,
            'no_gameplay_or_full_goal_completion_claim_from_observer_alone': True,
            'parent_observer_sha256': sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes()),
            'added_read_only_bankC_rows_for_sub_engine_not_a_different_host_hook': True,
            'script_sha256': sha(Path(__file__).read_bytes())})
        for patch in self.patches:
            assert self.free(patch['trampoline'], 0, 0x8000)
