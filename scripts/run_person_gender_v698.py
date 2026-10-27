"""Arcadius's original flag exception in actual Sailor Info, with bounded fixtures."""

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
from scripts.run_gender_exception_v697 import ACTOR, BASE, FLAG_MASK, FLAG_WORD
from scripts.run_gender_exception_v697 import Observer as FixtureMethods
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/person_gender_v698/final/screen1')
VIEW_OFFSET = 0x639C
TARGETS = ((0x02080324, 'update_entry'), (0x02080340, 'actor_ready'),
    (0x02080448, 'raw_gender'), (0x02080454, 'identity'), (0x02023C60, 'flag_entry'),
    (0x02080468, 'flag_return'), (0x02080470, 'processed'), (0x020804E4, 'view_ready'),
    (0x01FF92D8, 'gender_draw'))
FRAMES = (1, 60, 180, 1600, 2000, 2400, 2800, 3200, 3500, 3900, 4300, 4700,
          5100, 5500, 5900, 6200, 6600, 7000, 7400, 7600, 7800)


def word(raw, address):
    return struct.unpack_from('<I', raw, address - BASE)[0]


def prepare():
    ROOT.mkdir()
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    native_base, table = tables(core)
    old = read('work/analysis/equipment_cursor_v663/preflight.json')
    assert sha(Path(old['donor']).read_bytes()) == old['donor_sha256']
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    targets = []
    for pc, name in TARGETS:
        at = pc - BASE
        if pc < BASE:
            # Original corner-copy lives in the declared low-memory section.
            from scripts.probe_button_prompt_native import machine
            words = [bytes(machine(a).mem_read(pc, 4)) for a in arms]
        else:
            words = [a[at:at + 4] for a in arms]
        assert words[0] == words[1]
        value = int.from_bytes(words[0], 'little')
        index = ((value >> 16) & 0xFF0) | ((value >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': value, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - native_base})
    assert all(a[0x80440:0x804E4] == arms[1][0x80440:0x804E4] for a in arms)
    assert struct.unpack_from('<I', arms[0], 0x80A40)[0] == VIEW_OFFSET
    source = {'targets': targets, 'interpreter_table': table, 'actual_class': '22CPersonInformationView',
        'selected_pointer_field': 4, 'count_field': 8, 'index_field': 12,
        'original_record_resolver': 0x02080A84, 'gender_view_offset': VIEW_OFFSET,
        'flag_index': 9, 'flag_mask': FLAG_MASK, 'original_flag_return': 0x02080468,
        'native_input_controls_inherited': 'work/analysis/gender_exception_v697/native_input_controls.json',
        'native_input_controls_sha256': sha(Path('work/analysis/gender_exception_v697/native_input_controls.json').read_bytes())}
    save(ROOT / 'source_contract.json', source)
    scratch = ROOT / 'prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', source)
    old_check = checks.ROOT
    checks.ROOT = scratch
    try:
        checks.main()
    finally:
        checks.ROOT = old_check
    assert len(read(scratch / 'native_prefix_controls.json')['native_host_cases']) == 45
    inputs = [r for r in read('work/analysis/equipment_cursor_v663/inputs.json') if r['start'] <= 5901]
    inputs += [{'start': f, 'duration': 8, 'buttons': [button]} for f, button in
               ((6301, 'R'), (6701, 'L'), (7401, 'B'))]
    save(ROOT / 'inputs.json', inputs)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donor': old['donor'], 'donor_sha256': old['donor_sha256'],
        'donor_provenance': 'Retained V476 Syracuse prepared equipment test copy; no earned recruitment/reveal claim',
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'fixture_methods_source': 'scripts/run_gender_exception_v697.py',
        'fixture_methods_sha256': sha(Path('scripts/run_gender_exception_v697.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V697 actual second-parent Arcadius exception and restored fixtures',
        'full_goal_complete': False})
    print('V698 original Sailor Info exception, selected-array contract and45 prefix controls pinned.', flush=True)


class Observer:
    change, install, close = FixtureMethods.change, FixtureMethods.install, FixtureMethods.close

    def __init__(self, core, folder, flag, observed):
        self.core, self.folder, self.flag, self.observed = core, Path(folder) / 'observer', flag, observed
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.itcm = self.image.anchor('ITCM', 1, 0x8000)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.writes, self.errors, self.slots, self.counts = [], [], [], [], {}
        self.original, self.current, self.completed, self.closed = None, None, False, False
        self.calls, self.seen = 0, set()
        self.marker = NdsImage.open(ROM).read_file('/_pxl/__marker.pxl')

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                kind = target['name']
                self.counts[kind] = self.counts.get(kind, 0) + 1
                relevant, draw_data = False, None
                if kind == 'update_entry':
                    if not 5900 <= frame < 7401:
                        return
                    raw = ct.string_at(self.wram, 0x400000)
                    parent = values[4]
                    vtable = word(raw, parent)
                    name = word(raw, word(raw, vtable - 4) + 4)
                    expected_class = b'22CPersonInformationView\0'
                    assert raw[name - BASE:name - BASE + len(expected_class)] == expected_class
                    array, count, index = [word(raw, parent + n) for n in (4, 8, 12)]
                    assert count == 5 and 0 <= index < count
                    cell = array + index * 4
                    actor = word(raw, cell)
                    if self.original is None:
                        assert index == 0 and actor == 1
                        self.original = {'parent': parent, 'actor_cell': cell, 'actor': 1,
                                         'flag_word': word(raw, FLAG_WORD), 'array': array, 'count': count}
                        desired = (self.original['flag_word'] & ~FLAG_MASK) | (FLAG_MASK if flag else 0)
                        self.change(frame, 'install', raw, {cell: ACTOR, FLAG_WORD: desired})
                        actor = ACTOR
                    else:
                        assert parent == self.original['parent'] and word(raw, self.original['actor_cell']) == ACTOR
                    self.completed = False
                    if actor == ACTOR:
                        self.calls += 1
                        self.current, relevant = self.calls, True
                    else:
                        self.current = None
                elif self.current is not None and frame < 7401:
                    relevant = True
                    if kind == 'flag_entry':
                        relevant = values[18] == 0x02080468
                    elif kind == 'gender_draw':
                        relevant = False
                        if values[4] != 1:
                            return
                        if self.completed and (self.current, kind) not in self.seen:
                            raw, dtcm = ct.string_at(self.wram, 0x400000), ct.string_at(self.dtcm, 0x4000)
                            def guest(address, length):
                                if 0x027E0000 <= address and address + length <= 0x027E4000:
                                    return dtcm[address - 0x027E0000:address - 0x027E0000 + length]
                                assert BASE <= address and address + length <= BASE + len(raw)
                                return raw[address - BASE:address - BASE + length]
                            src = struct.unpack('<2I', guest(values[7], 8))
                            size_ptr, point_ptr = struct.unpack('<2I', guest(values[17], 8))
                            size = struct.unpack('<2I', guest(size_ptr, 8))
                            if src == ((232, 96), (240, 112))[flag] and size == (16, 16):
                                assert guest(values[5], len(self.marker)) == self.marker
                                point = struct.unpack('<2i', guest(point_ptr, 8))
                                assert values[4] == 1 and point == (84, 76)
                                draw_data = {'screen': values[4], 'whole_Marker_header': values[5],
                                             'source': list(src), 'size': list(size), 'destination': list(point)}
                                relevant = True
                    elif kind == 'view_ready':
                        self.completed = True
                if observed and relevant and (self.current, kind) not in self.seen:
                    raw, dtcm, itcm = [ct.string_at(a, n) for a, n in
                        ((self.wram, 0x400000), (self.dtcm, 0x4000), (self.itcm, 0x8000))]
                    row = {'kind': kind, 'frame': frame, 'call': self.current, 'CPU128_hex': cpu.hex()}
                    if draw_data:
                        row['actual_original_copy_arguments'] = draw_data
                    for name, data in (('RAM', raw), ('DTCM', dtcm), ('ITCM', itcm)):
                        path = self.folder / f'call{self.current}_{kind}_{frame:06d}.{name}.bin'
                        path.write_bytes(data)
                        row[name], row[name + '_sha256'] = str(path), sha(data)
                    self.rows.append(row)
                    self.seen.add((self.current, kind))
                    assert ct.string_at(self.wram, len(raw)) == raw
                    assert ct.string_at(self.dtcm, len(dtcm)) == dtcm and ct.string_at(self.itcm, len(itcm)) == itcm
                assert ct.string_at(self.cpu, 128) == cpu
            except BaseException as exc:  # noqa: BLE001 - never unwind through native code.
                self.errors.append({'frame': frame, 'error': repr(exc)})
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        targets = self.source['targets'] if observed else [self.source['targets'][0]]
        for index in sorted({t['instruction_index'] for t in targets}):
            selected = [t for t in targets if t['instruction_index'] == index]
            slot = core._handle + self.source['interpreter_table']['RVA'] + index * 8
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
            self.slots.append({'slot': slot, 'original': original, 'address': address,
                               'code_hex': code.hex(), 'assembly': assembly})

    def restore(self):
        assert self.original is not None and not self.errors
        raw = ct.string_at(self.wram, 0x400000)
        desired = (self.original['flag_word'] & ~FLAG_MASK) | (FLAG_MASK if self.flag else 0)
        assert word(raw, self.original['actor_cell']) == ACTOR and word(raw, FLAG_WORD) == desired
        self.change(7401, 'restore', raw, {self.original['actor_cell']: self.original['actor'],
                                        FLAG_WORD: self.original['flag_word']})

    def save(self, require_complete=True):
        assert self.closed
        save(self.folder / 'events.json', {'rows': self.rows, 'fixture_writes': self.writes,
            'errors': self.errors, 'counts': self.counts, 'calls': self.calls,
            'callbacks': self.header[2], 'mismatches': self.header[3], 'original_inputs': self.original,
            'flag_value': self.flag, 'extra_observer_enabled': self.observed, 'filters': self.slots,
            'all_host_slots_restored_core_file_exact': True,
            'recorded_state_read_only_except_declared_install_and_restore': True,
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'producer_sha256': sha(Path(__file__).read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        if require_complete:
            assert not self.errors and not self.header[3] and len(self.writes) == 2


def run(case, flag, observed):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path(__file__), 'producer_sha256'),
                        (Path(pre['fixture_methods_source']), 'fixture_methods_sha256'),
                        (ROOT / 'source_contract.json', 'source_contract_sha256'),
                        (ROOT / 'inputs.json', 'inputs_sha256'), (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    folder = CAP / ('person_gender_v698_screen1_' + case)
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'flag': flag, 'extra_observer': observed,
        'synthetic_selected_Arcadius_and_story_flag_inputs_not_earned': True,
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()), 'producer_sha256': pre['producer_sha256']})
    loader, instances = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder, flag, observed)
            observer.install()
            instances.append(observer)
            original = core.retro_run
            original.restype = None
            def advance():
                observer.header[0] += 1
                if observer.header[0] == 7401:
                    observer.restore()
                original()
            core.retro_run = advance
        return core
    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', '7800',
        '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen', '--battery-save', pre['donor'],
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in instances:
            observer.close()
            observer.save(require_complete=False)
    for observer in instances:
        assert not observer.errors and not observer.header[3] and len(observer.writes) == 2
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['synthetic_Arcadius_Sailor_Info_flag_fixture'] = {'flag9': flag,
        'events': str(folder / 'observer/events.json'), 'events_sha256': sha((folder / 'observer/events.json').read_bytes()),
        'selected_lookup_and_flag_inputs_restored_before_exit': True,
        'earned_actor_recruitment_or_story_reveal': False}
    save(rp, report)
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    print('V698 terminal Sailor Info exception test:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case')
    parser.add_argument('--flag', type=int, choices=(0, 1))
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if args.case == 'prepare':
        prepare()
    else:
        assert args.flag is not None
        run(args.case, args.flag, not args.baseline)
