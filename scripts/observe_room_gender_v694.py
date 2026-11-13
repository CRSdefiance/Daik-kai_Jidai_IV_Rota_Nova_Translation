"""Observe actual navigator parent casts, room lookup and complete gender updates."""

import ctypes as ct
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/room_gender_v694')


def word(raw, address):
    assert 0x02000000 <= address <= 0x023FFFFC
    return struct.unpack_from('<I', raw, address - 0x02000000)[0]


class Observer:
    def __init__(self, core, folder):
        self.folder = Path(folder) / 'observer'
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.slots, self.counts, self.seen = [], [], [], {}, set()
        self.closed, self.active = False, None

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                raw = ct.string_at(self.wram, 0x400000)
                dtcm, md = ct.string_at(self.dtcm, 0x4000), ct.string_at(self.md, 4)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                kind = target['name']
                self.counts[kind] = self.counts.get(kind, 0) + 1
                if kind == 'cast_done':
                    assert self.active is None
                    view, index, parent = values[10], values[9], values[11]
                    actor = word(raw, view + 0x18 + index * 4)
                    selected = word(raw, parent + 0x44) if parent else None
                    key = (view, actor, parent, selected)
                    self.active = {'number': self.counts[kind], 'key': key, 'keep': key not in self.seen,
                                   'helper_entered': False, 'selected_room': selected}
                    self.seen.add(key)
                assert self.active is not None
                if kind == 'gender_entry':
                    assert values[18] == 0x0209C27C
                    self.active['helper_entered'] = True
                if self.active['keep']:
                    prefix = self.folder / f'event_{len(self.rows):03d}_{kind}_{frame:06d}'
                    ram_path, dtcm_path = prefix.with_suffix('.RAM.bin'), prefix.with_suffix('.DTCM.bin')
                    ram_path.write_bytes(raw)
                    dtcm_path.write_bytes(dtcm)
                    self.rows.append({'frame': frame, 'kind': kind, 'call_number': self.active['number'],
                        'original_view_actor_parent_selected_room_key': list(self.active['key']),
                        'helper_entered': self.active['helper_entered'], 'CPU128_hex': cpu.hex(), 'MDTC_hex': md.hex(),
                        'RAM': str(ram_path), 'RAM_sha256': sha(raw), 'DTCM': str(dtcm_path), 'DTCM_sha256': sha(dtcm)})
                    assert len(self.rows) <= 500
                if kind == 'after_gender_or_bypass':
                    self.active = None
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert ct.string_at(self.dtcm, 0x4000) == dtcm and ct.string_at(self.md, 4) == md
            except BaseException as exc:  # noqa: BLE001 - never throw across native callbacks.
                self.errors.append({'frame': frame, 'error': repr(exc)})
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

    def close(self):
        if not self.closed:
            for row in self.slots:
                self.native.pointer(row['slot'], row['original'])
            self.closed = True
        assert all(self.image.qword(r['slot']) == r['original'] for r in self.slots)
        assert sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'events.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'counts': self.counts, 'mismatches': self.header[3],
            'active_call_at_end': self.active, 'CPU_WRAM_DTCM_configuration_unchanged': True,
            'all_host_slots_restored_core_file_exact': True, 'filters': self.slots,
            'anchors': self.image.entries, 'producer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and self.active is None
