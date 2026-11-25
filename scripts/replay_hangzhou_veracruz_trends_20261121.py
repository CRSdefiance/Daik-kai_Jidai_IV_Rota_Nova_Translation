"""Exercise all Maria dialogue turns with Lil's initialized name substitution."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import hangzhou_veracruz_trends_20261121 as stage
from scripts import replay_seville_stockholm_trends_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / "emulator"
PRIOR_BEFORE = Path("out/hangzhou_veracruz_validation_20261121_v1/emulator")
ARCHIVE, ENTRY_ARCHIVE = "/data/SC3.DK4", "/data/SC2.DK4"
CASES = {"hangzhou": (167, 11), "veracruz": (168, 20)}
LIVE, SHEET = ROOT / "gameplay.json", ROOT / "comparison.png"
build = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, ROOT=stage.ROOT, parent=stage.parent,
                        review=SimpleNamespace(OUTPUT=stage.OUTPUT))
offline = SimpleNamespace(PROOF=stage.NATIVE_PROOF)
REPLAY_SUFFIX = ""
env = vars(precedent) | {name: globals()[name] for name in (
    "ROOT", "PRIOR_BEFORE", "ARCHIVE", "ENTRY_ARCHIVE", "CASES", "LIVE", "SHEET", "build", "offline", "REPLAY_SUFFIX",
)}


def prepare():
    program = checked_text(getsource(precedent.prepare), {
        'bank = native.IlnkContainer.parse(image.read_file(ARCHIVE))':
            'bank = native.IlnkContainer.parse(image.read_file(ENTRY_ARCHIVE))',
        'entry, scene = bank.blocks[22], bank.blocks[index]':
            'entry = bank.blocks[22]\n'
            '            scene = native.IlnkContainer.parse(image.read_file(ARCHIVE)).blocks[index]',
        '            logical = bytearray(entry[:8] + prelude + scene[8:end])':
            '            selected = [c for c in complete if c["word"] == 0x4000 or c is complete[-1]]\n'
            '            assert complete[-1]["word"] == 0\n'
            '            assert len(selected) == panel_count + 1\n'
            '            prefix_and_branch = [c for c in complete if c not in selected]\n'
            '            complete = selected\n'
            '            dialogue = b"".join(bytes.fromhex(c["whole_command_hex"]) for c in complete)\n'
            '            assert scene[end - 4:end] == dialogue[-4:] == bytes(4)\n'
            '            logical = bytearray(entry[:8] + prelude + dialogue)',
        '                assert a["offset"] + len(prelude) == b["offset"]':
            '                assert a["native_extent"] == b["native_extent"]',
        'image.replace_file(ARCHIVE, bank.to_bytes())':
            'image.replace_file(ENTRY_ARCHIVE, bank.to_bytes())',
        '            image.save(target)':
            '            if side == "before":\n'
            '                target = PRIOR_BEFORE / name / target.name\n'
            '                assert target.read_bytes() == bytes(image.rom.save())\n'
            '            else:\n'
            '                image.save(target)',
        'underlying_ROM_sha256=base.digest(rom))':
            'underlying_ROM_sha256=base.digest(rom), original_archive=ARCHIVE,'
            ' copied_original_offsets=[c["offset"] for c in complete],'
            ' unexercised_controls=[(c["offset"], c["word"]) for c in prefix_and_branch])',
    })
    exec(compile(program, __file__ + "::complete-speech-fixtures", "exec"), env)
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
        program = checked_text(getsource(precedent.verify), {
            'path = folder / (side + REPLAY_SUFFIX) / "capture_report.json"':
                'path = (PRIOR_BEFORE / name if side == "before" else folder) / side / "capture_report.json"',
            'page, = receipts[row["id"]]["pages"]':
                'result = receipts[row["id"]]\n'
                '                page, = result.get("initialized_Lil_pages", result["pages"])',
            "All 18 Lil scene panels": "All 31 original speech panels",
            'initialized_scene=True,': 'initialized_scene=True, original_archive=ARCHIVE, speech_fixture=True,',
        })
        exec(compile(program, __file__ + "::verify-original-speeches", "exec"), env)
        env["verify"]()
    elif args.action == "prepare":
        prepare()
    else:
        FunctionType(precedent.capture.__code__, env)(args.action, args.side)
