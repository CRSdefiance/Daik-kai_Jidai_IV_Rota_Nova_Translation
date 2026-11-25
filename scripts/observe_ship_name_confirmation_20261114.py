"""Trace the two name-entry paths on the current cumulative build."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_tavern_toast_and_gift_20261114 as current
from scripts.replay_shipyard_fleet_setup_v1 import REFERENCES
from scripts.source_locked_derivation_v5118 import checked_text

base=current.base
ROOT=Path("work/ship_name_confirmation_20261114_v1")
RENAME=Path("work/emulation_v193/refit_dialogue_v832_name_entry/capture_report.json")
FOCUS={284,287,296,300,304}
CASES={
    "buy":(REFERENCES["yard"],8600,((8601,"X"),(9001,"B"),(9401,"X"),(9801,"A"),(10201,"B"))),
    "rename":(RENAME,13700,((13701,"X"),(14101,"B"),(14501,"X"),(14901,"A"),(15301,"B"))),
}


def schedule(case):
    history,end_prefix,branch=CASES[case]
    past=base.load(history)
    assert past["cold_boot"] and not past["savestate_loaded"] and not past["callback_errors"]
    donor=past["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    events=[row for row in past["scripted_input_schedule"] if row["start"]<end_prefix]
    events.extend(dict(start=frame,duration=8,buttons=[key]) for frame,key in branch)
    frames=[end_prefix,*[frame+149 for frame,_ in branch]]
    return events,frames,frames[-1]+25,history,donor


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=tuple(CASES))
    env=vars(playback)|dict(ROOT=ROOT,parent=current,FOCUS=FOCUS,observer=trace.scoped_observer,
        get_schedule=schedule,__file__=__file__)
    source=checked_text(getsource(playback.main),{
        "'--capture-at', *map(str, frames)]":"'--capture-at', *map(str, frames), '--dump-capture-ram']",
    })
    exec(compile(source,__file__+"::native-name-entry-request-observer","exec"),env)
    env["main"](parser.parse_args().case)


if __name__=="__main__":
    main()
