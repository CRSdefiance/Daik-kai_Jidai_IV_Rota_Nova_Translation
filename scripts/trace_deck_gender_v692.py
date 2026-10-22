"""Observe original Deck personnel gender setup without changing game state."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/deck_gender_v692')
ROM = Path('out/all_routes_combined_v685_candidate.nds')
DONORS = {
    'hodram': Path('E:/Rota Nova translations/Saves/hodram-copenhagen-rested-prepared-v461.dsv'),
    'maria': Path('E:/Rota Nova translations/Saves/maria-seoul-rested-v514.dsv'),
}
DONOR_HASHES = {
    'hodram': 'ea9265b93e599fcd7c95abe20ce8e68372cfe5d6355fe7b67d2fa1592dc37e73',
    'maria': '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f',
}
TARGETS = ((0x020157D8, 'entry'), (0x02015848, 'raw_sex'),
           (0x02015854, 'identity'), (0x020158DC, 'view_ready'), (0x0209C27C, 'return'))


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in ('work/clean.nds', ROM)]
    targets = []
    for pc, name in TARGETS:
        off = pc - 0x02000000
        assert arms[0][off:off + 4] == arms[1][off:off + 4]
        word = struct.unpack_from('<I', arms[0], off)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    # Original RTTI used by the caller's dynamic_cast.
    for addr, expected in ((0x02130264, b'5CView'), (0x02130D00, b'18CDeckPersonnelView')):
        off = addr - 0x02000000
        assert all(arm[off:off + len(expected) + 1] == expected + b'\0' for arm in arms)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    listings = {}
    for pc, size in ((0x020157D8, 0x220), (0x0209C1DC, 0xB0)):
        off = pc - 0x02000000
        listings[hex(pc)] = [f'{i.address:08X} {i.mnemonic} {i.op_str}'
                             for i in dis.disasm(arms[0][off:off + size], pc)]
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'CPSR_cpu_prefix_offset': 80, 'original_caller_class': '18CDeckPersonnelView',
        'original_caller': 0x0209C278, 'original_return': 0x0209C27C,
        'RTTI_name_address': 0x02130D00, 'disassembly': listings})
    scratch = ROOT / 'prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', read(ROOT / 'source_contract.json'))
    old = checks.ROOT
    checks.ROOT = scratch
    try:
        checks.main()
    finally:
        checks.ROOT = old
    controls = read(scratch / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 25 and len(controls['read_policy_cases']) == 8
    for name, path in DONORS.items():
        assert sha(path.read_bytes()) == DONOR_HASHES[name]
    prior = read('work/emulation_v193/crew_preparation_reload_v462/capture_report.json')
    inputs = list(prior['scripted_input_schedule'])
    inputs += [{'start': f, 'duration': 8, 'buttons': [button]} for f, button in
               ((7201, 'A'), (7601, 'DOWN'), (8001, 'DOWN'), (8401, 'UP'), (8801, 'UP'))]
    save(ROOT / 'pilot_inputs.json', inputs)
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('work/clean.nds'),
             Path('out/raphael_natural_v2_accepted_base.nds'))
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donors': {name: {'path': str(path), 'sha256': DONOR_HASHES[name]} for name, path in DONORS.items()},
        'donor_provenance': {'hodram': 'Normal saved Deck assignments/rest, retained V462 original saved-game evidence',
            'maria': 'V514 isolated selection unlock/bypass provenance; not an earned Maria unlock; no live code fixture here'},
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'no progress: previous turn answered status only; V691 was the last completed evidence checkpoint',
        'full_goal_complete': False})
    print('V692 original Deck parent/targets,25 host controls,donors pinned.', flush=True)


class Observer:
    def __init__(self, core, folder):
        self.folder = folder / 'observer'
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.slots = [], [], []
        self.closed, self.active, self.seen, self.counts = False, None, set(), {}

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                raw = ct.string_at(self.wram, 0x400000)
                dtcm, md = self.image.read(self.dtcm, 0x4000), self.image.read(self.md, 4)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                kind = target['name']
                self.counts[kind] = self.counts.get(kind, 0) + 1
                if kind == 'entry':
                    assert values[18] == 0x0209C27C and self.active is None
                    key = tuple(values[4:7])
                    self.active = {'key': key, 'selected': key not in self.seen,
                                   'number': self.counts[kind]}
                    self.seen.add(key)
                assert self.active is not None
                if self.active['selected']:
                    prefix = self.folder / f'event_{len(self.rows):03d}_{kind}_{frame:06d}'
                    ram_path, dtcm_path = prefix.with_suffix('.RAM.bin'), prefix.with_suffix('.DTCM.bin')
                    ram_path.write_bytes(raw)
                    dtcm_path.write_bytes(dtcm)
                    self.rows.append({'frame': frame, 'kind': kind, 'call_number': self.active['number'],
                        'entry_arguments': list(self.active['key']), 'CPU128_hex': cpu.hex(), 'MDTC_hex': md.hex(),
                        'RAM': str(ram_path), 'RAM_sha256': sha(raw), 'DTCM': str(dtcm_path), 'DTCM_sha256': sha(dtcm)})
                    assert len(self.rows) <= 500
                if kind == 'return':
                    self.active = None
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert self.image.read(self.dtcm, 0x4000) == dtcm and self.image.read(self.md, 4) == md
            except BaseException as exc:  # noqa: BLE001 - never throw across a native callback.
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


def run(case, donor, schedule, frames, observed):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['producer_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    donor_path = DONORS[donor]
    assert sha(donor_path.read_bytes()) == DONOR_HASHES[donor]
    folder = CAP / ('deck_gender_v692_' + case)
    assert not folder.exists()
    folder.mkdir()
    capture_frames = sorted({1, 60, 180, 1600, *range(2000, frames + 1, 400), frames})
    save(folder / 'run_contract.json', {'case': case, 'donor': donor, 'observed': observed,
        'schedule': str(schedule), 'schedule_sha256': sha(schedule.read_bytes()),
        'producer_sha256': pre['producer_sha256'], 'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'no_live_game_state_instruction_or_location_fixture': True,
        'Maria_donor_historical_selection_bypass_not_earned': donor == 'maria'})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if observed and str(path).lower().endswith('desmume_libretro.dll'):
            tracer = Observer(core, folder)
            tracer.install()
            installed.append(tracer)
            original = core.retro_run
            original.restype = None

            def advance():
                tracer.header[0] += 1
                original()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(frames), '--inputs-json', str(schedule), '--touchscreen',
        '--battery-save', str(donor_path), '--capture-every', '999999',
        '--capture-at', *map(str, capture_frames), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for tracer in installed:
            tracer.close()
    for tracer in installed:
        tracer.save()
    print('V692 terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'run'))
    parser.add_argument('--case')
    parser.add_argument('--donor', choices=DONORS)
    parser.add_argument('--schedule', type=Path)
    parser.add_argument('--frames', type=int)
    parser.add_argument('--observed', action='store_true')
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        run(args.case, args.donor, args.schedule, args.frames, args.observed)
