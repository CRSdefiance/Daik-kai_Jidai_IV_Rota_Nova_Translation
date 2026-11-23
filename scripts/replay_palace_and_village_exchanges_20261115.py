"""Replay the village lamp and dagger handover scenes on the cumulative test build."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_palace_and_village_exchanges_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASES = {
    "faith": ("faith", 89, (5, 8, 11, 15, 19, 23, 26, 30, 35, 39)),
    "dagger": ("dagger", 100, (5, 9, 15, 25)),
}
SCOPE = vars(quest) | dict(stage=stage, CASES=CASES, LAST=11201,
    CAPTURES=(*range(4350, 10151, 25), 10600, 11100))

for function, edits in (
    (quest.inputs, {"11901": "10076"}),
    (quest.prepare, {'row["turn"]': 'row["source_reference"]["record_index"]'}),
    (quest.verify, {"(12500, 13100)": "(10600, 11100)"}),
):
    source = checked_text(getsource(function), edits) if function != quest.prepare else getsource(function).replace(
        'row["turn"]', 'row["source_reference"]["record_index"]')
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)
for function in (quest.folder, quest.capture):
    SCOPE[function.__name__] = FunctionType(function.__code__, SCOPE)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    parser.add_argument("case", choices=CASES, nargs="?")
    args = parser.parse_args()
    if args.action == "startup":
        startup = quest.inherited
        FunctionType(startup.startup.__code__, vars(startup) | {"stage": stage})()
    elif args.case:
        SCOPE[args.action](args.case)
    else:
        parser.error("Choose the faith or dagger scenario.")


if __name__ == "__main__":
    main()
