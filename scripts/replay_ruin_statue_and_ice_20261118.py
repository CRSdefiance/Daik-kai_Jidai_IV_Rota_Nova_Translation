"""Replay all three stone selections in Maria's initialized ruin scene."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_ruin_statue_and_ice_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

CASES = {
    "front": ("Maria's Front stone outcome", 221, (5, 8, 11, 30, 52)),
    "left": ("Maria's Left stone outcome", 221, (5, 8, 11, 67, 89)),
    "right": ("Maria's Right stone and affirmative voice reply", 221,
              (5, 8, 11, 104, 110, 118, 121, 125, 132, 140, 162, 172, 176)),
}
LIMITS = {"front": (8901, 7701, 8200, 8850), "left": (8901, 7701, 8200, 8850),
          "right": (12501, 11551, 11900, 12400)}
SCOPE = vars(quest) | dict(stage=stage, CASES=CASES)


def inputs(case):
    start = quest.base.load(quest.prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    actions = [(f, "A") for f in (4200, 4525, 4850, 5175)]
    if case in ("left", "right"):
        actions.append((5300, "DOWN"))
    if case == "right":
        actions.append((5400, "DOWN"))
    advance_end = 11551 if case == "right" else 7701
    actions.extend((f, "A") for f in range(5500, advance_end, 325))
    return start + [dict(start=f, duration=16, buttons=[key]) for f, key in actions]


SCOPE["inputs"] = inputs
for function, edits in (
    (quest.prepare, {
        'row["turn"]': 'row["source_reference"]["record_index"]',
        '        assert raw[0] != 254': """        if raw[0] == 254:
            assert row["decision"] == "revision" and row["source_reference"]["record_index"] in (8, 11)
            full_ink = row["after_native"]["fe_plane_hex"]
            assert len(bytes.fromhex(full_ink)) == 228 * 64""",
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} using the original menus and branch commands from the initialized Maria entry."',
    }),
    (quest.verify, {
        "(12500, 13100)": "(5225, 5450, *TAIL_FRAMES)",
        '        expected = prior.TOOL.prior.masks(bytes.fromhex(row["plane"]))':
            '        raw = bytes.fromhex(row["plane"])\n'
            '        # The live FE palette maps original style 15 to the dark dialog ink.\n'
            '        if row["kind"] == "system-FE":\n'
            '            assert set(raw) <= {0, 15}\n'
            '            raw = bytes(int(bool(value)) for value in raw)\n'
            '        expected = prior.TOOL.prior.masks(raw)',
    }),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)
for function in (quest.folder, quest.capture):
    SCOPE[function.__name__] = FunctionType(function.__code__, SCOPE)


def run(action, case):
    last, regular_end, first_tail, second_tail = LIMITS[case]
    SCOPE.update(LAST=last, CAPTURES=(*range(4350, regular_end, 25), first_tail, second_tail),
                 TAIL_FRAMES=(first_tail, second_tail))
    SCOPE[action](case)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    parser.add_argument("case", choices=CASES, nargs="?")
    args = parser.parse_args()
    if args.action == "startup":
        startup = quest.inherited
        FunctionType(startup.startup.__code__, vars(startup) | {"stage": stage})()
    elif args.case:
        run(args.action, args.case)
    else:
        parser.error("Choose a stone to replay.")


if __name__ == "__main__":
    main()
