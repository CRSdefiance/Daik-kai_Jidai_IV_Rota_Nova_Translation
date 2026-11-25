"""Trace existing-save Grand Race and ordinary Quit Game against the exhibition key."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_gallery_empty_common_20261114 as earlier
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_alexandria_cooking_20261114 as current


base = current.base
ROOT = Path("work/race_and_quit_common_20261114_v1")
RACE_INPUTS = Path("work/analysis/miniature_consumers_v576/final_recorded_inputs.json")
RACE_REFERENCE = Path("work/emulation_v193/grand_race_v576_complete/capture_report.json")
FOCUS = {108,109,110,111,113,114,115,116,117,118,119,124,318,319}
RACE_FRAMES = [2400,3000,3400,4400,4800,5200,5600,7000,7400,8400,8800,
               9200,10000,10600,11000,11400,11800,12190]
QUIT_KEYS = (
    (1601,"START"),(2001,"A"),(2401,"A"),(2801,"A"),(3601,"X"),(4001,(146,93)),
    (4401,"A"),(4801,"DOWN"),(5201,"DOWN"),(5601,"A"),(6001,"B"),
    (6401,"A"),(6801,"A"),
)


def schedule(case):
    past = base.load(earlier.HISTORY)
    assert past["cold_boot"] and not past["savestate_loaded"] and not past["callback_errors"]
    assert not past.get("battery_save_preloaded")
    donor = dict(source=str(earlier.DONOR),source_sha256=base.digest(earlier.DONOR))
    if case == "race":
        events = base.load(RACE_INPUTS)
        assert events == base.load(RACE_REFERENCE)["scripted_input_schedule"]
        return events, RACE_FRAMES, 12200, RACE_INPUTS, donor
    assert case == "quit"
    events = [dict(start=frame,duration=8,buttons=[key]) if isinstance(key,str)
              else dict(start=frame,duration=8,buttons=[],touch=list(key)) for frame,key in QUIT_KEYS]
    return events, [frame+199 for frame,_ in QUIT_KEYS], 7200, earlier.HISTORY, donor


def main(case):
    env = vars(playback) | dict(ROOT=ROOT,parent=current,FOCUS=FOCUS,
        observer=trace.scoped_observer,get_schedule=schedule,__file__=__file__)
    exec(compile(getsource(playback.main), __file__+"::ordinary-save-original-options", "exec"),env)
    env["main"](case)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=("race","quit"))
    main(parser.parse_args().case)

