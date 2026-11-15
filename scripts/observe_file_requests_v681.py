"""Read actual original file requests; no filesystem or emulated state substitution."""

import ctypes as ct
import struct
from pathlib import Path

from keystone import KS_ARCH_X86, KS_MODE_64, Ks

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.prepare_file_requests_v681 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main_read(raw, address, length):
    if len(raw) != 0x400000 or not 0x02000000 <= address < 0x03000000:
        raise ValueError('Original DS main-RAM/mirror region required')
    at = (address - 0x02000000) & 0x3FFFFF
    if length < 0 or at + length > len(raw):
        raise ValueError('Bounded read crosses the physical mirror edge')
    return raw[at:at + length]


def assemble(cpu, header, callback, original, targets, address):
    ins = ['pushfq', 'push rax', 'push rcx', 'push rdx', 'push r8', 'push r9',
        'push r10', 'push r11', 'push rsi', 'push rdi', f'mov r10,{cpu}', f'mov r11,{header}',
        'cmp dword ptr [r11+4],1', 'jne done']
    for i, target in enumerate(targets):
        ins += [f"cmp dword ptr [r10+8],{target['PC']}", f'je selected_{i}']
    ins += ['jmp done']
    for i, target in enumerate(targets):
        ins += [f'selected_{i}:', f"cmp dword ptr [r10+4],{target['word']}", 'jne mismatch', 'jmp selected']
    ins += ['selected:', 'cmp ecx,dword ptr [r10+4]', 'jne mismatch', 'mov ecx,dword ptr [r11]',
        'sub rsp,40', f'mov rax,{callback}', 'call rax', 'add rsp,40', f'mov r11,{header}',
        'inc dword ptr [r11+8]', 'jmp done', 'mismatch:', 'inc dword ptr [r11+12]', 'done:',
        'pop rdi', 'pop rsi', 'pop r11', 'pop r10', 'pop r9', 'pop r8', 'pop rdx',
        'pop rcx', 'pop rax', 'popfq']
    assembly = ';'.join(ins)
    code = bytes(Ks(KS_ARCH_X86, KS_MODE_64).asm(assembly, address)[0])
    return code + b'\xff\x25\0\0\0\0' + struct.pack('<Q', original), assembly


class Observer:
    def __init__(self, core, folder):
        self.core, self.folder = core, Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.pending, self.slots = [], [], [], []
        self.closed = False
        rom = NdsImage.open(ROM)
        self.blocks = IlnkContainer.parse(rom.read_file('/GRP/SLACKIMG.DK4')).blocks

        def callback(frame):
            try:
                assert len(self.rows) < 20000
                cpu = ct.string_at(self.cpu, 128)
                raw = ct.string_at(self.wram, 0x400000)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert values[1] == target['word']
                row = {'frame': frame, 'PC': values[2], 'CPU128_hex': cpu.hex(),
                    'entire_before_WRAM_sha256': sha(raw), 'args': list(values[4:8]), 'LR': values[18]}
                if target['name'] == 'SDK_open_entry':
                    filename = main_read(raw, values[5], 128)
                    assert b'\0' in filename
                    row.update(filename=filename.split(b'\0')[0].decode('ascii'),
                        filename_pointer=values[5], filename128_hex=filename.hex(),
                        original_file_object=values[4], file_object64_hex=main_read(raw, values[4], 64).hex())
                elif target['name'] == 'raw_SLACK_entry':
                    block, dest, offset, length = values[4:8]
                    assert 0 <= block < len(self.blocks)
                    length = length or len(self.blocks[block])
                    assert offset + length <= len(self.blocks[block])
                    self.pending.append({'block': block, 'destination': dest, 'offset': offset, 'length': length,
                                         'entry_index': len(self.rows)})
                    row['original_raw_read'] = dict(self.pending[-1])
                else:
                    assert self.pending
                    request = self.pending.pop()
                    actual = main_read(raw, request['destination'], request['length'])
                    expected = self.blocks[request['block']][request['offset']:request['offset'] + request['length']]
                    assert actual == expected
                    path = self.folder / f"raw_return_{len(self.rows):04d}_block{request['block']:02d}.bin"
                    path.write_bytes(actual)
                    row.update(original_raw_read=dict(request), complete_actual_loaded_payload=str(path),
                               actual_loaded_payload_sha256=sha(actual), complete_source_bytes_exact=True)
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observation'] = True
                self.rows.append(row)
            except BaseException as exc:  # noqa: BLE001 - never throw across a native callback.
                self.errors.append(repr(exc))
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        for index in sorted({t['instruction_index'] for t in self.source['targets']}):
            targets = [t for t in self.source['targets'] if t['instruction_index'] == index]
            slot = core._handle + self.source['interpreter_table']['RVA'] + index * 8
            original = self.image.qword(slot)
            assert all(original == core._handle + t['handler_RVA'] for t in targets)
            address = self.native.alloc(None, 4096, 0x3000, 0x04)
            code, assembly = assemble(self.cpu, ct.addressof(self.header),
                ct.cast(self.callback, ct.c_void_p).value, original, targets, address)
            assert len(code) < 4096
            ct.memmove(address, code, len(code))
            old = ct.c_uint32()
            assert self.native.protect(address, 4096, 0x20, ct.byref(old))
            assert self.native.flush(self.native.process, address, len(code))
            self.slots.append({'slot': slot, 'original': original, 'address': address,
                'code_hex': code.hex(), 'assembly': assembly, 'instruction_index': index})

    def install(self):
        for item in self.slots:
            assert self.image.qword(item['slot']) == item['original']
            self.native.pointer(item['slot'], item['address'])

    def next_frame(self):
        self.header[0] += 1

    def close(self):
        if not self.closed:
            for item in self.slots:
                self.native.pointer(item['slot'], item['original'])
            self.closed = True
        assert all(self.image.qword(item['slot']) == item['original'] for item in self.slots)
        assert sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'requests.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'unreturned_raw_requests': self.pending,
            'all_three_opcode_slots_restored_before_free_and_core_file_exact': True,
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'host_filters': self.slots, 'CPU_and_WRAM_anchors': self.image.entries,
            'actual_entry_requests_not_all_SDK_interfaces_or_open_return_values': True,
            'full_goal_complete': False})
        for item in self.slots:
            assert self.native.free(item['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and not self.pending
