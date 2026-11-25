"""Read actual original modal invocation/return intervals without emulated writes."""

import ctypes as ct
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.run_opening_holds_v686 import ROOT
from scripts.verify_village_wrap_v608 import read, save


class Observer:
    def __init__(self, core, folder, version):
        self.folder, self.version = Path(folder), version
        self.folder.mkdir(parents=True)
        self.image, self.native = ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'wait_source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.md = self.image.anchor('MDTC', 4, 1)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.slots, self.errors, self.pending = [], [], [], None
        self.ignored, self.closed = 0, False

        def callback(frame):
            try:
                cpu, raw = ct.string_at(self.cpu, 128), ct.string_at(self.wram, 0x400000)
                dtcm, md = self.image.read(self.dtcm, 0x4000), self.image.read(self.md, 4)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                selected = target['name'] != 'modal_entry' or values[18] == 0x0202A218
                if selected:
                    cursor = struct.unpack_from('<I', raw, 0x18F254)[0]
                    block = struct.unpack_from('<I', raw, 0x18F2AC)[0]
                    assert block == 33 and 0x0218F2B0 <= cursor < 0x0218F2B0 + 2528
                    assert sha(raw[0x18F2B0:0x18F2B0 + 2528]) == self.source['chapter_sha256'][version]
                    command = struct.unpack_from('<H', raw, cursor - 0x02000000)[0]
                    assert command >> 8 == 0x20
                    row = {'frame': frame, 'kind': target['name'], 'CPU128_hex': cpu.hex(),
                        'actual_VM_cursor': cursor, 'chapter_offset': cursor - 0x0218F2B0,
                        'original_command': command, 'chapter_cache_index': block,
                        'owner96_hex': raw[0x18F250:0x18F2B0].hex()}
                    if target['name'] == 'modal_entry':
                        assert values[4:6] == (0, 0) and self.pending is None
                        row['actual_original_arguments'] = [0, 0]
                        self.pending = len(self.rows)
                    else:
                        assert self.pending is not None
                        row['matching_actual_entry_index'] = self.pending
                        row['native_modal_return_value_recorded_without_boolean_assumption'] = values[4]
                        assert self.rows[self.pending]['chapter_offset'] == row['chapter_offset']
                        self.pending = None
                    path = self.folder / f'event_{len(self.rows):03d}_{target["name"]}_{frame:06d}_RAM.bin'
                    path.write_bytes(raw)
                    row.update(actual_RAM=str(path), actual_RAM_sha256=sha(raw))
                    self.rows.append(row)
                else:
                    self.ignored += 1
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert self.image.read(self.dtcm, 0x4000) == dtcm and self.image.read(self.md, 4) == md
            except BaseException as exc:  # noqa: BLE001 - never throw across native callback.
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
            self.slots.append({'slot': slot, 'original': original, 'address': address,
                               'code_hex': code.hex(), 'assembly': assembly})

    def install(self):
        for row in self.slots:
            assert self.image.qword(row['slot']) == row['original']
            self.native.pointer(row['slot'], row['address'])

    def next_frame(self):
        self.header[0] += 1

    def close(self):
        if not self.closed:
            for row in self.slots:
                self.native.pointer(row['slot'], row['original'])
            self.closed = True
        assert all(self.image.qword(r['slot']) == r['original'] for r in self.slots)
        assert sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'actual_modal_intervals.json', {'rows': self.rows, 'errors': self.errors,
            'version': self.version, 'ignored_other_modal_callers': self.ignored,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'pending_entry': self.pending,
            'each_callback_CPU_WRAM_DTCM_and_configuration_unchanged': True,
            'all_slots_restored_before_free_core_file_exact': True,
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'wait_source_contract.json').read_bytes()),
            'filters': self.slots, 'anchors': self.image.entries, 'full_goal_complete': False})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and self.pending is None
