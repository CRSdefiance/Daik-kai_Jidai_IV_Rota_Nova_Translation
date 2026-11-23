"""Play Maria's Plett encounter with its original scene commands."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as workflow
from scripts import stage_guild_search_and_survey_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "maria_plett_tavern"
SCENE_TURNS = (4, 8, 16, 20, 23, 26, 30, 34, 38, 42, 53, 66, 71, 74, 78, 81, 84, 87, 91, 95, 99, 103, 107, 112)
# The B33 host is still recruiting its crew. This run takes the shorter surrender path.
TURNS = (4, 8, 16, 20, 23, 26, 30, 34, 38, 42, 66)
LAST = 14801
scope = vars(workflow) | dict(stage=stage, TURNS=TURNS, CASES={CASE: ("Maria's Plett encounter", 226, SCENE_TURNS)},
                              LAST=LAST, CAPTURES=(*range(4350, 14051, 25), 14500, 14800))


def inputs(case):
    assert case == CASE
    prefix = workflow.base.load(workflow.prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    return prefix + [dict(start=frame, duration=16, buttons=["A"]) for frame in range(4200, 14001, 350)]


scope["inputs"] = inputs
for function, edits in (
    (workflow.prepare, {
        'row["turn"]': 'row["source_reference"]["record_index"]',
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} using the untouched scene commands in the initialized Maria entry."',
    }),
    (workflow.verify, {
        "for row in fixture[\"expected_pages\"]:": "for row in fixture[\"expected_pages\"]:\n        if row[\"turn\"] not in TURNS:\n            continue",
        "(12500, 13100)": "(5000, 8500, 10500, 14500)",
    }),
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
