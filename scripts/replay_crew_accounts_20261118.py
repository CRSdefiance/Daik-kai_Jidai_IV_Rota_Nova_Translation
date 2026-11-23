"""Replay Rafael's West African letter and its page continuation in DeSmuME."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_crew_accounts_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "rafael_fleet_letter"
EXCERPTS = {(0, 247): (27, 31, 35, 38, 41, 44, 47, 50, 57)}
SCOPE = vars(quest) | dict(stage=stage, CASES={CASE: ("Rafael's fleet letter", None, None)},
                          LAST=11301, CAPTURES=(*range(4350, 9651, 25), 10400, 11200))


def excerpt_commands(image, arm, inventory):
    native = stage.native
    bank = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4"))
    commands, speeches = native.raw_speeches(arm, bank.blocks[247], inventory)
    rows = [row for row in stage.base.load(stage.MANUSCRIPT)["records"]
            if row["route"] == 0 and row["block"] == 247]
    assert tuple(row["source_reference"]["record_index"] for row in rows) == EXCERPTS[0, 247]
    assert list(native.references(commands, speeches)) == [
        {key: value for key, value in row["staged_reference"].items() if key != "block_sha256"}
        for row in rows
    ]
    assert [row["word"] for row in commands[:3]] == [0x4100, 0x4500, 0x4621]
    assert [row["word"] for row in commands[-2:]] == [0xa000, 0]
    # Keep the original letter prelude, scene-style toggles and every speech.
    return commands[:-2]


SCOPE["excerpt_commands"] = excerpt_commands
SCOPE["EXCERPTS"] = EXCERPTS
for function, edits in (
    (quest.inputs, {"11901": "9651"}),
    (quest.prepare, {
        'host, guest = bank.blocks[33], bank.blocks[block]': 'host = bank.blocks[33]',
        '''    guest_end = 8 + unpack_from("<H", guest, 4)[0]
    guest_commands, _ = inventory(arm, guest)
    assert guest_commands[-1]["whole_command_hex"] == "00000000"
    body = bytearray(host[:34] + guest[8:guest_end - 4] + bytes.fromhex("".join(cleanup)))''':
            '''    snippets = excerpt_commands(image, arm, inventory)
    speech_bytes = "".join(row["whole_command_hex"] for row in snippets)
    body = bytearray(host[:34] + bytes.fromhex(speech_bytes + "".join(cleanup)))''',
        'prefix + [r["whole_command_hex"] for r in guest_commands[:-1]] + cleanup':
            'prefix + [r["whole_command_hex"] for r in snippets] + cleanup',
        'f"Complete {group} from the initialized Maria entry."':
            'f"{group} from the initialized Maria entry. The letter prelude, styles and speeches are original. The initialized host owns the final exit."',
        '''    rows = [r for r in base.load(stage.MANUSCRIPT)["records"]
            if r["file_path"] == FILE and r["block"] == block]''':
            '''    reviewed = {(r["route"], r["block"], r["source_reference"]["record_index"]): r
                for r in base.load(stage.MANUSCRIPT)["records"]}
    rows = [reviewed[route, section, ident] for (route, section), ids in EXCERPTS.items() for ident in ids]''',
        '''        if row["turn"] not in selected:
            continue
''': '',
        'turn=row["turn"]': 'turn=row["source_reference"]["record_index"]',
    }),
    (quest.verify, {"(12500, 13100)": "(10400, 11200)"}),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)
for function in (quest.folder, quest.capture):
    SCOPE[function.__name__] = FunctionType(function.__code__, SCOPE)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify"))
    SCOPE[parser.parse_args().action](CASE)
