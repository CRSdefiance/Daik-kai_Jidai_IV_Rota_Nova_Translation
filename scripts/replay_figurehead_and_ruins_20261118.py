"""Replay Maria's original figurehead exchange and decline branch."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_figurehead_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

CASE = "maria_figurehead_decline"
SELECTED = (5, 9, 13, 16, 20, 24, 28, 31, 35, 39, 43, 47, 51, 55, 59, 63, 174, 178, 182)
CASES = {CASE: ("Maria's figurehead scene and Leave it branch", 215, SELECTED)}
SCOPE = vars(quest) | dict(stage=stage, CASES=CASES, LAST=12001,
    CAPTURES=(*range(4350, 11051, 25), 11400, 11900))


def inputs(case):
    assert case == CASE
    initial = quest.base.load(quest.prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    before = [(f, "A") for f in range(4200, 9401, 325)]
    decline = [(9530, "DOWN")]
    after = [(f, "A") for f in range(9725, 11026, 325)]
    return initial + [dict(start=f, duration=16, buttons=[button])
                      for f, button in before + decline + after]


SCOPE["inputs"] = inputs
for function, edits in (
    (quest.prepare, {
        'row["turn"]': 'row["source_reference"]["record_index"]',
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} using the untouched scene commands in the initialized Maria entry."',
    }),
    (quest.verify, {"(12500, 13100)": "(9500, 9650, 11400, 11900)"}),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)
for function in (quest.folder, quest.capture):
    SCOPE[function.__name__] = FunctionType(function.__code__, SCOPE)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    args = parser.parse_args()
    if args.action == "startup":
        startup = quest.inherited
        FunctionType(startup.startup.__code__, vars(startup) | {"stage": stage})()
    else:
        SCOPE[args.action](CASE)


if __name__ == "__main__":
    main()
