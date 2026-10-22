"""Original Japanese Maria opening control for three inherited blank holds."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_holds_v686')
CLEAN = Path('work/clean.nds')
CURRENT = Path('out/all_routes_combined_v685_candidate.nds')
FRAMES = (4000, 4600, 5200, 5800, 6400, 20800, 21400, 22000, 31000)


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    old = read('work/analysis/maria_intro_v684/preflight.json')
    manifest = read(old['unlock_manifest'])
    assert sha(CLEAN.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    manifest.update(production_ROM=str(CLEAN), production_ROM_sha256=sha(CLEAN.read_bytes()),
                    current_test_scope='Original Japanese source Maria scene holds with the same authorized isolated system unlock save')
    save(ROOT / 'source_unlock_manifest.json', manifest)
    assert sha(Path(old['donor']).read_bytes()) == old['donor_sha256']
    inputs = Path('work/analysis/maria_intro_v684/complete_inputs.json')
    current_report = CAP / 'story_percent_v685_maria/capture_report.json'
    report = read(current_report)
    assert report['ROM_sha256'] == sha(CURRENT.read_bytes())
    assert report['scripted_input_schedule'] == read(inputs)
    snapshots = {s['frame']: s for s in report['read_only_capture_RAM_snapshots']}
    shots = {s['frame']: s for s in report['frames_captured']}
    bindings = {}
    for frame in FRAMES:
        image, ram = shots[frame], snapshots[frame]
        assert sha(Path(image['path']).read_bytes()) == image['PNG_sha256']
        assert sha(Path(ram['path']).read_bytes()) == ram['sha256']
        bindings[str(frame)] = {'screenshot': image, 'RAM': ram}
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json',
             'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'clean': str(CLEAN), 'clean_sha256': sha(CLEAN.read_bytes()), 'source_unlock_manifest': str(ROOT / 'source_unlock_manifest.json'),
        'source_unlock_manifest_sha256': sha((ROOT / 'source_unlock_manifest.json').read_bytes()),
        'donor': old['donor'], 'donor_sha256': old['donor_sha256'], 'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'current_report': str(current_report), 'current_report_sha256': sha(current_report.read_bytes()),
        'current_selected_capture_bindings': bindings,
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (CURRENT, CURRENT.with_suffix('.manifest.json'),
            CURRENT.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'previous_goal_turn_classification': 'progress: V685 four percent defects repaired, final source format gate, actual Maria scene and314-file archive verified',
        'full_goal_complete': False})
    print('V686 original source/current held-frame bindings and unchanged save pinned.', flush=True)


def run():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CLEAN.read_bytes()) == pre['clean_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['inputs']).read_bytes()) == pre['inputs_sha256']
    assert sha(Path(pre['source_unlock_manifest']).read_bytes()) == pre['source_unlock_manifest_sha256']
    folder = CAP / 'opening_holds_v686_source'
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'source_ROM_sha256': pre['clean_sha256'],
        'runner_sha256': sha(Path(__file__).read_bytes()), 'frozen_preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'ordinary_same_inputs_source_ROM_existing_unlock_save_only_not_earned': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(CLEAN), '--out', str(folder),
        '--frames', '31000', '--inputs-json', pre['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', pre['source_unlock_manifest'],
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-capture-ram', '--dump-ram']
    harness.main()
    print('V686 original Japanese Maria opening terminal.', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'source'))
    if parser.parse_args().action == 'prepare':
        prepare()
    else:
        run()


if __name__ == '__main__':
    main()
