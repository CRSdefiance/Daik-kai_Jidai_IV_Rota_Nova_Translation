"""Observe the two original/current highlight frames with exact clock inputs."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_filter_clock_v693 import ROOT, WATCH, Observer
from scripts.observe_transition_scanlines_v659 import Observer as Scanlines
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v692_candidate.nds')


def prepare():
    ROOT.mkdir()
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in ('work/clean.nds', ROM)]
    targets = []
    for pc, name in ((0x020D32B8, 'paint_entry'), (0x020D3314, 'paint_return'), (0x02000FA8, 'clock_return')):
        offset = pc - 0x02000000
        assert arms[0][offset:offset + 4] == arms[1][offset:offset + 4]
        word = struct.unpack_from('<I', arms[0], offset)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'CPSR_cpu_prefix_offset': 80, 'lower_original_context': 0x023117C4,
        'clock_return_source': 'Original SDK_GetTick call02000FA4 returns at02000FA8; record R0/R1 before original modulo calculation'})
    scratch = ROOT / 'prefix_controls'
    scratch.mkdir()
    save(scratch / 'source_contract.json', read(ROOT / 'source_contract.json'))
    old = checks.ROOT
    checks.ROOT = scratch
    try:
        checks.main()
    finally:
        checks.ROOT = old
    old_plan = read('work/analysis/deck_gender_v692/all_choices/run_cases.json')
    plans = {name: old_plan['cases'][old] for name, old in (('source', 'source_full'), ('current', 'hodram_full'))}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('work/clean.nds'),
             Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'cases': plans, 'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_filter_clock_v693.py').read_bytes()),
        'scanline_observer_sha256': sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V692 shared Captain repair,full build and actual font/regression evidence recorded',
        'full_goal_complete': False})
    print('V693 original painter/clock targets15 prefix controls and unchanged source/current schedules pinned.', flush=True)


def run(case):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['producer_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['observer_sha256'] == sha(Path('scripts/observe_filter_clock_v693.py').read_bytes())
    assert pre['scanline_observer_sha256'] == sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes())
    row = pre['cases'][case]
    for path, key in ((row['ROM'], 'ROM_sha256'), (row['inputs'], 'inputs_sha256'), (row['donor_path'], 'donor_sha256')):
        assert sha(Path(path).read_bytes()) == row[key]
    folder = CAP / ('filter_clock_v693_' + case)
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'config': row,
        'producer_sha256': pre['producer_sha256'], 'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'read_only_host_observers_no_gameplay_state_fixture': True})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            tracer = Observer(core, folder)
            scan = Scanlines(core, folder / 'scanlines', (9600, 10800))
            tracer.install()
            installed.append((tracer, scan))
            original = core.retro_run
            original.restype = None

            def advance():
                tracer.header[0] += 1
                scan.frame = tracer.header[0]
                if scan.frame == min(scan.frames):
                    scan.install()
                original()
                if scan.frame == max(scan.frames):
                    scan.close()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    frames = sorted({1, 60, 180, 1600, *range(2000, 15201, 400), *WATCH})
    sys.argv = ['headless_desmume_v193.py', '--rom', row['ROM'], '--out', str(folder),
        '--frames', '15200', '--inputs-json', row['inputs'], '--touchscreen', '--battery-save', row['donor_path'],
        '--capture-every', '999999', '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram',
        '--capture-native-state-at', *map(str, sorted(WATCH))]
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for tracer, scan in installed:
            tracer.close()
            scan.close()
    for tracer, scan in installed:
        tracer.save()
        scan.save()
    print('V693 exact clock/scanline capture terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'source', 'current'))
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        run(args.action)
