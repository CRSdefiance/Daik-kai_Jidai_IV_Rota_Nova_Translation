"""Replay Rafael's original Proof of Conquest dialogue excerpts in DeSmuME."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_story_phrase_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


CASE = "rafael_proof"
EXCERPTS = {48: (403, 406, 409, 414, 418), 79: (10, 22, 29, 32)}
SCOPE = vars(quest) | dict(stage=stage, CASES={CASE: ("Rafael's two Proof of Conquest excerpts", None, None)},
                          LAST=10301, CAPTURES=(*range(4350, 8651, 25), 9700, 10200))


def excerpt_commands(image, arm, inventory):
    native = stage.native
    bank = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4"))
    selected = []
    for block, ids in EXCERPTS.items():
        commands, speeches = native.raw_speeches(arm, bank.blocks[block], inventory)
        by_id = {row["record_index"]: row for row in native.references(commands, speeches)}
        by_offset = {cmd["offset"]: cmd for cmd in commands}
        for number in ids:
            cmd = by_offset[by_id[number]["command_offset"]]
            assert cmd["word"] == 0x4000
            selected.append(cmd)
    return selected


SCOPE["excerpt_commands"] = excerpt_commands
SCOPE["EXCERPTS"] = EXCERPTS
for function, edits in (
    (quest.inputs, {"11901": "8651"}),
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
            'f"{group} from the initialized Maria entry. B79 uses the original selected conditional reply."',
        '''    rows = [r for r in base.load(stage.MANUSCRIPT)["records"]
            if r["file_path"] == FILE and r["block"] == block]''':
            '''    reviewed = {(r["block"], r["source_reference"]["record_index"]): r
                for r in base.load(stage.MANUSCRIPT)["records"] if r["file_path"] == "/data/SC0.DK4"}
    rows = [reviewed[section, ident] for section, ids in EXCERPTS.items() for ident in ids]''',
        '''        if row["turn"] not in selected:
            continue
''': '',
        'turn=row["turn"]': 'turn=row["source_reference"]["record_index"]',
    }),
    (quest.verify, {"(12500, 13100)": "(9700, 10200)"}),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), SCOPE)
for function in (quest.folder, quest.capture):
    SCOPE[function.__name__] = FunctionType(function.__code__, SCOPE)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify"))
    SCOPE[parser.parse_args().action](CASE)
