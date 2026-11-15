"""Observe shared-message requests on the registered ROM during trade and cancellation."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as precedent
from scripts import observe_setup_save_common_v1 as capture
from scripts import register_sailor_stat_labels_20261114 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('out/market_restart_common_20261114_v1')
PLAN = Path('work/market_goods_info_terminator_release_v1/market_run_v3/run_plan.json')
FOCUS = {750, 751, 752}
TRADE_ACTIONS = {
    'back': [(11601, 'B'), (12001, 'B'), (12401, 'A'), (12801, 'B'), (13201, 'B')],
    'finish': [(11601, 'X'), (12001, 'B'), (12401, 'A'), (12801, 'B'), (13201, 'B')],
    'confirm': [(11601, 'X'), (12001, 'A'), (12401, 'A'), (12801, 'A'), (13201, 'B')],
}


def schedule(case):
    plan = base.load(PLAN)
    report = base.load(plan['predecessor_report'])
    assert base.digest(plan['predecessor_report']) == plan['predecessor_report_sha256']
    assert base.digest(plan['unchanged_inputs']) == plan['unchanged_inputs_sha256']
    inputs = base.load(plan['unchanged_inputs'])
    assert inputs == report['scripted_input_schedule']
    donor = plan['source_save']
    assert base.digest(donor['source']) == donor['source_sha256']
    inputs.extend(dict(start=at, duration=8, buttons=[key]) for at, key in TRADE_ACTIONS[case])
    frames = [9600, 10000, 10400, 11600]
    frames.extend(at + 280 for at, _ in TRADE_ACTIONS[case])
    return inputs, frames, frames[-1] + 30, PLAN, donor


def main(case):
    source = checked_text(getsource(precedent.main), {
        "    if donor:\n        assert base.digest(donor['source']) == donor['source_sha256']\n    assert not any":
            "    if donor:\n        assert base.digest(donor['source']) == donor['source_sha256']\n"
            "        assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']\n"
            "    assert report['scripted_input_schedule'] == events\n    assert not any",
    })
    env = vars(precedent) | dict(ROOT=ROOT, parent=current, FOCUS=FOCUS,
        observer=capture.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(source, __file__ + '::registered-market-observation', 'exec'), env)
    env['main'](case)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=TRADE_ACTIONS)
    main(parser.parse_args().case)
