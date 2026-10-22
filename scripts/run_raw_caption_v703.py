"""Matched raw16 caption source and opacity control in a compatible live widget."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import ImageReader
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.prepare_raw_caption_v703 import (
    BASE,
    CASES,
    ORIGINAL_POSITION,
    POSITION,
    ROOT,
)
from scripts.prepare_raw_caption_v703 import ROM as PARENT_ROM
from scripts.run_gender_exception_v697 import Observer as Methods
from scripts.run_room_gender_v694 import CAP
from scripts.run_small_controls_v701 import PARENT, VIEW
from scripts.verify_room_gender_v694 import class_name
from scripts.verify_village_wrap_v608 import read, save

ROM = PARENT_ROM


def word(raw, address):
    return struct.unpack_from('<I', raw, address - BASE)[0]


def redirect(cpu):
    values = struct.unpack('<32I', cpu)
    if values[2] != 0x020CFDE8 or values[5:8] != (VIEW, 1, ORIGINAL_POSITION):
        raise ValueError('Exact original Sailor Info gender-widget arguments required')
    after = bytearray(cpu)
    struct.pack_into('<I', after, 28, POSITION)
    return bytes(after)


class Observer:
    change, install, close = Methods.change, Methods.install, Methods.close

    def __init__(self, core, folder, case):
        self.core, self.folder, self.case = core, Path(folder) / 'observer', case
        self.folder.mkdir()
        self.config, self.enabled = dict(CASES[case]), not CASES[case]['baseline']
        self.image, self.native = ImageReader(core), NativeMemory()
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)
        assert all(self.cpu + 128 <= p or p + n <= self.cpu for p, n in
                   ((self.wram, 0x400000), (self.dtcm, 0x4000), (self.itcm, 0x8000)))
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.slots, self.writes, self.errors, self.redirects, self.rows = [], [], [], [], []
        self.original, self.filename_pointer, self.drawn, self.closed = None, None, False, False
        self.phase_index = 0
        self.asset = NdsImage.open(ROM).read_file(self.config['path'])
        source = read(ROOT / 'source_contract.json')

        def callback(frame):
            before_cpu = None
            try:
                before_cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', before_cpu)
                kind = next(t['name'] for t in source['targets'] if t['PC'] == values[2])
                if kind == 'SDK_open_entry':
                    if self.filename_pointer is None or values[5] != self.filename_pointer:
                        return
                    name = ct.string_at(self.wram + self.filename_pointer - BASE, 80).split(b'\0', 1)[0].decode('ascii')
                    assert '/' + name.replace('\\', '/').lstrip('/') == self.config['path']
                    self.rows.append({'kind': kind, 'frame': frame, 'filename': name, 'CPU128_hex': before_cpu.hex()})
                elif kind == 'widget_entry':
                    if values[5:8] != (VIEW, 1, ORIGINAL_POSITION) or not 5900 <= frame < self.config['restore_frame']:
                        return
                    if self.original is None:
                        raw = ct.string_at(self.wram, 0x400000)
                        assert class_name(raw, PARENT) == '22CPersonInformationView'
                        assert word(raw, word(raw, PARENT + 4)) == 1 and word(raw, PARENT + 12) == 0
                        view = struct.unpack_from('<12I', raw, VIEW - BASE)
                        assert view[3] == 0x02313F74 and view[5] == 4 and view[7:9] == (232, 96)
                        assert view[9] & 0xFFFF == 48 and view[10:12] == (16, 16)
                        assert struct.unpack_from('<2I', raw, POSITION - BASE) == (192, 64)
                        self.original = {VIEW + i * 4: view[i] for i in (3, 7, 8, 9, 10, 11)}
                        self.filename_pointer = word(raw, self.config['owner'] + 12)
                        name = raw[self.filename_pointer - BASE:self.filename_pointer - BASE + 80].split(b'\0', 1)[0].decode('ascii')
                        assert '/' + name.replace('\\', '/').lstrip('/') == self.config['path']
                        self.rows.append({'kind': 'original_widget', 'frame': frame, 'CPU128_hex': before_cpu.hex(),
                            'view_words': list(view), 'owner_filename': name,
                            'source_owner_index_before': word(raw, self.config['owner'] + 16)})
                        if self.enabled:
                            x, y, width, height = self.config['rect']
                            desired = {VIEW + 12: self.config['owner'], VIEW + 28: x, VIEW + 32: y,
                                VIEW + 36: (view[9] & 0xFFFF0000) | self.config['bank'],
                                VIEW + 40: width, VIEW + 44: height}
                            self.change(frame, 'install', raw, desired)
                    if self.enabled:
                        after = redirect(before_cpu)
                        ct.memmove(self.cpu + 28, after[28:32], 4)
                        assert ct.string_at(self.cpu, 128) == after
                        self.redirects.append({'frame': frame, 'before_CPU128_hex': before_cpu.hex(),
                                              'after_CPU128_hex': after.hex()})
                        return
                elif not self.drawn and self.original is not None and values[4] == 1 and values[9] == VIEW:
                    raw, dtcm, itcm = [ct.string_at(p, n) for p, n in
                        ((self.wram, 0x400000), (self.dtcm, 0x4000), (self.itcm, 0x8000))]
                    assert BASE <= values[5] <= BASE + len(raw) - len(self.asset)
                    assert raw[values[5] - BASE:values[5] - BASE + len(self.asset)] == self.asset
                    def guest(address, length):
                        if 0x027E0000 <= address and address + length <= 0x027E4000:
                            return dtcm[address - 0x027E0000:address - 0x027E0000 + length]
                        assert BASE <= address and address + length <= BASE + len(raw)
                        return raw[address - BASE:address - BASE + length]
                    src = struct.unpack('<2I', guest(values[7], 8))
                    size_pointer, point_pointer = struct.unpack('<2I', guest(values[17], 8))
                    size = struct.unpack('<2I', guest(size_pointer, 8))
                    point = struct.unpack('<2I', guest(point_pointer, 8))
                    assert list(src + size) == self.config['rect'] and values[6] == self.config['bank']
                    assert point == ((192, 64) if self.enabled else (84, 76))
                    row = {'kind': kind, 'frame': frame, 'phase': self.phase_index, 'CPU128_hex': before_cpu.hex(),
                        'source': list(src), 'size': list(size), 'destination': list(point), 'whole_source_header': values[5],
                        'source_owner_index_after': word(raw, self.config['owner'] + 16)}
                    for field, blob in (('RAM', raw), ('DTCM', dtcm), ('ITCM', itcm)):
                        path = self.folder / f'copy_phase{self.phase_index:03d}.{field}.bin'
                        path.write_bytes(blob)
                        row[field], row[field + '_sha256'] = str(path), sha(blob)
                    self.rows.append(row)
                    self.drawn = True
                    assert ct.string_at(self.wram, len(raw)) == raw and ct.string_at(self.dtcm, len(dtcm)) == dtcm
                    assert ct.string_at(self.itcm, len(itcm)) == itcm
                assert ct.string_at(self.cpu, 128) == before_cpu
            except BaseException as exc:  # noqa: BLE001 - never unwind through native code.
                if before_cpu is not None:
                    ct.memmove(self.cpu, before_cpu, 128)
                self.errors.append({'frame': frame, 'error': repr(exc)})
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        for index in sorted({t['instruction_index'] for t in source['targets']}):
            selected = [t for t in source['targets'] if t['instruction_index'] == index]
            slot = core._handle + source['interpreter_table']['RVA'] + index * 8
            original = self.image.qword(slot)
            assert all(original == core._handle + t['handler_RVA'] for t in selected)
            address = self.native.alloc(None, 4096, 0x3000, 0x04)
            code, assembly = assemble(self.cpu, ct.addressof(self.header), ct.cast(self.callback, ct.c_void_p).value,
                original, selected, address)
            assert len(code) < 4096
            ct.memmove(address, code, len(code))
            old = ct.c_uint32()
            assert self.native.protect(address, 4096, 0x20, ct.byref(old))
            assert self.native.flush(self.native.process, address, len(code))
            self.slots.append({'slot': slot, 'original': original, 'address': address, 'code_hex': code.hex(), 'assembly': assembly})

    def advance_phase(self, frame):
        if not self.enabled or frame < 6101 or (frame - 6001) % 100:
            return
        phase = (frame - 6001) // 100
        if phase >= len(self.config['tiles']):
            return
        assert self.original is not None and self.drawn and not self.errors
        x, y, width, height = self.config['tiles'][phase]
        desired = {VIEW + 28: x, VIEW + 32: y, VIEW + 40: width, VIEW + 44: height}
        self.change(frame, f'phase{phase:03d}', ct.string_at(self.wram, 0x400000), desired)
        self.config['rect'] = [x, y, width, height]
        self.phase_index, self.drawn = phase, False

    def restore(self):
        if self.enabled and self.original is not None:
            self.change(self.config['restore_frame'], 'restore', ct.string_at(self.wram, 0x400000), self.original)

    def save(self):
        assert self.closed
        save(self.folder / 'events.json', {'case': self.case, 'rows': self.rows, 'fixture_writes': self.writes,
            'CPU_argument_redirects': self.redirects, 'errors': self.errors, 'original_view_fields': self.original,
            'enabled': self.enabled, 'whole_source_copy_recorded': self.drawn,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'filters': self.slots,
            'CPU128_host_interval_disjoint_from_WRAM_DTCM_ITCM': True,
            'all_host_slots_restored_core_file_exact': True,
            'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)


def run(case):
    global ROM
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    config = CASES[case]
    selected = pre['research_ROMs'][config['group']]
    ROM = PARENT_ROM if config['baseline'] else Path(selected['path'])
    expected_ROM = pre['candidate_sha256'] if config['baseline'] else selected['sha256']
    assert sha(ROM.read_bytes()) == expected_ROM
    for path, field in ((Path(__file__), 'producer_sha256'),
        (Path('scripts/prepare_raw_caption_v703.py'), 'preparer_sha256'),
        (Path('scripts/run_gender_exception_v697.py'), 'fixture_methods_sha256'),
        (ROOT / 'source_contract.json', 'source_contract_sha256'), (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    inputs = ROOT / (case + '_inputs.json')
    assert sha(inputs.read_bytes()) == pre['case_input_hashes'][case]
    folder = CAP / ('raw_caption_v703_' + case)
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'ROM': str(ROM), 'ROM_sha256': expected_ROM,
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'producer_sha256': pre['producer_sha256'], 'research_slot_and_tiled_widget_fixture': not config['baseline'],
        'original_standalone_filename_consumer_or_whole_scene_NOT_proven': True})
    loader, installed = ct.CDLL, []
    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder, case)
            observer.install()
            original = core.retro_run
            original.restype = None
            def advance():
                observer.header[0] += 1
                frame = observer.header[0]
                if frame == config['restore_frame']:
                    observer.restore()
                else:
                    observer.advance_phase(frame)
                original()
            core.retro_run = advance
            installed.append(observer)
        return core
    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['final_frame']), '--inputs-json', str(inputs), '--touchscreen',
        '--battery-save', pre['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, config['capture_frames']), '--dump-capture-ram', '--dump-ram', '--capture-native-state-at', '6080']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
            observer.save()
    assert len(installed) == 1
    observer = installed[0]
    assert not observer.errors and not observer.header[3] and observer.drawn
    assert len(observer.writes) == (0 if config['baseline'] else len(config['tiles']) + 1)
    assert len([r for r in observer.rows if r['kind'] == 'copy_entry']) == (1 if config['baseline'] else len(config['tiles']))
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['isolated_standalone_tile_fixture'] = {'enabled': not config['baseline'], 'case': case,
        'receipt': str(folder / 'observer/events.json'),
        'receipt_sha256': sha((folder / 'observer/events.json').read_bytes()),
        'source_path': config['legacy_source'], 'original_filename_consumer_or_scene_verified': False}
    if not config['baseline']:
        report['synthetic_borrowed_file_and_tiled_widget_fixture'] = True
    save(rp, report)
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    print('V703 terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=tuple(CASES))
    args = parser.parse_args()
    run(args.case)
