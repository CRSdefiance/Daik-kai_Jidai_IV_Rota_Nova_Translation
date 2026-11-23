"""Exercise the three complete dialogue tails in Lil's initialized opening."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import havana_calicut_istanbul_trends_20261121 as stage
from scripts import replay_seville_stockholm_trends_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "emulator"
ARCHIVE, ENTRY_ARCHIVE = "/data/SC3.DK4", "/data/SC2.DK4"
CASES = {"havana": (163, 17), "calicut": (164, 13), "istanbul": (165, 8)}
LIVE, SHEET = ROOT / "gameplay.json", ROOT / "comparison.png"
build = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, ROOT=stage.ROOT, parent=stage.parent,
                        review=SimpleNamespace(OUTPUT=stage.OUTPUT))
offline = SimpleNamespace(PROOF=stage.NATIVE_PROOF)
REPLAY_SUFFIX = ""
env = vars(precedent) | {name: globals()[name] for name in (
    "ROOT", "ARCHIVE", "ENTRY_ARCHIVE", "CASES", "LIVE", "SHEET", "build", "offline", "REPLAY_SUFFIX",
)}


def prepare():
    code = checked_text(getsource(precedent.prepare), {
        'bank = native.IlnkContainer.parse(image.read_file(ARCHIVE))':
            'bank = native.IlnkContainer.parse(image.read_file(ENTRY_ARCHIVE))',
        'entry, scene = bank.blocks[22], bank.blocks[index]':
            'entry = bank.blocks[22]\n'
            '            scene = native.IlnkContainer.parse(image.read_file(ARCHIVE)).blocks[index]',
        '            logical = bytearray(entry[:8] + prelude + scene[8:end])':
            '            number = next(i for i, command in enumerate(complete) if command["word"] == 0x4000)\n'
            '            prefix = complete[:number]\n'
            '            complete = complete[number:]\n'
            '            assert [c["word"] for c in complete] == [0x4000] * panel_count + [0xC200, 0]\n'
            '            start = complete[0]["offset"]\n'
            '            logical = bytearray(entry[:8] + prelude + scene[start:end])',
        'a["offset"] + len(prelude) == b["offset"]':
            'a["offset"] + len(prelude) + 8 - start == b["offset"]',
        'image.replace_file(ARCHIVE, bank.to_bytes())':
            'image.replace_file(ENTRY_ARCHIVE, bank.to_bytes())',
        'underlying_ROM_sha256=base.digest(rom))':
            'underlying_ROM_sha256=base.digest(rom),'
            ' original_archive=ARCHIVE, first_dialogue_offset=start, '
            ' omitted_pre_dialogue_commands=[(c["offset"], c["word"]) for c in prefix])',
    })
    exec(compile(code, __file__ + "::original-dialogue-commands", "exec"), env)
    env["prepare"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "verify", "startup", *CASES))
    parser.add_argument("side", nargs="?", choices=("before", "after"))
    args = parser.parse_args()
    if args.action == "startup":
        run = precedent.precedent.startup
        FunctionType(run.__code__, run.__globals__ | {"build": build})()
    elif args.action == "verify":
        code = checked_text(getsource(precedent.verify), {
            "All 18 Lil scene panels": "All 38 excerpt panels",
            'initialized_scene=True,': 'initialized_scene=True, original_archive=ARCHIVE, dialogue_tail_only=True,',
        })
        exec(compile(code, __file__ + "::complete-dialogue-tails", "exec"), env)
        env["verify"]()
    elif args.action == "prepare":
        prepare()
    else:
        FunctionType(precedent.capture.__code__, env)(args.action, args.side)
