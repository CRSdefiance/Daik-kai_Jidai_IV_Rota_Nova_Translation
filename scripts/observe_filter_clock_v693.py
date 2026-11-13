"""Read exact original lower-paint entries, clock returns and completed outputs."""

import ctypes as ct
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/filter_clock_v693')
LOWER = 0x023117C4
WATCH = {9599, 9600, 9601, 10799, 10800, 10801}


class Observer:
    def __init__(self, core, folder):
        self.folder = Path(folder) / 'clock_observer'
        self.folder.mkdir()
        self.image, self.gpu_image, self.native = ImageReader(core), ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.io = self.gpu_image.anchor('9REG', 1, 0x2000)
        self.lcdm = self.image.anchor('LCDM', 1, 0xA4000)
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.paints, self.clocks, self.errors, self.slots = [], [], [], []
        self.closed, self.active, self.counts = False, None, {}

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                kind = target['name']
                self.counts[kind] = self.counts.get(kind, 0) + 1
                # The same original iterator handles both screens. Capture its
                # actual lower context and paired return; ignore other contexts.
                if kind == 'paint_entry' and values[8] == LOWER and frame in WATCH:
                    assert self.active is None
                    prefix = self.folder / f'paint_{len(self.paints):03d}_{frame:06d}'
                    raw = ct.string_at(self.wram, 0x400000)
                    regions = {'RAM': raw, 'DTCM': ct.string_at(self.dtcm, 0x4000),
                        'IO': ct.string_at(self.io, 0x2000), 'LCDM': ct.string_at(self.lcdm, 0xA4000),
                        'ITCM': ct.string_at(self.itcm, 0x8000), 'MDTC': ct.string_at(self.md, 4)}
                    paths = {}
                    for name, data in regions.items():
                        path = prefix.with_suffix('.' + name + '.bin')
                        path.write_bytes(data)
                        paths[name] = {'path': str(path), 'sha256': sha(data), 'bytes': len(data)}
                    row = {'entry_frame': frame, 'entry_CPU128_hex': cpu.hex(),
                           'regions': paths, 'clocks': [], 'context': values[8]}
                    self.paints.append(row)
                    self.active = row
                    assert len(self.paints) <= 30
                    assert all(ct.string_at({'RAM': self.wram, 'DTCM': self.dtcm, 'IO': self.io,
                        'LCDM': self.lcdm, 'ITCM': self.itcm, 'MDTC': self.md}[name], len(data)) == data
                               for name, data in regions.items())
                elif kind == 'clock_return' and self.active is not None:
                    tick = values[4] | values[5] << 32
                    origin = struct.unpack('<Q', ct.string_at(self.wram + 0x170374, 8))[0]
                    item = {'frame': frame, 'CPU128_hex': cpu.hex(), 'tick': tick,
                            'origin': origin, 'actual_SDK_return_PC': values[2],
                            'caller_LR': values[18]}
                    self.active['clocks'].append(item)
                    self.clocks.append(item)
                elif kind == 'paint_return' and values[8] == LOWER and self.active is not None:
                    raw, dtcm = ct.string_at(self.wram, 0x400000), ct.string_at(self.dtcm, 0x4000)
                    prefix = self.folder / f'paint_{len(self.paints) - 1:03d}_return_{frame:06d}'
                    for name, data in (('RAM', raw), ('DTCM', dtcm)):
                        path = prefix.with_suffix('.' + name + '.bin')
                        path.write_bytes(data)
                        self.active['return_' + name] = {'path': str(path), 'sha256': sha(data), 'bytes': len(data)}
                    self.active.update(return_frame=frame, return_CPU128_hex=cpu.hex())
                    assert ct.string_at(self.wram, len(raw)) == raw and ct.string_at(self.dtcm, len(dtcm)) == dtcm
                    self.active = None
                assert ct.string_at(self.cpu, 128) == cpu
            except BaseException as exc:  # noqa: BLE001 - never throw across a native callback.
                self.errors.append({'frame': frame, 'PC': values[2] if 'values' in locals() else None, 'error': repr(exc)})
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
        save(self.folder / 'events.json', {'paints': self.paints, 'errors': self.errors,
            'callbacks': self.header[2], 'counts': self.counts, 'mismatches': self.header[3],
            'active_call_at_end': self.active, 'all_host_slots_restored_core_file_exact': True,
            'filters': self.slots, 'anchors': self.image.entries, 'IO_anchors': self.gpu_image.entries,
            'no_game_CPU_RAM_VRAM_IO_ITCM_DTCM_writes': True,
            'producer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and self.active is None
