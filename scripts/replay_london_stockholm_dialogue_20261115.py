"""Run the same ordinary controllers and cumulative startup on the staged ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_london_riga_towns_20261115 as baseline
from scripts import replay_refit_help_startup_20261115 as boot
from scripts import stage_london_stockholm_dialogue_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = stage.base, stage.ROOT
STARTUP = ROOT / 'own_startup_verification.json'


def town(case):
    staged = base.load(stage.STORED)
    receipt = ROOT / f'{case}_staged_selection.json'
    assert not receipt.exists()
    base.save(receipt, dict(candidate=str(stage.ROM), candidate_sha256=staged['candidate_sha256']))
    successor = SimpleNamespace(ROM=stage.ROM, RELEASE=receipt)
    namespace = vars(baseline) | dict(ROOT=ROOT, current=successor, __file__=__file__)
    exec(compile(getsource(baseline.main), __file__ + '::staged-town-inputs', 'exec'), namespace)
    namespace['main'](case)


def cold_boot():
    receipt = base.load(stage.parent.RELEASE)
    prior = Path(base.load(receipt['own_registered_startup'])['read_only_snapshot']['path']).parent.parent
    source = checked_text(getsource(boot.startup.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    env = vars(boot.startup) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(source, __file__ + '::cumulative-startup', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=(*baseline.HISTORY, 'startup'))
    case = parser.parse_args().case
    cold_boot() if case == 'startup' else town(case)
