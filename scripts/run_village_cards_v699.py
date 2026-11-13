"""Exercise village cards through the real event-image parent using one CPU input."""

import argparse
import ctypes as ct
import struct
import sys
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, ImageReader
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_resource_dispatch_v668 import NativeMemory
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.verify_event_still_routing_v426 import CARDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_cards_v699/final')
BASE, PC, WORD = 0x02000000, 0x02028AA8, 0xE92D4070
FRAMES = (1, 60, 180, 1600, 2000, 2400, 2800, 3000, 3200, 3400,
          3600, 3700, 3800, 3900, 4000)


def plan(cpu, raw, dtcm, card, *, enabled=True, already=False):
    if len(cpu) != 128 or len(raw) != 0x400000 or len(dtcm) != 0x4000 or card not in CARDS:
        raise ValueError('Complete original CPU/RAM and a declared village card required')
    values = struct.unpack('<32I', cpu)
    if values[1:3] != (WORD, PC):
        raise ValueError('Original event parent entry/word required')
    if not enabled or already or values[5] != 84:
        return cpu, False
    if values[4] != 0x02276F88 or values[18] != 0x02029FB8:
        raise ValueError('Original script event-image caller and scene object required')
    if struct.unpack_from('<I', raw, 0x022796B0 - BASE)[0] != 3:
        raise ValueError('Original Maria captain state required')
    def guest(address, size):
        if 0x027E0000 <= address and address + size <= 0x027E4000:
            return dtcm[address - 0x027E0000:address - 0x027E0000 + size]
        if BASE <= address and address + size <= BASE + len(raw):
            return raw[address - BASE:address - BASE + size]
        raise ValueError('Bounded original RAM or DTCM operand required')
    instruction = struct.unpack('<I', guest(values[9] + 4, 4))[0]
    first, second = struct.unpack('<2H', guest(instruction, 4))
    if first & 0xFF00 != 0x4600 or not second & 0x8000 or second & 255 != 84:
        raise ValueError('Original direct image84 instruction required')
    options = (first >> 4 & 15, first >> 2 & 3, first & 3)
    if struct.unpack('<3I', guest(values[6], 12)) != options:
        raise ValueError('Original scene options required')
    after = bytearray(cpu)
    struct.pack_into('<I', after, 20, card)
    return bytes(after), True


def prepare():
    ROOT.mkdir()
    prior = read('work/analysis/maria_opening_v674/preflight.json')
    manifest = deepcopy(read(prior['manifest']))
    manifest.update(production_ROM=str(ROM), production_ROM_sha256=sha(ROM.read_bytes()),
        current_test_scope='Eight village cards at original event parent; selected CPU argument fixture, no earned scene use')
    save(ROOT / 'unlock_manifest.json', manifest)
    save(ROOT / 'inputs.json', read('work/analysis/maria_opening_v674/dispatch_inputs.json'))
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    assert all(a[PC - BASE:PC - BASE + 4] == struct.pack('<I', WORD) for a in arms)
    assert arms[0][0x28AA8:0x28BA8] == arms[1][0x28AA8:0x28BA8]
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    native_base, table = tables(core)
    index = ((WORD >> 16) & 0xFF0) | ((WORD >> 4) & 15)
    source = {'targets': [{'PC': PC, 'word': WORD, 'name': 'original_event_parent',
        'instruction_index': index,
        'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - native_base}],
        'interpreter_table': table, 'original_request': 84, 'source_cards': list(CARDS)}
    save(ROOT / 'source_contract.json', source)
    old_root = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = old_root
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'donor': prior['donor'], 'donor_sha256': prior['donor_sha256'],
        'manifest': str(ROOT / 'unlock_manifest.json'),
        'manifest_sha256': sha((ROOT / 'unlock_manifest.json').read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V698 actual Sailor Info symbol and80 plaque crops; replay gaps retained',
        'full_goal_complete': False})
    print('V699 original event-image fixture and unchanged release pinned.', flush=True)


class Fixture:
    def __init__(self, core, folder, card, enabled):
        self.core, self.folder, self.card, self.enabled = core, Path(folder), card, enabled
        self.folder.mkdir()
        self.image, self.native = ImageReader(core), NativeMemory()
        self.cpu = self.image.anchor('9REG', 4, 16) - 16
        self.regions = {tag: (self.image.anchor(tag, 1, n), n) for tag, n in
                        (('WRAM', 0x400000), ('DTCM', 0x4000), ('ITCM', 0x8000))}
        self.rows, self.errors, self.applied, self.closed = [], [], False, False
        self.header = (ct.c_uint32 * 4)(0, 1, 0, 0)
        source = read(ROOT / 'source_contract.json')
        target = source['targets'][0]
        self.slot = core._handle + source['interpreter_table']['RVA'] + target['instruction_index'] * 8
        self.original = self.image.qword(self.slot)
        assert self.original == core._handle + target['handler_RVA']

        def callback(frame):
            before = None
            try:
                assert len(self.rows) < 32
                before = ct.string_at(self.cpu, 128)
                regions = {tag: ct.string_at(a, n) for tag, (a, n) in self.regions.items()}
                after, applied = plan(before, regions['WRAM'], regions['DTCM'], card, enabled=enabled, already=self.applied)
                directory = self.folder / f'entry_{len(self.rows):02d}_{frame:06d}'
                directory.mkdir()
                files = {}
                for tag, blob in {'CPU_before': before, 'CPU_after': after, **regions}.items():
                    path = directory / (tag + '.bin')
                    path.write_bytes(blob)
                    files[tag] = {'path': str(path), 'sha256': sha(blob)}
                if applied:
                    ct.memmove(self.cpu + 20, after[20:24], 4)
                assert ct.string_at(self.cpu, 128) == after
                assert all(ct.string_at(a, n) == regions[tag] for tag, (a, n) in self.regions.items())
                self.applied |= applied
                self.rows.append({'frame': frame, 'applied': applied, 'card': card, 'files': files,
                    'only_R1_changed_full_WRAM_DTCM_ITCM_and_other_CPU_bytes_exact': True})
                print('V699 event parent:', frame, 'card', card, 'applied', applied, flush=True)
            except BaseException as exc:  # noqa: BLE001 - do not unwind through native code.
                if before is not None:
                    ct.memmove(self.cpu, before, 128)
                    save(self.folder / 'failure.json', {'frame': frame, 'CPU128_hex': before.hex(),
                        'error': repr(exc)})
                self.errors.append(repr(exc))
                self.header[1] = 0
        self.callback = ct.WINFUNCTYPE(None, ct.c_uint32)(callback)
        self.address = self.native.alloc(None, 4096, 0x3000, 0x04)
        self.code, self.assembly = assemble(self.cpu, ct.addressof(self.header),
            ct.cast(self.callback, ct.c_void_p).value, self.original, source['targets'], self.address)
        assert len(self.code) < 4096
        ct.memmove(self.address, self.code, len(self.code))
        old = ct.c_uint32()
        assert self.native.protect(self.address, 4096, 0x20, ct.byref(old))
        assert self.native.flush(self.native.process, self.address, len(self.code))

    def install(self):
        assert self.image.qword(self.slot) == self.original
        self.native.pointer(self.slot, self.address)

    def close(self):
        if not self.closed:
            self.native.pointer(self.slot, self.original)
            self.closed = True
        assert self.image.qword(self.slot) == self.original and sha(CORE.read_bytes()) == CORE_SHA

    def save(self):
        assert self.closed
        save(self.folder / 'fixture.json', {'rows': self.rows, 'errors': self.errors,
            'enabled': self.enabled, 'applied': self.applied, 'card': self.card,
            'callbacks': self.header[2], 'mismatches': self.header[3],
            'host_slot_restored_core_file_exact': True, 'code_hex': self.code.hex(), 'assembly': self.assembly,
            'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
        assert self.native.free(self.address, 0, 0x8000)


def run(card, disabled):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path(__file__), 'producer_sha256'), (ROOT / 'source_contract.json', 'source_contract_sha256'),
                        (ROOT / 'inputs.json', 'inputs_sha256'), (Path(pre['manifest']), 'manifest_sha256'),
                        (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    case = 'disabled' if disabled else f'card{card}'
    folder = CAP / ('village_cards_v699_final_' + case)
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'producer_sha256': pre['producer_sha256'], 'isolated_image_request_not_ordinary_village_scene': not disabled})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            fixture = Fixture(core, folder / 'fixture', card, not disabled)
            fixture.install()
            original_run = core.retro_run
            original_run.restype = None
            def advance():
                fixture.header[0] += 1
                original_run()
            core.retro_run = advance
            installed.append(fixture)
        return core
    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', '4000',
        '--inputs-json', str(ROOT / 'inputs.json'), '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', pre['manifest'], '--capture-every', '999999',
        '--capture-at', *map(str, FRAMES), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for fixture in installed:
            fixture.close()
            fixture.save()
    assert len(installed) == 1 and not installed[0].errors and not installed[0].header[3]
    assert installed[0].applied == (not disabled)
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['isolated_event_request_fixture'] = {'enabled': not disabled, 'requested_card': card,
        'receipt': str(folder / 'fixture/fixture.json'),
        'receipt_sha256': sha((folder / 'fixture/fixture.json').read_bytes()),
        'ordinary_scene_reachability_or_earned_village_trigger_verified': False}
    if not disabled:
        report['synthetic_original_event_image_argument_fixture'] = True
    save(rp, report)
    print('V699 terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--card', type=int, choices=CARDS, default=168)
    parser.add_argument('--disabled', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
    else:
        run(args.card, args.disabled)
