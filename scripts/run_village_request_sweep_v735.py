"""Trace the remaining23 complete village flows using the frozen V734 observer.

Each child is a separate diagnostic process. Ezo's paired V734 result carries
forward; other cases rely on the same validated read-only filter and preserve
guest state at every callback. Original saves and production files are protected.
"""

import argparse
import ctypes as ct
import io
import json
import subprocess
import sys
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts import native_village_visits_v664 as old_location
from scripts.observe_village_images_v734 import ROOT as OBSERVER_ROOT
from scripts.observe_village_images_v734 import Observer
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_images_v734 import ARM_SHA, CAP, ROM
from scripts.verify_village_visits_v664 import model
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_request_sweep_v735')
CARDS = (168, 169, 170, 171, 206, 207, 208, 209)


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    prior = read(OBSERVER_ROOT / 'preflight.json')
    assert prior['observer_sha256'] == sha(Path('scripts/observe_village_images_v734.py').read_bytes())
    assert sha(ROM.read_bytes()) == prior['candidate_sha256']
    rows = read('work/analysis/village_development_v665/proof.json')['all24_development_cases']
    karibib = read('work/analysis/Karibib_return_v667/proof.json')
    cases = []
    for row in rows:
        index = row['index']
        if index == 18:
            continue
        report_path = Path(karibib['report'] if index == 9 else row['report']['path'])
        expected_sha = karibib['report_sha256'] if index == 9 else row['report']['sha256']
        assert sha(report_path.read_bytes()) == expected_sha
        report = read(report_path)
        controller_path = report_path.parent / 'controller_progress.json'
        controller = read(controller_path)
        assert controller['error'] is None and report['frames'] == controller['phases']['developed_town_return']
        journal = read(report_path.parent / 'navigation_command_journal.json')['commands_received']
        assert all(r['validation_passed'] for r in journal)
        assert controller['commands'] == [{'frame': r['frame'], 'command': r['command']} for r in journal]
        allowed = {'until', 'location_town', 'stop', 'buttons', 'duration', 'touch'}
        assert all(set(r['command']) <= allowed for r in controller['commands'])
        source = report['battery_save_preloaded']
        donor = Path(source['source'])
        digest = sha(donor.read_bytes())
        assert digest == source['source_sha256']
        copied = ROOT / f'donor_{digest[:16]}_TEST_ONLY.dsv'
        if not copied.exists():
            copy(donor, copied)
        assert sha(copied.read_bytes()) == digest
        folder = ROOT / f'case_{index:02d}'
        folder.mkdir()
        save(folder / 'inputs.json', report['scripted_input_schedule'])
        commands = [{k: v for k, v in r['command'].items() if k in ('until', 'location_town', 'stop')}
            for r in controller['commands']]
        assert commands[-1] == {'stop': True}
        assert all(c.get('location_town', index) == index for c in commands)
        save(folder / 'commands.json', commands)
        cases.append({'index': index, 'name': row['village_name'], 'answer': row['answer'],
            'frames': report['frames'], 'phases': controller['phases'],
            'historical_report': str(report_path), 'historical_report_sha256': expected_sha,
            'historical_controller': str(controller_path), 'historical_controller_sha256': sha(controller_path.read_bytes()),
            'original_donor': str(donor), 'original_donor_sha256': digest,
            'test_copy': str(copied), 'test_copy_sha256': digest,
            'inputs': str(folder / 'inputs.json'), 'inputs_sha256': sha((folder / 'inputs.json').read_bytes()),
            'commands': str(folder / 'commands.json'), 'commands_sha256': sha((folder / 'commands.json').read_bytes()),
            'output': str(CAP / f'village_request_sweep_v735_{index:02d}'),
            'captain': 3 if index == 9 else 1,
            'Maria_case_uses_previously_authorized_selection_bypass_save_not_earned_unlock': index == 9})
    assert len(cases) == 23 and {r['index'] for r in cases} == set(range(24)) - {18}
    save(ROOT / 'cases.json', cases)
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': prior['candidate_sha256'],
        'release_hashes': prior['release_hashes'], 'runner_sha256': sha(Path(__file__).read_bytes()),
        'shared_observer_sha256': prior['observer_sha256'],
        'shared_source_contract': str(OBSERVER_ROOT / 'source_contract.json'),
        'shared_source_contract_sha256': sha((OBSERVER_ROOT / 'source_contract.json').read_bytes()),
        'paired_Ezo_proof': str(OBSERVER_ROOT / 'proof.json'),
        'paired_Ezo_proof_sha256': sha((OBSERVER_ROOT / 'proof.json').read_bytes()),
        'cases_sha256': sha((ROOT / 'cases.json').read_bytes()),
        'other23_observed_only_not23_additional_baseline_pairs': True,
        'previous_goal_turn_classification': 'progress: V734 complete current Ezo progression and API trace',
        'full_goal_complete': False})
    print('V735 prepared23 protected replay cases; Ezo carried forward; Karibib uses its successful Maria path.', flush=True)


def run_case(index):
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['shared_observer_sha256'] == sha(Path('scripts/observe_village_images_v734.py').read_bytes())
    assert pre['shared_source_contract_sha256'] == sha(Path(pre['shared_source_contract']).read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    case = next(r for r in read(ROOT / 'cases.json') if r['index'] == index)
    for key in ('original_donor', 'test_copy', 'inputs', 'commands'):
        assert sha(Path(case[key]).read_bytes()) == case[key + '_sha256']
    out = Path(case['output'])
    assert not out.exists()
    out.mkdir()
    save(out / 'run_contract.json', {'case': case, 'runner_sha256': pre['runner_sha256'],
        'observer_sha256': pre['shared_observer_sha256'],
        'observer_contract': pre['shared_source_contract'],
        'observer_contract_sha256': pre['shared_source_contract_sha256'],
        'coordinate_fixtures_only_and_observer_readonly': True})
    current = NdsImage.open(ROM).read_file('/__arm9__.bin')
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert sha(current) == ARM_SHA and sha(reference) == old_location.ARM
    assert all(current[a:b] == reference[a:b] for a, b in old_location.SPANS)

    def relocate(arm, raw, village):
        assert sha(arm) == ARM_SHA and village == index
        after, receipt = old_location.relocate(reference, raw, village)
        receipt.update(actual_current_ARM9_sha256=sha(arm),
            V735_current_guard='pinned-V712-coordinate-code-exact-V653',
            village_request_sweep_case=index)
        return after, receipt

    observers = []

    class CtypesProxy:
        def __getattr__(self, name):
            return getattr(ct, name)

        def CDLL(self, path, *extra, **kwargs):
            core = ct.CDLL(path, *extra, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = Observer(core, out / 'observer')
                observer.install()
                observers.append(observer)
                original = core.retro_run
                original.restype = None

                def run():
                    observer.next_frame()
                    original()
                core.retro_run = run
            return core

    previous_ct, previous_stdin, previous_relocate = harness.ct, sys.stdin, location.relocate
    harness.ct, location.relocate = CtypesProxy(), relocate
    sys.stdin = io.StringIO(''.join(json.dumps(c) + '\n' for c in read(case['commands'])))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(out),
        '--frames', str(case['frames']), '--inputs-json', case['inputs'], '--battery-save', case['test_copy'],
        '--pause-at', '5200', '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        harness.ct, sys.stdin, location.relocate = previous_ct, previous_stdin, previous_relocate
        for observer in observers:
            observer.close()
    for observer in observers:
        observer.save()
    for key in ('original_donor', 'test_copy'):
        assert sha(Path(case[key]).read_bytes()) == case[key + '_sha256']
    print(f'V735 case{index:02d} terminal.', flush=True)


def sweep():
    assert not (ROOT / 'sweep_result.json').exists()
    cases = read(ROOT / 'cases.json')
    queue, finished, active, signals = iter(cases), [], {}, []
    card_ids = {NdsImage.open(ROM).path_map()[f'/evstill/evstill{n:03d}.pxl'] for n in CARDS}

    def worker(case):
        log = ROOT / f"case_{case['index']:02d}" / 'process.log'
        with log.open('w', encoding='utf-8') as output:
            result = subprocess.run([sys.executable, str(Path(__file__)), 'case', '--index', str(case['index'])],
                stdout=output, stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), check=False)
        return result.returncode

    def launch(pool):
        case = next(queue, None)
        if case is not None:
            print(f"Starting {case['index']:02d} {case['name']} ({case['frames']}frames)", flush=True)
            active[pool.submit(worker, case)] = case

    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    with ThreadPoolExecutor(max_workers=3) as pool:
        for _ in range(3):
            launch(pool)
        while active:
            done, _ = wait(active, return_when=FIRST_COMPLETED)
            for task in done:
                case = active.pop(task)
                code = task.result()
                out = Path(case['output'])
                if code:
                    signals.append({'index': case['index'], 'process_exit_code': code,
                        'log': str(ROOT / f"case_{case['index']:02d}" / 'process.log')})
                else:
                    report = read(out / 'capture_report.json')
                    actual = model(arm, Path(report['read_only_RAM_snapshot']['path']).read_bytes(),
                        case['index'], case['name'], True)
                    assert actual['native_development'] == 2
                    meta = read(out / 'observer/requests.json')
                    hits = [r for r in meta['rows'] if
                        (r['kind'] == 'numeric_ID' and r['file_ID'] in card_ids) or
                        (r['kind'] == 'event_still_formatter' and r['original_image_index'] in CARDS) or
                        (r['kind'] == 'raw_SLACK_entry' and r['raw_request']['block'] == 19)]
                    finished.append({'index': case['index'], 'name': case['name'], 'report': str(out / 'capture_report.json'),
                        'report_sha256': sha((out / 'capture_report.json').read_bytes()),
                        'trace': str(out / 'observer/requests.json'), 'trace_sha256': sha((out / 'observer/requests.json').read_bytes()),
                        'frames': report['frames'], 'request_count': len(meta['rows']), 'native_final_model': actual})
                    if hits:
                        signals.append({'index': case['index'], 'new_card_or_comic_request': hits})
                    print(f"Finished {case['index']:02d} {case['name']}: {len(meta['rows'])}requests,development2 ({len(finished)}/23)", flush=True)
                save(ROOT / 'live_progress.json', {'finished': finished, 'signals': signals,
                    'active_case_indices': [c['index'] for c in active.values()],
                    'progress_file_not_process_liveness_proof': True})
                if not signals:
                    launch(pool)
    save(ROOT / 'sweep_result.json', {'finished': finished, 'signals': signals,
        'all23_workers_terminal': len(finished) == 23 and not signals,
        'runner_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    assert len(finished) == 23 and not signals, 'Sweep stopped after a retained failure or a new image-consumer lead.'
    print('V735 all23 new workers terminal; Ezo carried forward; final verification still required.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('prepare', 'case', 'sweep'))
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
    elif args.mode == 'case':
        run_case(args.index)
    else:
        sweep()
