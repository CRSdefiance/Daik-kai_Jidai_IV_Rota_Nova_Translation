"""Observe filename, numeric-ID and direct-range entries without game-state writes."""

import argparse
import ctypes as ct
import struct
import sys
from collections import Counter
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as prefix
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, SOURCE, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble, main_read
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.research_graphics_file_open_v301 import scan
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/file_ids_v683')
ROM = Path('out/all_routes_combined_v678_candidate.nds')
TARGETS = ((0x020DED50, 'filename'), (0x020DEDA0, 'numeric_ID'), (0x020DEE1C, 'direct_range'))


def mapped_read(raw, dtcm, dtcm_base, address, length):
    """ARM9 CPU read policy: configured DTCM takes priority over RAM mirrors."""
    if len(dtcm) != 0x4000 or dtcm_base & 0x3FFF or length < 0:
        raise ValueError('Exact aligned DTCM source and nonnegative length required')
    if dtcm_base <= address < dtcm_base + 0x4000:
        offset = address - dtcm_base
        if offset + length > 0x4000:
            raise ValueError('Read crosses the DTCM boundary')
        return dtcm[offset:offset + length]
    if address < dtcm_base and address + length > dtcm_base:
        raise ValueError('Read crosses into DTCM')
    return main_read(raw, address, length)


def controls():
    source = read(ROOT / 'source_contract.json')
    mmu = SOURCE / 'MMU.h'
    text = mmu.read_text(encoding='utf-8')
    assert 'if((addr&(~0x3FFF)) == MMU.DTCMRegion)' in text
    assert 'return T1ReadByte(MMU.ARM9_DTCM, addr & 0x3FFF);' in text
    source['ARM9_CPU_read_policy'] = {'DTCM_precedes_main_RAM_mirrors': True,
        'MMU_header': str(mmu), 'MMU_header_sha256': sha(mmu.read_bytes()),
        'SFORMAT_source': str(SOURCE / 'saves.cpp'),
        'SFORMAT_source_sha256': sha((SOURCE / 'saves.cpp').read_bytes()),
        'DTCM_anchor': ['DTCM', 1, 0x4000], 'DTCM_base_anchor': ['MDTC', 4, 1]}
    save(ROOT / 'source_contract.json', source)
    old_root, old_assemble = prefix.ROOT, prefix.assemble

    def grouped(cpu, header, callback, original_handler, selected, address):
        group = [t for t in source['targets'] if t['instruction_index'] == selected[0]['instruction_index']]
        return assemble(cpu, header, callback, original_handler, group, address)

    prefix.ROOT, prefix.assemble = ROOT, grouped
    try:
        prefix.main()
    finally:
        prefix.ROOT, prefix.assemble = old_root, old_assemble
    result = read(ROOT / 'native_prefix_controls.json')
    result['current_trace_source_sha256'] = sha(Path(__file__).read_bytes())
    result['actual_shared_target_groups_tested'] = True
    ram, dtcm, base = b'\x35' * 0x400000, bytes(range(256)) * 64, 0x027E0000
    rows = []
    for address, length, valid, is_dtcm in (
        (base, 16, True, True), (base + 0x3FE0, 32, True, True),
        (base + 0x3FFF, 1, True, True), (base + 0x3FFF, 2, False, True),
        (base - 1, 2, False, False), (base - 16, 16, True, False),
        (base + 0x4000, 16, True, False), (0x02001000, 128, True, False),
        (0x02401000, 128, True, False), (0x03000000, 1, False, False)):
        try:
            actual = mapped_read(ram, dtcm, base, address, length)
        except ValueError:
            assert not valid
        else:
            assert valid
            expected = dtcm[address - base:address - base + length] if is_dtcm else b'\x35' * length
            assert actual == expected
            if is_dtcm and length:
                assert actual != main_read(ram, address, length)
        rows.append({'address': address, 'length': length, 'accepted': valid, 'DTCM_selected': is_dtcm and valid})
    result['DTCM_precedence_boundary_and_mirror_cases'] = rows
    save(ROOT / 'native_prefix_controls.json', result)
    print('V68315 grouped prefixes,8 mirror and10 DTCM precedence/boundary controls pass.', flush=True)


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert arm[0xDED50:0xDEEE0] == original[0xDED50:0xDEEE0]
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    targets = []
    for pc, name in TARGETS:
        word = struct.unpack_from('<I', arm, pc - 0x02000000)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    census = scan(rom, arm, tuple(pc for pc, _ in TARGETS))
    old = scan(clean, original, tuple(pc for pc, _ in TARGETS))
    assert census['aligned_ARM_BL_calls'] == old['aligned_ARM_BL_calls']
    assert not census['literal_pointers'] and not census['Thumb_calls']
    # Pin exact original bytes around every declared direct caller, not names
    # inferred from the surrounding SDK address range.
    for row in census['aligned_ARM_BL_calls']:
        assert row['unit'] == 'main-0'
        at = row['address'] - 0x02000000
        assert arm[at - 32:at + 4] == original[at - 32:at + 4]
    source = {'targets': targets, 'interpreter_table': table, 'core_sha256': CORE_SHA,
        'source_exact_SDK_range': [0xDED50, 0xDEEE0], 'direct_caller_census': census,
        'original_assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'file_IDs': {str(index): path for path, index in rom.path_map().items()},
        'numeric_entry_registers': ['FSFile', 'FSArchive', 'file_ID'],
        'direct_range_registers': ['FSFile', 'FSArchive', 'begin', 'end'],
        'direct_range_fifth_stack_argument_is_file_ID': True}
    save(ROOT / 'source_contract.json', source)
    old_root, old_assemble = prefix.ROOT, prefix.assemble

    def grouped(cpu, header, callback, original_handler, selected, address):
        group = [t for t in targets if t['instruction_index'] == selected[0]['instruction_index']]
        return assemble(cpu, header, callback, original_handler, group, address)

    prefix.ROOT, prefix.assemble = ROOT, grouped
    try:
        prefix.main()
    finally:
        prefix.ROOT, prefix.assemble = old_root, old_assemble
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15
    controls['current_trace_source_sha256'] = sha(Path(__file__).read_bytes())
    controls['actual_shared_target_groups_tested'] = True
    save(ROOT / 'native_prefix_controls.json', controls)
    prior = read('work/analysis/file_requests_v681/run_cases.json')
    for case in prior:
        p = CAP / f'file_requests_v681_{case}_baseline/capture_report.json'
        assert p.exists() and read(p)['ROM_sha256'] == sha(ROM.read_bytes())
        prior[case]['retained_unmodified_baseline_report'] = str(p)
        prior[case]['retained_baseline_report_sha256'] = sha(p.read_bytes())
    save(ROOT / 'run_cases.json', prior)
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json',
             'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'previous_goal_turn_classification': 'progress: V682 full Save/Load evidence and121-file archive verified',
        'full_goal_complete': False})
    print('V683 original three SDK entries, direct callers, file IDs and grouped prefix controls bound.', flush=True)


class Observer:
    def __init__(self, core, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.native, self.image = NativeMemory(), ImageReader(core)
        self.source = read(ROOT / 'source_contract.json')
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.wram = self.image.anchor('WRAM', 1, 0x400000)
        self.dtcm = self.image.anchor('DTCM', 1, 0x4000)
        self.dtcm_base = self.image.anchor('MDTC', 4, 1)
        assert self.image.anchor('9INS', 4, 1) == self.cpu + 4
        assert self.image.anchor('9INA', 4, 1) == self.cpu + 8
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        self.rows, self.errors, self.slots = [], [], []
        self.closed = False

        def callback(frame):
            try:
                assert len(self.rows) < 20000
                cpu, raw = ct.string_at(self.cpu, 128), ct.string_at(self.wram, 0x400000)
                dtcm = self.image.read(self.dtcm, 0x4000)
                base_raw = self.image.read(self.dtcm_base, 4)
                base = struct.unpack('<I', base_raw)[0]

                def memory(address, length):
                    return mapped_read(raw, dtcm, base, address, length)

                values = struct.unpack('<32I', cpu)
                target = next(t for t in self.source['targets'] if t['PC'] == values[2])
                assert target['word'] == values[1]
                row = {'frame': frame, 'kind': target['name'], 'CPU128_hex': cpu.hex(),
                    'args': list(values[4:8]), 'LR': values[18],
                    'entire_before_WRAM_sha256': sha(raw),
                    'DTCM_base': base, 'DTCM16384_hex': dtcm.hex(), 'DTCM_sha256': sha(dtcm),
                    'file_object64_hex': memory(values[4], 64).hex(),
                    'stack32_hex': memory(values[17], 32).hex()}
                if target['name'] == 'filename':
                    text = memory(values[5], 128)
                    assert b'\0' in text
                    row['filename128_hex'], row['filename'] = text.hex(), text.split(b'\0')[0].decode('ascii')
                else:
                    row['archive128_hex'] = memory(values[5], 128).hex()
                    if target['name'] == 'numeric_ID':
                        row['file_ID'] = values[6]
                    else:
                        row['file_ID'] = struct.unpack_from('<I', bytes.fromhex(row['stack32_hex']))[0]
                        row['byte_range'] = list(values[6:8])
                assert ct.string_at(self.cpu, 128) == cpu and ct.string_at(self.wram, 0x400000) == raw
                assert self.image.read(self.dtcm, 0x4000) == dtcm
                assert self.image.read(self.dtcm_base, 4) == base_raw
                row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observation'] = True
                row['entire_DTCM_and_configuration_unchanged_by_observation'] = True
                self.rows.append(row)
            except BaseException as exc:  # noqa: BLE001 - native callback boundary.
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
        save(self.folder / 'SDK_entries.json', {'rows': self.rows, 'errors': self.errors,
            'callbacks': self.header[2], 'mismatches': self.header[3],
            'all_opcode_slots_restored_and_core_file_unchanged': True,
            'trace_source_sha256': sha(Path(__file__).read_bytes()),
            'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
            'filters': self.slots, 'anchors': self.image.entries, 'full_goal_complete': False})
        for row in self.slots:
            assert self.native.free(row['address'], 0, 0x8000)
        assert not self.errors and not self.header[3]


def run(case):
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_cases.json')[case]
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert read(ROOT / 'native_prefix_controls.json')['current_trace_source_sha256'] == sha(Path(__file__).read_bytes())
    folder = CAP / f'file_ids_v683_v2_{case}'
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'config': config,
        'inputs_sha256': sha(Path(config['inputs']).read_bytes()),
        'trace_source_sha256': sha(Path(__file__).read_bytes()),
        'reuses_retained_V681_unmodified_core_baseline': True})
    loader, installed = ct.CDLL, []

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer')
            observer.install()
            installed.append(observer)
            original = core.retro_run
            original.restype = None

            def advance():
                observer.next_frame()
                original()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']), '--dump-ram']
    if case == 'gallery':
        sys.argv += ['--battery-save', config['save'], '--allow-gallery-fixtures',
                     '--gallery-save-fixture-manifest', config['fixture_manifest']]
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V683 terminal:', case, dict(Counter(r['kind'] for r in installed[0].rows)), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'controls', 'ordinary', 'gallery'))
    action = parser.parse_args().action
    if action == 'prepare':
        prepare()
    elif action == 'controls':
        controls()
    else:
        run(action)


if __name__ == '__main__':
    main()
