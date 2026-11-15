"""Trace the shared-text consumers in an ordinary Istanbul square and shop visit."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as precedent
from scripts import observe_setup_save_common_v1 as observer
from scripts import register_sailor_stat_labels_20261114 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('out/istanbul_shared_text_20261114_v1')
PLAN = Path('work/analysis/square_context_actual_v2122/run_plan.json')
LEGACY = Path('translations/editorial_checkpoints/SharedText_20261110_v1/legacy_common_35_checkpoint_v1.json')


def schedule(case):
    assert case == 'istanbul'
    plan = base.load(PLAN)
    assert base.digest(plan['prior_report']) == plan['prior_report_sha256']
    assert base.digest(plan['inputs']) == plan['inputs_sha256']
    events = base.load(plan['inputs'])
    old = base.load(plan['prior_report'])
    donor = old['battery_save_preloaded']
    assert events == old['scripted_input_schedule']
    assert base.digest(donor['source']) == donor['source_sha256'] == plan['donor_sha256']
    frames = sorted(set(plan['captures']) | {row['start'] + 80 for row in events[4:]})
    return events, frames, 6501, PLAN, donor


def main():
    focus = {row['message_ID'] for row in base.load(LEGACY)['records']} - {336}
    focus |= precedent.FOCUS
    source = checked_text(getsource(precedent.main), {
        "    if donor:\n        assert base.digest(donor['source']) == donor['source_sha256']\n    assert not any":
            "    if donor:\n        assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']\n"
            "        assert base.digest(donor['source']) == donor['source_sha256']\n"
            "    assert report['scripted_input_schedule'] == events\n    assert not any",
    })
    env = vars(precedent) | dict(ROOT=ROOT, parent=current, FOCUS=focus,
        observer=observer.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(source, __file__ + '::original-istanbul-inputs', 'exec'), env)
    env['main']('istanbul')


if __name__ == '__main__':
    main()
