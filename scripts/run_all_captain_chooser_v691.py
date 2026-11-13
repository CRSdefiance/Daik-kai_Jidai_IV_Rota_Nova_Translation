"""Cycle all four captains with existing unlock and declared raw-buffer controls."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import trace_chooser_raw_independence_v690 as observer
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/all_captain_chooser_v691')
ROM = Path('out/all_routes_combined_v685_candidate.nds')
STATES = ((2700, 0), (3100, 1), (3500, 2), (3900, 3), (4300, 2), (4700, 1), (5100, 0))
FRAMES = (1, 60, 180, 1600, 2000, 2400, *[f for f, _ in STATES], 5200)


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    source_root = observer.ROOT
    proof = read(source_root / 'proof.json')
    assert proof['producer_sha256'] == sha(Path(observer.__file__).read_bytes())
    assert sha(CORE.read_bytes()) == CORE_SHA
    source_path = source_root / 'source_contract.json'
    (ROOT / 'source_contract.json').write_bytes(source_path.read_bytes())
    fixture = read(source_root / 'isolated_raw_buffer_fixture.json')
    assert fixture['ROM_sha256'] == sha(ROM.read_bytes())
    assert fixture['replacement_sha256'] == sha(observer.PATTERN)
    fixture['current_scope'] = 'All four captain selections; isolated source-buffer input control; not production artwork'
    save(ROOT / 'isolated_raw_buffer_fixture.json', fixture)
    unlock_path = Path('work/analysis/opening_holds_v686/current_unlock_manifest.json')
    unlock = read(unlock_path)
    assert unlock['production_ROM_sha256'] == sha(ROM.read_bytes())
    donor = Path(unlock['fixture_save'])
    assert sha(donor.read_bytes()) == unlock['fixture_save_sha256']
    assert sha(Path(unlock['original_donor']).read_bytes()) == unlock['original_donor_sha256']
    unlock['current_test_scope'] = 'Cycle actual Rafael/Hodram/Lil/Maria captain chooser with the existing authorized system unlock only'
    save(ROOT / 'unlock_manifest.json', unlock)
    inputs = [{'start': 1601, 'duration': 8, 'buttons': ['START']},
              {'start': 2001, 'duration': 8, 'buttons': ['DOWN']},
              {'start': 2401, 'duration': 8, 'buttons': ['A']}]
    inputs += [{'start': frame, 'duration': 8, 'buttons': [key]}
               for frame, key in ((2801, 'RIGHT'), (3201, 'RIGHT'), (3601, 'RIGHT'),
                                  (4001, 'LEFT'), (4401, 'LEFT'), (4801, 'LEFT'))]
    save(ROOT / 'inputs.json', inputs)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
             Path('translations/release_stack.json'), Path('work/clean.nds'),
             Path('out/raphael_natural_v2_accepted_base.nds'))
    controls_path = source_root / 'prefix_controls/native_prefix_controls.json'
    controls = read(controls_path)
    assert len(controls['native_host_cases']) == 20 and len(controls['read_policy_cases']) == 8
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_source': str(Path(observer.__file__)),
        'observer_source_sha256': sha(Path(observer.__file__).read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'fixture_manifest_sha256': sha((ROOT / 'isolated_raw_buffer_fixture.json').read_bytes()),
        'unlock_manifest_sha256': sha((ROOT / 'unlock_manifest.json').read_bytes()),
        'donor': str(donor), 'donor_sha256': sha(donor.read_bytes()),
        'original_donor': unlock['original_donor'], 'original_donor_sha256': unlock['original_donor_sha256'],
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'inherited_identical_host_controls': str(controls_path), 'host_controls_sha256': sha(controls_path.read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V690 actual initialization and live final-buffer controls verified and archived',
        'full_goal_complete': False})
    print('V691 all-four chooser schedule and unchanged unlock donor/source observer pinned.', flush=True)


def run(case):
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert pre['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['observer_source_sha256'] == sha(Path(observer.__file__).read_bytes())
    for path, key in ((ROOT / 'inputs.json', 'inputs_sha256'),
                      (ROOT / 'unlock_manifest.json', 'unlock_manifest_sha256'),
                      (ROOT / 'isolated_raw_buffer_fixture.json', 'fixture_manifest_sha256')):
        assert sha(path.read_bytes()) == pre[key]
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder = CAP / ('all_captain_chooser_v691_' + case)
    assert not folder.exists()
    folder.mkdir()
    # Process-local configuration of the frozen observer, never a source-file edit.
    observer.ROOT, observer.FOLDER = ROOT, folder
    save(folder / 'run_contract.json', {'case': case,
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': pre['runner_sha256'], 'observer_source_sha256': pre['observer_source_sha256'],
        'existing_system_unlock_not_earned': True, 'one_raw_buffer_fixture': case == 'poison'})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            tracer = observer.Observer(core, case == 'poison')
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
        '--frames', '5200', '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen',
        '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', str(ROOT / 'unlock_manifest.json'),
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES),
        '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for tracer in installed:
            tracer.close()
    for tracer in installed:
        tracer.save()
    report = read(folder / 'capture_report.json')
    report['synthetic_raw_portrait_buffer_fixture'] = case == 'poison'
    report['raw_portrait_buffer_fixture_manifest'] = str(ROOT / 'isolated_raw_buffer_fixture.json') if case == 'poison' else None
    save(folder / 'capture_report.json', report)
    print('V691 all-four chooser terminal:', case, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'control', 'poison'))
    action = parser.parse_args().action
    if action == 'prepare':
        prepare()
    else:
        run(action)
