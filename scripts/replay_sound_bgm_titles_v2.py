"""Replay the original Sound Setup controls on the staged title revisions."""

from inspect import getsource

from scripts import replay_sound_bgm_titles_v1 as prior
from scripts import stage_sound_bgm_titles_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / 'sound_setup'


if __name__ == '__main__':
    source = checked_text(getsource(prior.main), {
        'release = base.load(parent.RELEASE)': 'release = base.load(stage.PROOF)',
        'parent.ROM': 'stage.ROM',
    })
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::staged-title-replay', 'exec'), environment)
    environment['main']()
