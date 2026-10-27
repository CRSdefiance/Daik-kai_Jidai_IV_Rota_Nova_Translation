"""Read actual interpreter input before/after original commands; never edit state."""

import ctypes as ct
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.trace_file_ids_v683 import mapped_read
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/script_sources_v733')
ROM = Path('out/all_routes_combined_v712_candidate.nds')


class Observer:
    def __init__(self, core, folder):
        self.core, self.folder = core, Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.dtcm_base = self.image.anchor('MDTC', 4, 1)
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.pending, self.slots = [], [], {}, []
        self.closed = False
        rom = NdsImage.open(ROM)
        self.blocks = [IlnkContainer.parse(rom.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)]
        self.saved, self.unknown_saved = {}, 0

        def callback(frame):
            try:
                assert len(self.rows) < 20000
                cpu, raw = ct.string_at(self.cpu, 128), ct.string_at(self.wram, 0x400000)
                dtcm, itcm = self.image.read(self.dtcm, 0x4000), self.image.read(self.itcm, 0x8000)
                base_raw = self.image.read(self.dtcm_base, 4)
                base = struct.unpack('<I', base_raw)[0]
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert values[1] == target['word']

                def memory(address, length):
                    return mapped_read(raw, dtcm, base, address, length)

                before = target['name'] == 'before_command'
                player = values[5] if before else values[17]
                assert player == values[17], 'Original interpreter local object must be its stack frame'
                row = {'frame': frame, 'kind': target['name'], 'PC': values[2], 'CPU128_hex': cpu.hex(),
                    'player': player, 'WRAM_sha256': sha(raw), 'DTCM_sha256': sha(dtcm),
                    'ITCM_sha256': sha(itcm), 'DTCM_base': base,
                    'player_descriptor16_hex': memory(player, 16).hex()}
                try:
                    vtable, index = struct.unpack('<2I', memory(player + 0x58, 8))
                    route = struct.unpack('<I', memory(0x022796B0, 4))[0]
                    pointer = struct.unpack('<I', memory(player + 4, 4))[0]
                    payload = player + 0x60
                    assert vtable == 0x02134578 and 0 <= route < 4 and index < len(self.blocks[route])
                    expected = self.blocks[route][index]
                    actual = memory(payload, len(expected))
                    offset = pointer - payload
                    assert 8 <= offset <= len(expected) - 2
                    key = route, index, payload, sha(actual)
                    if key not in self.saved:
                        path = self.folder / f'resident_{len(self.saved):04d}_SC{route}_block{index:03d}.bin'
                        path.write_bytes(actual)
                        self.saved[key] = str(path)
                    row['source'] = {'classification': 'original_SC_cache', 'route': route, 'block': index,
                        'cache_vtable': vtable, 'cache_address': player + 0x58,
                        'payload_address': payload, 'payload_bytes': len(expected), 'instruction_pointer': pointer,
                        'instruction_offset': offset, 'first_word': struct.unpack('<H', memory(pointer, 2))[0],
                        'packet_prefix_hex': memory(pointer, min(16, len(expected) - offset)).hex(),
                        'actual_sha256': sha(actual), 'registered_sha256': sha(expected),
                        'whole_resident_payload_exact_ROM': actual == expected,
                        'actual_payload_file': self.saved[key]}
                except (AssertionError, ValueError, IndexError) as exc:
                    row['source'] = {'classification': 'unidentified', 'reason': repr(exc)}
                    if self.unknown_saved < 3:
                        prefix = self.folder / f'unknown_{self.unknown_saved:02d}'
                        for suffix, data in (('CPU.bin', cpu), ('RAM.bin', raw), ('DTCM.bin', dtcm), ('ITCM.bin', itcm)):
                            prefix.with_name(prefix.name + '_' + suffix).write_bytes(data)
                        row['source']['diagnostic_prefix'] = str(prefix)
                        self.unknown_saved += 1
                if before:
                    assert player not in self.pending, 'Unexpected reentry at the same interpreter stack'
                    row['mode'] = values[7]
                    self.pending[player] = len(self.rows)
                else:
                    assert player in self.pending, 'Original command return has no recorded entry'
                    row['entry_row'] = self.pending.pop(player)
                    row['decoded_length'] = struct.unpack('<I', memory(player + 8, 4))[0]
                    row['result_words'] = list(struct.unpack('<2I', memory(player + 12, 8)))
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert self.image.read(self.dtcm, 0x4000) == dtcm and self.image.read(self.itcm, 0x8000) == itcm
                assert self.image.read(self.dtcm_base, 4) == base_raw
                row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] = True
                self.rows.append(row)
            except BaseException as exc:  # noqa: BLE001 - never raise across a native callback.
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
        save(self.folder / 'commands.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3],
            'unreturned_at_capture_end': [{'player': p, 'entry_row': r} for p, r in self.pending.items()],
            'all_host_slots_restored_and_core_file_exact': True,
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'host_filters': self.slots, 'anchors': self.image.entries,
            'entry_return_snapshots_do_not_exclude_temporary_write_then_restore': True,
            'full_goal_complete': False})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3]
