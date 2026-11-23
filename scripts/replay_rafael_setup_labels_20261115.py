"""Replay all five edit fields, the birthday calendar, and startup controls."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_rafael_character_setup_20261115 as exploratory
from scripts import observe_setup_save_common_v1 as trace
from scripts import replay_refit_help_startup_20261115 as boot
from scripts import stage_rafael_setup_labels_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = stage.base, stage.ROOT
STARTUP = ROOT / 'own_startup_verification.json'
CONTROLS = (
    (2401, 'Y'), (2801, 'DOWN'), (3201, 'DOWN'), (3601, 'DOWN'), (4001, 'DOWN'), (4401, 'A'),
    (4801, (174, 62)), (5201, (195, 97)), (5601, 'A'), (6001, 'X'), (6401, 'B'),
)


def schedule(_):
    prior = exploratory.PRIOR
    prefix = base.load(prior)[:4]
    assert [e['buttons'] for e in prefix] == [['START'], ['A'], ['A'], ['B']]
    actions = [dict(start=frame, duration=8, buttons=[key]) if isinstance(key, str)
                else dict(start=frame, duration=8, buttons=[], touch=list(key)) for frame, key in CONTROLS]
    return prefix + actions, [1800, 2200, *(n + 190 for n, _ in CONTROLS)], 6601, prior, None


def replay(side):
    parent = stage.parent
    if side == 'after':
        staged = base.load(stage.STORED)
        release = ROOT / 'staged_replay_selection.json'
        assert not release.exists()
        base.save(release, dict(candidate=str(stage.ROM), candidate_sha256=staged['candidate_sha256']))
        parent = SimpleNamespace(ROM=stage.ROM, RELEASE=release)
    source = checked_text(getsource(playback.main), {
        '    installed = []': "    argv += ['--touchscreen']\n    installed = []",
    })
    env = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS={*range(100, 108), *range(120, 122)}, __file__=__file__)
    exec(compile(source, __file__ + '::paired-original-input', 'exec'), env)
    env['main'](side)


def startup():
    release = base.load(stage.parent.RELEASE)
    receipt = base.load(release['own_registered_startup'])
    prior = Path(receipt['read_only_snapshot']['path']).parent.parent
    source = checked_text(getsource(boot.startup.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    env = vars(boot.startup) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(source, __file__ + '::registered-startup', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('before', 'after', 'startup'))
    case = parser.parse_args().case
    startup() if case == 'startup' else replay(case)
