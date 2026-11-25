"""Replay Maria's Frozen Rose return and church lead on the cumulative test build."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_frozen_rose_pagination_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "maria_frozen_rose"
CASES = {CASE: ("Maria's Frozen Rose handoff and church lead", 214, (5, 9, 12, 25, 29, 39, 43, 46, 51, 60))}
SCOPE = vars(quest) | dict(stage=stage, CASES=CASES, LAST=10801,
    CAPTURES=(*range(4350, 9301, 25), 10000, 10700))

def rumor_excerpt(bank, arm, inventory):
    block = bank.blocks[212]
    commands, speeches = stage.native.raw_speeches(arm, block, inventory)
    draft = stage.base.load(stage.MANUSCRIPT)
    row, = (r for r in draft["records"] if r["route"] == 3 and r["block"] == 212
            and r["source_reference"]["record_index"] == 109)
    ref = row["staged_reference"]
    current, = (r for r in stage.native.references(commands, speeches)
                if r["command_offset"] == ref["command_offset"])
    assert current["raw_hex"] == ref["raw_hex"]
    cmd, = (r for r in commands if r["offset"] == ref["command_offset"])
    assert cmd["word"] == 0x4000
    return row, cmd["whole_command_hex"]


SCOPE["rumor_excerpt"] = rumor_excerpt
for function, edits in (
    (quest.inputs, {"11901": "9301"}),
    (quest.prepare, {
        '    body = bytearray(host[:34] + guest[8:guest_end - 4] + bytes.fromhex("".join(cleanup)))':
            '    extra, extra_hex = rumor_excerpt(bank, arm, inventory)\n'
            '    body = bytearray(host[:34] + bytes.fromhex(extra_hex) + guest[8:guest_end - 4] + bytes.fromhex("".join(cleanup)))',
        'prefix + [r["whole_command_hex"] for r in guest_commands[:-1]] + cleanup':
            'prefix + [extra_hex] + [r["whole_command_hex"] for r in guest_commands[:-1]] + cleanup',
        '    planes = []':'    rows.insert(0, extra)\n    planes = []',
        '        if row["turn"] not in selected:':
            '        if row is not extra and row["source_reference"]["record_index"] not in selected:',
        'turn=row["turn"]': 'turn=row["source_reference"]["record_index"]',
        'f"Complete {group} from the initialized Maria entry."':
            'f"Complete {group} and the original two-page Havana rumor command from the initialized Maria entry."',
    }),
    (quest.verify, {"(12500, 13100)": "(10000, 10700)"}),
):
    source = checked_text(getsource(function), edits)
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
        parser.error("Choose the Frozen Rose scenario.")


if __name__ == "__main__":
    main()
