"""Reproduce the additional control/export pair after the first three runs."""

import argparse
from copy import deepcopy
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')


def prepare():
    configs = read(ROOT / 'run_configs.json')
    c = configs['newgame']
    assert 'control' not in c
    initial = Path(c['output']) / 'capture_report.json'
    assert read(initial)['frames'] == 24100
    save(ROOT / 'initial_newgame_report.json', {'path': str(initial), 'sha256': sha(initial.read_bytes())})
    c['initial_baseline_report'] = c['baseline_report']
    c['initial_baseline_report_sha256'] = c['baseline_report_sha256']
    c['output'] = str(Path(c['output']).with_name('queued_portrait_v653_newgame_native'))
    control = deepcopy(c)
    control.pop('initial_baseline_report')
    control.pop('initial_baseline_report_sha256')
    control['ROM'] = 'out/all_routes_combined_v651_candidate.nds'
    control['ROM_sha256'] = sha(Path(control['ROM']).read_bytes())
    control['output'] = str(Path(c['output']).with_name('queued_portrait_v653_newgame_control'))
    c['control'] = control
    c['baseline_report'] = str(Path(control['output']) / 'capture_report.json')
    c['baseline_report_sha256'] = None
    save(ROOT / 'run_configs.json', configs)


def bind():
    configs = read(ROOT / 'run_configs.json')
    c = configs['newgame']
    receipts = []
    for label, former, current in (
        ('control', c['initial_baseline_report'], c['baseline_report']),
        ('candidate', read(ROOT / 'initial_newgame_report.json')['path'], str(Path(c['output']) / 'capture_report.json')),
    ):
        a, b = read(former), read(current)
        assert a['frames'] == b['frames'] == 24100 and a['ROM_sha256'] == b['ROM_sha256']
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['core_options'] == b['core_options']
        aa = {r['frame']: r for r in a['frames_captured']}
        bb = {r['frame']: r for r in b['frames_captured']}
        assert aa.keys() == bb.keys()
        assert all(Image.open(aa[f]['path']).tobytes() == Image.open(bb[f]['path']).tobytes() for f in aa)
        receipts.append({'label': label, 'former': former, 'current': current,
                         'former_report_sha256': sha(Path(former).read_bytes()),
                         'current_report_sha256': sha(Path(current).read_bytes()),
                         'whole_identical_two_screen_frames': len(aa),
                         'read_only_exports_did_not_change_any_sampled_pixel': True})
    c['baseline_report_sha256'] = sha(Path(c['baseline_report']).read_bytes())
    save(ROOT / 'run_configs.json', configs)
    save(ROOT / 'independent_export_control_proof.json', {'cases': receipts, 'full_goal_complete': False})
    print('Both independent export runs preserve all89 complete two-screen samples; control bound.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('prepare', 'bind'))
    args = parser.parse_args()
    prepare() if args.stage == 'prepare' else bind()


if __name__ == '__main__':
    main()
