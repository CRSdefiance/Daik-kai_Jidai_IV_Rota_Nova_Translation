"""Ordinary Maria opening navigation on V678 using the authorized unlock save."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.trace_file_ids_v683 import Observer
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/maria_intro_v684')
ROM = Path('out/all_routes_combined_v678_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    old = read('work/analysis/maria_opening_v674/preflight.json')
    manifest = read(old['manifest'])
    manifest.update(production_ROM=str(ROM), production_ROM_sha256=sha(ROM.read_bytes()),
                    current_test_scope='Ordinary complete Maria New Game opening; existing system unlock, not earned')
    save(ROOT / 'unlock_manifest.json', manifest)
    save(ROOT / 'initial_inputs.json', read('work/analysis/maria_opening_v674/dispatch_inputs.json'))
    assert sha(Path(old['donor']).read_bytes()) == old['donor_sha256']
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json',
             'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'donor': old['donor'], 'donor_sha256': old['donor_sha256'],
        'unlock_manifest': str(ROOT / 'unlock_manifest.json'),
        'unlock_manifest_sha256': sha((ROOT / 'unlock_manifest.json').read_bytes()),
        'previous_goal_turn_classification': 'progress: V682 and V683 source/interface evidence archived;121 and643 files verified',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'full_goal_complete': False})
    print('V684 current Maria opening/source save and complete original scope pinned.', flush=True)


def run(case):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['unlock_manifest']).read_bytes()) == pre['unlock_manifest_sha256']
    folder = CAP / ('maria_intro_v684_' + case)
    assert not folder.exists()
    folder.mkdir()
    pilot = case.startswith('pilot')
    config = {'frames': 80000, 'inputs': str(ROOT / 'initial_inputs.json')} if pilot else read(ROOT / 'run_config.json')
    save(folder / 'run_contract.json', {'case': case, 'config': config,
        'inputs_sha256': sha(Path(config['inputs']).read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/trace_file_ids_v683.py').read_bytes()),
        'observer_source_contract': 'work/analysis/file_ids_v683/source_contract.json',
        'observer_source_contract_sha256': sha(Path('work/analysis/file_ids_v683/source_contract.json').read_bytes()),
        'ordinary_buttons_only_existing_unlock_save_no_earned_unlock_claim': True})
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

    if case == 'observed':
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', pre['unlock_manifest'], '--capture-every', '999999', '--dump-ram']
    if pilot:
        sys.argv += ['--pause-at', '4000', '--dump-pause-ram']
    else:
        sys.argv += ['--capture-at', *map(str, config['capture_frames'])]
        if case == 'observed':
            sys.argv += ['--dump-capture-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V684 terminal:', case, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('prepare', 'pilot', 'pilot_interactive', 'observed', 'baseline'))
    case = parser.parse_args().case
    if case == 'prepare':
        prepare()
    else:
        run(case)


if __name__ == '__main__':
    main()
