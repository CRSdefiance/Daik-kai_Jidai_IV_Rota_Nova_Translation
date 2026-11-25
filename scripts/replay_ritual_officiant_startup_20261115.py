"""Run the registered startup replay against the staged Officiant candidate."""

from inspect import getsource
from pathlib import Path

from scripts import replay_refit_help_startup_20261115 as replay
from scripts import stage_ritual_officiant_labels_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    release = stage.base.load(stage.parent.RELEASE)
    receipt = stage.base.load(release['own_registered_startup'])
    prior = Path(receipt['read_only_snapshot']['path']).parent.parent
    original = checked_text(getsource(replay.startup.main), {
        'prior = stage.parent.stage.ROOT/"startup_retry"': 'prior = PRIOR_CAPTURE',
        'output = root/"own_startup"': 'output = root/"own_startup_retry"',
        'original = getsource(boot.startup_check.verify_startup)':
            'original = getsource(boot.startup_check.verify_startup).replace("ROOT / \'own_startup/", "ROOT / \'own_startup_retry/")',
    })
    env = vars(replay.startup) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(original, __file__ + '::startup_retry', 'exec'), env)
    env['main']()
