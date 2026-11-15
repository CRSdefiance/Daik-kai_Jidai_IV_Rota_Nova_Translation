"""Trace every About Extras page on the current cumulative candidate."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_grand_race_stopping_20261114 as parent


ROOT=Path("work/extras_tie_in_common_20261114_v1")
HISTORY=Path("work/emulation_v193/alternate_title_v238/navigation/capture_report.json")
FOCUS=set(range(3289,3320))
KEYS=((1000,"START"),(1100,"DOWN"),(1160,"DOWN"),(1220,"A"),(1900,"A"),
      (2400,"R"),(2900,"R"),(3400,"R"),(3900,"R"),(4400,"L"),(4900,"B"),(5400,"B"))


def schedule(case):
    assert case in ("tie_in","tie_in_advance")
    previous=parent.base.load(HISTORY)
    assert previous["cold_boot"] and not previous["savestate_loaded"]
    assert [(q["start"],q["buttons"][0]) for q in previous["scripted_input_schedule"][:5]]==list(KEYS[:5])
    events=[dict(start=n,duration=8,buttons=["A" if case=="tie_in_advance" and key in ("R","L") else key])
            for n,key in KEYS]
    frames=[n+199 for n,_ in KEYS[3:]]
    return events,frames,5750,HISTORY,None


def main(case):
    namespace=vars(playback) | dict(ROOT=ROOT,parent=parent,FOCUS=FOCUS,observer=trace.scoped_observer,
        get_schedule=schedule,__file__=__file__)
    exec(compile(getsource(playback.main),__file__+"::observed-about-extras", "exec"),namespace)
    namespace["main"](case)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",nargs="?",default="tie_in",choices=("tie_in","tie_in_advance"))
    main(parser.parse_args().case)

