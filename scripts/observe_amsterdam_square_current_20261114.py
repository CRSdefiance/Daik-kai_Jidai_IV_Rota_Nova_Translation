"""Visit the three Amsterdam Square shops on the registered cumulative ROM."""

import argparse
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_name_or_words_confirmation_20261114 as current
from scripts.source_locked_derivation_v5118 import checked_text


base=current.base
ROOT=Path("work/current_amsterdam_square_20261114_v1")
HISTORY=Path("work/emulation_v193/plaque_audit_v300_person/capture_report.json")
KEYS=(
    (8751,"B"),(9151,(180,29)),(9551,"A"),(9951,"A"),(10351,"A"),
    (10751,(130,58)),(11151,"A"),(11551,"A"),(11951,"A"),
    (12351,(130,90)),(12751,"A"),(13151,"A"),(13551,"A"),
    (13951,(130,122)),(14351,"A"),(14751,"A"),(15151,"A"),
    (15551,"B"),(15951,"B"),
)


def schedule(case):
    assert case in ("square","food")
    keys=KEYS if case=="square" else (*KEYS[:5],
        (10751,"A"),(11151,"A"),(11551,"A"),(11951,"A"),
        (12351,"A"),(12751,"A"),(13151,"B"),(13551,"B"),(13951,"B"))
    original=base.load(HISTORY)
    assert original["cold_boot"] and not original["savestate_loaded"] and not original["callback_errors"]
    assert original.get("battery_save_preloaded") is None
    events=[row for row in original["scripted_input_schedule"] if row["start"]<8751]
    for n,key in keys:
        entry=dict(buttons=[key]) if isinstance(key,str) else dict(touch=list(key),buttons=[])
        events.append(dict(start=n,duration=8,**entry))
    return events,[n+150 for n,_ in keys],keys[-1][0]+199,HISTORY,None


def main():
    source=checked_text(getsource(playback.main),{
        "    installed = []":"    argv.append('--touchscreen')\n    installed = []",
    })
    env=vars(playback)|dict(ROOT=ROOT,parent=current,FOCUS=set(range(3668)),observer=trace.scoped_observer,
        get_schedule=schedule,__file__=__file__)
    exec(compile(source,__file__+"::ordinary-amsterdam-square-observer","exec"),env)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",nargs="?",default="square",choices=("square","food"))
    env["main"](parser.parse_args().case)


if __name__=="__main__":
    main()
