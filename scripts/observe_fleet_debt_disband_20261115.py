"""Replay the fleet picker, refusal, and confirmation with a copied existing save."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_london_stockholm_dialogue_20261115 as current
from scripts import replay_shipyard_fleet_setup_v1 as original
from scripts import replay_shipyard_fleet_setup_v2 as sealed
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('work/fleet_debt_disband_20261115_v1')
FRAMES = (9400, 10360, 10840, 11080, 11440, 11560, 11680, 11800)


def schedule(_):
    events, known, end, donor = sealed.replay_plan('fleet')
    assert set(FRAMES).issubset(known) and base.digest(donor['source']) == donor['source_sha256']
    return events, FRAMES, end, original.REFERENCES['fleet'], donor


def main():
    src = checked_text(getsource(playback.main), {
        '    installed = []': "    argv += ['--dump-capture-ram']\n    installed = []",
    })
    namespace = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule,
        FOCUS=set(range(3668)), observer=trace.scoped_observer, __file__=__file__)
    exec(compile(src, __file__ + '::fleet-disband-screen', 'exec'), namespace)
    namespace['main']('fleet')


if __name__ == '__main__':
    main()
