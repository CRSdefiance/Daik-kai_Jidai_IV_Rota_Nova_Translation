"""Observe original battle/result image calls with an identical baseline."""

import argparse
import ctypes as ct
import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_battle_proximity_v673 import apply_fixture
from scripts.observe_graphic_paints_v669 import Observer
from scripts.prepare_battle_paints_v673 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for key in ('donor', 'inputs', 'commands', 'observer', 'observer_contract', 'fixture_wrapper'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    folder = CAP / f"battle_paints_v673_{'baseline' if args.baseline else 'observed'}"
    assert not folder.exists()
    folder.mkdir(parents=True)
    save(folder / 'run_contract.json', {'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'baseline': args.baseline,
        'existing_V654_inputs_two_coordinate_fixtures_no_outcome_edits': True})
    loader, installed, fixture_receipts = ct.CDLL, [], []
    previous_dispatch = dispatch.apply_fixture

    def fixture(arm, raw, action):
        after, receipt = apply_fixture(arm, raw, action)
        path = folder / f'fixture_{len(fixture_receipts):02d}_before_RAM.bin'
        path.write_bytes(raw)
        fixture_receipts.append({'before_RAM_path': str(path), 'before_RAM_sha256': sha(raw),
            'after_RAM_sha256': sha(after), 'receipt': receipt})
        return after, receipt

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer')
            original_run = core.retro_run
            original_run.restype = None
            observer.install()

            def run():
                observer.next_frame()
                original_run()
            core.retro_run = run
            installed.append(observer)
        return core

    dispatch.apply_fixture = fixture
    if not args.baseline:
        ct.CDLL = loaded
    previous_stdin = sys.stdin
    sys.stdin = io.StringIO('\n'.join(json.dumps(c) for c in read(pre['commands'])) + '\n')
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', '100000', '--inputs-json', pre['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', '4800', '--battery-save', pre['donor'],
        '--pause-at', '4800', '--dump-ram', '--allow-battle-fixtures']
    try:
        harness.main()
    finally:
        ct.CDLL, dispatch.apply_fixture, sys.stdin = loader, previous_dispatch, previous_stdin
        for observer in installed:
            observer.close()
        save(folder / 'fixture_receipts.json', {'fixtures': fixture_receipts,
            'no_earned_travel_or_victory_inferred_from_coordinate_fixture': True})
    for observer in installed:
        observer.save()
    print('V673 battle source tracing terminal; baseline:', args.baseline, flush=True)


if __name__ == '__main__':
    main()
