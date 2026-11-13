"""Read actual non-disk stream objects and payloads during normal Save/Load UI."""

import ctypes as ct
import struct
from collections import Counter
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_file_requests_v681 import assemble, main_read
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.prepare_memory_streams_v682 import BUFFERS, ROOT
from scripts.verify_village_wrap_v608 import read, save


class Observer:
    def __init__(self, core, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.native, self.image, self.core = NativeMemory(), ImageReader(core), core
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.slots, self.ignored = [], [], [], Counter()
        self.closed = False

        def callback(frame):
            try:
                cpu, raw = ct.string_at(self.cpu, 128), ct.string_at(self.wram, 0x400000)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                obj = values[8] if 'caller_return' in target['name'] else values[4]
                fields = struct.unpack('<10I', main_read(raw, obj, 40))
                selected = (values[6] in BUFFERS if target['name'] == 'stream_open' else fields[7] in BUFFERS.values())
                if selected:
                    assert len(self.rows) < 1000
                    index = len(self.rows)
                    snapshot = self.folder / f'entry_{index:03d}_frame_{frame:06d}_RAM.bin'
                    snapshot.write_bytes(raw)
                    row = {'frame': frame, 'PC': values[2], 'kind': target['name'], 'CPU128_hex': cpu.hex(),
                        'owner': obj, 'owner_register': 'r4' if 'caller_return' in target['name'] else 'r0',
                        'complete_stream_fields': list(fields), 'snapshot': str(snapshot), 'snapshot_sha256': sha(raw)}
                    if target['name'] == 'stream_open':
                        row['requested_mode'] = values[6]
                        row['filename_pointer_not_consumed_by_these_modes'] = values[5]
                    else:
                        provider, cursor, size = fields[7], fields[8], fields[2]
                        assert 0 <= cursor <= 0x100000 and 0 <= size <= 0x100000
                        length = max(128, size) if target['name'] == 'stream_close' else 128
                        payload = main_read(raw, provider, length)
                        path = self.folder / f'entry_{index:03d}_buffer.bin'
                        path.write_bytes(payload)
                        row.update(provider=provider, cursor=cursor, highwater=size,
                            payload=str(path), payload_bytes=length, payload_sha256=sha(payload))
                        if 'caller_return' in target['name']:
                            mode = 1 if target['name'].startswith('mode1') else 2
                            assert provider == BUFFERS[mode] and cursor == 0 and values[4] == 1
                    row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observer'] = True
                    self.rows.append(row)
                else:
                    self.ignored[target['name']] += 1
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
            except BaseException as exc:  # noqa: BLE001 - no exception crosses the native boundary.
                self.errors.append(repr(exc))
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        for index in sorted({t['instruction_index'] for t in self.source['targets']}):
            targets = [t for t in self.source['targets'] if t['instruction_index'] == index]
            slot = core._handle + self.source['interpreter_table']['RVA'] + index * 8
            original = self.image.qword(slot)
            assert all(original == core._handle + t['handler_RVA'] for t in targets)
            address = self.native.alloc(None, 4096, 0x3000, 0x04)
            code, assembly = assemble(self.cpu, ct.addressof(self.header), ct.cast(self.callback, ct.c_void_p).value,
                                      original, targets, address)
            assert len(code) < 4096
            ct.memmove(address, code, len(code))
            old = ct.c_uint32()
            assert self.native.protect(address, 4096, 0x20, ct.byref(old))
            assert self.native.flush(self.native.process, address, len(code))
            self.slots.append({'slot': slot, 'original': original, 'address': address, 'code_hex': code.hex(),
                               'assembly': assembly, 'instruction_index': index})

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
        save(self.folder / 'memory_streams.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'ignored_nonmemory_entries': dict(self.ignored),
            'all_opcode_slots_restored_before_free_and_core_file_exact': True,
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'filters': self.slots, 'anchors': self.image.entries,
            'actual_entry_objects_payloads_and_known_open_returns_not_every_stream_operation': True,
            'full_goal_complete': False})
        for item in self.slots:
            assert self.native.free(item['address'], 0, 0x8000)
        assert not self.errors and not self.header[3]
