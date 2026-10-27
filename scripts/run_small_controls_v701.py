"""Exact control artwork through an original live image widget; diagnostic only."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.probe_button_prompt_native import machine
from scripts.run_gender_exception_v697 import Observer as Methods
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_room_gender_v694 import class_name
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/small_controls_v701')
BASE, PARENT, VIEW = 0x02000000, 0x02189E24, 0x021901C0
POSITION, ORIGINAL_POSITION = 0x0213BEE4, 0x02119614
FRAMES = (1, 60, 180, 1600, 2000, 2400, 2800, 3200, 3500, 3900, 4300,
          4700, 5100, 5500, 5900, 6200, 6400, 6500, 6600, 7000)
TARGETS = ((0x020CFDE8, 'widget_entry'), (0x01FF92D8, 'copy_entry'),
           (0x020DED50, 'SDK_open_entry'))
CASES = {'confirm': {'label': 'Confirm', 'path': '/_pxl/kakutei.pxl', 'owner': 0x023139C0,
                     'rect': [0, 0, 48, 20], 'bank': 0}}
for label, box in CELLS:
    x0, y0, x1, y1 = box
    CASES[label.lower().replace(' ', '_')] = {'label': label, 'path': '/_pxl/__frame.pxl',
        'owner': 0x02313F60, 'rect': [x0, y0, x1 - x0, y1 - y0], 'bank': 9}
CASES['baseline'] = {'label': 'Original gender widget', 'path': '/_pxl/__marker.pxl',
    'owner': 0x02313F74, 'rect': [232, 96, 16, 16], 'bank': 48}


def word(raw, address):
    return struct.unpack_from('<I', raw, address - BASE)[0]


def redirect(cpu):
    values = struct.unpack('<32I', cpu)
    if values[2] != 0x020CFDE8 or values[5:8] != (VIEW, 1, ORIGINAL_POSITION):
        raise ValueError('Exact original Sailor Info gender-widget arguments required')
    after = bytearray(cpu)
    struct.pack_into('<I', after, 28, POSITION)
    return bytes(after)


def prepare():
    ROOT.mkdir()
    current, clean = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    for address, expected in ((POSITION, (192, 64)), (ORIGINAL_POSITION, (84, 76))):
        assert all(struct.unpack_from('<2I', a, address - BASE) == expected for a in (current, clean))
    assert current[0xCFDE8:0xCFE64] == clean[0xCFDE8:0xCFE64]
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    native_base, table = tables(core)
    targets = []
    for pc, name in TARGETS:
        words = [bytes(machine(a).mem_read(pc, 4)) for a in (current, clean)]
        assert words[0] == words[1]
        value = int.from_bytes(words[0], 'little')
        index = ((value >> 16) & 0xFF0) | ((value >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': value, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - native_base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'cases': CASES, 'original_class': '22CPersonInformationView',
        'fixture_destination_read_from_unchanged_registered_pair': {'pointer': POSITION, 'XY': [192, 64]},
        'ordinary_control_parent_or_intended_palette_NOT_proven': True})
    old = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = old
    inputs = [r for r in read('work/analysis/equipment_cursor_v663/inputs.json') if r['start'] <= 5901]
    inputs.append({'start': 6501, 'duration': 8, 'buttons': ['B']})
    save(ROOT / 'inputs.json', inputs)
    donor = read('work/analysis/equipment_cursor_v663/preflight.json')
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donor': donor['donor'], 'donor_sha256': donor['donor_sha256'],
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'fixture_methods_sha256': sha(Path('scripts/run_gender_exception_v697.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V700 bounded Thumb leads and first unmapped replay I/O diagnosed',
        'full_goal_complete': False})
    print('V701 exact files, original widget, safe source-data point and15 host controls pinned.', flush=True)


class Observer:
    change, install, close = Methods.change, Methods.install, Methods.close

    def __init__(self, core, folder, case):
        self.core, self.folder, self.case = core, Path(folder) / 'observer', case
        self.folder.mkdir()
        self.config, self.enabled = CASES[case], case != 'baseline'
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
                    if values[5:8] != (VIEW, 1, ORIGINAL_POSITION) or not 5900 <= frame < 6401:
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
                    row = {'kind': kind, 'frame': frame, 'CPU128_hex': before_cpu.hex(),
                        'source': list(src), 'size': list(size), 'destination': list(point), 'whole_source_header': values[5],
                        'source_owner_index_after': word(raw, self.config['owner'] + 16)}
                    for field, blob in (('RAM', raw), ('DTCM', dtcm), ('ITCM', itcm)):
                        path = self.folder / ('copy.' + field + '.bin')
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

    def restore(self):
        if self.enabled and self.original is not None:
            self.change(6401, 'restore', ct.string_at(self.wram, 0x400000), self.original)

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
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path(__file__), 'producer_sha256'), (Path('scripts/run_gender_exception_v697.py'), 'fixture_methods_sha256'),
                        (ROOT / 'source_contract.json', 'source_contract_sha256'), (ROOT / 'inputs.json', 'inputs_sha256'),
                        (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    folder = CAP / ('small_controls_v701_' + case)
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'producer_sha256': pre['producer_sha256'], 'isolated_original_widget_not_ordinary_control_context': case != 'baseline'})
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
                if observer.header[0] == 6401:
                    observer.restore()
                original()
            core.retro_run = advance
            installed.append(observer)
        return core
    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', '7000',
        '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen', '--battery-save', pre['donor'],
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-capture-ram', '--dump-ram']
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
    assert len(observer.writes) == (2 if case != 'baseline' else 0)
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['isolated_original_widget_fixture'] = {'enabled': case != 'baseline', 'case': case,
        'receipt': str(folder / 'observer/events.json'), 'receipt_sha256': sha((folder / 'observer/events.json').read_bytes()),
        'normal_control_location_palette_or_gameplay_context_verified': False}
    if case != 'baseline':
        report['synthetic_exact_control_widget_fixture'] = True
    save(rp, report)
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    print('V701 terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=(*CASES, 'prepare'))
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        run(args.case)
