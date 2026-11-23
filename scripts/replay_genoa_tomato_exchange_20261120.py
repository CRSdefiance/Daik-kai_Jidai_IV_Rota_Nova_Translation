"""Observe the staged Genoa scene through the same ordinary Square visit."""

from inspect import getsource
from types import SimpleNamespace

from scripts import observe_additional_town_visits_20261120 as baseline
from scripts import stage_genoa_tomato_exchange_20261120 as staged
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = staged.ROOT / 'playback'


def schedule(case):
    events, captures, _, source, donor = baseline.schedule(case)
    return [row for row in events if row['start'] <= 8201], [frame for frame in captures if frame <= 8350], 8400, source, donor


if __name__ == '__main__':
    source = checked_text(getsource(baseline.main), {'get_schedule=schedule': 'get_schedule=scene_schedule'})
    env = vars(baseline) | dict(ROOT=ROOT, head=SimpleNamespace(ROM=staged.ROM, RELEASE=staged.STORED),
                                scene_schedule=schedule, __file__=__file__)
    exec(compile(source, __file__ + '::ordinary-staged-genoa', 'exec'), env)
    env['main']('genoa')
