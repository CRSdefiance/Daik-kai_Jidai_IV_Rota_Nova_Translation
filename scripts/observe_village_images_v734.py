"""Actual named/numeric/range/raw/event image requests, with read-only callbacks."""

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

ROOT = Path('work/analysis/village_images_v734')
ROM = Path('out/all_routes_combined_v712_candidate.nds')


class Observer:
    def __init__(self, core, folder):
        self.folder, self.native, self.image = Path(folder), NativeMemory(), ImageReader(core)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)
        self.dtcm_base = self.image.anchor('MDTC', 4, 1)
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.pending, self.slots = [], [], [], []
        self.closed = False
        self.blocks = IlnkContainer.parse(NdsImage.open(ROM).read_file('/GRP/SLACKIMG.DK4')).blocks

        def callback(frame):
            row = {'frame': frame}
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

                row.update(kind=target['name'], PC=values[2], CPU128_hex=cpu.hex(),
                    args=list(values[4:8]), LR=values[18], WRAM_sha256=sha(raw),
                    DTCM_sha256=sha(dtcm), ITCM_sha256=sha(itcm), DTCM_base=base)
                kind = target['name']
                if kind == 'filename':
                    text = bytearray()
                    for n in range(128):
                        value = memory(values[5] + n, 1)
                        text += value
                        if value == b'\0':
                            break
                    assert text[-1:] == b'\0'
                    row.update(filename=text[:-1].decode('ascii'), filename_pointer=values[5],
                        filename_with_NUL_hex=bytes(text).hex(),
                        file_object64_hex=memory(values[4], 64).hex())
                elif kind in ('numeric_ID', 'direct_range'):
                    row['archive128_hex'] = memory(values[5], 128).hex()
                    row['stack32_hex'] = memory(values[17], 32).hex()
                    if kind == 'numeric_ID':
                        row['file_ID'] = values[6]
                    else:
                        row['file_ID'] = struct.unpack_from('<I', bytes.fromhex(row['stack32_hex']))[0]
                        row['byte_range'] = list(values[6:8])
                elif kind == 'event_still_formatter':
                    row.update(original_view=values[4], original_image_index=values[5])
                elif kind == 'raw_SLACK_entry':
                    index, destination, offset, length = values[4:8]
                    assert 0 <= index < len(self.blocks)
                    length = length or len(self.blocks[index])
                    assert offset + length <= len(self.blocks[index])
                    request = {'block': index, 'destination': destination, 'offset': offset, 'length': length,
                        'entry_row': len(self.rows)}
                    self.pending.append(request)
                    row['raw_request'] = dict(request)
                else:
                    assert kind == 'raw_SLACK_known_return' and self.pending
                    request = self.pending.pop()
                    actual = memory(request['destination'], request['length'])
                    expected = self.blocks[request['block']][request['offset']:request['offset'] + request['length']]
                    assert actual == expected
                    path = self.folder / f"raw_return_{len(self.rows):04d}_block{request['block']:02d}.bin"
                    path.write_bytes(actual)
                    row.update(raw_request=request, exact_source_return_payload=str(path), payload_sha256=sha(actual))
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert self.image.read(self.dtcm, 0x4000) == dtcm and self.image.read(self.itcm, 0x8000) == itcm
                assert self.image.read(self.dtcm_base, 4) == base_raw
                row['CPU128_WRAM_DTCM_ITCM_and_configuration_unchanged_by_observer'] = True
                self.rows.append(row)
            except BaseException as exc:  # noqa: BLE001 - do not unwind a native callback.
                self.errors.append({'error': repr(exc), 'context': row})
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
        assert all(self.image.qword(row['slot']) == row['original'] for row in self.slots)
        assert sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'requests.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'unreturned_raw_requests': self.pending,
            'all_host_slots_restored_and_core_file_exact': True,
            'observer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'host_filters': self.slots, 'anchors': self.image.entries,
            'entry_requests_not_successful_open_or_every_possible_filesystem_route': True,
            'full_goal_complete': False})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and not self.pending
