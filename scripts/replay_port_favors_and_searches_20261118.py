"""Replay Maria's meeting with Peralonso and return to the original host."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as workflow
from scripts import stage_port_favor_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "maria_peralonso_tavern"
TURNS = (4, 7, 11, 14, 18, 21, 25, 29, 33, 37, 41, 44, 47)
LAST = 11901
scope = vars(workflow) | dict(stage=stage, CASES={CASE: ("Maria's Peralonso meeting", 234, TURNS)},
                              LAST=LAST, CAPTURES=(*range(4350, 11051, 25), 11400, 11900))


def inputs(case):
    assert case == CASE
    prefix = workflow.base.load(workflow.prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    return prefix + [dict(start=frame, duration=16, buttons=["A"]) for frame in range(4200, 11001, 350)]


scope["inputs"] = inputs
for function, edits in (
    (workflow.prepare, {
        'row["turn"]': 'row["source_reference"]["record_index"]',
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} with original scene controls in the initialized Maria entry."',
    }),
    (workflow.verify, {"(12500, 13100)": "(11400, 11900)"}),
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
