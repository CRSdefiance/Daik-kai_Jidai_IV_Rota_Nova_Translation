"""Observe ordinary Square and Tavern visits after Maria's New Game introduction."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_maria_B18_B20_20261122 as current
from scripts.observe_regional_town_dialogue_20261115 import VISITS
from scripts.observe_setup_save_common_v1 import scoped_observer


ROOT=Path("work/analysis/hangzhou_early_actual_20261122")
base=current.base


def schedule(case):
    assert case=="hangzhou"
    origin=current.STARTUP_CAPTURE
    previous=base.load(origin)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert previous["ROM_sha256"]==base.digest(current.ROM)
    donor=previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    events=previous["scripted_input_schedule"].copy()
    offset=27600
    assert events[-1]["start"]<VISITS[0][0]+offset
    for frame,action in VISITS:
        fields=dict(buttons=[],touch=list(action)) if isinstance(action,tuple) else dict(buttons=[action])
        events.append(dict(start=frame+offset,duration=8,**fields))
    return events,[31000,*(n+offset+149 for n,_ in VISITS)],39400,origin,donor


def main():
    scope=vars(playback)|dict(ROOT=ROOT,parent=current,observer=scoped_observer,get_schedule=schedule,
        FOCUS=set(range(3668)),__file__=__file__)
    exec(compile(getsource(playback.main),__file__+"::ordinary-Hangzhou-after-introduction","exec"),scope)
    scope["main"]("hangzhou")


if __name__=="__main__":
    main()

