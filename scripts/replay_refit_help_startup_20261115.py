"""Replay the registered parent's startup controls for the Refit revision."""

from inspect import getsource
from pathlib import Path

from scripts import replay_tavern_toast_startup_20261114 as startup
from scripts import stage_refit_help_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    release = stage.base.load(stage.parent.RELEASE)
    parent_receipt = stage.base.load(release['own_registered_startup'])
    prior = Path(parent_receipt['read_only_snapshot']['path']).parent.parent
    source = checked_text(getsource(startup.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    env = vars(startup) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(source, __file__ + '::startup-controls', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
