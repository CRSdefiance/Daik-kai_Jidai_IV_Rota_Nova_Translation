"""Observe both pages of Rafael's courier exchange in the initialized host."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_story_phrase_wraps_20261118 as excerpts
from scripts import stage_port_favor_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


quest = excerpts.quest
CASE = "rafael_julian_pages"
EXCERPTS = {277: (6, 9)}
scope = vars(quest) | dict(stage=stage, EXCERPTS=EXCERPTS,
    CASES={CASE: ("Rafael's two original courier speeches", None, None)}, LAST=6851,
    CAPTURES=(*range(4350, 6201, 25), 6550, 6850))
scope["excerpt_commands"] = FunctionType(excerpts.excerpt_commands.__code__, scope)

for function, edits in (
    (quest.inputs, {"11901": "6151"}),
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
            'f"{group} in the initialized Maria host, including both pages of the second speech."',
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
    (quest.verify, {"(12500, 13100)": "(5300, 6550, 6850)"}),
):
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + "::" + function.__name__, "exec"), scope)
for function in (quest.folder, quest.capture):
    scope[function.__name__] = FunctionType(function.__code__, scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify"))
    scope[parser.parse_args().action](CASE)
