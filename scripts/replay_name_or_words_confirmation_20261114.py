"""Replay the revised ship confirmation and observe its original caller."""

import argparse
from inspect import getsource
from types import SimpleNamespace,FunctionType

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_ship_name_confirmation_20261114 as before
from scripts import observe_setup_save_common_v1 as trace
from scripts import replay_tavern_toast_startup_20261114 as boot
from scripts import stage_name_or_words_literal_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base=stage.base
ROOT=stage.ROOT


def capture(case):
    candidate=SimpleNamespace(ROM=stage.ROM,RELEASE=ROOT/"replay_identity.json")
    stored=base.load(stage.STORED)
    expected=dict(candidate_sha256=stored["candidate_sha256"])
    if candidate.RELEASE.exists():
        assert base.load(candidate.RELEASE)==expected
    else:
        base.save(candidate.RELEASE,expected)
    observer=FunctionType(trace.scoped_observer.__code__,vars(trace)|dict(REQUESTS=trace.REQUESTS|{0x0205466C:4}))
    env=vars(playback)|dict(ROOT=ROOT,parent=candidate,FOCUS={296},observer=observer,
        get_schedule=before.schedule,__file__=__file__)
    source=checked_text(getsource(playback.main),{
        "'--capture-at', *map(str, frames)]":"'--capture-at', *map(str, frames), '--dump-capture-ram']",
    })
    exec(compile(source,__file__+"::revised-name-entry-observer","exec"),env)
    env["main"](case)


def startup():
    script=checked_text(getsource(boot.main),{
        'stage.parent.stage.ROOT/"startup_retry"':'stage.parent.stage.ROOT/"own_startup"',
    })
    env=vars(boot)|dict(stage=stage,__file__=__file__)
    exec(compile(script,__file__+"::registered-startup-replay","exec"),env)
    env["main"]()


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=("buy","rename","startup"))
    choice=parser.parse_args().case
    startup() if choice=="startup" else capture(choice)
