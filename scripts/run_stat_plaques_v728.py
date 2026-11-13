"""Current normal plaque screens with declared six-byte stat display fixtures.

The shared harness and core DLL are unchanged. A process-local Python core proxy
calls every original retro_run once, changing only six actor bytes at two exact
frame boundaries. Original saves and ROMs are never modified.
"""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.inspect_desmume_state_v249 import export
from scripts.prepare_plaque_review_v714 import ROOT as PREVIOUS
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/stat_plaques_v728')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
FRAMES = (4300, 5500, 5799, 6300, 6700, 7100, 7900, 8300, 8700, 9100, 9500)


def actor_stats(arm, raw):
    assert len(raw) == 0x400000
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB184, ())
    store = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x7F244, ())
    captain = u.reg_read(UC_ARM_REG_R0)
    assert captain == 1, ('Unexpected test-save captain', captain)
    offset = struct.unpack_from('<I', arm, 0x80ABC)[0]
    assert offset == 0x19E4
    actor = store + offset
    assert BASE <= actor and actor + 32 <= BASE + len(raw)
    vtable = struct.unpack('<I', u.mem_read(actor, 4))[0]
    name_getter = struct.unpack('<I', u.mem_read(vtable + 0x20, 4))[0]
    call(u, name_getter - BASE, (actor,))
    name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 96)).split(b'\0')[0].decode('cp932')
    assert name == 'Hodram', ('Copied saved captain profile differs', name)
    values = []
    for attribute in range(6):
        call(u, 0x7E944, (actor, attribute))
        value = u.reg_read(UC_ARM_REG_R0)
        assert value == raw[actor + 8 + attribute - BASE]
        values.append(value)
    return actor, values


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    prior = read(PREVIOUS / 'preflight.json')
    donor = Path(prior['donor'])
    assert sha(donor.read_bytes()) == prior['donor_sha256']
    copied = ROOT / 'copied_source_for_stat_checks.dsv'
    copy(donor, copied)
    inputs = read(prior['inputs']) + [
        {'start': frame, 'duration': 8, 'buttons': [button]}
        for frame, button in ((7201, 'B'), (7601, 'A'), (8001, 'B'),
                              (8401, 'B'), (8801, 'B'), (9201, 'B'))]
    save(ROOT / 'inputs.json', inputs)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges = [(0x7E944, 0x7E950), (0x80A84, 0x80AC0), (0xCEF18, 0xCEFD0)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in ranges)
    assert sha(harness.CORE.read_bytes()) == CORE_SHA
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'ARM9_sha256': sha(arm), 'original_getter_actor_resolution_and_bar_scaler_ranges': ranges,
        'donor': str(copied), 'donor_sha256': sha(copied.read_bytes()),
        'original_donor': str(donor), 'original_donor_sha256': sha(donor.read_bytes()),
        'saved_captain_profile_name': 'Hodram', 'locked_localization_name': 'Joakim',
        'saved_profile_not_renamed_by_this_test': True,
        'inputs': str(ROOT / 'inputs.json'), 'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'shared_harness_sha256': sha(Path('scripts/headless_desmume_v193.py').read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'capture_frames': list(FRAMES), 'last_frame': 9500, 'fixture_before_frames': [5801, 7201],
        'fixture_changes_only_six_actor_attribute_bytes': True,
        'natural_attribute_growth_or_combat_mechanics_verified': False, 'full_goal_complete': False})
    print('V728: exact source copy,normal controls and original six-byte getter contract frozen.')


class CoreProxy:
    def __init__(self, core, mode, out, arm):
        self.core, self.mode, self.out, self.arm = core, mode, out, arm
        self.frame = 0
        self.original = None
        self.rows = []

    def __getattr__(self, key):
        return getattr(self.core, key)

    def retro_run(self):
        self.frame += 1
        if self.frame in (5801, 7201):
            self.intervene()
        self.core.retro_run()

    def intervene(self):
        core = self.core
        core.retro_get_memory_data.argtypes = [ct.c_uint]
        core.retro_get_memory_data.restype = ct.c_void_p
        core.retro_get_memory_size.argtypes = [ct.c_uint]
        core.retro_get_memory_size.restype = ct.c_size_t
        pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
        assert pointer and size == 0x400000
        before = ct.string_at(pointer, size)
        actor, values = actor_stats(self.arm, before)
        if self.frame == 5801:
            self.original = list(values)
            target = values if self.mode == 'disabled' else [0 if self.mode == 'zero' else 100] * 6
        else:
            assert self.original is not None
            if self.mode != 'disabled':
                assert values == [0 if self.mode == 'zero' else 100] * 6
            target = self.original
        folder = self.out / f'fixture_before_frame_{self.frame:06d}'
        native_before = export(core, folder / 'before', before)
        offset = actor + 8 - BASE
        expected = bytearray(before)
        expected[offset:offset + 6] = bytes(target)
        if self.mode != 'disabled':
            ct.memmove(pointer + offset, bytes(target), 6)
        after = ct.string_at(pointer, size)
        assert after == bytes(expected)
        before_path, after_path = folder / 'before_RAM.bin', folder / 'after_RAM.bin'
        before_path.write_bytes(before)
        after_path.write_bytes(after)
        native_after = export(core, folder / 'after', after)
        assert native_before['ARM9_registers'] == native_after['ARM9_registers']
        assert native_before['ARM9_instruction_address'] == native_after['ARM9_instruction_address']
        for region in ('DTCM', 'ITCM'):
            assert native_before['regions'][region]['sha256'] == native_after['regions'][region]['sha256']
        row = {'before_original_retro_run_frame': self.frame, 'mode': self.mode,
            'actor': 1, 'saved_captain_profile_name': 'Hodram', 'actor_address': actor,
            'only_allowed_main_RAM_span': [actor + 8, actor + 14], 'before_values': values, 'after_values': target,
            'original_values': self.original, 'write_performed': self.mode != 'disabled',
            'entire4MiB_RAM_exact_except_declared_six_bytes': True,
            'CPU_registers_PC_DTCM_ITCM_unchanged_by_intervention': True,
            'before_RAM_sha256': sha(before), 'after_RAM_sha256': sha(after),
            'before_RAM_path': str(before_path), 'after_RAM_path': str(after_path),
            'native_before': native_before, 'native_after': native_after,
            'natural_stat_acquisition_or_mechanics_verified': False}
        self.rows.append(row)
        save(self.out / 'fixture_receipts.json', self.rows)


def run(mode):
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['shared_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in ((pre['donor'], pre['donor_sha256']),
                         (pre['original_donor'], pre['original_donor_sha256']),
                         (pre['inputs'], pre['inputs_sha256'])):
        assert sha(Path(path).read_bytes()) == digest
    out = CAP / ('stat_plaques_v728_' + mode)
    assert not out.exists()
    out.mkdir(parents=True)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    assert sha(arm) == pre['ARM9_sha256']
    instances = []
    original_ct = harness.ct

    class CTProxy:
        def __getattr__(self, key):
            if key != 'CDLL':
                return getattr(ct, key)
            def load(path, *args, **kwargs):
                core = ct.CDLL(path, *args, **kwargs)
                assert Path(path).resolve() == harness.CORE.resolve()
                proxy = CoreProxy(core, mode, out, arm)
                instances.append(proxy)
                return proxy
            return load

    harness.ct = CTProxy()
    save(out / 'run_contract.json', {'mode': mode, 'preflight': str(ROOT / 'preflight.json'),
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'process_local_Python_proxy_no_game_code_or_core_DLL_patch': True,
        'every_original_retro_run_called_once': True, 'not_a_natural_stat_growth_test': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(out),
        '--frames', str(pre['last_frame']), '--inputs-json', pre['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--capture-every', '999999', '--dump-capture-ram',
        '--capture-at', *map(str, FRAMES)]
    try:
        harness.main()
    finally:
        harness.ct = original_ct
    assert len(instances) == 1 and instances[0].frame == 9500 and len(instances[0].rows) == 2
    assert instances[0].rows[1]['after_values'] == instances[0].rows[0]['before_values']
    report_path = out / 'capture_report.json'
    report = read(report_path)
    report['stat_plaque_fixture_control_mode'] = mode
    if mode != 'disabled':
        report['synthetic_sailor_stat_display_fixture'] = {'receipts': str(out / 'fixture_receipts.json'),
            'sha256': sha((out / 'fixture_receipts.json').read_bytes()), 'only_six_actor_stat_bytes': True,
            'original_stats_restored_before_reopen': True, 'natural_stat_growth_verified': False}
    save(report_path, report)
    assert sha(harness.CORE.read_bytes()) == CORE_SHA
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['original_donor']).read_bytes()) == pre['original_donor_sha256']
    print(f'V728 {mode} terminal: original stats restored,donors/core/ROM unchanged.', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('prepare', 'disabled', 'zero', 'hundred'), required=True)
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
    else:
        run(args.mode)


if __name__ == '__main__':
    main()
