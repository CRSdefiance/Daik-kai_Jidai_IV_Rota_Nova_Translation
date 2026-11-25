"""Replay Maria's Clive handover and the two-page illustrated-map clue."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as workflow
from scripts import stage_bounty_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "maria_clive_map"
TURNS = (4, 8, 11, 15, 60, 63, 66)
LAST = 10401
scope = vars(workflow) | dict(stage=stage, CASES={CASE: ("Clive's handover and the illustrated map clue", 247, TURNS)},
                              LAST=LAST, CAPTURES=(*range(4350, 9601, 25), 10000, 10400))


def inputs(case):
    assert case == CASE
    prefix = workflow.base.load(workflow.prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    return prefix + [dict(start=frame, duration=16, buttons=["A"]) for frame in range(4200, 9601, 350)]


scope["inputs"] = inputs
for function, edits in (
    (workflow.prepare, {
        'row["turn"]': 'row["source_reference"]["record_index"]',
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} with the original dialogue and reward commands in the initialized Maria entry."',
    }),
    (workflow.verify, {"(12500, 13100)": "(5725, 6000, 10000, 10400)"}),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), scope)
for function in (workflow.folder, workflow.capture):
    scope[function.__name__] = FunctionType(function.__code__, scope)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    args = parser.parse_args()
    if args.action == "startup":
        startup = workflow.inherited
        FunctionType(startup.startup.__code__, vars(startup) | {"stage": stage})()
    else:
        scope[args.action](CASE)


if __name__ == "__main__":
    main()
