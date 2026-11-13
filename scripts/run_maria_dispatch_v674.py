"""Repeat the pilot with full-interval original FLS-request observation."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_graphic_paints_v669 as paints
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

CAPTURE_FRAMES = (2000, 2400, 2800, 3000, 3200, 3400, 3600, 3700, 3800, 3900, 4000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder = CAP / f"maria_dispatch_v674_{'baseline' if args.baseline else 'observed'}"
    assert not folder.exists()
    folder.mkdir(parents=True)
    inputs = ROOT / 'dispatch_inputs.json'
    save(folder / 'run_contract.json', {'candidate_sha256': pre['candidate_sha256'],
        'inputs_sha256': sha(inputs.read_bytes()), 'factory_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'baseline': args.baseline,
        'FLS_entry_r0_index_r1_flag_r2_r3_LR_only_not_blitter_fields': True,
        'same_native_push_opcode_table_handler_with_additional_PC_filter': True})
    loader, installed = ct.CDLL, []
    previous_root = paints.ROOT
    # Process-local contract configuration, not an edit of the shared observer.
    paints.ROOT = ROOT

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = paints.Observer(core, folder / 'observer', capacity=500000)
            original_run = core.retro_run
            original_run.restype = None
            observer.install()

            def run():
                observer.next_frame()
                original_run()
            core.retro_run = run
            installed.append(observer)
        return core

    if not args.baseline:
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', '4000', '--inputs-json', str(inputs), '--battery-save', pre['donor'],
        '--allow-gallery-fixtures', '--gallery-save-fixture-manifest', pre['manifest'],
        '--capture-every', '999999', '--capture-at', *map(str, CAPTURE_FRAMES),
        '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    paints.ROOT = previous_root
    print('V674 native Maria-selection/FLS-dispatch terminal; baseline:', args.baseline, flush=True)


if __name__ == '__main__':
    main()
