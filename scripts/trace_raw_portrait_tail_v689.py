"""Observe original raw portrait read boundaries and the following chooser loop."""

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
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/raw_portrait_tail_v689')
ROM = Path('out/all_routes_combined_v685_candidate.nds')
FOLDER = CAP / 'raw_portrait_tail_v689_current'


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists() and not FOLDER.exists()
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'),
             Path('work/clean.nds'))
    baseline_path = CAP / 'story_percent_v685_ordinary/capture_report.json'
    baseline = read(baseline_path)
    assert baseline['ROM_sha256'] == sha(ROM.read_bytes())
    save(ROOT / 'inputs.json', baseline['scripted_input_schedule'])
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in ('work/clean.nds', ROM)]
    targets = []
    for pc, name in ((0x0204704C, 'raw_entry'), (0x0209EDEC, 'raw_return'), (0x0209EE94, 'loop_complete')):
        offset = pc - 0x02000000
        assert arms[0][offset:offset + 4] == arms[1][offset:offset + 4]
        word = struct.unpack_from('<I', arms[0], offset)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'CPSR_cpu_prefix_offset': 80,
        'CPSR_source': 'work/analysis/ending_gpu_state_v630/desmume-95b4d79/desmume/src/armcpu.h'})
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
    assert len(controls['native_host_cases']) == 15
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'baseline_report': str(baseline_path), 'baseline_report_sha256': sha(baseline_path.read_bytes()),
        'older_4000_frame_baseline': str(CAP / 'file_requests_v681_ordinary_baseline/capture_report.json'),
        'inputs': str(ROOT / 'inputs.json'), 'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'capture_frames': sorted({s['frame'] for s in baseline['frames_captured'] if s['frame'] <= 4000}),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V688 owner boundaries/alias limits recorded and verified',
        'full_goal_complete': False})
    print('V689 original raw-entry/return/loop targets and15 host controls pinned.', flush=True)


class Observer:
    def __init__(self, core):
        self.folder = FOLDER / 'observer'
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm, self.md = self.image.anchor('DTCM', 1, 0x4000), self.image.anchor('MDTC', 4, 1)
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.slots = [], [], []
        self.closed, self.ignored = False, 0

        def callback(frame):
            try:
                cpu = ct.string_at(self.cpu, 128)
                raw = ct.string_at(self.wram, 0x400000)
                dtcm, md = self.image.read(self.dtcm, 0x4000), self.image.read(self.md, 4)
                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                if target['name'] != 'raw_entry' or values[18] == 0x0209EDEC:
                    prefix = self.folder / f'event_{len(self.rows):02d}_{target["name"]}_{frame:06d}'
                    ram_path, dtcm_path = prefix.with_suffix('.RAM.bin'), prefix.with_suffix('.DTCM.bin')
                    ram_path.write_bytes(raw)
                    dtcm_path.write_bytes(dtcm)
                    self.rows.append({'frame': frame, 'kind': target['name'], 'CPU128_hex': cpu.hex(),
                        'MDTC_hex': md.hex(), 'RAM': str(ram_path), 'RAM_sha256': sha(raw),
                        'DTCM': str(dtcm_path), 'DTCM_sha256': sha(dtcm)})
                    assert len(self.rows) <= 9
                else:
                    self.ignored += 1
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
            'callbacks': self.header[2], 'ignored': self.ignored, 'mismatches': self.header[3],
            'CPU_WRAM_DTCM_configuration_unchanged_at_every_callback': True,
            'all_host_slots_restored_core_file_exact': True, 'filters': self.slots,
            'anchors': self.image.entries, 'producer_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes())})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3] and len(self.rows) == 9


def run():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['producer_sha256'] == sha(Path(__file__).read_bytes())
    assert not FOLDER.exists()
    FOLDER.mkdir()
    save(FOLDER / 'run_contract.json', {'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'producer_sha256': pre['producer_sha256'], 'no_save_or_live_gameplay_fixture': True})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core)
            observer.install()
            installed.append(observer)
            original = core.retro_run
            original.restype = None

            def advance():
                observer.header[0] += 1
                original()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
        '--frames', '4000', '--inputs-json', pre['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, pre['capture_frames']), '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V689 actual four raw reads, four returns and loop boundary terminal.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'run'))
    if parser.parse_args().action == 'prepare':
        prepare()
    else:
        run()
