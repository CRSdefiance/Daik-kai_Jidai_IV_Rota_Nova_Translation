"""Exercise original Arcadius gender selection using declared isolated UI inputs."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.probe_button_prompt_native import call, machine
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.trace_deck_gender_v692 import DONOR_HASHES, DONORS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/gender_exception_v697')
BASE, FLAG_OBJECT, FLAG_WORD = 0x02000000, 0x02276F90, 0x02276F94
PARENT, VIEW = 0x0218BD98, 0x0218A644
ACTOR, FLAG_MASK = 8, 1 << 9
TARGETS = ((0x0209C1DC, 'selection_entry'), (0x020157D8, 'helper_entry'),
    (0x02015848, 'raw_gender'), (0x02015854, 'identity'), (0x02023C60, 'flag_entry'),
    (0x02015868, 'flag_return'), (0x020158DC, 'view_ready'),
    (0x0209C27C, 'helper_return'), (0x02014E2C, 'gender_draw'))


def word(raw, address):
    return struct.unpack_from('<I', raw, address - BASE)[0]


def prepare():
    ROOT.mkdir()
    assert sha(CORE.read_bytes()) == CORE_SHA
    native_base, table = tables(CORE.read_bytes())
    current, clean = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    targets = []
    for pc, name in TARGETS:
        at = pc - BASE
        assert current[at:at + 4] == clean[at:at + 4]
        value = struct.unpack_from('<I', current, at)[0]
        index = ((value >> 16) & 0xFF0) | ((value >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': value, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', CORE.read_bytes(), table['file_offset'] + index * 8)[0] - native_base})
    assert current[0x157D8:0x15948] == clean[0x157D8:0x15948]
    assert current[0x23C60:0x23CE4] == clean[0x23C60:0x23CE4]
    assert struct.unpack_from('<I', current, 0x1593C)[0] == FLAG_OBJECT
    name_ptr = struct.unpack_from('<I', current, 0x120B80 + ACTOR * 32)[0]
    assert current[name_ptr - BASE:name_ptr - BASE + 9] == b'Arcadius\0'
    source = {'targets': targets, 'interpreter_table': table, 'flag_object': FLAG_OBJECT,
        'flag_word': FLAG_WORD, 'flag_index': 9, 'flag_mask': FLAG_MASK,
        'actual_selected_actor': ACTOR, 'actual_source_name': 'Arcadius',
        'original_getter': 0x02023C60, 'original_setter': 0x02023C8C,
        'only_lookup_word_and_one_flag_bit_in_private_test_process': True}
    save(ROOT / 'source_contract.json', source)
    scratch = ROOT / 'prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', source)
    old = checks.ROOT
    checks.ROOT = scratch
    try:
        checks.main()
    finally:
        checks.ROOT = old
    assert len(read(scratch / 'native_prefix_controls.json')['native_host_cases']) == 45
    events = read(CAP / 'room_gender_v694_hodram_ITCM/observer/events.json')
    captured = next(r for r in events['rows'] if r['kind'] == 'gender_entry')
    raw = Path(captured['RAM']).read_bytes()
    assert sha(raw) == captured['RAM_sha256']
    u = machine(current)
    u.mem_write(BASE, raw)
    call(u, 0xCB184, ())
    people = u.reg_read(UC_ARM_REG_R0)
    record = people + 4 + ACTOR * 32
    call(u, 0x7EE08, (record,))
    assert u.reg_read(UC_ARM_REG_R0) == ACTOR
    call(u, 0x7E9B8, (record,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    flag_controls = []
    original_word = word(raw, FLAG_WORD)
    for value in (0, 1):
        u.mem_write(BASE, raw)
        before = bytes(u.mem_read(BASE, 0x400000))
        call(u, 0x23C8C, (FLAG_OBJECT, 9, value))
        expected = bytearray(before)
        desired = (original_word & ~FLAG_MASK) | (FLAG_MASK if value else 0)
        struct.pack_into('<I', expected, FLAG_WORD - BASE, desired)
        assert bytes(u.mem_read(BASE, 0x400000)) == expected
        call(u, 0x23C60, (FLAG_OBJECT, 9))
        assert u.reg_read(UC_ARM_REG_R0) == (FLAG_MASK if value else 0)
        flag_controls.append({'set': value, 'word': desired, 'native_getter_return': u.reg_read(UC_ARM_REG_R0),
                              'whole_main_RAM_only_declared_flag_bit_changed': True})
    save(ROOT / 'native_input_controls.json', {'actor': ACTOR, 'actual_name': 'Arcadius',
        'original_identity': ACTOR, 'original_raw_gender': 1, 'person_record': record,
        'original_flag_setter_and_getter': flag_controls,
        'source_RAM': captured['RAM'], 'source_RAM_sha256': captured['RAM_sha256']})
    inputs = [r for r in read('work/analysis/room_gender_v694/inputs.json') if r['start'] <= 8401]
    inputs.append({'start': 10001, 'duration': 8, 'buttons': ['B']})
    save(ROOT / 'inputs.json', inputs)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('work/clean.nds'),
             Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donor': str(DONORS['hodram']), 'donor_sha256': DONOR_HASHES['hodram'],
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V696 final comic guard and byte-exact complete V692 rebuild',
        'full_goal_complete': False})
    print('V697 Arcadius identity/raw-gender, original flag9 setter/getter and45 host controls pinned.', flush=True)


class Observer:
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
        self.original, self.active, self.completed, self.closed = None, False, False, False
        self.seen = set()

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                kind = target['name']
                self.counts[kind] = self.counts.get(kind, 0) + 1
                relevant = False
                if kind == 'selection_entry':
                    view, index = values[4:6]
                    if view != VIEW or not 8400 <= frame < 10001:
                        return
                    raw = ct.string_at(self.wram, 0x400000)
                    if word(raw, view + 0x3DC) != PARENT or word(raw, PARENT + 0x44) != 5:
                        return
                    if self.original is None:
                        assert 8400 <= frame < 10001 and index == 0 and word(raw, view + 0x354) == 1
                        actor_cell = view + 0x18 + index * 4
                        assert word(raw, actor_cell) == 1
                        self.original = {'actor_cell': actor_cell, 'actor': 1, 'flag_word': word(raw, FLAG_WORD)}
                        desired = (self.original['flag_word'] & ~FLAG_MASK) | (FLAG_MASK if flag else 0)
                        self.change(frame, 'install', raw, {actor_cell: ACTOR, FLAG_WORD: desired})
                        relevant = True
                    else:
                        assert word(raw, self.original['actor_cell']) == ACTOR
                elif self.original is not None and frame < 10001:
                    if kind == 'helper_entry':
                        assert values[6] == ACTOR
                        self.active = True
                    if kind == 'gender_draw':
                        relevant = self.completed and values[5] == 0x0218DFCC
                    elif kind == 'flag_entry':
                        relevant = self.active and values[18] == 0x02015868
                    else:
                        relevant = self.active
                    if kind == 'helper_return' and self.active:
                        self.active, self.completed = False, True
                if relevant and observed and kind not in self.seen:
                    raw, dtcm, itcm = [ct.string_at(a, n) for a, n in
                        ((self.wram, 0x400000), (self.dtcm, 0x4000), (self.itcm, 0x8000))]
                    row = {'kind': kind, 'frame': frame, 'CPU128_hex': cpu.hex()}
                    for name, data in (('RAM', raw), ('DTCM', dtcm), ('ITCM', itcm)):
                        path = self.folder / f'{kind}_{frame:06d}.{name}.bin'
                        path.write_bytes(data)
                        row[name], row[name + '_sha256'] = str(path), sha(data)
                    self.rows.append(row)
                    self.seen.add(kind)
                    assert ct.string_at(self.wram, len(raw)) == raw
                    assert ct.string_at(self.dtcm, len(dtcm)) == dtcm and ct.string_at(self.itcm, len(itcm)) == itcm
                assert ct.string_at(self.cpu, 128) == cpu
            except BaseException as exc:  # noqa: BLE001 - native callbacks must not unwind.
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

    def change(self, frame, kind, before, values):
        cpu, dtcm, itcm = [ct.string_at(a, n) for a, n in ((self.cpu, 128), (self.dtcm, 0x4000), (self.itcm, 0x8000))]
        expected = bytearray(before)
        for address, value in values.items():
            struct.pack_into('<I', expected, address - BASE, value)
            ct.memmove(self.wram + address - BASE, struct.pack('<I', value), 4)
        after = ct.string_at(self.wram, 0x400000)
        assert after == expected
        assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.dtcm, 0x4000) == dtcm
        assert ct.string_at(self.itcm, 0x8000) == itcm
        row = {'frame': frame, 'kind': kind, 'declared_word_values': values,
               'CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact': True}
        for name, data in (('before', before), ('after', after)):
            path = self.folder / f'fixture_{kind}_{name}.RAM.bin'
            path.write_bytes(data)
            row[name], row[name + '_sha256'] = str(path), sha(data)
        self.writes.append(row)

    def restore(self):
        assert self.original is not None and not self.errors
        raw = ct.string_at(self.wram, 0x400000)
        desired = (self.original['flag_word'] & ~FLAG_MASK) | (FLAG_MASK if self.flag else 0)
        assert word(raw, self.original['actor_cell']) == ACTOR and word(raw, FLAG_WORD) == desired
        self.change(10001, 'restore', raw, {self.original['actor_cell']: self.original['actor'],
                                         FLAG_WORD: self.original['flag_word']})

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
        save(self.folder / 'events.json', {'rows': self.rows, 'fixture_writes': self.writes, 'errors': self.errors,
            'counts': self.counts, 'callbacks': self.header[2], 'mismatches': self.header[3],
            'original_inputs': self.original, 'all_host_slots_restored_core_file_exact': True,
            'recorded_state_read_only_except_declared_install_and_restore': True,
            'synthetic_actor8_lookup_and_flag9_fixture_not_earned_recruitment_or_story': True,
            'flag_value': self.flag, 'extra_observer_enabled': self.observed, 'filters': self.slots,
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'producer_sha256': sha(Path(__file__).read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and len(self.writes) == 2


def run(case, flag, observed):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['producer_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert pre['inputs_sha256'] == sha((ROOT / 'inputs.json').read_bytes())
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder = CAP / ('gender_exception_v697_' + case)
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'flag_value': flag, 'extra_observer': observed,
        'synthetic_selected_actor_lookup_and_story_flag_inputs': True,
        'producer_sha256': pre['producer_sha256'], 'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes())})
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
                if observer.header[0] == 10001:
                    observer.restore()
                original()
            core.retro_run = advance
        return core
    ct.CDLL = loaded
    frames = [1, 60, 180, 1600, *range(2000, 10801, 400)]
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', '10800',
        '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen', '--battery-save', pre['donor'],
        '--capture-every', '999999', '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in instances:
            observer.close()
    for observer in instances:
        observer.save()
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['synthetic_actor8_gender_story_flag_fixture'] = {'flag9': flag,
        'events': str(folder / 'observer/events.json'),
        'events_sha256': sha((folder / 'observer/events.json').read_bytes()),
        'actor_and_flag_inputs_restored_before_exit': True, 'earned_recruitment_or_story_progress': False}
    save(rp, report)
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    print('V697 terminal isolated Arcadius flag test:', case, flush=True)


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
